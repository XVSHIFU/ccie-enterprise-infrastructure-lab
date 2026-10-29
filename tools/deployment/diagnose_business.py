"""Read-only gateway and HTTPS diagnosis; use the rebuilt lab's actual console port."""
import argparse
from datetime import datetime, timezone
import getpass
import json
from pathlib import Path
import re
import sys
import paramiko

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from g7_console import Console

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--eve-host',required=True)
    p.add_argument('--gateway-port',required=True,type=int)
    p.add_argument('--console-host',help='Optional localhost when using an SSH tunnel')
    p.add_argument('--username',default='root')
    p.add_argument('--label',default='normal')
    p.add_argument('--out',type=Path,default=Path('tests/rebuild/business'))
    a=p.parse_args();password=getpass.getpass('EVE SSH password: ')
    c=Console(a.console_host or a.eve_host,a.gateway_port);raw=c.read(.5)
    try:
        for cmd in ['','enable','terminal length 0','show ip interface brief','show track','show ip route static','show ip nat translations']:
            c.s.sendall(cmd.encode()+b'\r');raw+=c.read(1.2)
    finally:c.s.close()
    links={}
    for ident,name,interface in [(41,'SD-WAN','Ethernet0/1'),(61,'DMVPN','Ethernet0/2')]:
        match=re.search(r'Track '+str(ident)+r'\s*\n(.*?)(?=\nTrack |\n\w+[>#]|\Z)',raw,re.S)
        state=re.search(r'Reachability is (\w+)',match.group(1)) if match else None
        iface=next((x.strip() for x in raw.splitlines() if x.startswith(interface+' ')),None)
        links[name]={'track':state.group(1) if state else 'unknown','interface':iface}
    s=paramiko.SSHClient();s.load_system_host_keys();s.set_missing_host_key_policy(paramiko.RejectPolicy())
    s.connect(a.eve_host,username=a.username,password=password,timeout=10)
    apps=[]
    try:
        for address in ['10.2.100.20','10.3.101.20']:
            _,o,e=s.exec_command('ip netns exec ccie-branch python3 /opt/ccie-business-lab/probe.py https://'+address+':8443/api/orders')
            body=o.read().decode();error=e.read().decode()
            try:apps.append(json.loads(body))
            except ValueError:apps.append({'error':error or body})
    finally:s.close()
    findings=[]
    for name,item in links.items():
        if item['track']!='Up':
            reason='本地上联被管理性关闭' if 'administratively down' in (item['interface'] or '') else '探测目标不可达或采集不完整，检查接口、下一跳、隧道与回程'
            findings.append(name+'：'+reason)
    healthy=all(x.get('status')==200 for x in apps)
    report={'time':datetime.now(timezone.utc).isoformat(),'label':a.label,
            'status':'PASS' if healthy and not findings else 'DEGRADED' if healthy else 'FAIL',
            'links':links,'applications':apps,'diagnosis':findings or ['接口探测正常；结合应用结果判断业务状态']}
    a.out.mkdir(parents=True,exist_ok=True)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    (a.out/(stamp+'-gateway.txt')).write_text(raw,encoding='utf-8')
    (a.out/(stamp+'-diagnosis.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
