import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

import mlflow

logging.basicConfig(
    filename='logs.log',
    format='[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# Data Ingestion
logging.info('Preparing data for machine learning.')

ingestion = DataIngestion()
ingestion.prepare_dataframe()
ingestion.to_csv('data/processed/ml_dataset.csv')

# Data Transformation
logging.info('Transforming data.')

transformation = DataTransformation()
transformation.transform_data(scaler='standard',
                              resampler='ros|rus')

transformation.to_csv(train_directory='data/train',
                      test_directory='data/test')

# Model Training
logging.info('Model hyperparameter tuning.')

model_training = ModelTrainer()

grid_search = model_training.get_gridsearch_dict()
scores = model_training.get_tuned_models_scores(grid_search, verbose=True)
classifier, params = model_training.get_best_classifier(scores)

model_training.save_best_classifier(classifier, params)
