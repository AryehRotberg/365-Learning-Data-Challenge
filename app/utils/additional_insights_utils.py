import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class additional_insights_utils:
    def __init__(self):
        self.student_info_df = pd.read_csv('data/raw/365_student_info.csv')
        self.student_learning_df = pd.read_csv('data/raw/365_student_learning.csv')
        self.course_info_df = pd.read_csv('data/raw/365_course_info.csv')
        self.course_ratings_df = pd.read_csv('data/raw/365_course_ratings.csv')
        self.student_engagement_df = pd.read_csv('data/raw/365_student_engagement.csv')
        self.student_purchases_df = pd.read_csv('data/raw/365_student_purchases.csv')
        self.exam_info_df = pd.read_csv('data/raw/365_exam_info.csv')
        self.quiz_info_df = pd.read_csv('data/raw/365_quiz_info.csv')
        self.hub_questions_df = pd.read_csv('data/raw/365_student_hub_questions.csv')
        self.merged_student_info_purchase = pd.read_csv('data/processed/merged_student_info_purchase.csv')

        self.student_learning_df.date_watched = pd.to_datetime(self.student_learning_df.date_watched)
        self.course_ratings_df.date_rated = pd.to_datetime(self.course_ratings_df.date_rated)
        self.student_engagement_df.date_engaged = pd.to_datetime(self.student_engagement_df.date_engaged)
        self.student_purchases_df.date_purchased = pd.to_datetime(self.student_purchases_df.date_purchased)
        self.merged_student_info_purchase.date_registered = pd.to_datetime(self.merged_student_info_purchase.date_registered)
        self.hub_questions_df.date_question_asked = pd.to_datetime(self.hub_questions_df.date_question_asked)


        self.month_names_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October'}
    
    def get_purchases_onboarded_per_month(self):
        onboarded_per_month = self.student_engagement_df.copy()
        purchases_per_month = self.student_purchases_df.copy()

        # Onboarded Per Month
        onboarded_per_month['month'] = onboarded_per_month.date_engaged.apply(lambda date : date.month)
        onboarded_per_month = onboarded_per_month[['month']].groupby('month').size().reset_index()
        onboarded_per_month = onboarded_per_month.rename(columns={0: 'Onboarded'})

        # Purchases Per Month
        purchases_per_month['month'] = purchases_per_month.date_purchased.apply(lambda date : date.month)
        purchases_per_month = purchases_per_month[['month']].groupby('month').size().reset_index()
        purchases_per_month = purchases_per_month.rename(columns={0: 'Purchases'})

        purchases_onboarded_per_month = pd.merge(purchases_per_month, onboarded_per_month, on='month')
        purchases_onboarded_per_month.month = purchases_onboarded_per_month.month.map(self.month_names_dict)
        purchases_onboarded_per_month['Percentage'] = (purchases_onboarded_per_month.Purchases / purchases_onboarded_per_month.Onboarded).round(4) * 100

        # Plot
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=purchases_onboarded_per_month.month,
                                 y=purchases_onboarded_per_month.Purchases,
                                 name='Purchases'), secondary_y=False)
        
        fig.add_trace(go.Scatter(x=purchases_onboarded_per_month.month,
                                 y=purchases_onboarded_per_month.Onboarded,
                                 name='Onboarded'), secondary_y=True)

        fig.update_xaxes(title_text='Month')

        fig.update_yaxes(title_text='Amount of Purchases', secondary_y=False)
        fig.update_yaxes(title_text='Onboarded', secondary_y=True)

        return fig
    
    def get_student_and_purchase_type(self):
        plot = px.histogram(data_frame=self.student_purchases_df,
                            x='purchase_type',
                            color='purchase_type',
                            labels={'purchase_type': 'Purchase Type'},
                            color_discrete_sequence=px.colors.qualitative.Vivid)
        plot.update_layout(yaxis_title='Purchases')

        return plot
    
    def get_student_engagement_countries(self):
        student_engagement_countries = pd.merge(self.student_info_df[['student_id', 'student_country']], self.student_engagement_df[['student_id']], on='student_id', how='left')
        student_engagement_countries = student_engagement_countries.groupby('student_country').size().reset_index().sort_values(by=0, ascending=False).head()
        student_engagement_countries = student_engagement_countries.rename(columns={0: 'engaged'})

        # Plot
        plot = px.bar(data_frame=student_engagement_countries,
                      x='student_country',
                      y='engaged',
                      color='student_country',
                      labels={'student_country': 'Student Country'},
                      color_discrete_sequence=px.colors.qualitative.G10_r)
        plot.update_layout(yaxis_title='Engaged')

        return plot
    
    def get_hub_questions_asked_per_month(self):
        questions_per_month = self.hub_questions_df.copy()

        questions_per_month['month'] = questions_per_month.date_question_asked.dt.month
        questions_per_month = questions_per_month[['month', 'hub_question_id']].groupby('month').size().reset_index()
        questions_per_month = questions_per_month.rename(columns={0: 'Questions'})
        questions_per_month.month = questions_per_month.month.map(self.month_names_dict)

        # Plot
        plot = px.bar(data_frame=questions_per_month,
                      x='month',
                      y='Questions',
                      color='month',
                      color_discrete_sequence=px.colors.qualitative.Vivid)
        
        return plot
    
    def get_engagements_amount(self):
        return self.student_engagement_df.shape[0] / 1000
    
    def get_exams_amount(self):
        return self.exam_info_df.shape[0]

    def get_quizzes_amount(self):
        return self.quiz_info_df.shape[0]

    def get_hub_questions_amount(self):
        return self.hub_questions_df.shape[0]
