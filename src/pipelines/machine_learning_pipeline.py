from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

from src.components.machine_learning_grid_search import grid_search

# Data Ingestion
ingestion = DataIngestion()
ingestion.prepare_dataframe()
ingestion.to_csv('data/processed/ml_dataset.csv')

# Data Transformation
transformation = DataTransformation()
transformation.transform_data(scaler='standard',
                              resampler='ros|rus')

transformation.to_csv(train_directory='data/train',
                      test_directory='data/test')

# Model Training
model_training = ModelTrainer()

scores = model_training.get_tuned_models_scores(grid_search, verbose=True)
classifier, params = model_training.get_best_classifier(scores)

model_training.save_best_classifier(classifier, params)
