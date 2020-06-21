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

    x_data = 0
    y_data = np.loadtxt('../Data/feature/quantity.csv', dtype=np.str, delimiter=',')[1:, 2].astype(np.float)
    x_train = 0
    x_test = 0
    y_train = 0
    y_test = 0

    recipes = ['1', '2', '3', '4']
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
        mlp_hidden_layer_sizes,
        mlp_activation,
        mlp_solver
    ]

    def get_rrse(self,predict,target):
        a = ((predict - target) ** 2).sum()
        b = ((target - target.mean()) ** 2).sum()
        rrse = (a / b) ** 0.5
        return rrse

    def train_and_assess(self,model_func,params,name,recipe):
        for param in params:
            model = model_func(self,param)
            model.fit(self.x_train,self.y_train)
            output_folder = self.output_model + name + '/' + str(param) + '/'
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            joblib.dump(model, output_folder + recipe + '.pkl')
            train_predict = model.predict(self.x_train)
            test_predict = model.predict(self.x_test)
            train_loss = self.get_rrse(train_predict,self.y_train)
            test_loss = self.get_rrse(test_predict, self.y_test)

            time = datetime.now()
            output_line = ','.join([str(time), name, str(param), recipe, str(train_loss), str(test_loss)])
            with open(self.output_info_file, 'a', encoding='utf-8') as f:
                f.write(output_line + '\n')
            print(output_line)


    def __init__(self):
        total_length = len(self.y_data)
        train_length = int(0.8*total_length)
        self.y_train = self.y_data[:train_length]
        self.y_test = self.y_data[train_length:]
        for recipe in self.recipes:
            self.x_data = np.loadtxt(self.x_data_dir + recipe + '.csv',
                                     dtype=np.str, delimiter=',')[1:, 2:].astype(np.float)
            self.x_data = preprocessing.scale(self.x_data)
            self.x_train = self.x_data[:train_length]
            self.x_test = self.x_data[train_length:]
            for [params,model_func,name] in self.try_list:
                self.train_and_assess(model_func,params,name,recipe)


model_params_testor()