import pandas as pd

class app_utils:
    def __init__(self, user_type_option: str, subscription_type_option: str, country_option: str):
        self.user_type_option = user_type_option
        self.subscription_type_option = subscription_type_option
        self.country_option = country_option

        self.student_info_df = pd.read_csv('notebook/data/raw/365_student_info.csv')
        self.merged_student_info_purchase = pd.read_csv('notebook/data/processed/merged_student_info_purchase.csv')
        self.student_learning_df = pd.read_csv('notebook/data/raw/365_student_learning.csv')
        self.course_info_df = pd.read_csv('notebook/data/raw/365_course_info.csv')
        self.course_ratings_df = pd.read_csv('notebook/data/raw/365_course_ratings.csv')

        self.student_learning_df.date_watched = pd.to_datetime(self.student_learning_df.date_watched)
        self.course_ratings_df.date_rated = pd.to_datetime(self.course_ratings_df.date_rated)
    
    def get_country_list(self):
        return self.student_info_df.student_country.unique().tolist()
    
    def modify_options(self, df):
        if self.user_type_option == 'Free':
            user_type_option = False
            subscription_type_option = df['purchase_type']

        else:
            user_type_option = self.user_type_option
            subscription_type_option = self.subscription_type_option
            country_option = self.country_option
        
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
        course_info_ratings = pd.merge(self.course_info_df, self.course_ratings_df[['course_id', 'course_rating']], on='course_id')
        course_info_ratings = course_info_ratings.rename(columns={'course_rating': 'average_course_rating'})
        course_info_ratings['ratings'] = course_info_ratings.average_course_rating
        course_info_ratings = course_info_ratings.groupby(['course_id', 'course_title']).agg({'average_course_rating': 'mean', 'ratings': 'size'}).reset_index().round(2)

        course_minutes_watched = pd.merge(course_info_ratings, self.student_learning_df[['course_id', 'minutes_watched']], on='course_id')
        course_minutes_watched['average_minutes_watched'] = course_minutes_watched.minutes_watched
        course_minutes_watched = course_minutes_watched.groupby(['course_id', 'course_title', 'average_course_rating', 'ratings']).agg({'minutes_watched': 'sum', 'average_minutes_watched': 'mean'}).reset_index().round(2)
        course_minutes_watched = course_minutes_watched.sort_values(by='minutes_watched', ascending=False)
        course_minutes_watched = course_minutes_watched.drop('course_id', axis=1)

        return course_minutes_watched
    
    def get_platform_minutes_watched(self):
        self.student_country = self.get_student_country()

        country_minutes_watched = pd.merge(self.merged_student_info_purchase, self.student_learning_df[['student_id', 'minutes_watched']], on='student_id', how='left')

        user_type_option, subscription_type_option, country_option = self.modify_options(country_minutes_watched)
        country_minutes_watched = country_minutes_watched[(country_minutes_watched.paid == user_type_option)
                                                 & (country_minutes_watched.purchase_type == subscription_type_option)
                                                 & (country_minutes_watched.student_country == country_option)]

        country_minutes_watched = country_minutes_watched[['student_country', 'minutes_watched']].groupby('student_country').sum().reset_index().sort_values(by='minutes_watched', ascending=False)

        return country_minutes_watched
    
    def get_monthly_average_minutes_watched(self):
        monthly_average_minutes_watched = pd.merge(self.merged_student_info_purchase, self.student_learning_df, on='student_id', how='left')

        user_type_option, subscription_type_option, country_option = self.modify_options(monthly_average_minutes_watched)
        monthly_average_minutes_watched = monthly_average_minutes_watched[(monthly_average_minutes_watched.paid == user_type_option)
                                                                          & (monthly_average_minutes_watched.purchase_type == subscription_type_option)
                                                                          & (monthly_average_minutes_watched.student_country == country_option)]

        monthly_average_minutes_watched['month'] = monthly_average_minutes_watched.date_watched.apply(lambda date : date.month)
        monthly_average_minutes_watched['average_minutes_watched'] = monthly_average_minutes_watched.minutes_watched
        monthly_average_minutes_watched = monthly_average_minutes_watched[['month', 'minutes_watched', 'average_minutes_watched']].groupby('month').agg({'minutes_watched': 'sum', 'average_minutes_watched': 'mean'}).reset_index().round(2)

        return monthly_average_minutes_watched