import pandas as pd
import optuna

import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, f1_score


X_train = pd.read_csv('data/train/X_train.csv').values
X_test = pd.read_csv('data/test/X_test.csv').values
y_train = pd.read_csv('data/train/y_train.csv').values
y_test = pd.read_csv('data/test/y_test.csv').values

def objective(trial: optuna.trial.Trial):
    n_neighbors = trial.suggest_categorical('n_neighbors', [5, 7, 9, 11, 13, 15])
    weights = trial.suggest_categorical('weights', ['uniform', 'distance'])
    metric = trial.suggest_categorical('metric', ['minkowski', 'euclidean', 'manhattan'])

    classifier = KNeighborsClassifier(n_neighbors=n_neighbors,
                                      weights=weights,
                                      metric=metric)
    
    score = cross_val_score(classifier, X_train, y_train.ravel(), n_jobs=-1, cv=5, scoring='f1')
    
    return score.mean()

def objective(trial: optuna.trial.Trial):
    bootstrap = trial.suggest_categorical('bootstrap', [True, False])
    max_depth = trial.suggest_categorical('max_depth', [1, 5, 10, 20, 30, None])
    max_features = trial.suggest_categorical('max_features', ['log2', 'sqrt'])
    min_samples_split = trial.suggest_categorical('min_samples_split', [2, 5, 10])
    n_estimators = trial.suggest_categorical('n_estimators', [1, 5, 10, 20, 30])

    classifier = RandomForestClassifier(bootstrap=bootstrap,
                                        max_depth=max_depth,
                                        max_features=max_features,
                                        min_samples_split=min_samples_split,
                                        n_estimators=n_estimators)
    
    score = cross_val_score(classifier, X_train, y_train.ravel(), n_jobs=-1, cv=5, scoring='f1')
    f1_score = score.mean()

    return f1_score

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

print(study.best_params)
print(study.best_value)
