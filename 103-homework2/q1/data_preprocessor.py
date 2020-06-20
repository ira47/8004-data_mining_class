import datetime
import csv
import os

class data_preprocessor:
    input_file = '../Data/trade_new.csv'
    output_dir = '../Data/preprocessing/'

    pluno_to_day_sequence = {}
    pluno_to_bndno_dict = {}
    start_date = datetime.datetime.strptime('2030-01-01', '%Y-%m-%d')
    end_date = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')

    sequence_converter_names = \
        ['day_sequence','week_sequence','month_sequence']
    pluno_converter_names = \
        ['pluno','category_1','category_2',
         'category_3','category_4','bndno']

    '''
    --------------------------------------
    以下是各个转换器的定义函数部分
    --------------------------------------
    '''

    def get_day_sequence_to_day_sequence(self, day_sequence):
        return day_sequence

    def get_day_sequence_to_week_sequence(self, day_sequence):
        week_sequence = []
        for day_offset, sales in enumerate(day_sequence):
            day = self.start_date + datetime.timedelta(days=day_offset)
            weekday = day.weekday()
            if len(week_sequence) == 0 or weekday == 0:
                week_sequence.append(0.0)
            week_sequence[-1] += sales
        return week_sequence

    def get_day_sequence_to_month_sequence(self, day_sequence):
        month_sequence = []
        for day_offset, sales in enumerate(day_sequence):
            day = self.start_date + datetime.timedelta(days=day_offset)
            dayday = day.day
            if len(month_sequence) == 0 or dayday == 1:
                month_sequence.append(0.0)
            month_sequence[-1] += sales
        return month_sequence

    def get_pluno_to_pluno(self, pluno):
        return pluno

    def get_pluno_to_category_1(self, pluno):
        return pluno[:2]

    def get_pluno_to_category_2(self, pluno):
        return pluno[:3]

    def get_pluno_to_category_3(self, pluno):
        return pluno[:4]

    def get_pluno_to_category_4(self, pluno):
        return pluno[:5]

    def get_pluno_to_bndno(self, pluno):
        if self.pluno_to_bndno_dict[pluno] == '':
            return pluno
        return self.pluno_to_bndno_dict[pluno]

    sequence_converters = [
        get_day_sequence_to_day_sequence,
        get_day_sequence_to_week_sequence,
        get_day_sequence_to_month_sequence
    ]
    pluno_converters = [
        get_pluno_to_pluno,
        get_pluno_to_category_1,
        get_pluno_to_category_2,
        get_pluno_to_category_3,
        get_pluno_to_category_4,
        get_pluno_to_bndno
    ]

    '''
    --------------------------------------
    以下是核心函数部分
    --------------------------------------
    '''

    def load_start_and_end_date(self):
        with open(self.input_file,'r',encoding='utf8') as f:
            lines = csv.reader(f)
            for line in lines:
                date_str = line[1][:10]
                date = datetime.datetime.strptime(date_str,'%Y-%m-%d')
                if date < self.start_date:
                    self.start_date = date
                if date > self.end_date:
                    self.end_date = date

    def load_data(self):
        with open(self.input_file, 'r', encoding='utf8') as f:
            lines = csv.reader(f)
            for line in lines:
                pluno = line[7]
                bndno = line[14]
                if '.' in bndno:
                    bndno = bndno.split('.')[0]
                qty = float(line[16])
                date_str = line[1][:10]
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                day_offset = (date - self.start_date).days
                
                if pluno not in self.pluno_to_bndno_dict.keys() or \
                    self.pluno_to_bndno_dict[pluno] == '':
                    self.pluno_to_bndno_dict[pluno] = bndno

                if pluno not in self.pluno_to_day_sequence.keys():
                    self.pluno_to_day_sequence[pluno] = \
                        [0.0 for i in range((self.end_date-self.start_date).days+1)]
                self.pluno_to_day_sequence[pluno][day_offset] += qty

    def get_converted_data(self,pluno_converter,sequence_converter):
        key_to_sequence = {}
        for pluno,day_sequence in self.pluno_to_day_sequence.items():
            key = pluno_converter(self,pluno)
            sequence = sequence_converter(self,day_sequence)
            if key not in key_to_sequence.keys():
                key_to_sequence[key] = sequence
            else:
                old_sequence = key_to_sequence[key]
                new_sequence = []
                for old_sales,sales in zip(old_sequence,sequence):
                    new_sales = old_sales + sales
                    new_sequence.append(new_sales)
                key_to_sequence[key] = new_sequence
                # key_to_sequence[key] += sequence
        return key_to_sequence

    def output_data(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        for pluno_converter_index in range(len(self.pluno_converters)):
            for sequence_converter_index in range(len(self.sequence_converters)):
                pluno_converter = self.pluno_converters[pluno_converter_index]
                sequence_converter = self.sequence_converters[sequence_converter_index]
                key_to_sequence = self.get_converted_data(pluno_converter,sequence_converter)

                pluno_converter_name = self.pluno_converter_names[pluno_converter_index]
                sequence_converter_name = self.sequence_converter_names[sequence_converter_index]
                output_file = pluno_converter_name + '_to_' + sequence_converter_name + '.csv'
                output_dir_file = self.output_dir + output_file
                print('正在输出文件 ' + output_file)
                with open(output_dir_file, 'w', newline='', encoding='utf8') as w:
                    writer = csv.writer(w)
                    for key,sequence in key_to_sequence.items():
                        output_line = [key] + sequence
                        writer.writerow(output_line)

    '''
    --------------------------------------
    以下是主函数部分
    --------------------------------------
    '''

    def __init__(self):
        self.load_start_and_end_date()
        print('加载最小和最大日期成功')
        print('最小日期：' + str(self.start_date))
        print('最大日期：' + str(self.end_date))
        print('------------------------------------')
        self.load_data()
        print('加载数据成功')
        print('一共有的pluno数量：' + str(len(self.pluno_to_day_sequence.keys())))
        print('------------------------------------')
        self.output_data()
        print('输出数据成功')

data_preprocessor()




