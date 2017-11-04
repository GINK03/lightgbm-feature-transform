import f


fps = []
for i in range(100):
  fp = eval('f.PredictTree%d'%i)
  fps.append(fp)

import statistics
for line in open('../misc/xgb_format'):
  line = line.strip()
  es = line.split()
  ans = es.pop(0)
  vals = []
  for val in [e.split(':') for e in es]:
    key = int(val[0])
    val = float(val[1])
    vals.append( (key,val) )
  vals = dict(vals)
  for i in range(500000):
    if vals.get(i) is None:
      vals[i] = 0.0
  #print(ans, vals)

  ws = []
  for fp in fps:
    ws.append( fp(vals) )
  print(ws)
  print(sum(ws))

print('a')
