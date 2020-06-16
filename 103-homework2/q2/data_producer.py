import csv
import datetime

class data_producer:
    sequence_input_dir = '../Data/preprocessing/'
    input_file = '../Data/trade_new.csv'
    train_start_day = 28
    test_start_day = 151
    test_end_day = 182
    start_date = datetime.datetime.strptime('2016-02-01', '%Y-%m-%d')

    pluno_to_bndno = {}
    pluno_to_sequence = {}
    bndno_to_sequence = {}
    category1_to_sequence = {}
    category2_to_sequence = {}
    category3_to_sequence = {}
    category4_to_sequence = {}
    x_names = ['pluno', 'category_1', 'category_2',
               'category_3', 'category_4', 'bndno']
    suffix_addr = '_to_day_sequence.csv'
    x_to_sequence = [pluno_to_sequence,category1_to_sequence,category2_to_sequence,
                     category3_to_sequence,category4_to_sequence,bndno_to_sequence]
    data_recipes = [[0],
                    [0,3],
                    [0,1,2,3],
                    [0,1,2,3,4,5]]


    def __init__(self):
        self.load_data()
        self.get_data_recipe('22002240',100,3)

    def load_data(self):
        for x,x_name in zip(self.x_to_sequence,self.x_names):
            addr = self.sequence_input_dir + x_name + self.suffix_addr
            with open(addr, 'r', encoding='utf8') as f:
                lines = csv.reader(f)
                for line in lines:
                    key = line[0]
                    value = list(map(float,line[1:]))
                    x[key] = value
        with open(self.input_file, 'r', encoding='utf8') as f:
            lines = csv.reader(f)
            for line in lines:
                pluno = line[7]
                bndno = line[14]
                if pluno not in self.pluno_to_bndno.keys() or \
                    self.pluno_to_bndno[pluno] == '':
                    self.pluno_to_bndno[pluno] = bndno
        for pluno,bndno in self.pluno_to_bndno.items():
            if bndno == '':
                self.pluno_to_bndno[pluno] = pluno
        # print(len(self.pluno_to_bndno.keys()))
        # for i in self.pluno_to_sequence.keys():
        #     print(i)
        #     break

    def get_feature_set_1(self, pluno, day_offset):
        if day_offset < self.train_start_day:
            return []
        # print(len(self.pluno_to_sequence.keys()))
        # print(pluno in self.pluno_to_sequence.keys())
        bndno = self.pluno_to_bndno[pluno]
        category1 = pluno[:2]
        category2 = pluno[:3]
        category3 = pluno[:4]
        category4 = pluno[:5]
        day = self.start_date + datetime.timedelta(days=day_offset)
        weekday = day.weekday()
        if weekday < 5:
            is_weekday = 1
        else:
            is_weekday = 0
        quantity = self.pluno_to_sequence[pluno][day_offset]
        past_week1 = self.pluno_to_sequence[pluno][day_offset - 7:day_offset]
        output = [pluno,bndno,category1,category2,category3,category4,
                  day_offset,is_weekday,quantity]
        output += past_week1
        return output

    def get_feature_set_2(self, pluno, day_offset):
        if day_offset < self.train_start_day:
            return []
        bndno = self.pluno_to_bndno[pluno]
        past_week1 = self.bndno_to_sequence[bndno][day_offset - 7:day_offset]
        output = past_week1
        return output

    def get_feature_set_3(self, pluno, day_offset):
        if day_offset < self.train_start_day:
            return []
        category1 = pluno[:2]
        category2 = pluno[:3]
        category3 = pluno[:4]
        category4 = pluno[:5]
        past_category1 = self.category1_to_sequence[category1][day_offset - 7:day_offset]
        past_category2 = self.category2_to_sequence[category2][day_offset - 7:day_offset]
        past_category3 = self.category3_to_sequence[category3][day_offset - 7:day_offset]
        past_category4 = self.category4_to_sequence[category4][day_offset - 7:day_offset]
        output = past_category1 + past_category2 + past_category3 + past_category4
        return output

    def get_average_max_min(self,lst):
        average = sum(lst) / len(lst)
        max_ = max(lst)
        min_ = min(lst)
        return [average,max_,min_]

    def get_feature_set_4(self, pluno, day_offset):
        if day_offset < self.train_start_day:
            return []
        past_week2 = self.pluno_to_sequence[pluno][day_offset - 14:day_offset - 7]
        past_week3 = self.pluno_to_sequence[pluno][day_offset - 21:day_offset - 14]
        past_week4 = self.pluno_to_sequence[pluno][day_offset - 28:day_offset - 21]
        output = past_week4 + past_week3 + past_week2
        return output

    def get_feature_set_5(self, pluno, day_offset):
        if day_offset < self.train_start_day:
            return []
        bndno = self.pluno_to_bndno[pluno]
        past_week2 = self.bndno_to_sequence[bndno][day_offset - 14:day_offset - 7]
        past_week3 = self.bndno_to_sequence[bndno][day_offset - 21:day_offset - 14]
        past_week4 = self.bndno_to_sequence[bndno][day_offset - 28:day_offset - 21]
        output = past_week4 + past_week3 + past_week2
        return output

    def get_feature_set_6(self, pluno, day_offset):
        if day_offset < self.train_start_day:
            return []
        category1 = pluno[:2]
        category2 = pluno[:3]
        category3 = pluno[:4]
        category4 = pluno[:5]
        past_week2 = self.category1_to_sequence[category1][day_offset - 14:day_offset - 7]
        past_week3 = self.category1_to_sequence[category1][day_offset - 21:day_offset - 14]
        past_week4 = self.category1_to_sequence[category1][day_offset - 28:day_offset - 21]
        output1 = past_week4 + past_week3 + past_week2
        past_week2 = self.category2_to_sequence[category2][day_offset - 14:day_offset - 7]
        past_week3 = self.category2_to_sequence[category2][day_offset - 21:day_offset - 14]
        past_week4 = self.category2_to_sequence[category2][day_offset - 28:day_offset - 21]
        output2 = past_week4 + past_week3 + past_week2
        past_week2 = self.category3_to_sequence[category3][day_offset - 14:day_offset - 7]
        past_week3 = self.category3_to_sequence[category3][day_offset - 21:day_offset - 14]
        past_week4 = self.category3_to_sequence[category3][day_offset - 28:day_offset - 21]
        output3 = past_week4 + past_week3 + past_week2
        past_week2 = self.category4_to_sequence[category4][day_offset - 14:day_offset - 7]
        past_week3 = self.category4_to_sequence[category4][day_offset - 21:day_offset - 14]
        past_week4 = self.category4_to_sequence[category4][day_offset - 28:day_offset - 21]
        output4 = past_week4 + past_week3 + past_week2
        output = output1 + output2 + output3 + output4
        return output

    feature_functions = [get_feature_set_1,get_feature_set_2,get_feature_set_3,
                             get_feature_set_4,get_feature_set_5,get_feature_set_6]

    def get_data_recipe(self, pluno, day_offset, recipe_index):
        feature_function_indexes = self.data_recipes[recipe_index]
        for feature_function_index in feature_function_indexes:
            feature_function = self.feature_functions[feature_function_index]
            data = feature_function(self,pluno,day_offset)
            print(data)

data_producer()


