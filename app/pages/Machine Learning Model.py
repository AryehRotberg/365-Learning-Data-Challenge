import streamlit as st
import pandas as pd


st.set_page_config(page_title='Machine Learning Model',
                   layout='wide',
                   page_icon='🧠')

st.title('Machine Learning Model 🧠')

ml_df = pd.read_csv('data/processed/ml_dataset.csv')

# st.dataframe(ml_df)

column_1 = st.columns(3, gap='large')

with column_1[0]:
    st.number_input('Days Engaged',
                    min_value=0)

with column_1[1]:
    st.number_input('Minutes Watched',
                    min_value=0)

with column_1[2]:
    st.selectbox('Engaged With Quizzes',
                ['Yes', 'No'])

column_2 = st.columns(2, gap='large')

with column_2[0]:
    st.selectbox('Engaged With Exams',
                ['Yes', 'No'])

with column_2[1]:
    st.selectbox('Engaged With Q&A',
                ['Yes', 'No'])

st.write('')
st.write('')

st.info(f'**Prediction: {0.87}**')