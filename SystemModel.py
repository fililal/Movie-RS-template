import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow as tf

class ModelProcess(object):
    def __init__(self, rate_data, Nuser, Nmovie, similarity_matrix=None, user_profile=None, item_profile=None, Nfeature=50):
        self.rate = rate_data
        self.Nuser = Nuser
        self.Nmovie = Nmovie
        self.Nfeature = 50
        self.sim_matrix = similarity_matrix
        self.normalize()
        self.rating_sparse_tensor = self.making_sparse_tensor()
        self.lda = 0.1
        self.lr = 0.5
        self.opt = tf.keras.optimizers.Adam(learning_rate=self.lr)
        self.flag = 0
        if not (user_profile.all() == None):
            self.U = tf.Variable(initial_value=user_profile, name='user_profile')
            self.I = tf.Variable(initial_value=item_profile, name='item_profile')
        else:
            self.U = tf.Variable(initial_value=tf.random.truncated_normal([self.Nuser, self.Nfeature]), name='user_profile')
            self.I = tf.Variable(initial_value=tf.random.truncated_normal([self.Nfeature, self.Nmovie]), name='movie_profile')
            self.train()

        if similarity_matrix.all == None:
            self.make_sim_matrix()
        else:
            self.sim_matrix = similarity_matrix

        print(self.loss_function())

    ##Function for train
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

    def making_sparse_tensor(self):
        rate_sparse = tf.sparse.SparseTensor(indices=self.rate_normalize[:, :2],
                                            values=self.rate_normalize[:, 2],
                                            dense_shape=[self.Nuser, self.Nmovie])
        return rate_sparse

    def make_sim_matrix(self):
        self.sim_matrix = cosine_similarity(self.U, self.U)


    ##Training
    @tf.function
    def loss_function(self):
        rate_predict = tf.gather_nd(tf.matmul(self.U, self.I),
                                    self.rating_sparse_tensor.indices)
        loss = tf.losses.mean_squared_error(self.rating_sparse_tensor.values, rate_predict)
        return loss

    @tf.function
    def loss_regulization(self):
        regularization_loss = self.lda * (
            tf.reduce_sum(self.U*self.U)/self.U.shape[0] + tf.reduce_sum(self.I*self.I)/self.I.shape[1])
        loss = self.loss_function() + regularization_loss
        return loss

    def train(self):
        Niter = 100
        current_loss = self.loss_regulization()
        for iter in range(Niter + 1):
            self.opt.minimize(self.loss_regulization, var_list=[self.U, self.I])
            if iter % 10 == 0:
                print("Iteration ", iter,"Loss is: ", self.loss_function())
            if abs(current_loss - self.loss_regulization()) < 1e-5:
                print("Stop at iteration:", iter, "Loss is: ", self.loss_function())
                break
      
            current_loss = self.loss_regulization()
        print(self.loss_function())


    ##System Function
    def addRating(self, user, movie, rating):
        # Kiểm tra xem user đã xem movie chưa
        idx = np.where(self.rate[:, 0] == user)[0].astype(np.int32)
        idx = np.where(self.rate[idx, 1] == movie)[0]
        if idx.shape[0] == 0:
            self.rate = np.concatenate((self.rate, np.array([[user, movie, rating]])))
            self.reorderRating()
            self.normalize()
        else:
            self.rate[idx, 2] = rating

    def recommend(self, user, Nrecommend = 30):
        if user > 942:
            #Gợi ý những bộ phim mới
            # print('Hello, world')
            hot = np.where(self.rate[:, 2] == 5)[0].astype(np.int32)
            movie = self.rate[hot, 1].tolist()
            hot = list(set(self.rate[hot, 1].tolist()))
            tmp = []
            recommend_list = []
            for i in hot:
                tmp.append((i, movie.count(i)))
            tmp.sort(key=lambda x:-x[1])
            for i in tmp[:30]:
                recommend_list.append(i[0])
            # print(recommend_list)
            return recommend_list

        # Cho người dùng đã tồn tại trong hệ thống   

        # Lấy 10 user tương đồng nhất
        user_sim = self.sim_matrix[user].argsort(axis=0)[-10:-1]
        re_list = []
        user_list = self.rate[[np.where(self.rate[:, 0] == user)[0].astype(np.int32)], 1]
  
        # Từ những bộ phim mà người dùng tương đồng thích (đã xem và đánh giá cao)
        # đưa vào đề xuất cho người dùng
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

        # Xếp hạng dựa trên việc dự đoán rating các bộ phim gợi ý
        # và đưa ra 30 bộ phim có dự đoán cao nhất
        for movie in re_list:
            rate_pre = predict_matrix[user, movie]
            pre_recom.append((movie, rate_pre))

        index = np.array(pre_recom).argsort(axis=0)
        order_re_list = np.array(pre_recom)[index[-Nrecommend:, 1], 0].astype(np.int32).tolist()
        order_re_list.reverse()
        print(order_re_list)
        return order_re_list
    



