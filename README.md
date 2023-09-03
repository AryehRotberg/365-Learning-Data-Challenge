
# 365 Learning Data Challenge: Insights & Machine Learning to Understand Student Behavior

## Overview
This repository is the culmination of my participation in the "365 Learning Data Challenge," where the task was to create a dashboard and a machine learning model for "365 Data Science" to better understand student behavior on their educational platform. The challenge might be over, but the journey has just begun!

## Table of Contents
1. Datasets
2. Key Insights
3. Tools Used
4. Machine Learning Model
5. Dashboard Features
6. Installation
7. Usage
8. Contributing
9. License

## Datasets
The project employs several datasets captured between January to October 2022 to provide a holistic view of the student behavior:

1. Course Ratings: Contains ratings for each course on the platform.
2. Student Engagement: Includes metrics for onboarded students and their activities.
3. Student Learning: Details the number of minutes watched for every course by each student.
4. Student Purchases: Showcases purchase types, which are Monthly, Quarterly, and Annual.
5. Course Info: Contains the Course ID and corresponding course title.
6. Student Hub Questions: Holds the ID of each question asked in the student hub, the student ID, and the date it was asked.

## Key Insights
- Peak in August: The month of August recorded the highest student engagement across the platform.
- Annual Subscription Preference: Annual purchase plans are the most popular among students.
- Global Variation: Significant geographical differences in onboarded students, suggesting an opportunity for localized marketing strategies.

## Tools Used
Streamlit: For dashboard creation and visualization.
Plotly & Matplotlib: For data visualization.
Pandas: For data manipulation.
Scikit-Learn (sklearn): For machine learning models.
Optuna: For hyperparameter optimization.
Langchain: For creating a chatbot.

## Machine Learning Model
The Random Forest Classifier model is used to differentiate between free-tier and paid-tier students. This model achieved an impressive f1-score of 97%.

## Dashboard Features
- General Analytics: A complete overview of key performance indicators.
- Time Series Analysis: Temporal distribution of key metrics.
- Ask ChatGPT: A unique feature where you can ask additional questions about the data used in the machine learning model training.

## Installation

Clone the repository
git clone https://github.com/AryehRotberg/365-Learning-Data-Challenge.git

Navigate to the directory
cd 365-Learning-Data-Challenge

Install dependencies
pip install -r requirements.txt

## Usage
To run the Streamlit app: streamlit run app/Dashboard.py

## Contributing
Feel free to fork the project and submit a pull request with your changes!

For a live demo, check out the Streamlit Dashboard.

Happy Learning! 🎓📊