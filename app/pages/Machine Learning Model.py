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

ml_expander = st.expander('Introduction:')

for i in range(1, 19):
    ml_expander.markdown(description[f'ml_introduction_1.{i}'])

    if i == 6 or i == 2 or i == 12 or i == 17:
        ml_expander.write('')

ml_expander.write('')
ml_expander.write('')

ml_expander.dataframe(pd.read_csv('outputs/best_classifier_report.csv') \
                      .drop('support', axis=1) \
                      .rename(columns={'Unnamed: 0': '',
                                         'precision': 'Precision',
                                         'recall': 'Recall',
                                         'f1-score': 'F1-Score'}), hide_index=True, use_container_width=True)

img_col_1, img_col_2 = ml_expander.columns(2, gap='large')
img_col_1.image('outputs/images/confusion_matrix.png', use_column_width=True)
img_col_2.image('outputs/images/roc_curve.png', use_column_width=True)

st.write('')

column_1 = st.columns(3, gap='large')

with column_1[0]:
    days_engaged_value = st.number_input('Days Engaged', min_value=0)
with column_1[1]:
    minutes_watched_value = st.number_input('Minutes Watched', min_value=0)
with column_1[2]:
    engaged_with_quizzes_value = st.selectbox('Engaged With Quizzes', ['Yes', 'No'])

column_2 = st.columns(2, gap='large')

with column_2[0]:
    engaged_with_exams_value = st.selectbox('Engaged With Exams', ['Yes', 'No'])
with column_2[1]:
    engaged_with_qa_value = st.selectbox('Engaged With Q&A', ['Yes', 'No'])

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

with open('outputs/models/model.pkl', 'rb') as file:
    classifier = pickle.load(file)

with open('outputs/standard_scaler.pickle', 'rb') as file:
    standard_scaler = pickle.load(file)

input_df = standard_scaler.transform(input_df)

if button:
    pred = 'Potential paid tier user' if classifier.predict(input_df)[0] == True else 'Potential free tier user'
    st.info(f'Prediction: {pred}.')
