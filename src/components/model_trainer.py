import numpy as np
import pandas as pd

from xgboost import XGBClassifier

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import GridSearchCV

from dataclasses import dataclass


@dataclass
class ModelTrainerConfig:
    X_train = pd.read_csv('data/train/X_train.csv').values
    X_test = pd.read_csv('data/test/X_test.csv').values
    y_train = pd.read_csv('data/train/y_train.csv')
    y_test = pd.read_csv('data/test/y_test.csv')


class ModelTrainer:
    def __init__(self):
        self.config = ModelTrainerConfig()
    
    # def get_gridsearch_dict():
    #     grid_search = {
    #         'rfc': {'classifier': RandomForestClassifier(),
    #         'params': {
    #             'bootstrap': [True, False],
    #             'max_depth': [10, 20, 30, 40, 50, None],
    #             'max_features': ['auto', 'sqrt'],
    #             'min_samples_leaf': [1, 2, 4],
    #             'min_samples_split': [2, 5, 10],
    #             'n_estimators': [200, 400, 600]
    #         }}
    #     }

    #     grid_search = {
    #         'logistic_regression': {'classifier': LogisticRegression(), 'params': {'C': np.logspace(-4, 4, 20)}},
    #         'rfc': {'classifier': RandomForestClassifier(), 'params': {'n_estimators': [1, 5, 10], 'max_depth': [1, 5, 10]}},
    #         'xgb_classifier': {'classifier': XGBClassifier(), 'params': {'n_estimators': [1, 5, 10], 'max_depth': [1, 5, 10]}},
    #         'knn': {'classifier': KNeighborsClassifier(), 'params': {'n_neighbors': list(range(1, 10))}}
    #     }