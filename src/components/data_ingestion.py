import numpy as np
import pandas as pd

from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    exam_info_df = pd.read_csv('data/raw/365_exam_info.csv')
    quiz_info_df = pd.read_csv('data/raw/365_quiz_info.csv')
    student_engagement_df = pd.read_csv('data/raw/365_student_engagement.csv')
    student_hub_questions_df = pd.read_csv('data/raw/365_student_hub_questions.csv')
    student_info_df = pd.read_csv('data/raw/365_student_info.csv')
    student_learning_df = pd.read_csv('data/raw/365_student_learning.csv')
    student_purchases_df = pd.read_csv('data/raw/365_student_purchases.csv')


class DataIngestion:
    def __init__(self):
        self.config = DataIngestionConfig()

        self.config.student_engagement_df.date_engaged = pd.to_datetime(self.config.student_engagement_df.date_engaged)
        self.config.student_hub_questions_df.date_question_asked = pd.to_datetime(self.config.student_hub_questions_df.date_question_asked)
        self.config.student_info_df.date_registered = pd.to_datetime(self.config.student_info_df.date_registered)
        self.config.student_learning_df.date_watched = pd.to_datetime(self.config.student_learning_df.date_watched)
        self.config.student_purchases_df.date_purchased = pd.to_datetime(self.config.student_purchases_df.date_purchased)
    
    def has_student_engaged_with_quizzes(self, student_id: str):
        return (self.config.student_engagement_df[self.config.student_engagement_df.student_id == student_id].engagement_quizzes == 1).any()

    def has_student_engaged_with_exams(self, student_id: str):
        return (self.config.student_engagement_df[self.config.student_engagement_df.student_id == student_id].engagement_exams == 1).any()
    
    def prepare_dataframe(self):
        self.df = self.config.student_info_df.copy()

        sum_minutes_watched = pd.merge(self.config.student_info_df.student_id, self.config.student_learning_df[['student_id', 'minutes_watched']], on='student_id', how='left')
        sum_minutes_watched = sum_minutes_watched.fillna(0)
        sum_minutes_watched = sum_minutes_watched.groupby('student_id').sum().reset_index()

        days_engaged = self.config.student_engagement_df[['student_id', 'date_engaged']].groupby('student_id').size().reset_index()
        days_engaged = pd.merge(self.config.student_info_df.student_id, days_engaged, on='student_id', how='left').fillna(0).astype(np.int32)
        days_engaged = days_engaged.rename(columns={0: 'days_engaged'})

        self.df = pd.merge(self.df.student_id, sum_minutes_watched, on='student_id')
        self.df = pd.merge(self.df, days_engaged, on='student_id', how='left')

        self.df['engaged_with_quizzes'] = self.df.student_id.map(self.has_student_engaged_with_quizzes)
        self.df['engaged_with_exams'] = self.df.student_id.map(self.has_student_engaged_with_exams)
        self.df['engaged_with_qa'] = self.df.student_id.isin(self.config.student_hub_questions_df.student_id)
        self.df['subscribed'] = self.df.student_id.isin(self.config.student_purchases_df.student_id)

        self.df = self.df[~((self.df.subscribed == True) & (self.df.days_engaged == 0))]
        self.df = self.df.drop('student_id', axis=1)
    
    def save_dataframe_to_csv(self):
        self.df.to_csv('data/processed/ml_dataset.csv', index=False)
