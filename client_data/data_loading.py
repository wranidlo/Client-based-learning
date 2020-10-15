import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_m1(x):
    return -np.log((1 / x) - 1)


class data_preparing:
    def __init__(self):
        # LOADING DATA, SELECTING COLUMNS AND FILLING NAN-S
        self.loaded_data = pd.read_csv("data/COVID19_open_line_list.csv")
        self.loaded_data['sex'] = self.loaded_data['sex'].str.lower()
        self.loaded_data['outcome'] = self.loaded_data['outcome'].fillna(0.01)
        self.data = self.loaded_data[['sex', 'city', 'province', 'country', 'age']]
        self.data = self.data.fillna('0')

        # ONE-HOT ENCODING DATA
        self.x_train = self.data[['sex', 'city', 'province', 'country', 'age']].copy()
        self.ohe_sex = OneHotEncoder(sparse=False)
        sex_temp = np.argmax(self.ohe_sex.fit_transform(self.x_train[['sex']]), axis=1)
        self.ohe_city = OneHotEncoder(sparse=False)
        city_temp = np.argmax(self.ohe_city.fit_transform(self.x_train[['city']]), axis=1)
        self.ohe_prov = OneHotEncoder(sparse=False)
        prov_temp = np.argmax(self.ohe_prov.fit_transform(self.x_train[['province']]), axis=1)
        self.ohe_country = OneHotEncoder(sparse=False)
        country_temp = np.argmax(self.ohe_country.fit_transform(self.x_train[['country']]), axis=1)
        self.ohe_age = OneHotEncoder(sparse=False)
        age_temp = np.argmax(self.ohe_age.fit_transform(self.x_train[['age']]), axis=1)

        # CONNECTING COLUMNS
        self.x_train = np.array([sex_temp, city_temp, prov_temp, country_temp, age_temp]).transpose()

        self.print_top_rows()
        # print(self.ohe_sex.inverse_transform([self.x_train[4]]))
        # print(self.ohe_city.get_feature_names())

        # PREPARING TARGET DATA
        self.y_train = self.loaded_data.pop('outcome').values
        self.y_train[self.y_train == 'death'] = 1
        self.y_train[self.y_train == 'died'] = 1
        self.y_train[self.y_train == 'discharged'] = 0
        self.y_train[self.y_train == 'discharge'] = 0
        self.y_train[self.y_train == 'stable'] = 0.005
        self.y_train[(self.y_train != 1) & (self.y_train != 0) & (self.y_train != 0.05) & (self.y_train != 0.1)] = 0

        # DIVIDING DATA INTO GROUPS
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.x_train, self.y_train, test_size=0.2, random_state=42)

        # LINEAR REGRESSION
        self.lin = LinearRegression()
        self.lin.fit(self.x_train, sigmoid_m1(self.y_train.astype(float) * 0.9 + 0.05))

    def get_columns(self):
        return self.data.columns

    def print_top_rows(self):
        print("Normal data\n", self.data.head(5))
        print("Encoded data\n", self.x_train[0:5])

    def encode(self, data):
        print(len(data['sex']))
        if len(data['sex']) == 1:
            sex_temp = np.argmax(self.ohe_sex.transform([data['sex']]), axis=1)
            city_temp = np.argmax(self.ohe_city.transform([data['city']]), axis=1)
            prov_temp = np.argmax(self.ohe_prov.transform([data['province']]), axis=1)
            country_temp = np.argmax(self.ohe_country.transform([data['country']]), axis=1)
            age_temp = np.argmax(self.ohe_age.transform([data['age']]), axis=1)
            return np.array([sex_temp, city_temp, prov_temp, country_temp, age_temp]).transpose()
        sex_temp = np.argmax(self.ohe_sex.transform(np.array(data['sex']).reshape(-1, 1)), axis=1)
        city_temp = np.argmax(self.ohe_city.transform(np.array(data['city']).reshape(-1, 1)), axis=1)
        prov_temp = np.argmax(self.ohe_prov.transform(np.array(data['province']).reshape(-1, 1)), axis=1)
        country_temp = np.argmax(self.ohe_country.transform(np.array(data['country']).reshape(-1, 1)), axis=1)
        age_temp = np.argmax(self.ohe_age.transform(np.array(data['age']).reshape(-1, 1)), axis=1)
        return np.array([sex_temp, city_temp, prov_temp, country_temp, age_temp]).transpose()

    def decode(self, data):
        print(data.transpose())
        sex_temp = self.ohe_sex.inverse_transform([data[0]])
        city_temp = self.ohe_city.inverse_transform([data[1]])
        prov_temp = self.ohe_prov.inverse_transform([data[2]])
        country_temp = self.ohe_country.inverse_transform([data[3]])
        age_temp = self.ohe_age.inverse_transform([data[4]])
        return np.array([sex_temp, city_temp, prov_temp, country_temp, age_temp]).transpose()

    def predict_probability(self, data):
        encoded = self.encode(data)
        return sigmoid(self.lin.predict(encoded))

'''
data_dict = {'sex': ['male'], 'city': ['Chaohu City, Hefei City'], 'province': ['Anhui'], 'country': ['China'],
             'age': ['80']}
data_frame = pd.DataFrame.from_dict(data_dict)
dat_prep = data_preparing()
enc = dat_prep.encode(data_frame)
print("Encoded test data\n", enc)
for e in dat_prep.lin.predict(dat_prep.x_test):
    print(sigmoid(e))
'''