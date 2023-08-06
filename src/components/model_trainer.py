import numpy as np
import pandas as pd

import mlflow

from xgboost import XGBClassifier

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import GridSearchCV

from sklearn.metrics import classification_report, roc_auc_score, f1_score

# from sklearn.metrics import RocCurveDisplay
# RocCurveDisplay.from_estimator(classifier, X_test, y_test)

class ModelTrainer:
    def __init__(self):
        self.X_train = pd.read_csv('data/train/X_train.csv').values
        self.X_test = pd.read_csv('data/test/X_test.csv').values
        self.y_train = pd.read_csv('data/train/y_train.csv').values
        self.y_test = pd.read_csv('data/test/y_test.csv').values
    
    def get_gridsearch_dict(self):
        self.grid_search = {
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

        return self.grid_search
    
    def get_tuned_models_scores(self, grid_search: dict, verbose=False):
        scores = []

        for classifier_name, classifier_params in grid_search.items():
            gs = GridSearchCV(classifier_params['classifier'],
                            classifier_params['params'],
                            cv=5,
                            scoring=['f1_micro', 'roc_auc'],
                            refit='f1_micro',
                            verbose=10 if verbose else 0)
            
            gs.fit(self.X_train, self.y_train.ravel())
            
            scores.append({
                'classifier': classifier_name,
                'best_score': gs.best_score_,
                'best_params': gs.best_params_,
                'best_estimator': gs.best_estimator_
            })
        
        scores_df = pd.DataFrame(scores).sort_values(by='best_score', ascending=False)
        return scores_df
    
    def get_best_classifier(self, scores_df: pd.DataFrame):
        classifier = scores_df.loc[scores_df.best_score.idxmax()].best_estimator
        params = scores_df.loc[scores_df.best_score.idxmax()].best_params

        classifier.fit(self.X_train, self.y_train.ravel())

        return classifier, params
    
    def save_best_classifier(self, classifier, params):
        y_pred = classifier.predict(self.X_test)

        report = pd.DataFrame(classification_report(self.y_test, y_pred, output_dict=True)).transpose()
        report.to_csv('data/processed/best_classifier_report.csv', index=False)

        mlflow.set_experiment('365 Learning Data Challenge - Machine Learning')

        with mlflow.start_run():
            if params is not None:
                for param_type, value in params.items():
                    mlflow.log_param(param_type, value)
            
            mlflow.log_artifact('data/processed/best_classifier_report.csv')

            mlflow.log_metric('f1_score', f1_score(self.y_test, y_pred))
            mlflow.log_metric('roc_auc_score', roc_auc_score(self.y_test, y_pred))

            mlflow.sklearn.log_model(classifier, 'Best_Classifier', registered_model_name=type(classifier).__name__)
