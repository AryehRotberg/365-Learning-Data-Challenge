import pandas as pd

import plotly.express as px
import streamlit as st

from app_utils import app_utils


st.title('365 Learning Data Challenge Dashboard')

st.sidebar.title('Parameters')

user_type_option = st.sidebar.selectbox('Select User Type', ('All', 'Free', 'Paid'))
subscription_type_option = st.sidebar.selectbox('Select User Subscription Type', ('All', 'Monthly', 'Quarterly', 'Annual'))

countries_list = pd.read_csv('notebook/data/raw/365_student_info.csv').student_country.unique().tolist()
countries_list = ['All']
countries_list.extend(pd.read_csv('notebook/data/raw/365_student_info.csv').student_country.unique().tolist())

country_option = st.sidebar.selectbox('Select Country', countries_list)

course_minutes_watched = app_utils(user_type_option, subscription_type_option, country_option).get_course_minutes_watched()
student_country = app_utils(user_type_option, subscription_type_option, country_option).get_student_country()
platform = app_utils(user_type_option, subscription_type_option, country_option).get_platform_minutes_watched()
monthly_average_minutes_watched = app_utils(user_type_option, subscription_type_option, country_option).get_monthly_average_minutes_watched()

st.write(course_minutes_watched.head())
st.write(px.bar(student_country.head(), x='students', y='student_country', orientation='h', color='student_country', title='Chart 1.1 - Top 5 Largest Number of Users'))
st.write(px.bar(platform.head(), x='minutes_watched', y='student_country', orientation='h', color='student_country', title='Chart 1.2 - Minutes watched on the platform by users'))
st.write(px.bar(monthly_average_minutes_watched, x='month', y='average_minutes_watched'))

# st.write('')
# fig = px.line(monthly_average_minutes_watched, x='month', y='average_minutes_watched')
# fig.add_bar(x=monthly_average_minutes_watched.month, y=monthly_average_minutes_watched.minutes_watched)
# # st.write(px.bar(monthly_average_minutes_watched, x='month', y='minutes_watched'))
# st.write(fig)