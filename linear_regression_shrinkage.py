from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

import numpy as np
import sys
import pickle
if '--shrinkage' in sys.argv:
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

from sklearn.datasets import load_svmlight_file
if '--original' in sys.argv:
  if '--make' in sys.argv:

    # at firset scan max
    max_index = 0
    for enume, line in enumerate(open('./dataset/test')):
      ents = line.split()
      target = ents.pop(0)
      max_index = max( [max_index, max([int(index) for index, weight in [x.split(':') for x in ents] ]) ] )
      #print(max_index)
    Xs, ys = [], []
    Xst, yst = [], []
    for enume, line in enumerate(open('./dataset/test')):
      print( enume )
      ents = line.split()
      y = float(ents.pop(0))
      xs = [0.0]*(max_index+1)
      for index, weight in [x.split(':') for x in ents]:
        index, weight = int(index), float(weight)    
        xs[index] = weight 
     
      if enume < 3000:
        Xst.append( xs )
        yst.append( y )
      else:
        Xs.append( xs )
        ys.append( y )
      
      if enume > 15000:
        break
    from scipy import sparse
    open('dataset_original.pkl','wb').write( pickle.dumps( [sparse.csr_matrix(np.array(Xs)), np.array(ys), sparse.csr_matrix(np.array(Xst)), np.array(yst) ], protocol=4 ))

  if '--train' in sys.argv:
    Xs, ys, Xst, yst = pickle.loads( open('dataset_original.pkl','rb').read() )
    print(Xs.shape)
    print(ys.shape)
    for name, model in [('linear_regression', linear_model.LinearRegression()), ('bayesian_ridge', linear_model.BayesianRidge()), ('elastic_net', linear_model.ElasticNet() )] :
      model = linear_model.BayesianRidge()
      print('now fitting', name)
      model.fit(Xs.todense(), ys)
    
      yspred = model.predict(Xs.todense())
      print("Mean squared error of train: %.2f"%mean_squared_error(ys, yspred))
      delta = mean_squared_error(ys, yspred)
      ystpred = model.predict(Xst.todense())
      print("Mean squared error of test: %.2f"%mean_squared_error(yst, ystpred))
      deltat = mean_squared_error(yst, ystpred)

      open('models/original_%s_%.2f_%.2f'%(name, delta, deltat), 'wb').write( pickle.dumps(model) )
