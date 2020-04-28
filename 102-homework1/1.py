import csv
import random


class assignment1:

    K = 10
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
        变量含义：a和b是顾客的索引号index，满足a<b。J-distance是a b顾客间的Jaccard值。
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

        a_dict = self.buy_dicts[a]
        b_dict = self.buy_dicts[b]

        for key in a_dict.keys():
            if key in b_dict.keys():
                union_dict[key] = min(a_dict[key], b_dict[key])
                intersection_dict[key] = max(a_dict[key], b_dict[key])
            else:
                intersection_dict[key] = a_dict[key]
        for key in b_dict.keys():
            if key not in a_dict.keys():
                intersection_dict[key] = b_dict[key]

        # 计算Jaccard系数
        union_total = 0
        intersection_total = 0

        for key in intersection_dict.keys():
            intersection_total += intersection_dict[key]
        for key in union_dict.keys():
            union_total += union_dict[key]
        return union_total/intersection_total

    # 作业1-2 计算所有人的Jaccard系数

    def count_jaccard(self):
        count = 0
        for a_index in range(len(self.customers_id)):
            for b_index in range(len(self.customers_id)):
                if a_index < b_index:
                    similarity = self.get_similarity(a_index, b_index)
                    self.jaccard[a_index, b_index] = similarity
                    count += 1
        print('-----------------------------------------')
        print('已完成Jaccard系数计算，一共有%d个。' % len(self.jaccard))

    '''
    

    以下是作业1-3代码。


    '''

    def init_centroids(self):
        customer_index_list = []
        while len(customer_index_list) < K:
            customer_index = int(
                random.random()*self.N_CUSTOMER) % self.N_CUSTOMER
            if customer_index not in customer_index_list:
                self.centroids.apppend(buy_dicts[customer_index])
                customer_index_list.append(customer_index)

    def clustering(self):

    def compare_cluster_result(self):

    def next_generation(self):

    def evaluate_cluster(self):

    def kmeans(self):
        self.init_centroids()
        while 1:
            self.clustering()
            is_equal_clustering_result = self.compare_cluster_result()
            if is_equal_clustering_result:
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
