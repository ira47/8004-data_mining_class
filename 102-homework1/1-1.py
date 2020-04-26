import csv

count = [0.0 for i in range(100010)]
category_list = []
Jaccard = [[0.0 for i in range(100010)] for j in range(100010)]


def init_count_category():
    with open('trade_new.csv', 'r', encoding='utf-8') as myFile:
        lines = csv.reader(myFile)
        for line in lines:
            category = int(line[7][:5])
            count[category] += float(line[17])

    total_category = 0

    for i in range(100010):
        if count[i] != 0.0:
            category_list.append(i)
            print(i, count[i])
            total_category += 1
    print('第四品类一共有种类：' + str(total_category))

