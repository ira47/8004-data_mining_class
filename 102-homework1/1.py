import csv
import random


class assignment1:

    K = 40
    N_CUSTOMER = 486
    N_CATEGORY = 979

    '''
    成员变量注释：
    1. customers_id：
        含义：记录顾客的ID编码。
        长度：N_CUSTOMER
        成员类型：str
    2. jaccard：
        成员为字典[a,b]->J-distance。
        变量含义：a和b是buy_dict实例。J-distance是a b顾客间的Jaccard值。
        长度：0.5*(N_CUSTOMER)^2。
        成员类型：[int,int]->float
    3. buy_dicts。
        含义：每一个顾客买了什么，以dict的形式展示。
        长度：N_CUSTOMER
        成员类型：dict。key是种类的int形式表示，value是各种类的订单的amt求和。
    4. centroids
        含义：每个簇的质心。
        长度：K。
        类型：dict。key是种类的int形式表示，value取属于该簇各点中，各种类的订单的amt求和的平均数。
    5. K
        含义：K-means中划分的簇的个数。
    '''
    customers_id = []
    jaccard = {}
    buy_dicts = []
    centroids = []
    clusters_old = []
    clusters_new = []
    iter_time = 0
    '''


    以下是作业1-1代码。


    '''

    # 获得所有顾客的id

    def get_all_customers(self):
        with open('trade_new.csv', 'r', encoding='utf-8') as myFile:
            lines = csv.reader(myFile)
            for line in lines:
                customer_id = line[5]
                if customer_id not in self.customers_id:
                    self.customers_id.append(customer_id)
        print('-----------------------------------------')
        print("加载所有的顾客id信息，一共有%d人。" % len(self.customers_id))

    # 作业1-1 批量更新buy_dict

    def update_buy_dicts(self):
        self.buy_dicts = [{} for i in range(len(self.customers_id))]
        with open('trade_new.csv', 'r', encoding='utf-8') as myFile:
            lines = csv.reader(myFile)
            for line in lines:
                customer_index = self.customers_id.index(line[5])
                category = int(line[7][:5])
                if category in self.buy_dicts[customer_index].keys():
                    self.buy_dicts[customer_index][category] += float(line[17])
                else:
                    self.buy_dicts[customer_index][category] = float(line[17])

    def output_buy_dicts(self):
        print('-----------------------------------------')
        print("已按类别对用户进行商品金额汇总。下面显示一些数据。")
        for i in range(len(self.buy_dicts)):
            if i % 100 == 0:
                buy_dict = self.buy_dicts[i]
                print('用户ID：%s。它的词典：%s。' %
                      (self.customers_id[i], str(buy_dict)))
                print()

    '''


    以下是作业1-2代码。


    '''

    # 作业1-2 计算两个特定人之间的相似度

    def get_similarity(self, a, b):
        # 创建交集字典和并集字典
        union_dict = {}
        intersection_dict = {}

        # a_dict = self.buy_dicts[a]
        # b_dict = self.buy_dicts[b]

        for key in a.keys():
            if key in b.keys():
                union_dict[key] = max(a[key], b[key])
                intersection_dict[key] = min(a[key], b[key])
            else:
                union_dict[key] = a[key]
        for key in b.keys():
            if key not in a.keys():
                union_dict[key] = b[key]

        # 计算Jaccard系数
        union_total = 0
        intersection_total = 0

        for key in intersection_dict.keys():
            intersection_total += intersection_dict[key]
        for key in union_dict.keys():
            union_total += union_dict[key]
        return intersection_total/union_total

    # 作业1-2 计算所有人的Jaccard系数

    def count_jaccard(self):
        count = 0
        for a_index in range(len(self.customers_id)):
            for b_index in range(len(self.customers_id)):
                if a_index < b_index:
                    similarity = self.get_similarity(
                        self.buy_dicts[a_index], self.buy_dicts[b_index])
                    self.jaccard[a_index, b_index] = similarity
                    count += 1
        print('-----------------------------------------')
        print('已完成Jaccard系数计算，一共有%d个。' % len(self.jaccard))

    '''


    以下是作业1-3代码。


    '''

    def init_centroids(self):
        customer_index_list = []
        while len(customer_index_list) < self.K:
            customer_index = int(
                random.random()*self.N_CUSTOMER) % self.N_CUSTOMER
            if customer_index not in customer_index_list:
                self.centroids.append(self.buy_dicts[customer_index])
                customer_index_list.append(customer_index)

    def clustering(self):
        # 初始化cluster_new，使得可以存储K个数组。
        self.clusters_new = [[] for i in range(self.K)]

        # 对每个顾客，计算离他们最近的重心，并将index放入对应的cluster
        for customer_index in range(self.N_CUSTOMER):
            min_j_distance = 2
            cluster_index_for_min_j_distance = -1
            for cluster_index in range(self.K):
                similarity = self.get_similarity(
                    self.centroids[cluster_index], self.buy_dicts[customer_index])
                j_distance = 1 - similarity
                if j_distance < min_j_distance:
                    min_j_distance = j_distance
                    cluster_index_for_min_j_distance = cluster_index
            self.clusters_new[cluster_index_for_min_j_distance].append(
                customer_index)

        self.iter_time += 1

        print('-----------------------------------------')
        print('已完成第%d轮聚类计算。' % self.iter_time)

    def compare_cluster_result(self):
        return self.clusters_new == self.clusters_old

    def get_new_centroid(self, cluster_index):
        centroid = {}
        for customer_index in self.clusters_old[cluster_index]:
            buy_dict = self.buy_dicts[customer_index]
            for key in buy_dict.keys():
                if key in centroid.keys():
                    centroid[key] += buy_dict[key]
                else:
                    centroid[key] = buy_dict[key]

        cluster_member_size = len(self.clusters_old[cluster_index])
        for key in centroid.keys():
            centroid[key] /= cluster_member_size

        return centroid

    def next_generation(self):
        # 把旧的cluster数据，用新的cluster数据替换
        self.clusters_old = self.clusters_new

        # 计算新的重心对应的dict。
        for cluster_index in range(self.K):
            self.centroids[cluster_index] = self.get_new_centroid(
                cluster_index)

    def evaluate_cluster(self):
        n_show_each_cluster = 10

        print('-----------------------------------------')
        print('聚类已完成。共经历%d轮聚类计算。' % self.iter_time)

        print('以下展示聚类的结果。每个簇展示前%d个实例对应的index编号。' % n_show_each_cluster)
        for cluster_index in range(self.K):
            print('第%d个簇，共有%d个成员。部分成员index：%s。' % (cluster_index+1,  len(
                self.clusters_old[cluster_index]), self.clusters_old[cluster_index][:n_show_each_cluster]))

        # 计算SC
        sc_total_distance = 0.0
        sc_line_sum = 0
        for cluster_members in self.clusters_old:
            for i in cluster_members:
                for j in cluster_members:
                    if i < j:
                        similarity = self.jaccard[i, j]
                        distance = 1 - similarity
                        sc_total_distance += distance
                        sc_line_sum += 1
        SC = sc_total_distance/sc_line_sum

        print('该聚类的SC系数为：%f。' % SC)

        # 计算CP
        cp_total_distance = 0.0
        cp_line_sum = 0
        for cluster_index in range(self.K):
            cluster_members = self.clusters_old[cluster_index]
            for customer_index in cluster_members:
                similarity = self.get_similarity(
                    self.buy_dicts[customer_index], self.centroids[cluster_index])
                distance = 1 - similarity
                cp_total_distance += distance
                cp_line_sum += 1

        CP = cp_total_distance / cp_line_sum

        print('该聚类的CP系数为：%f。' % CP)

    def kmeans(self):
        self.init_centroids()
        while 1:
            self.clustering()
            is_equal_clustering = self.compare_cluster_result()
            if is_equal_clustering:
                break
            self.next_generation()
        self.evaluate_cluster()


if __name__ == '__main__':
    ass1 = assignment1()
    print('=========================================')
    print('作业1-1')
    ass1.get_all_customers()
    ass1.update_buy_dicts()
    ass1.output_buy_dicts()
    print('=========================================')
    print('作业1-2')
    ass1.count_jaccard()
    print('=========================================')
    print('作业1-3')
    ass1.kmeans()
