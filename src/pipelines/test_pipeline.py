import numpy as np
import pandas as pd
import pickle


# # 29.0,531.2,True,True,False,True

input_df = pd.DataFrame([20,
                         1,
                         True,
                         False,
                         True]).transpose()

input_df.columns = ['days_engaged',
                    'minutes_watched',
                    'engaged_with_quizzes',
                    'engaged_with_exams',
                    'engaged_with_qa']

with open('outputs/models/model.pkl', 'rb') as file:
    classifier = pickle.load(file)

with open('outputs/standard_scaler.pickle', 'rb') as file:
    standard_scaler = pickle.load(file)

input_df = standard_scaler.transform(input_df)

print(classifier.predict(input_df)[0])


# from sklearn.ensemble import RandomForestClassifier

# X_train = pd.read_csv('data/train/X_train.csv').values
# y_train = pd.read_csv('data/train/y_train.csv').values

# classifier = RandomForestClassifier()
# classifier.set_params(**{'bootstrap': False, 'max_depth': 30, 'max_features': 'sqrt', 'min_samples_split': 2, 'n_estimators': 10})
# classifier.fit(X_train, y_train.ravel())
# print(classifier.predict(np.array([[5, 5, True, False, True]])))

# with open('model.pkl', 'wb') as file:
#     pickle.dump(classifier, file, protocol=pickle.HIGHEST_PROTOCOL)

# with open('outputs/models/model.pkl', 'rb') as file:
#     classifier = pickle.load(file)

# print(classifier.predict(np.array([[0, 0, True, False, True]])))
