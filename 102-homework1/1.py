import csv


class assignment1:
    count = [0.0 for i in range(100010)]
    category_list = []
    jaccard = []
    customers_id = []
    buy_dicts = []

    # 作业1-1 获得所有的种类，并统计每个种类的amt总值

    def init_count_category(self):
        with open('trade_new.csv', 'r', encoding='utf-8') as myFile:
            lines = csv.reader(myFile)
            for line in lines:
                category = int(line[7][:5])
                self.count[category] += float(line[17])

        total_category = 0
        print('以下每隔100种，输出一个种类的信息。')
        for i in range(100010):
            if self.count[i] != 0.0:
                total_category += 1
                self.category_list.append(i)
                if total_category % 100 == 0:
                    print('第%d种品类：种类id：%d，总价：%.2f' %
                          (total_category, i, self.count[i]))

        print('一共有%d个种类。' % total_category)

    # 得到单个人的buy_list，效率过低，现已经弃用。

    def get_buy_dict(self, a):
        buy_dict = {}

        with open('trade_new.csv', 'r', encoding='utf-8') as myFile:
            lines = csv.reader(myFile)
            for line in lines:
                if line[0] == a:
                    category = int(line[7][:5])
                    if category in buy_dict:
                        buy_dict[category] += float(line[17])
                    else:
                        buy_dict[category] = float(line[17])

        return buy_dict

    # 批量更新buy_dict

    def update_buy_dicts(self):
        self.buy_dicts = [{} for i in range(len(self.customers_id))]
        with open('trade_new.csv', 'r', encoding='utf-8') as myFile:
            lines = csv.reader(myFile)
            for line in lines:
                index = self.customers_id.index(line[5])
                category = int(line[7][:5])
                if category in self.buy_dicts[index].keys():
                    self.buy_dicts[index][category] += float(line[17])
                else:
                    self.buy_dicts[index][category] = float(line[17])

        # return buy_dicts

    # 作业1-2 计算两个特定人之间的相似度

    def get_similarity(self, a, b):
        # 创建交集树和并集树
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

    def get_all_customers(self):
        with open('trade_new.csv', 'r', encoding='utf-8') as myFile:
            lines = csv.reader(myFile)
            for line in lines:
                customer_id = line[5]
                if customer_id not in self.customers_id:
                    self.customers_id.append(customer_id)
        print('-----------------------------------------')
        print("加载所有的顾客id信息，一共有%d人。" % len(self.customers_id))

    # 作业1-2 计算所有人的Jaccard系数

    def count_jaccard(self):
        self.get_all_customers()
        self.update_buy_dicts()
        count = 0
        for a_index in range(len(self.customers_id)):
            for b_index in range(len(self.customers_id)):
                if a_index < b_index:
                    similarity = self.get_similarity(a_index, b_index)
                    self.jaccard.append(, [a_index, b_index similarity])

                    count += 1
        print('-----------------------------------------')
        print('已完成Jaccard系数计算，一共有%d个。以下输出一些示例。' % len(self.jaccard))
        for i in range(len(self.jaccard)):
            if i % 10000 == 0:
                print(self.jaccard[i])


if __name__ == '__main__':
    ass1 = assignment1()
    print('=========================================')
    print('作业1-1')
    ass1.init_count_category()
    print('=========================================')
    print('作业1-2')
    ass1.count_jaccard()
