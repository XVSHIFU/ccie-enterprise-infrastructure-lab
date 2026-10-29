"""Run on EVE: migrate the read-only order demo, verify content, switch entrypoint."""
import hashlib
import json
from pathlib import Path
import sqlite3
from contextlib import closing

root=Path('/opt/ccie-business-lab')
def rows(site):
    with closing(sqlite3.connect(root/site/'orders.sqlite')) as c:
        return c.execute('SELECT * FROM orders ORDER BY id').fetchall()

with sqlite3.connect(root/'dc/orders.sqlite') as source, sqlite3.connect(root/'cloud/orders.sqlite') as target:
    source.backup(target)
source.close()
target.close()
before,after=rows('dc'),rows('cloud')
if before!=after or not before:
    raise SystemExit('Migration verification failed; entrypoint unchanged.')
digest=hashlib.sha256(json.dumps(after,separators=(',',':')).encode()).hexdigest()
(root/'dc/mode').write_text('proxy-cloud')
report={'order_count':len(after),'data_sha256':digest,'backend':'cloud','entrypoint':'https://10.2.100.20:8443/api/orders'}
(root/'migration.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
