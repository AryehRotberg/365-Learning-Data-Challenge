import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, f1_score, ConfusionMatrixDisplay
# import pickle
import mlflow


X_train = pd.read_csv('data/train/X_train.csv').values
X_test = pd.read_csv('data/test/X_test.csv').values
y_train = pd.read_csv('data/train/y_train.csv').values
y_test = pd.read_csv('data/test/y_test.csv').values

# with open('outputs/models/model.pkl', 'rb') as file:
#     classifier = pickle.load(file)
classifier = mlflow.sklearn.load_model('runs:/f1f5530e3ba647c09b9cd043e1a5312f/Best_Classifier')

y_pred = classifier.predict(X_test)

conf = confusion_matrix(y_test, y_pred)
score = f1_score(y_test, y_pred)

print(conf)
print(score)

disp = ConfusionMatrixDisplay(conf)
disp.plot()
plt.show()

# sns.heatmap(conf, cmap=plt.cm.get_cmap('Greens'), fmt='d', annot=True)
# plt.show()