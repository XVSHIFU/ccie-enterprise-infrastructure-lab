"""Run on EVE as root; connect Linux namespaces to explicitly selected bridges."""
import argparse
import json
import os
from pathlib import Path
import re
import secrets
import shlex
import sqlite3
import subprocess
import xml.etree.ElementTree as ET

BASE = Path('/opt/ccie-business-lab')

def run(*args):
    return subprocess.run(args, check=True, text=True, capture_output=True).stdout

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lab-file',type=Path)
    for name in ('dc', 'cloud', 'hq', 'branch'):
        parser.add_argument('--'+name+'-bridge')
    args = parser.parse_args()
    if os.geteuid() != 0:
        raise SystemExit('Run as root on EVE.')
    if args.lab_file:
        tree=ET.parse(args.lab_file).getroot()
        for role,network in [('dc','DC-ERP-Linux'),('cloud','Cloud-ERP-Linux'),('branch','Hybrid-Users-Linux')]:
            if not getattr(args,role+'_bridge'):
                matches=[x for x in tree.findall('.//network') if x.get('name')==network]
                if len(matches)!=1:raise ValueError('Expected one network named '+network)
                setattr(args,role+'_bridge','vnet0_'+matches[0].get('id'))
        if not args.hq_bridge:
            hosts=[x for x in tree.findall('.//node') if x.get('name')=='host12']
            if len(hosts)!=1:raise ValueError('Expected host12 to identify HQ VLAN2001 bridge.')
            interfaces=[x for x in hosts[0].findall('interface') if x.get('name') in ('e0/0','Ethernet0/0')]
            if len(interfaces)!=1:raise ValueError('Expected host12 Ethernet0/0.')
            args.hq_bridge='vnet0_'+interfaces[0].get('network_id')
    if not all(getattr(args,n+'_bridge') for n in ('dc','cloud','hq','branch')):
        parser.error('Supply --lab-file or all four bridge names.')
    specs = [('dc', args.dc_bridge, '10.2.100.20/24', '10.2.100.1'),
             ('cloud', args.cloud_bridge, '10.3.101.20/24', '10.3.101.1'),
             ('hq', args.hq_bridge, '10.1.101.110/24', '10.1.101.1'),
             ('branch', args.branch_bridge, '10.4.210.110/24', '10.4.210.1')]
    for _, bridge, _, _ in specs:
        if not re.fullmatch(r'[A-Za-z0-9_.:-]{1,15}', bridge):
            raise ValueError('Invalid bridge name: '+bridge)
        link = json.loads(run('ip', '-d', '-j', 'link', 'show', bridge))[0]
        if link.get('linkinfo', {}).get('info_kind') != 'bridge':
            raise ValueError('Not a Linux bridge: '+bridge)
    BASE.mkdir(mode=0o700, parents=True, exist_ok=True)
    if not (BASE/'erp_lab.py').is_file() or not (BASE/'probe.py').is_file():
        raise SystemExit('Upload erp_lab.py and probe.py into '+str(BASE)+' first.')
    credentials = BASE/'credentials.json'
    if not credentials.exists():
        credentials.write_text(json.dumps({'user':'erp-lab','password':secrets.token_urlsafe(24)}))
    credentials.chmod(0o600)
    for site in ('dc', 'cloud'):
        folder=BASE/site;folder.mkdir(mode=0o700, exist_ok=True)
        with sqlite3.connect(folder/'orders.sqlite') as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY, customer TEXT, item TEXT, quantity INTEGER)')
            if site=='dc' and conn.execute('SELECT count(*) FROM orders').fetchone()[0]==0:
                conn.executemany('INSERT INTO orders VALUES(?,?,?,?)',[(1001,'Demo-A','Router',2),(1002,'Demo-B','Switch',5),(1003,'Demo-C','Service',1)])
        conn.close()
        if not (folder/'mode').exists(): (folder/'mode').write_text('local')
    if not (BASE/'server.crt').exists():
        run('openssl','req','-x509','-newkey','rsa:2048','-nodes',
            '-keyout',str(BASE/'server.key'),'-out',str(BASE/'server.crt'),'-days','365',
            '-subj','/CN=CCIE-ERP-LAB','-addext','subjectAltName=IP:10.2.100.20,IP:10.3.101.20')
    (BASE/'server.key').chmod(0o600)
    lines=['#!/bin/bash','set -euo pipefail']
    for name, bridge, address, gateway in specs:
        ns='ccie-'+name;veth='erp-'+name
        lines += [f'ip netns list | grep -q "^{ns} " || ip netns add {ns}',
                  f'ip link show {veth} >/dev/null 2>&1 || ip link add {veth} type veth peer name eth0 netns {ns}',
                  f'ip link set {veth} master {bridge}', f'ip link set {veth} up',
                  f'ip -n {ns} link set lo up', f'ip -n {ns} link set eth0 up',
                  f'ip -n {ns} address replace {address} dev eth0',
                  f'ip -n {ns} route replace default via {gateway}']
    for site in ('dc','cloud'):
        pattern=f'python3 {BASE}/erp_lab.py {BASE} {site}'
        lines += [f'if ! ip netns pids ccie-{site} | xargs -r ps -o args= -p | grep -Fq {shlex.quote(pattern)}; then',
                  f'  ip netns exec ccie-{site} nohup {pattern} >{BASE}/{site}/service.log 2>&1 &',
                  f'  echo $! > {BASE}/{site}/pid', 'fi']
    start=BASE/'start.sh';start.write_text('\n'.join(lines)+'\n');start.chmod(0o700)
    (BASE/'bridge-map.json').write_text(json.dumps(specs,indent=2))
    run('bash',str(start))
    print('Namespace services started. Credentials stay in '+str(credentials))

if __name__=='__main__':
    main()
