import pandas as pd

import optuna

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import cross_val_score


class ModelTrainer:
    def __init__(self):
        self.X_train = pd.read_csv('data/train/X_train.csv').values
        self.X_test = pd.read_csv('data/test/X_test.csv').values
        self.y_train = pd.read_csv('data/train/y_train.csv').values
        self.y_test = pd.read_csv('data/test/y_test.csv').values
    
    def objective(self, trial: optuna.trial.Trial):
        name = trial.suggest_categorical('classifier', ['lr', 'rfc', 'knn'])

        if name == 'lr':
            classifier = LogisticRegression(C=trial.suggest_float('C', 1, 4, log=True),
                                            solver=trial.suggest_categorical('solver', ['newton-cg', 'lbfgs', 'liblinear'])) # 150
        
        if name == 'rfc':
            classifier = RandomForestClassifier(bootstrap=trial.suggest_categorical('bootstrap', [True, False]),
                                                max_depth=trial.suggest_categorical('max_depth', [1, 5, 10, 20, 30, None]),
                                                max_features=trial.suggest_categorical('max_features', ['log2', 'sqrt']),
                                                min_samples_split=trial.suggest_categorical('min_samples_split', [2, 5, 10]),
                                                n_estimators=trial.suggest_categorical('n_estimators', [1, 5, 10, 20, 30])) # 360
        
        if name == 'knn':
            classifier = KNeighborsClassifier(n_neighbors=trial.suggest_categorical('n_neighbors', [5, 7, 9, 11, 13, 15]),
                                              weights=trial.suggest_categorical('weights', ['uniform', 'distance']),
                                              metric=trial.suggest_categorical('metric', ['minkowski', 'euclidean', 'manhattan'])) # 36
        
        score = cross_val_score(classifier, self.X_train, self.y_train.ravel(), n_jobs=-1, cv=5, scoring='f1')
        return score.mean()
    
    def create_optuna_pipeline(self, n_trials):
        study = optuna.create_study(direction='maximize')
        study.optimize(self.objective, n_trials=n_trials)

        return study
    
    def get_study_values(self, study):
        return {'best_params': study.best_params,
                'best_value': study.best_value}
    
    def get_best_classifier(self, study_values):
        best_params = study_values['best_params']
        best_classifier = study_values['best_params']['classifier']

        classifiers = {'lr': LogisticRegression(), 'rfc': RandomForestClassifier(), 'knn': KNeighborsClassifier()}
        classifier = classifiers[best_classifier]

        best_params.pop('classifier')
        classifier.set_params(**best_params)

        classifier.fit(self.X_train, self.y_train.ravel())

        return classifier
