import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

from dataclasses import dataclass


@dataclass
class DataTransformationConfig:
    df = pd.read_csv('data/processed/ml_dataset.csv')


class DataTransformation:
    def __init__(self):
        self.config = DataTransformationConfig()

        self.ros = RandomOverSampler()
        self.rus = RandomUnderSampler()
        self.scaler = StandardScaler()
    
    def transform_data(self):
        X = self.config.df.drop('subscribed', axis=1)
        y = self.config.df.subscribed

        X_oversampled, y_oversampled = self.ros.fit_resample(X, y)
        X_resampled, y_resampled = self.rus.fit_resample(X_oversampled, y_oversampled)

        X_scaled = self.scaler.fit_transform(X_resampled)

        print(y_resampled.value_counts())

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X_scaled, y_resampled, test_size=0.2)
    
    def to_csv(self):
        self.X_train = pd.DataFrame(self.X_train)
        self.X_test = pd.DataFrame(self.X_test)

        self.X_train.to_csv('data/train/X_train.csv', index=False)
        self.X_test.to_csv('data/test/X_test.csv', index=False)
        self.y_train.to_csv('data/train/y_train.csv', index=False)
        self.y_test.to_csv('data/test/y_test.csv', index=False)
