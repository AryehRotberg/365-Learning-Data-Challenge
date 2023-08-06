import numpy as np

from xgboost import XGBClassifier

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier


grid_search = {
    'logistic_regression': {
        'classifier': LogisticRegression(), 'params': {
            'C': np.logspace(-4, 4, 20),
            'penalty': ['l1', 'l2'],
            'solver': ['newton-cg', 'lbfgs', 'liblinear']
        }
    },

    'rfc': {
        'classifier': RandomForestClassifier(), 'params': {
            'bootstrap': [True, False],
            'max_depth': [1, 5, 10, 20, 30, None],
            'max_features': ['log2', 'sqrt'],
            'min_samples_split': [2, 5, 10],
            'n_estimators': [1, 5, 10, 20, 30]
        }
    },

    'xgb_classifier': {
        'classifier': XGBClassifier(), 'params': {
            'min_child_weight': [1, 5, 10],
            'gamma': [0.5, 1, 1.5, 2, 5],
            'subsample': [0.6, 0.8, 1.0],
            'colsample_bytree': [0.6, 0.8, 1.0],
            'max_depth': [3, 4, 5]
        }
    },

    'knn': {
        'classifier': KNeighborsClassifier(), 'params': {
            'n_neighbors': [5, 7, 9, 11, 13, 15],
            'weights' : ['uniform','distance'],
            'metric' : ['minkowski','euclidean','manhattan']
        }
    },

    'gradient_boosting': {
        'classifier': GradientBoostingClassifier(), 'params': {
            "loss": ["deviance"],
            "learning_rate": [0.01, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2],
            "min_samples_split": np.linspace(0.1, 0.5, 12),
            "min_samples_leaf": np.linspace(0.1, 0.5, 12),
            "max_depth": [3,5,8],
            "max_features": ["log2","sqrt"],
            "criterion": ["friedman_mse",  "mae"],
            "subsample": [0.5, 0.618, 0.8, 0.85, 0.9, 0.95, 1.0],
            "n_estimators": [10]
        }
    }
}
