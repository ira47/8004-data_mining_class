from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
import numpy as np
from datetime import datetime
import os

class model_runner:
    x_data_dir = '../Data/feature/'
    y_data_addr = '../Data/feature/quantity.csv'
    output_info_file = '../Data/model_info.csv'
    output_model = '../Data/model/'
    num_of_x_data = 4

    x_data = 0
    y_data = np.loadtxt('../Data/feature/quantity.csv', dtype=np.str, delimiter=',')[1:, 2].astype(np.float)
    x_train = 0
    x_test = 0
    y_train = 0
    y_test = 0


    svm_model = SVR()
    rf_model = RandomForestRegressor()
    mlp_model = MLPRegressor()

    svm_C = [0.1,1,10,100,300]
    svm_kernel = ['linear', 'poly', 'rbf', 'sigmoid']

    rf_n_estimators = [10,50,100,200]
    rf_oob_score = [True,False]

    mlp_hidden_layer_sizes = [5,10,20,30,40]
    mlp_activation = ['identity', 'logistic', 'tanh', 'relu']
    mlp_solver = ['lbfgs', 'sgd', 'adam']
    mlp_alpha = [0.00001,0.00005,0.0001,0.0002]

    def train_and_assess(self,model,folder):
        model.fit(self.x_train,self.y_train)
        joblib.dump(model, self.output_model + folder + 'model.pkl')
        y_predict = model.predict(self.x_test)
        a = ((y_predict - self.y_test) ** 2).sum()
        b = ((self.y_test - self.y_test.mean()) ** 2).sum()
        rrse = (a / b) ** 0.5

        time = datetime.now()
        output_line = ','.join([str(time), folder, str(rrse)])
        with open(self.output_info_file, 'a', encoding='utf-8') as f:
            f.write(output_line + '\n')
        print(output_line)
        return rrse


    def __init__(self):
        for recipe_index in range(self.num_of_x_data):
            self.x_data = np.loadtxt(self.x_data_dir+str(1+recipe_index)+'.csv',
                                     dtype=np.str, delimiter=',')[1:, 2:].astype(np.float)
            self.x_data = preprocessing.scale(self.x_data)
            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
                self.x_data, self.y_data, test_size=0.2)
            dir1 = 'recipe=' + str(recipe_index+1) + '/'

            for c in self.svm_C:
                dir2 = dir1 + 'svm/C=' + str(c) + '/'
                for k in self.svm_kernel:
                    dir3 = dir2 + 'kernel=' + str(k) + '/'
                    if not os.path.exists(dir3):
                        os.makedirs(dir3)
                    self.svm_model = SVR(C=c,kernel=k,max_iter=200)
                    self.train_and_assess(self.svm_model,dir3)

            for e in self.rf_n_estimators:
                dir2 = dir1 + 'rf/n_estimators=' + str(e) + '/'
                for o in self.rf_oob_score:
                    dir3 = dir2 + 'oob_score=' + str(o) + '/'
                    if not os.path.exists(dir3):
                        os.makedirs(dir3)
                    self.rf_model = RandomForestRegressor(n_estimators=e,oob_score=o)
                    self.train_and_assess(self.rf_model,dir3)

            for h in self.mlp_hidden_layer_sizes:
                dir2 = dir1 + 'mlp/hidden_layer_sizes=' + str(h) + '/'
                for a in self.mlp_activation:
                    dir3 = dir2 + 'activation=' + str(a) + '/'
                    for s in self.mlp_solver:
                        dir4 = dir3 + 'solver=' + str(s) + '/'
                        for l in self.mlp_alpha:
                            dir5 = dir4 + 'alpha=' + str(l) + '/'
                            if not os.path.exists(dir5):
                                os.makedirs(dir5)
                            self.mlp_model = MLPRegressor(hidden_layer_sizes=h,activation=a,
                                                          solver=s,alpha=l,max_iter=200)
                            self.train_and_assess(self.mlp_model,dir5)



model_runner()


