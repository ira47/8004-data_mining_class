import csv


class assignment1:
    category_max_sell = []
    jaccard = []                    # 一个
    customers_id = []
    buy_dicts = []
    category_index = {}
    category_total = 0

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
                    self.jaccard.append([a_index, b_index, similarity])

                    count += 1
        print('-----------------------------------------')
        print('已完成Jaccard系数计算，一共有%d个。以下输出一些示例。' % len(self.jaccard))
        for i in range(len(self.jaccard)):
            if i % 10000 == 0:
                print(self.jaccard[i])
    # 设计一个获得种类索引的函数

    def update_category_index(self):
        with open('trade_new.csv', 'r', encoding='utf-8') as myFile:
            lines = csv.reader(myFile)
            for line in lines:
                category = int(line[7][:5])
                if category not in self.category_index.keys():
                    self.category_index[category] = self.category_total
                    self.category_total += 1

        print('-----------------------------------------')
        print('已完成种类索引，一共有%d个种类。' % self.category_total)

    # 针对一个购买词典，生成其对应的向量，用来做k-means
    def get_sample_vector(self, buy_dict):
        vector = [0.0 for i in range(self.category_total)]
        for key in buy_dict.keys():
            index = self.category_index[key]
            vector[index] = buy_dict[key]
        return vector

    def kmeans(self):
        # 把用户的dict做成向量
        buy_vectors = []
        for buy_dict in self.buy_dicts:
            vector = self.get_sample_vector(buy_dict)
            buy_vectors.append(vector)


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
    ass1.update_category_index()
