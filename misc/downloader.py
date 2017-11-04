import os
import sys


if '--specified' in sys.argv:
  os.system('mc cp hatsuzuki/lightgbm-shrinkage-dataset/xgb_format .')
  os.system('mc cp hatsuzuki/lightgbm-shrinkage-dataset/term_index.pkl .')
  os.system('mc cp hatsuzuki/lightgbm-shrinkage-dataset/LightGBM_model.txt .')
  os.system('mc cp hatsuzuki/lightgbm-shrinkage-dataset/gbdt_prediction.cpp .')
