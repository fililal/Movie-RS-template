import pandas as pd
import numpy as np
import tensorflow as tf

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from SystemModel import ModelProcess

# Start recommend engine
# return SystemModel
def process():
  U = pd.read_csv('User_profile.csv').to_numpy()
  I = pd.read_csv('Item_profile.csv').to_numpy()
  Nuser = int(943)
  Nmovie = int(1682)
  r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
  ratings_base = pd.read_csv('ua.base', sep = '\t', names = r_cols, encoding='latin-1')
  del ratings_base['unix_timestamp']
  rate = ratings_base.to_numpy()
  rate[:, :2] -= 1
  # print(rate[0, :])
  sim_matrix = pd.read_csv('sim_matrix.csv').to_numpy()
  U = pd.read_csv('User_profile.csv').to_numpy()
  I = pd.read_csv('Item_profile.csv').to_numpy()
  return ModelProcess(rate_data=rate, Nuser=Nuser, Nmovie=Nmovie,
                      similarity_matrix=sim_matrix,
                      U=U, I=I)
  