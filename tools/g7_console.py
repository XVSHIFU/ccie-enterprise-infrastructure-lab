"""Collect EVE lab console evidence using explicitly selected console ports."""
import argparse, socket, time, re
from pathlib import Path

class Console:
    def __init__(self, host, port):
        self.s = socket.create_connection((host, port), 5)
        self.s.settimeout(.25)
        self.pending = b''
    def read(self, seconds=2):
        end = time.monotonic() + seconds
        out = bytearray()
        while time.monotonic() < end:
            try: data = self.pending + self.s.recv(65536)
            except socket.timeout: continue
            self.pending = b''
            if not data: break
            i = 0
            while i < len(data):
                if data[i] != 255:
                    out.append(data[i]); i += 1; continue
                if i + 1 >= len(data): self.pending = data[i:]; break
                cmd = data[i+1]
                if cmd == 255: out.append(255); i += 2
                elif cmd in (251,252,253,254):
                    if i+2 >= len(data): self.pending = data[i:]; break
                    opt=data[i+2]
                    if cmd == 251: self.s.sendall(bytes([255,253 if opt in (0,1,3) else 254,opt]))
                    elif cmd == 253: self.s.sendall(bytes([255,251 if opt in (0,3) else 252,opt]))
                    i += 3
                elif cmd == 250:
                    stop=data.find(b'\xff\xf0',i+2)
                    if stop < 0: self.pending=data[i:]; break
                    i=stop+2
                else: i += 2
        text=out.decode('utf-8','replace')
        text=re.sub(r'\x1b\][^\x07]*(?:\x07)', '', text)
        return re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', text).replace('\r','')
    def send(self, command): self.s.sendall(command.encode()+b'\r\n')

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('port',type=int); p.add_argument('name')
    p.add_argument('commands',nargs='*'); p.add_argument('--wait',type=float,default=2)
    a=p.parse_args()
    c=Console('192.168.1.19',a.port)
    output=c.read(1); c.send(''); output+=c.read(1)
    for cmd in a.commands:
        c.send(cmd); output+=c.read(a.wait)
    c.s.close()
    dest=Path(__file__).resolve().parents[1]/'tests'/'G7-restore'
    dest.mkdir(parents=True,exist_ok=True)
    (dest/(a.name+'.txt')).write_text(output,encoding='utf-8')
    print(output)
