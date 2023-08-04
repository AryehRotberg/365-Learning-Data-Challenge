import streamlit as st

import json

from utils.additional_insights_utils import additional_insights_utils


with open('app/utils/descriptions.json', 'r') as file:
    description = json.load(file)

utils = additional_insights_utils()

st.set_page_config(page_title='Additional Features', layout='wide', page_icon='📈')
st.title('Additional Insights 📈')

st.markdown(description['additional_insights_description'])
st.write('')
st.markdown("**Additional KPI'S**")

col1_kpi, col2_kpi, col3_kpi, col4_kpi = st.columns(4)
col1_kpi.metric('Engagements', value=f'{utils.get_engagements_amount()} K')
col2_kpi.metric('Exams', utils.get_exams_amount())
col3_kpi.metric('Quizzes', utils.get_quizzes_amount())
col4_kpi.metric('Hub Questions', utils.get_hub_questions_amount())

col1_chart, col2_chart = st.columns(2, gap='large')
col1_chart.plotly_chart(utils.get_purchases_onboarded_per_month(), use_container_width=True)
col1_chart.expander('See details:').write('This chart represents the distribution...')

col2_chart.plotly_chart(utils.get_student_and_purchase_type(), use_container_width=True)
col2_chart.expander('See details:').write('This chart represents the distribution...')

col3_chart, col4_chart = st.columns(2, gap='large')
col3_chart.plotly_chart(utils.get_student_engagement_countries(), use_container_width=True)
col3_chart.expander('See details:').write('This chart represents the distribution...')

col4_chart.plotly_chart(utils.get_hub_questions_asked_per_month(), use_container_width=True)
col4_chart.expander('See details:').write('This chart represents the distribution...')
