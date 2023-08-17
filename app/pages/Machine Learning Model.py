import streamlit as st
import pandas as pd

import json
import pickle


with open('app/utils/descriptions.json', 'r') as file:
    description = json.load(file)

st.set_page_config(page_title='Machine Learning Model',
                   layout='wide',
                   page_icon='🧠')

st.title('Machine Learning Model 🧠')

ml_expander = st.expander('Machine Learning')
ml_expander.markdown(description['machine_learning_description_todo'])
ml_expander.markdown(description['machine_learning_description_todo_bullet_1'])
ml_expander.markdown(description['machine_learning_description_todo_bullet_2'])
ml_expander.markdown(description['machine_learning_description_todo_bullet_3'])

column_1 = st.columns(3, gap='large')

with column_1[0]:
    days_engaged_value = st.number_input('Days Engaged',
                                             min_value=0)

with column_1[1]:
    minutes_watched_value = st.number_input('Minutes Watched',
                                                min_value=0)

with column_1[2]:
    engaged_with_quizzes_value = st.selectbox('Engaged With Quizzes',
                                                  ['Yes', 'No'])

column_2 = st.columns(2, gap='large')

with column_2[0]:
    engaged_with_exams_value = st.selectbox('Engaged With Exams',
                                                  ['Yes', 'No'])

with column_2[1]:
    engaged_with_qa_value = st.selectbox('Engaged With Q&A',
                                             ['Yes', 'No'])

st.write('')
st.write('')

button = st.button('Predict')

st.write('')
st.write('')

engaged_with_quizzes_value = True if 'Yes' else False
engaged_with_exams_value = True if 'Yes' else False
engaged_with_qa_value = True if 'Yes' else False

input_df = pd.DataFrame([days_engaged_value,
                         minutes_watched_value,
                         engaged_with_quizzes_value,
                         engaged_with_exams_value,
                         engaged_with_qa_value]).transpose()

input_df.columns = ['days_engaged',
                    'minutes_watched',
                    'engaged_with_quizzes',
                    'engaged_with_exams',
                    'engaged_with_qa']

import mlflow
# with open('outputs/models/model.pkl', 'rb') as file:
#     classifier = pickle.load(file)
classifier = mlflow.sklearn.load_model('runs:/f1f5530e3ba647c09b9cd043e1a5312f/Best_Classifier')

with open('outputs/standard_scaler.pickle', 'rb') as file:
    standard_scaler = pickle.load(file)

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

X_train = pd.read_csv('data/train/X_train.csv').values
X_test = pd.read_csv('data/test/X_test.csv').values
y_train = pd.read_csv('data/train/y_train.csv').values
y_test = pd.read_csv('data/test/y_test.csv').values

conf = confusion_matrix(y_test, classifier.predict(X_test))

disp = ConfusionMatrixDisplay(conf)
disp.plot()
# st.pyplot(disp)


input_df = standard_scaler.transform(input_df)

if button:
    pred = 'Potential paid tier user' if classifier.predict(input_df)[0] == True else 'Potential free tier user'
    st.info(f'Prediction: {pred}.')
