from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

import numpy as np
import sys
import pickle
if '--make' in sys.argv:
  Xs, ys = [], []
  Xst, yst = [], []
  for index,line in enumerate(open('shrinkage/shrinkage.data')) :
    xs = [float(x) for x in line.split()]
    if index < 5000:
      yst.append(xs.pop())
      Xst.append(xs)
    else:
      ys.append(xs.pop())
      Xs.append(xs)

  open('dataset.pkl','wb').write( pickle.dumps( list(map(np.array, [Xs, ys, Xst, yst])) ) )

if '--train' in sys.argv:
  Xs, ys, Xst, yst = pickle.loads( open('dataset.pkl','rb').read() )
  print(Xs.shape)
  for name, model in [('linear_regression', linear_model.LinearRegression()), ('bayesian_ridge', linear_model.BayesianRidge()), ('elastic_net', linear_model.ElasticNet() )] :
    model = linear_model.BayesianRidge()
    model.fit(Xs, ys)

    yspred = model.predict(Xs)
    print("Mean squared error of train: %.2f"%mean_squared_error(ys, yspred))
    delta = mean_squared_error(ys, yspred)
    ystpred = model.predict(Xst)
    print("Mean squared error of test: %.2f"%mean_squared_error(yst, ystpred))
    deltat = mean_squared_error(yst, ystpred)

    open('models/%s_%.2f_%.2f'%(name, delta, deltat), 'wb').write( pickle.dumps(model) )
