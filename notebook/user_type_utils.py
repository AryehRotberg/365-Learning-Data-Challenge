import numpy as np
import pandas as pd

from datetime import datetime


class user_type_utils:
    def __init__(self, input_df):
        self.student_purchases = pd.read_csv('data/raw/365_student_purchases.csv')
        self.student_purchases.date_purchased = pd.to_datetime(self.student_purchases.date_purchased)

        self.input_df = input_df
    
    def is_paid_tier(self, student_id: str):
        if student_id not in self.student_purchases.values:
            return False

        df = self.input_df[self.input_df.student_id == student_id]

        latest_date = datetime(2022, 10, 20).date()
        latest_date_purchased = df.date_purchased.iloc[0].date()

        latest_purchase_type = df.purchase_type.iloc[0]

        difference = (latest_date - latest_date_purchased).days

        if latest_purchase_type == 'Monthly':
            return difference <= 30
        if latest_purchase_type == 'Quarterly':
            return difference <= 90
        if latest_purchase_type == 'Annual':
            return difference <= 365

    def replace_purchase_type(self, paid: bool, purchase_type: str):
        if paid == False or purchase_type == np.nan:
            return 'Free'
        return purchase_type
