import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

import streamlit as st

from app_utils import app_utils


st.set_page_config(page_title='Dashboard', layout='wide', page_icon='📉')

st.title('365 Learning Data Challenge Dashboard 📉')

st.sidebar.title('Parameters')

user_type_option = st.sidebar.selectbox('Select User Type', ('All', 'Free', 'Paid'))
subscription_type_option = st.sidebar.selectbox('Select User Subscription Type', ('All', 'Monthly', 'Quarterly', 'Annual'))

countries_list = ['All']
countries_list.extend(pd.read_csv('data/raw/365_student_info.csv').student_country.unique().tolist())

country_option = st.sidebar.selectbox('Select Country', countries_list)

utils = app_utils(user_type_option, subscription_type_option, country_option)

course_minutes_watched = utils.get_course_minutes_watched()
student_country = utils.get_student_country()
platform = utils.get_platform_minutes_watched()
monthly_average_minutes_watched = utils.get_monthly_average_minutes_watched()
students_registered_onboarded = utils.get_students_registered_onboarded()

st.write(course_minutes_watched.head())
st.write('')

col1_kpi, col2_kpi, col3_kpi, col4_kpi = st.columns(4)
col1_kpi.metric('Registered Students', value=utils.get_registered_students_kpi(), )
col2_kpi.metric('Purchases', value=utils.get_purchases_kpi())
col3_kpi.metric('Average Minutes Watched', value=utils.get_average_minutes_watched_kpi())
col4_kpi.metric('Onboarded from Registered', value=f'{utils.get_onboarded_from_registered_kpi()}%')

st.write('')
col1_chart, col2_chart = st.columns(2, gap='large')
col1_chart.write(px.bar(student_country.head(), x='students', y='student_country', orientation='h', color='student_country', title='Chart 1.1 - Top 5 Largest Number of Users'))
col2_chart.write(px.bar(platform.head(), x='minutes_watched', y='student_country', orientation='h', color='student_country', title='Chart 1.2 - Minutes watched on the platform by users'))

col3_chart, col4_chart = st.columns(2, gap='large')
col3_chart.write(go.Figure(data=[go.Bar(name='Minutes Watched', x=monthly_average_minutes_watched.month, y=monthly_average_minutes_watched.minutes_watched, offsetgroup=1),
                                 go.Line(name='Average Minutes Watched', x=monthly_average_minutes_watched.month, y=monthly_average_minutes_watched.average_minutes_watched, offsetgroup=2)])
                                 .update_layout(title='Chart 1.3 - Minutes Watched by Month'))
col4_chart.write(go.Figure(data=[go.Bar(name='Students', x=students_registered_onboarded.month, y=students_registered_onboarded.students, offsetgroup=1),
                                 go.Bar(name='Onboarded', x=students_registered_onboarded.month, y=students_registered_onboarded.onboarded, offsetgroup=2)])
                                 .update_layout(title='Chart 1.4 - Number of Registered Students Compared to Onboarded'))
