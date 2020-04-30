import csv
import random


class assignment3:

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
    dicts = []
    clusters_old = []
    clusters_new = []
    iter_time = 0

    # 获得所有顾客的id

    def get_all_customers(self):
        with open('trade_new.csv', 'r', encoding='utf-8') as myFile:
            lines = csv.reader(myFile)
            for line in lines:
                customer_id = line[5]
                if customer_id not in self.customers_id:
                    self.customers_id.append(customer_id)

    # 批量更新第四等级的buy_dict

    def update_basic_dicts(self):
        self.dicts = [[{}, {}, {}, {}] for i in range(len(self.customers_id))]

        with open('trade_new.csv', 'r', encoding='utf-8') as myFile:
            lines = csv.reader(myFile)
            for line in lines:
                customer_index = self.customers_id.index(line[5])
                category = int(line[7][:5])
                if category in self.dicts[customer_index][3].keys():
                    self.dicts[customer_index][3][category] += float(line[17])
                else:
                    self.dicts[customer_index][3][category] = float(line[17])

    def update_higher_level_buy_dicts(self):
        for customer_index in range(len(self.customers_id)):
            for level in range(3, 0, -1):
                buy_dict_new = {}
                buy_dict_old = self.dicts[customer_index][level]
                for key_old in buy_dict_old.keys():
                    key_new = int(key_old / 10)
                    if key_new in buy_dict_new.keys():
                        buy_dict_new[key_new] += buy_dict_old[key_old]
                    else:
                        buy_dict_new[key_new] = buy_dict_old[key_old]
                self.dicts[customer_index][level-1] = buy_dict_new

    # 计算交集树和并集树在某一个level上的相似度
    def get_similarity(self, intersection, union, get_all_included):
        # total_similarity其中的一个similarity，是一个节点对UR的相似度。
        total_similarity = 0.0
        node_size = len(intersection)

        for key_intersection in intersection.keys():
            # 计算一个节点对UR的相似度。
            intersection_price = intersection[key_intersection]
            union_price = 0.0
            parent_intersection = int(key_intersection/10)
            for key_union in union.keys():
                parent_union = int(key_intersection/10)
                if get_all_included or parent_union == parent_intersection:
                    union_price += union[key_union]
            total_similarity += intersection_price/union_price
        similarity = total_similarity/node_size

        return similarity
    # 计算两个dict_vector之间的距离

    def get_distance(self, a, b):
        # 创建交集字典和并集字典
        union = []
        intersection = []

        for level in range(4):
            union_dict = {}
            intersection_dict = {}
            a_dict = a[level]
            b_dict = b[level]
            for key in a_dict.keys():
                if key in b_dict.keys():
                    union_dict[key] = max(a_dict[key], b_dict[key])
                    intersection_dict[key] = min(a_dict[key], b_dict[key])
                else:
                    union_dict[key] = a_dict[key]
            for key in b_dict.keys():
                if key not in a_dict.keys():
                    union_dict[key] = b_dict[key]

            union.append(union_dict)
            intersection.append(intersection_dict)

        # 计算距离
        sim1 = self.get_similarity(intersection[0], union[0], True)
        sim2 = self.get_similarity(intersection[1], union[1], False)
        sim3 = self.get_similarity(intersection[2], union[2], False)
        sim4 = self.get_similarity(intersection[3], union[3], False)

        distance = 1 - (sim1+sim2*2+sim3*3+sim4*4)/10
        return distance

    # 计算所有人的Jaccard系数

    def count_all_jaccard(self):
        for a_index in range(len(self.customers_id)):
            for b_index in range(len(self.customers_id)):
                if a_index < b_index:
                    jaccard = self.get_jaccard_sample_sample(a_index, b_index)
                    self.jaccard[a_index, b_index] = jaccard
        print('-----------------------------------------')
        print('已完成Jaccard系数计算，一共有%d个。' % len(self.jaccard))

    def init_centroids(self):
        customer_index_list = []
        while len(customer_index_list) < self.K:
            customer_index = int(
                random.random()*self.N_CUSTOMER) % self.N_CUSTOMER
            if customer_index not in customer_index_list:
                self.centroids_level_4.append(
                    self.buy_dicts_level_4[customer_index])
                self.centroids_level_3.append(
                    self.buy_dicts_level_3[customer_index])
                self.centroids_level_2.append(
                    self.buy_dicts_level_2[customer_index])
                self.centroids_level_1.append(
                    self.buy_dicts_level_1[customer_index])
                customer_index_list.append(customer_index)

    def clustering(self):
        # 初始化cluster_new，使得可以存储K个数组。
        self.clusters_new = [[] for i in range(self.K)]

        # 对每个顾客，计算离他们最近的重心，并将index放入对应的cluster
        for customer_index in range(self.N_CUSTOMER):
            min_j_distance = 2
            cluster_index_for_min_j_distance = -1
            for cluster_index in range(self.K):
                similarity = self.get_jaccard_centroid_sample(
                    cluster_index, customer_index)
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

    # 给一个cluster，计算其质心。
    def get_new_centroid(self, cluster_index, level):
        centroid = {}
        for customer_index in self.clusters_old[cluster_index]:
            # 取对应level的buy_dict
            if level == 1:
                buy_dict = self.buy_dicts_level_1[customer_index]
            elif level == 2:
                buy_dict = self.buy_dicts_level_2[customer_index]
            elif level == 3:
                buy_dict = self.buy_dicts_level_3[customer_index]
            elif level == 4:
                buy_dict = self.buy_dicts_level_4[customer_index]

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
            self.centroids_level_1[cluster_index] = self.get_new_centroid(
                cluster_index, 1)
            self.centroids_level_2[cluster_index] = self.get_new_centroid(
                cluster_index, 2)
            self.centroids_level_3[cluster_index] = self.get_new_centroid(
                cluster_index, 3)
            self.centroids_level_4[cluster_index] = self.get_new_centroid(
                cluster_index, 4)

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
                similarity = self.get_jaccard_centroid_sample(
                    cluster_index, customer_index)
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
    ass2 = assignment2()
    print('=========================================')
    print('作业2-1')
    ass2.get_all_customers()
    ass2.buy_dicts_level_4 = ass2.update_basic_buy_dicts()
    ass2.buy_dicts_level_3 = ass2.update_higher_level_buy_dicts(
        ass2.buy_dicts_level_4)
    ass2.buy_dicts_level_2 = ass2.update_higher_level_buy_dicts(
        ass2.buy_dicts_level_3)
    ass2.buy_dicts_level_1 = ass2.update_higher_level_buy_dicts(
        ass2.buy_dicts_level_2)
    ass2.output_buy_dicts([100, 200])
    print('=========================================')
    print('作业2-2')
    ass2.count_all_jaccard()
    print('=========================================')
    print('作业2-3')
    ass2.kmeans()
