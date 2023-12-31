import pandas as pd
import json

import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards

from utils.main_dashboard_utils import main_dashboard_utils


with open('app/utils/descriptions.json', 'r') as file:
    description = json.load(file)

st.set_page_config(page_title='Dashboard', layout='wide', page_icon='📉')

st.title('365 Learning Data Challenge Dashboard 📉')

st.sidebar.title('Parameters')

user_type_option = st.sidebar.selectbox('Select User Type', ('All', 'Free', 'Paid'))
subscription_type_option = st.sidebar.selectbox('Select User Subscription Type', ('All', 'Monthly', 'Quarterly', 'Annual'))

countries_list = ['All']
countries_list.extend(pd.read_csv('data/raw/365_student_info.csv').student_country.unique().tolist())

country_option = st.sidebar.selectbox('Select Country', countries_list)

utils = main_dashboard_utils(user_type_option, subscription_type_option, country_option)

st.markdown(description['main_dashboard_description'])
st.write('')

course_minutes_watched = utils.get_course_minutes_watched().rename(columns={'course_title': 'Course Title',
                                                                            'average_course_rating': 'Average Course Rating',
                                                                            'ratings': 'Ratings',
                                                                            'minutes_watched': 'Minutes Watched',
                                                                            'average_minutes_watched': 'Average Minutes Watched'})
st.write('**Top 5 Courses Ratings**')
st.dataframe(course_minutes_watched.head(), hide_index=True)

st.write('')
st.markdown("**KPI'S**")

col1_kpi, col2_kpi, col3_kpi, col4_kpi = st.columns(4)
col1_kpi.metric(label='Registered Students', value=utils.get_registered_students_kpi())
col2_kpi.metric(label='Total Purchases', value=utils.get_purchases_kpi())
col3_kpi.metric(label='Total Average Minutes Watched', value=utils.get_average_minutes_watched_kpi())
col4_kpi.metric(label='Onboarded from Registered', value=f'{utils.get_onboarded_from_registered_kpi()}%')

style_metric_cards(background_color='#0000')

st.write('')

col1_chart, col2_chart = st.columns(2, gap='large')

col1_chart.plotly_chart(utils.plot_top_largest_number_of_users(), use_container_width=True)
col1_chart_expander = col1_chart.expander('See details:')
col1_chart_expander.write(description['main_chart_1.1'])
col1_chart_expander.write(description['main_chart_1.2'])

col2_chart.plotly_chart(utils.plot_minutes_watched_by_country(), use_container_width=True)
col2_chart_expander = col2_chart.expander('See details:')

for i in range(1, 8):
    col2_chart_expander.markdown(description[f'main_chart_2.{i}'])

st.write('')

col3_chart, col4_chart = st.columns(2, gap='large')

col3_chart.plotly_chart(utils.plot_minutes_watched_by_month(), use_container_width=True)
col3_chart_expander = col3_chart.expander('See details:')
col3_chart_expander.write(description['main_chart_3.1'])
col3_chart_expander.write(description['main_chart_3.2'])

col4_chart.plotly_chart(utils.plot_registered_onboarded(), use_container_width=True)
col4_chart_expander = col4_chart.expander('See details:')
col4_chart_expander.write(description['main_chart_4.1'])
col4_chart_expander.write(description['main_chart_4.2'])

st.write('')
st.markdown('**Overall Conclusions:**')

for i in range(1, 5):
    st.markdown(description[f'main_dashboard_summary_1.{i}'])
