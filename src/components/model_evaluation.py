import os

import pandas as pd
import matplotlib.pyplot as plt

import pickle

from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, RocCurveDisplay, f1_score


class ModelEvaluation:
    def __init__(self, classifier):
        self.classifier = classifier

        self.X_train = pd.read_csv('data/train/X_train.csv').values
        self.X_test = pd.read_csv('data/test/X_test.csv').values
        self.y_train = pd.read_csv('data/train/y_train.csv').values
        self.y_test = pd.read_csv('data/test/y_test.csv').values

        self.y_pred = self.classifier.predict(self.X_test)
    
    def get_classification_report(self):
        return pd.DataFrame(classification_report(self.y_test, self.y_pred, output_dict=True)).transpose()
    
    def get_confusion_matrix(self, plot=True):
        self.confusion_matrix_plot = ConfusionMatrixDisplay.from_estimator(self.classifier, self.X_test, self.y_test)
        
        if plot:
            plt.show()
        
        else:
            return confusion_matrix(self.y_test, self.y_pred)
    
    def get_f1_score(self):
        return f1_score(self.y_test, self.y_pred)
    
    def save_outputs(self, directory):
        self.get_classification_report().to_csv(os.path.join(directory, 'best_classifier_report.csv'))

        with open(os.path.join(directory, 'models/model.pkl'), 'wb') as file:
            pickle.dump(self.classifier, file, protocol=pickle.HIGHEST_PROTOCOL)
        
        self.confusion_matrix_plot.figure_.savefig(os.path.join(directory, 'images/confusion_matrix.png'))
        RocCurveDisplay.from_estimator(self.classifier, self.X_test, self.y_test).figure_ \
        .savefig(os.path.join(directory, 'images/roc_curve.png'))
