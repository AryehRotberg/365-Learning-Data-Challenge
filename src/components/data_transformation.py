import os

import pandas as pd

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split

from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler


class DataTransformation:
    def __init__(self):
        self.df = pd.read_csv('data/processed/ml_dataset.csv')

        self.ros = RandomOverSampler()
        self.rus = RandomUnderSampler()
        self.standard_scaler = StandardScaler()
        self.minmax_scaler = MinMaxScaler()
    
    def transform_data(self, scaler='standard', resampler='ros|rus'):
        X = self.df.drop('subscribed', axis=1)
        y = self.df.subscribed

        if resampler == 'ros|rus':
            X_oversampled, y_oversampled = self.ros.fit_resample(X, y)
            X_resampled, y_resampled = self.rus.fit_resample(X_oversampled, y_oversampled)
        
        if resampler == 'ros':
            X_resampled, y_resampled = self.ros.fit_resample(X, y)
        
        if resampler == 'rus':
            X_resampled, y_resampled = self.rus.fit_resample(X, y)

        if scaler == 'standard':
            X_scaled = self.standard_scaler.fit_transform(X_resampled)
        if scaler == 'minmax':
            X_scaled = self.minmax_scaler.fit_transform(X_resampled)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X_scaled, y_resampled, test_size=0.2)
    
    def to_csv(self, train_directory, test_directory):
        self.X_train = pd.DataFrame(self.X_train)
        self.X_test = pd.DataFrame(self.X_test)

        self.X_train.to_csv(os.path.join(train_directory, 'X_train.csv'), index=False)
        self.X_test.to_csv(os.path.join(test_directory, 'X_test.csv'), index=False)
        self.y_train.to_csv(os.path.join(train_directory, 'y_train.csv'), index=False)
        self.y_test.to_csv(os.path.join(test_directory, 'y_test.csv'), index=False)
