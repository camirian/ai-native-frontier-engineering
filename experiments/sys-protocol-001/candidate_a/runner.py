import json,sys
from protocol import initial,step
d=initial()
for line in sys.stdin:
 r=step(d,json.loads(line));d=r['snapshot'];print(json.dumps(r,sort_keys=True))
