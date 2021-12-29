import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow as tf

class ModelProcess(object):
    def __init__(self, rate_data, Nuser, Nmovie, similarity_matrix=None, U=None, I=None):
        self.rate = rate_data
        self.Nuser = Nuser
        self.Nmovie = Nmovie
        self.Nfeature = 50

        self.sim_matrix = similarity_matrix
        self.U = U
        self.I = I
        self.change = 0

    def addRating(self, user, movie, rating):
        #if user has watched movie
        #we change it else add it to rate data
        idx = np.where(self.rate[:, 0] == user)[0].astype(np.int32)
        index = np.where(self.rate[idx, 1] == movie)[0].astype(np.int32)
        if index.shape[0] == 0:
            self.rate = np.concatenate((self.rate, np.array([[user, movie, rating]])))
        else :
            # print("Update rating from", self.rate[index, 2], "to ", rating)
            self.rate[index, 2] = rating
        self.reorderRating()
        self.normalize()
        self.change += 1
        if self.change == 30:
            self.change = 0
            self.update_model(user=user)

    # def recommend(self, user):
    #     user_sim = self.sim_matrix[user].argsort(axis=0)[-11:-1]
    #     user_list = self.rate[np.where(self.rate[:, 0] == user)[0].astype(np.int32), 1]
    #     recommend_list = []
    #     predict_for_user = np.matmul(self.U[user, :], self.I[:])
    #     for n in user_sim:
    #         index = np.where(self.rate[:, 0] == n)[0].astype(np.int32)
    #         sim_list = self.rate[index, 1]
    #         for item in sim_list:
    #             if item not in user_list:
    #                 if predict_for_user[item] > 0:
    #                     recommend_list.append(item)
    
    #     return recommend_list

    def recommend(self, user, Nrecommend = 30):
        user_sim = self.sim_matrix[user].argsort(axis=0)[-10:-1]
        re_list = []
        user_list = self.rate[[np.where(self.rate[:, 0] == user)[0].astype(np.int32)], 1]
  
        for user_re in user_sim.tolist():
            idx = np.where(self.rate[:, 0] == user_re)[0].astype(np.int32)
            for sample in idx.tolist():
                movie = self.rate[sample, 1]
                if self.rate[sample, 2] > 3:
                    if movie not in user_list:
                        re_list.append(movie)

        re_list = list(set(re_list))

        pre_recom = []
        predict_matrix = tf.matmul(self.U, self.I).numpy()
        #ranking recommend list
        for movie in re_list:
            rate_pre = predict_matrix[user, movie]
            pre_recom.append((movie, rate_pre))

        index = np.array(pre_recom).argsort(axis=0)
        order_re_list = np.array(pre_recom)[index[-Nrecommend:, 1], 0].astype(np.int32).tolist()
        order_re_list.reverse()
        print(order_re_list)
        return order_re_list

    def normalize(self):
        rate_copy = self.rate.copy().astype(np.float)
        mu = np.zeros((self.Nuser, ))
        userCol = self.rate[:, 0]
        for n in range(self.Nuser):
            idx = np.where(userCol == n)[0].astype(np.int32)
            if idx.shape[0] == 0:
                continue
        item_idx = self.rate[idx, 1]
        ratings = self.rate[idx, 2]
        m = np.mean(ratings)
        mu[n] = m
        rate_copy[idx, 2] = ratings - mu[n]
        self.rate_normalize = rate_copy
        self.mu = mu
    
    def reorderRating(self):
        temp = self.rate.astype(np.int32)
        index = np.lexsort((temp[:, 1], temp[:, 0]))
        self.rate = self.rate[index]

    def update_model(self, user):
        u = self.U[user, :]
        lr = 0.1
        maxIter = 100
        idx = np.where(self.rate[:, 0] == user)[0].astype(np.int32)
        s = idx.shape[0]
        movie_idx, rating_idx = self.rate_normalize[idx, 1], self.rate_normalize[idx, 2]
        Ix = self.I[:, movie_idx.astype(np.int32)]
        lr_s = lr / s
        for iter in range(maxIter):
          grad = np.matmul(u, Ix).T - rating_idx
          grad = np.matmul(Ix, grad.reshape(s, 1)).T
          u = (u - grad * lr_s).reshape((50, ))
        self.U[user, :] = u
        self.sim_matrix = cosine_similarity(self.U)
