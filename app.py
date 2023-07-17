import pandas as pd

import plotly.express as px
import streamlit as st

from app_utils import app_utils


# merged_student_info_purchase = pd.read_csv('notebook/data/processed/merged_student_info_purchase.csv')
# student_learning_df = pd.read_csv('data/raw/365_student_learning.csv')
# course_info_df = pd.read_csv('data/raw/365_course_info.csv')
# course_ratings_df = pd.read_csv('data/raw/365_course_ratings.csv')

# student_learning_df.date_watched = pd.to_datetime(student_learning_df.date_watched)
# course_ratings_df.date_rated = pd.to_datetime(course_ratings_df.date_rated)

st.title('365 Learning Data Challenge Dashboard')

st.sidebar.title('Parameters')

user_type_option = st.sidebar.selectbox('Select User Type', ('All', 'Free', 'Paid'))
subscription_type_option = st.sidebar.selectbox('Select User Subscription Type', ('All', 'Monthly', 'Quarterly', 'Annual'))

country_option = st.sidebar.selectbox('Select Country', ('All', 'Country 1', 'Country 2'))

#     monthly_average_minutes_watched = pd.merge(merged_student_info_purchase, student_learning_df, on='student_id', how='left')
#     monthly_average_minutes_watched = monthly_average_minutes_watched[(monthly_average_minutes_watched.purchase_type == subscription_type_option) & (monthly_average_minutes_watched.paid == paid)]
#     monthly_average_minutes_watched['month'] = monthly_average_minutes_watched.date_watched.apply(lambda date : date.month)
#     monthly_average_minutes_watched['average_minutes_watched'] = monthly_average_minutes_watched.minutes_watched
#     monthly_average_minutes_watched = monthly_average_minutes_watched[['month', 'minutes_watched', 'average_minutes_watched']].groupby('month').agg({'minutes_watched': 'sum', 'average_minutes_watched': 'mean'}).reset_index().round(2)

#     platform = pd.merge(student_country, country_minutes_watched, on='student_country')


course_minutes_watched = app_utils(user_type_option, subscription_type_option, country_option).get_course_minutes_watched()

st.write(course_minutes_watched.head())

student_country = app_utils(user_type_option, subscription_type_option, country_option).get_student_country()
platform = app_utils(user_type_option, subscription_type_option, country_option).get_platform_minutes_watched()
monthly_average_minutes_watched = app_utils(user_type_option, subscription_type_option, country_option).get_monthly_average_minutes_watched()

st.write(px.bar(student_country.head(), x='students', y='student_country', orientation='h', color='student_country', title='Top 5 Largest Number of Users'))
st.write(px.bar(platform.head(), x='minutes_watched', y='student_country', orientation='h', color='student_country', title='Minutes watched on the platform by users'))
st.write(px.bar(monthly_average_minutes_watched, x='month', y='average_minutes_watched'))

# st.write('')
# fig = px.line(monthly_average_minutes_watched, x='month', y='average_minutes_watched')
# fig.add_bar(x=monthly_average_minutes_watched.month, y=monthly_average_minutes_watched.minutes_watched)
# # st.write(px.bar(monthly_average_minutes_watched, x='month', y='minutes_watched'))
# st.write(fig)