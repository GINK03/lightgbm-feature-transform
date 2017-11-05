
from sklearn.linear_model import LinearRegression
import json
import numpy as np
import sys
import pickle
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import mean_absolute_error as mae
if '--data_gen' in sys.argv:
  ys, Xs, yts, Xts = [], [], [], []
  for index, line in enumerate(open('./shrinkaged.jsonp')):
    line = line.strip()
    try:
      obj = json.loads(line)
    except json.decoder.JSONDecodeError as e:
      continue
    y, X = obj
    y = float(y)
    if index < 100000:
      yts.append(y)
      Xts.append(X)
      continue
      
    ys.append(y)
    Xs.append(X)
  ys, Xs, yts, Xts = np.array(ys), np.array(Xs), np.array(yts), np.array(Xts)
  open('dataset.pkl', 'wb').write( pickle.dumps( (ys,Xs, yts, Xts) ) )

if '--fit' in sys.argv:
  ys,Xs, yts, Xts = pickle.loads( open('dataset.pkl', 'rb').read() )
  # print(ys.shape)
  # print(Xs.shape)
  model = LinearRegression()
  model.fit(Xs, ys)

  yp = model.predict(Xs)
  delta = mae(yp.tolist(), ys.tolist())

  print('train mse: %.2f'%delta )
  
  ytp = model.predict(Xts)
  delta = mae(ytp.tolist(), yts.tolist())
  print('test mse: %.2f'%delta )
