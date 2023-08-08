import pandas as pd


class DataIngestion:
    def __init__(self):
        self.student_engagement_df = pd.read_csv('data/raw/365_student_engagement.csv')
        self.student_hub_questions_df = pd.read_csv('data/raw/365_student_hub_questions.csv')
        self.student_info_df = pd.read_csv('data/raw/365_student_info.csv')
        self.student_learning_df = pd.read_csv('data/raw/365_student_learning.csv')
        self.student_purchases_df = pd.read_csv('data/raw/365_student_purchases.csv')

        self.student_engagement_df.date_engaged = pd.to_datetime(self.student_engagement_df.date_engaged)
        self.student_hub_questions_df.date_question_asked = pd.to_datetime(self.student_hub_questions_df.date_question_asked)
        self.student_info_df.date_registered = pd.to_datetime(self.student_info_df.date_registered)
        self.student_learning_df.date_watched = pd.to_datetime(self.student_learning_df.date_watched)
        self.student_purchases_df.date_purchased = pd.to_datetime(self.student_purchases_df.date_purchased)
    
    def has_student_engaged_with_quizzes(self, student_id: str):
        return (self.student_engagement_df[self.student_engagement_df.student_id == student_id].engagement_quizzes == 1).any()

    def has_student_engaged_with_exams(self, student_id: str):
        return (self.student_engagement_df[self.student_engagement_df.student_id == student_id].engagement_exams == 1).any()
    
    def prepare_dataframe(self):
        sum_minutes_watched = pd.merge(self.student_info_df.student_id,
                                       self.student_learning_df[['student_id', 'minutes_watched']],
                                       on='student_id',
                                       how='left')

        sum_minutes_watched = sum_minutes_watched.groupby('student_id').sum().reset_index()

        days_engaged = self.student_engagement_df[['student_id']].groupby('student_id').size().reset_index()
        days_engaged = days_engaged.rename(columns={0: 'days_engaged'})

        self.df = pd.merge(days_engaged,
                           sum_minutes_watched,
                           on='student_id',
                           how='right')

        self.df = self.df.fillna(0)

        self.df['engaged_with_quizzes'] = self.df.student_id.map(self.has_student_engaged_with_quizzes)
        self.df['engaged_with_exams'] = self.df.student_id.map(self.has_student_engaged_with_exams)
        self.df['engaged_with_qa'] = self.df.student_id.isin(self.student_hub_questions_df.student_id)
        self.df['paid'] = self.df.student_id.isin(self.student_purchases_df.student_id)

        self.df = self.df[~((self.df.paid == True) & (self.df.days_engaged == 0))]
        self.df = self.df.drop('student_id', axis=1)
    
    def to_csv(self, file_path):
        self.df.to_csv(file_path, index=False)
