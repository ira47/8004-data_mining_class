from sklearn import preprocessing
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
import numpy as np
from datetime import datetime

class train_and_test:
    x_data_dir = '../Data/feature/'
    y_data_addr = '../Data/feature/quantity.csv'
    recipes = ['1', '2', '3', '4']

    x_trains = []
    x_tests = []
    y_train = 0
    y_test = 0

    svm_model = SVR(C=1,kernel='rbf',max_iter=200)
    rf_model = RandomForestRegressor(n_estimators=200,oob_score=True,n_jobs=-1)
    mlp_model = MLPRegressor(hidden_layer_sizes=5,activation='identity',solver='adam',max_iter=200)

    try_list = [
        [svm_model,'svm'],
        [rf_model,'rf'],
        [mlp_model,'mlp']
    ]

    def get_rrse(self, predict, target):
        a = ((predict - target) ** 2).sum()
        b = ((target - target.mean()) ** 2).sum()
        rrse = (a / b) ** 0.5
        return rrse

    def train_and_test(self, model, name, recipe, recipe_index):
        model.fit(self.x_trains[recipe_index], self.y_train)

        train_predict = model.predict(self.x_trains[recipe_index])
        test_predict = model.predict(self.x_tests[recipe_index])
        train_loss = self.get_rrse(train_predict, self.y_train)
        test_loss = self.get_rrse(test_predict, self.y_test)

        time = datetime.now()
        output_line = ','.join([str(time), name, recipe, str(train_loss), str(test_loss)])
        print(output_line)

    def init_data(self):
        y_data = np.loadtxt(self.y_data_addr, dtype=np.str, delimiter=',')[1:, 2].astype(np.float)
        data_length = len(y_data)
        train_and_validate_length = int(0.8 * data_length)
        self.y_train = y_data[:train_and_validate_length]
        self.y_test = y_data[train_and_validate_length:]
        for recipe in self.recipes:
            x_data_addr = self.x_data_dir + recipe + '.csv'
            x_data = np.loadtxt(x_data_addr, dtype=np.str, delimiter=',')[1:, 2:].astype(np.float)
            x_data = preprocessing.scale(x_data)
            self.x_trains.append(x_data[:train_and_validate_length])
            self.x_tests.append(x_data[train_and_validate_length:])

    def work(self):
        for recipe_index, recipe in enumerate(self.recipes):
            for [model, name] in self.try_list:
                self.train_and_test(model, name, recipe, recipe_index)

    def __init__(self):
        self.init_data()
        self.work()

train_and_test()