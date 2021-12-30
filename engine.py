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
  U = pd.read_csv('Data/U.csv').to_numpy()
  I = pd.read_csv('Data/I.csv').to_numpy()
  Nuser = int(943)
  Nmovie = int(1682)
  ratings_base = pd.read_csv('Data/train.csv')
  rate = ratings_base.to_numpy()
  sim_matrix = pd.read_csv('Data/sim.csv').to_numpy()
  U = pd.read_csv('Data/U.csv').to_numpy()
  I = pd.read_csv('Data/I.csv').to_numpy()
  return ModelProcess(rate_data=rate, Nuser=Nuser, Nmovie=Nmovie,
                      similarity_matrix=sim_matrix,
                      user_profile=U, item_profile=I)


  