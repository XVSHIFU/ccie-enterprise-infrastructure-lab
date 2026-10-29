"""Run inside a lab namespace; credentials never appear in stdout."""
import base64,json,ssl,sys,urllib.request,urllib.error,time
from pathlib import Path
p=Path('/opt/ccie-business-lab')
c=json.loads((p/'credentials.json').read_text())
url=sys.argv[1]
headers={} if '--anonymous' in sys.argv else {'Authorization':'Basic '+base64.b64encode((c['user']+':'+c['password']).encode()).decode()}
start=time.monotonic()
try:
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers),context=ssl.create_default_context(cafile=str(p/'server.crt')),timeout=10) as r:
        result={'url':url,'status':r.status,'body':json.load(r)}
except urllib.error.HTTPError as e:result={'url':url,'status':e.code,'body':e.read().decode()}
except Exception as e:result={'url':url,'error':str(e)}
result['elapsed_seconds']=round(time.monotonic()-start,3)
print(json.dumps(result))
sys.exit(0 if result.get('status')==(401 if '--anonymous' in sys.argv else 200) else 1)
