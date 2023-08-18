import numpy as np
import pandas as pd

import json

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from datetime import datetime


with open('app/utils/chart_titles.json', 'r') as file:
    chart_titles = json.load(file)


class main_dashboard_utils:
    def __init__(self, user_type_option: str, subscription_type_option: str, country_option: str):
        self.user_type_option = user_type_option
        self.subscription_type_option = subscription_type_option
        self.country_option = country_option

        self.student_info_df = pd.read_csv('data/raw/365_student_info.csv')
        self.student_learning_df = pd.read_csv('data/raw/365_student_learning.csv')
        self.course_info_df = pd.read_csv('data/raw/365_course_info.csv')
        self.course_ratings_df = pd.read_csv('data/raw/365_course_ratings.csv')
        self.student_engagement_df = pd.read_csv('data/raw/365_student_engagement.csv')
        self.student_purchases_df = pd.read_csv('data/raw/365_student_purchases.csv')
        self.merged_student_info_purchase = pd.read_csv('data/processed/merged_student_info_purchase.csv')

        self.student_learning_df.date_watched = pd.to_datetime(self.student_learning_df.date_watched)
        self.course_ratings_df.date_rated = pd.to_datetime(self.course_ratings_df.date_rated)
        self.student_engagement_df.date_engaged = pd.to_datetime(self.student_engagement_df.date_engaged)
        self.student_purchases_df.date_purchased = pd.to_datetime(self.student_purchases_df.date_purchased)
        self.merged_student_info_purchase.date_registered = pd.to_datetime(self.merged_student_info_purchase.date_registered)

        self.month_names_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October'}

    def get_country_list(self):
        return self.student_info_df.student_country.unique().tolist()
    
    def modify_options(self, df):
        country_option = self.country_option

        if self.user_type_option == 'Free':
            user_type_option = False
            subscription_type_option = df['purchase_type']

        else:
            user_type_option = self.user_type_option
            subscription_type_option = self.subscription_type_option
        
        if self.user_type_option == 'Paid':
            user_type_option = True
        
        if self.user_type_option == 'All':
            user_type_option = df['paid']
        if self.subscription_type_option == 'All':
            subscription_type_option = df['purchase_type']
        if self.country_option == 'All':
            country_option = df['student_country']
        
        return user_type_option, subscription_type_option, country_option
            
    def get_student_country(self):
        user_type_option, subscription_type_option, country_option = self.modify_options(self.merged_student_info_purchase)
        student_country = self.merged_student_info_purchase[(self.merged_student_info_purchase.paid == user_type_option)
                                                 & (self.merged_student_info_purchase.purchase_type == subscription_type_option)
                                                 & (self.merged_student_info_purchase.student_country == country_option)]
        
        return student_country[['student_country']].groupby('student_country').size().reset_index().sort_values(by=0, ascending=False).rename(columns={0: 'students'})
    
    def get_course_minutes_watched(self):
        course_info_ratings = pd.merge(self.course_info_df,
                                       self.course_ratings_df[['course_id', 'course_rating']],
                                       on='course_id')
        
        course_info_ratings = course_info_ratings.rename(columns={'course_rating': 'average_course_rating'})
        course_info_ratings['ratings'] = course_info_ratings.average_course_rating
        course_info_ratings = course_info_ratings.groupby(['course_id', 'course_title']).agg({'average_course_rating': 'mean', 'ratings': 'size'}).reset_index().round(2)

        course_minutes_watched = pd.merge(course_info_ratings,
                                          self.student_learning_df[['course_id', 'minutes_watched']],
                                          on='course_id')
        
        course_minutes_watched['average_minutes_watched'] = course_minutes_watched.minutes_watched
        course_minutes_watched = course_minutes_watched.groupby(['course_id', 'course_title', 'average_course_rating', 'ratings']).agg({'minutes_watched': 'sum', 'average_minutes_watched': 'mean'}).reset_index().round(2)
        course_minutes_watched = course_minutes_watched.sort_values(by='minutes_watched', ascending=False)
        course_minutes_watched = course_minutes_watched.drop('course_id', axis=1)

        return course_minutes_watched
    
    def get_platform_minutes_watched(self):
        # self.student_country = self.get_student_country()

        country_minutes_watched = pd.merge(self.merged_student_info_purchase,
                                           self.student_learning_df[['student_id', 'minutes_watched']],
                                           on='student_id',
                                           how='left')

        user_type_option, subscription_type_option, country_option = self.modify_options(country_minutes_watched)
        country_minutes_watched = country_minutes_watched[(country_minutes_watched.paid == user_type_option)
                                                 & (country_minutes_watched.purchase_type == subscription_type_option)
                                                 & (country_minutes_watched.student_country == country_option)]

        country_minutes_watched = country_minutes_watched[['student_country', 'minutes_watched']].groupby('student_country').sum().reset_index().sort_values(by='minutes_watched', ascending=False)

        return country_minutes_watched
    
    def get_monthly_average_minutes_watched(self):
        monthly_average_minutes_watched = pd.merge(self.merged_student_info_purchase,
                                                   self.student_learning_df,
                                                   on='student_id',
                                                   how='left')

        user_type_option, subscription_type_option, country_option = self.modify_options(monthly_average_minutes_watched)
        monthly_average_minutes_watched = monthly_average_minutes_watched[(monthly_average_minutes_watched.paid == user_type_option)
                                                                          & (monthly_average_minutes_watched.purchase_type == subscription_type_option)
                                                                          & (monthly_average_minutes_watched.student_country == country_option)]

        monthly_average_minutes_watched['month'] = monthly_average_minutes_watched.date_watched.dt.month
        monthly_average_minutes_watched['average_minutes_watched'] = monthly_average_minutes_watched.minutes_watched
        monthly_average_minutes_watched = monthly_average_minutes_watched[['month', 'minutes_watched', 'average_minutes_watched']].groupby('month').agg({'minutes_watched': 'sum', 'average_minutes_watched': 'mean'}).reset_index().round(2)
        monthly_average_minutes_watched.month = monthly_average_minutes_watched.month.map(self.month_names_dict)

        return monthly_average_minutes_watched
    
    def get_students_registered_onboarded(self):
        monthly_registered_students = pd.merge(self.merged_student_info_purchase, self.student_engagement_df, on='student_id', how='left')
        # monthly_registered_students.date_registered = pd.to_datetime(monthly_registered_students.date_registered)

        monthly_onboarded_students = monthly_registered_students.copy()

        monthly_registered_students = monthly_registered_students.drop_duplicates(subset='student_id')

        user_type_option, subscription_type_option, country_option = self.modify_options(monthly_registered_students)
        monthly_registered_students = monthly_registered_students[(monthly_registered_students.paid == user_type_option)
                                                                  & (monthly_registered_students.purchase_type == subscription_type_option)
                                                                  & (monthly_registered_students.student_country == country_option)]

        monthly_registered_students['month'] = monthly_registered_students.date_registered.dt.month
        monthly_registered_students = monthly_registered_students[['month']].groupby(['month']).size().reset_index()
        monthly_registered_students = monthly_registered_students.rename(columns={0: 'students'})

        user_type_option, subscription_type_option, country_option = self.modify_options(monthly_onboarded_students)
        monthly_onboarded_students = monthly_onboarded_students[(monthly_onboarded_students.paid == user_type_option)
                                                                  & (monthly_onboarded_students.purchase_type == subscription_type_option)
                                                                  & (monthly_onboarded_students.student_country == country_option)]

        monthly_onboarded_students['month'] = monthly_onboarded_students.date_engaged.dt.month
        monthly_onboarded_students = monthly_onboarded_students[['month']].groupby(['month']).size().reset_index()
        monthly_onboarded_students = monthly_onboarded_students.rename(columns={0: 'onboarded'})

        students_registered_onboarded = pd.merge(monthly_registered_students,
                                                 monthly_onboarded_students,
                                                 on='month')
        
        students_registered_onboarded.month = students_registered_onboarded.month.map(self.month_names_dict)

        return students_registered_onboarded
    
    def plot_top_largest_number_of_users(self):
        student_country = self.get_student_country()

        return px.bar(student_country.head(),
                      x='students',
                      y='student_country',
                      orientation='h',
                      color='student_country',
                      title=chart_titles['main_chart_1'],
                      labels={'students': 'Students', 'student_country': 'Student Country'},    
                      color_discrete_sequence=px.colors.qualitative.Prism)
        
    def plot_minutes_watched_by_country(self):
        platform_minutes_watched = self.get_platform_minutes_watched()

        return px.bar(platform_minutes_watched.head(),
                      x='minutes_watched',
                      y='student_country',
                      orientation='h',
                      color='student_country',
                      title='Amount of Minutes Watched on the Platform by Country',
                      labels={'minutes_watched': 'Minutes Watched', 'student_country': 'Student Country'},
                      color_discrete_sequence=px.colors.qualitative.Prism)
    
    def plot_minutes_watched_by_month(self):
        monthly_average_minutes_watched = self.get_monthly_average_minutes_watched()

        if monthly_average_minutes_watched.shape[0] > 0:
            colors = ['lightslategray'] * monthly_average_minutes_watched.shape[0]
            colors[monthly_average_minutes_watched.minutes_watched.idxmax()] = 'orange'
        else:
            colors = []

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=monthly_average_minutes_watched.month,
                             y=monthly_average_minutes_watched.minutes_watched,
                             name='Minutes Watched',
                             offsetgroup=1,
                             marker_color=colors), secondary_y=False)
                
        fig.add_trace(go.Scatter(x=monthly_average_minutes_watched.month,
                                 y=monthly_average_minutes_watched.average_minutes_watched,
                                 name='Average Minutes Watched',
                                 offsetgroup=2,
                                 marker_color='green',
                                 mode='markers+lines'), secondary_y=True)

        fig.update_xaxes(title_text='Month')
        fig.update_yaxes(title_text='Minutes Watched', secondary_y=False)
        fig.update_yaxes(title_text='Average Minutes Watched', secondary_y=True)
        fig.update_layout(title='Minutes Watched by Month')

        return fig
    
    def plot_registered_onboarded(self):
        students_registered_onboarded = self.get_students_registered_onboarded()

        if students_registered_onboarded.shape[0] > 0:
            colors_students = ['lightslategray'] * students_registered_onboarded.shape[0]
            colors_students[students_registered_onboarded.students.idxmax()] = 'orange'

            colors_onboarded = ['lightslategray'] * students_registered_onboarded.shape[0]
            colors_onboarded[students_registered_onboarded.onboarded.idxmax()] = 'orange'
        else:
            colors_students = []
            colors_onboarded = []

        return go.Figure(data=[
             go.Bar(name='Students', x=students_registered_onboarded.month,
                    y=students_registered_onboarded.students,
                    offsetgroup=1,
                    marker_color=colors_students),
            
             go.Bar(name='Onboarded',
                    x=students_registered_onboarded.month,
                    y=students_registered_onboarded.onboarded,
                    offsetgroup=2,
                    marker_color=colors_onboarded)]).update_layout(title='Number of Registered Students Compared to Onboarded')
    
    def get_registered_students_kpi(self):
        return self.student_info_df.student_id.nunique()
    
    def get_minutes_watched_kpi(self):
        return self.student_learning_df.minutes_watched.sum().round()
    
    def get_purchases_kpi(self):
        return self.student_purchases_df.purchase_id.nunique()
    
    def get_average_minutes_watched_kpi(self):
        return (self.get_minutes_watched_kpi() / self.student_learning_df.student_id.nunique()).round()
    
    def get_onboarded_from_registered_kpi(self):
        return round(self.student_engagement_df.student_id.nunique() / self.student_info_df.student_id.nunique(), 3) * 100
    
    def prepare_dashboard_helper_dataframe(self):
        self.merged_student_info_purchase = pd.merge(self.student_info_df, self.student_purchases_df, on='student_id', how='left')
        self.merged_student_info_purchase = self.merged_student_info_purchase.drop_duplicates(subset='student_id', keep='last')

        self.merged_student_info_purchase['latest_date_recorded'] = datetime(2022, 10, 20).date()
        self.merged_student_info_purchase.latest_date_recorded = pd.to_datetime(self.merged_student_info_purchase.latest_date_recorded)

        self.merged_student_info_purchase['days'] = (self.merged_student_info_purchase.latest_date_recorded - self.merged_student_info_purchase.date_purchased).dt.days

        self.merged_student_info_purchase['paid'] = self.merged_student_info_purchase.student_id.map(self.is_paid_tier)
        self.merged_student_info_purchase.purchase_type = self.merged_student_info_purchase.apply(lambda cols : self.replace_purchase_type(cols.paid, cols.purchase_type), axis=1)

        self.merged_student_info_purchase = self.merged_student_info_purchase.drop(['date_purchased', 'purchase_id', 'latest_date_recorded', 'days'], axis=1)

        self.merged_student_info_purchase.to_csv('data/processed/merged_student_info_purchase.csv', index=False)

    def is_paid_tier(self, student_id: str):
        df = self.merged_student_info_purchase[self.merged_student_info_purchase.student_id == student_id]

        days = df.days.iloc[0]
        purchase_type = df.purchase_type.iloc[0]

        if np.isnan(days):
            return False

        if purchase_type == 'Monthly':
            return days <= 30
        if purchase_type == 'Quarterly':
            return days <= 90
        if purchase_type == 'Annual':
            return days <= 365

    def replace_purchase_type(self, paid: bool, purchase_type: str):
            if paid == False or purchase_type == np.nan:
                return 'Free'
            return purchase_type
