import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

logging.basicConfig(
    filename='logs.log',
    format='[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# Data Ingestion
logging.info('Preparing data for machine learning.')

di = DataIngestion()
di.prepare_dataframe()
di.to_csv('data/processed/ml_dataset.csv')

# Data Transformation
logging.info('Transforming data.')

dt = DataTransformation()
dt.transform_data(scaler='standard',
                  resampler='ros|rus')

dt.to_csv(train_directory='data/train',
          test_directory='data/test')

# Model Training
logging.info('Model hyperparameter tuning.')

mt = ModelTrainer()

grid_search = mt.get_gridsearch_dict()
scores = mt.get_tuned_models_scores(grid_search, verbose=True)
classifier, params = mt.get_best_classifier(scores)
mt.save_best_classifier(classifier, params)
