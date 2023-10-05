import os

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split

from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

import pickle


np.random.seed(42)


class DataTransformation:
    def __init__(self):
        self.df = pd.read_csv('data/processed/ml_dataset.csv')

        self.ros = RandomOverSampler()
        self.rus = RandomUnderSampler()
        self.standard_scaler = StandardScaler()
    
    def transform_data(self):
        X = self.df.drop('paid', axis=1)
        y = self.df.paid

        X_oversampled, y_oversampled = self.ros.fit_resample(X, y)
        X_resampled, y_resampled = self.rus.fit_resample(X_oversampled, y_oversampled)

        X_scaled = self.standard_scaler.fit_transform(X_resampled)

        with open('outputs/standard_scaler.pickle', 'wb') as file:
            pickle.dump(self.standard_scaler, file, protocol=pickle.HIGHEST_PROTOCOL)

        self.X_train, remaining_data, self.y_train, remaining_target = train_test_split(X_scaled, y_resampled, test_size=0.4)
        self.X_val, self.X_test, self.y_val, self.y_test = train_test_split(remaining_data, remaining_target, test_size=0.5)

    def to_csv(self, train_directory, val_directory, test_directory):
        self.X_train = pd.DataFrame(self.X_train)
        self.X_test = pd.DataFrame(self.X_test)
        self.X_val = pd.DataFrame(self.X_val)

        self.X_train.to_csv(os.path.join(train_directory, 'X_train.csv'), index=False)
        self.y_train.to_csv(os.path.join(train_directory, 'y_train.csv'), index=False)

        self.X_val.to_csv(os.path.join(val_directory, 'X_val.csv'), index=False)
        self.y_val.to_csv(os.path.join(val_directory, 'y_val.csv'), index=False)

        self.X_test.to_csv(os.path.join(test_directory, 'X_test.csv'), index=False)
        self.y_test.to_csv(os.path.join(test_directory, 'y_test.csv'), index=False)
