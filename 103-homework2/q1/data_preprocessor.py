import datetime

class data_preprocessor:
    INPUT_FILE = '../Data/trade_new.csv'
    OUTPUT_DIR = '../Data/preprocessing/'

    get_pluno_to_day_sequence = {}
    pluto_to_bndno_dict = {}
    start_date = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')
    end_date = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')

    day_sequence_converters = [
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
    day_sequence_converter_names = \
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
                week_sequence.append(0)
            week_sequence[-1] += sales
        return week_sequence

    def get_day_sequence_to_month_sequence(self, day_sequence):
        month_sequence = []
        for day_offset, sales in enumerate(day_sequence):
            day = self.start_date + datetime.timedelta(days=day_offset)
            dayday = day.day
            if len(month_sequence) == 0 or dayday == 1:
                month_sequence.append(0)
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
        return self.pluto_to_bndno_dict[pluno]





