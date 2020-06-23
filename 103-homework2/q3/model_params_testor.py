from sklearn import preprocessing
from sklearn.externals import joblib
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
import numpy as np
from datetime import datetime
import os

class model_params_testor:
    x_data_dir = '../Data/feature/'
    y_data_addr = '../Data/feature/quantity.csv'
    output_info_file = '../Data/model_info.csv'
    output_model = '../Data/model/'
    num_of_section = 3
    recipes = ['1', '2', '3', '4']

    x_datas = []
    y_data = 0
    x_train = 0
    x_validation = 0
    y_train = 0
    y_validation = 0
    section_to_start = []
    section_to_end = []
    train_and_validate_length = 0

    svm_model = SVR()
    rf_model = RandomForestRegressor()
    mlp_model = MLPRegressor()

    def svm_c_func(self,c):
        return SVR(C=c,max_iter=200)
    svm_C = [[0.1,1,10,100,300],svm_c_func,'svm_c']

    def svm_kernel_func(self,k):
        return SVR(kernel=k,max_iter=200)
    svm_kernel = [['linear','poly','rbf','sigmoid'],svm_kernel_func,'svm_kernel']

    def rf_n_estimators_func(self,e):
        return RandomForestRegressor(n_estimators=e,n_jobs=-1)
    rf_n_estimators = [[10,50,100,200],rf_n_estimators_func,'rf_n_estimators']

    def rf_oob_score_func(self,o):
        return RandomForestRegressor(oob_score=o,n_jobs=-1)
    rf_oob_score = [[True,False],rf_oob_score_func,'rf_oob_score']

    def mlp_hidden_layer_sizes_func(self,h):
        return MLPRegressor(hidden_layer_sizes=h,max_iter=200)
    mlp_hidden_layer_sizes = [[5,10,20,30,40],mlp_hidden_layer_sizes_func,'mlp_hidden_layer_sizes']

    def mlp_activation_func(self,a):
        return MLPRegressor(activation=a,max_iter=200)
    mlp_activation = [['identity', 'logistic', 'tanh', 'relu'],mlp_activation_func,'mlp_activation']

    def mlp_solver_func(self,s):
        return MLPRegressor(solver=s,max_iter=200)
    mlp_solver = [['lbfgs', 'adam'],mlp_solver_func,'mlp_solver']

    try_list = [
        svm_C,
        svm_kernel,
        rf_n_estimators,
        rf_oob_score,
        mlp_hidden_layer_sizes,
        mlp_activation,
        mlp_solver
    ]

    def get_rrse(self,predict,target):
        a = ((predict - target) ** 2).sum()
        b = ((target - target.mean()) ** 2).sum()
        rrse = (a / b) ** 0.5
        return rrse

    def train_and_validate(self,model_func,params,name,recipe,recipe_index):
        for param in params:
            train_losses = []
            validation_losses = []
            for section in range(self.num_of_section):
                self.update_train_and_validate_xy(recipe_index, section)
                model = model_func(self,param)
                model.fit(self.x_train,self.y_train)
                output_folder = self.output_model + name + '/' + str(param) + '/'
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                joblib.dump(model, output_folder + recipe + '_' + str(section) + '.pkl')
                train_predict = model.predict(self.x_train)
                validation_predict = model.predict(self.x_validation)
                train_loss = self.get_rrse(train_predict,self.y_train)
                validation_loss = self.get_rrse(validation_predict, self.y_validation)
                train_losses.append(train_loss)
                validation_losses.append(validation_loss)
            train_loss = sum(train_losses) / len(train_losses)
            validation_loss = sum(validation_losses) / len(validation_losses)

            time = datetime.now()
            output_line = ','.join([str(time), name, str(param), recipe, str(train_loss), str(validation_loss)])
            with open(self.output_info_file, 'a', encoding='utf-8') as f:
                f.write(output_line + '\n')
            print(output_line)

    def init_data(self):
        self.y_data = np.loadtxt(self.y_data_addr, dtype=np.str, delimiter=',')[1:, 2].astype(np.float)
        for recipe in self.recipes:
            x_data_addr = self.x_data_dir + recipe + '.csv'
            x_data = np.loadtxt(x_data_addr, dtype=np.str, delimiter=',')[1:, 2:].astype(np.float)
            self.x_datas.append(preprocessing.scale(x_data))
        data_length = len(self.y_data)
        self.train_and_validate_length = int(0.8*data_length)
        self.section_to_start = \
            [int(i * self.train_and_validate_length / self.num_of_section)
             for i in range(self.num_of_section)]
        self.section_to_end = \
            [int((i + 1) * self.train_and_validate_length / self.num_of_section)
             for i in range(self.num_of_section)]

    def update_train_and_validate_xy(self, recipe_index, section):
        self.x_validation = self.x_datas[recipe_index] \
            [self.section_to_start[section]: self.section_to_end[section]]
        self.y_validation = self.y_data \
            [self.section_to_start[section]: self.section_to_end[section]]
        x_train_part1 = self.x_datas[recipe_index][0: self.section_to_start[section]]
        y_train_part1 = self.y_data[0: self.section_to_start[section]]
        x_train_part2 = self.x_datas[recipe_index] \
            [self.section_to_end[section]: self.train_and_validate_length]
        y_train_part2 = self.y_data \
            [self.section_to_end[section]: self.train_and_validate_length]
        self.x_train = np.concatenate((x_train_part1, x_train_part2), axis=0)
        self.y_train = np.concatenate((y_train_part1, y_train_part2), axis=0)
        
    def work(self):
        for recipe_index,recipe in enumerate(self.recipes):
            for [params,model_func,name] in self.try_list:
                self.train_and_validate(model_func, params, name, recipe, recipe_index)

    def __init__(self):
        self.init_data()
        self.work()


model_params_testor()