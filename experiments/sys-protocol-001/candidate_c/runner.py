import json,sys
from protocol import initial,apply
d=initial()
for line in sys.stdin:
 r=apply(d,json.loads(line));d=r['snapshot'];print(json.dumps(r,sort_keys=True))
