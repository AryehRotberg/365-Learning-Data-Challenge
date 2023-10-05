import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation


# Logging Configuration
logging.basicConfig(filename='logs/ml_pipeline_standardized_data.log',
                    format='[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.info('Experiment - Used standardized data.\n')

# Data Ingestion
# ingestion = DataIngestion()

# ingestion.prepare_dataframe()
# ingestion.to_csv('data/processed/ml_dataset.csv')

# Data Transformation
transformation = DataTransformation()

transformation.transform_data(scaler=None,
                              resampler='ros|rus')
transformation.to_csv(train_directory='data/train',
                      val_directory='data/val',
                      test_directory='data/test')

# Model Training
model_training = ModelTrainer()

optuna_pipeline = model_training.create_optuna_pipeline(n_trials=550)
scores = model_training.get_study_values(optuna_pipeline)
classifier, params = model_training.get_best_classifier(scores)

logging.info(f'Best tuned model -> {classifier}')
logging.info(f'Model Parameters -> {params}\n')

# Model Evaluation - Validation Set
model_evaluation = ModelEvaluation(classifier, study=optuna_pipeline, val=True)

report = model_evaluation.get_classification_report()
conf = model_evaluation.get_confusion_matrix(plot=False)
f1_score = model_evaluation.get_f1_score()

logging.info(f'Validation Set -> Report: \n{report}\n')
logging.info(f'Validation Set -> Confusion Matrix: \n{conf}\n')
logging.info(f'Validation Set -> F1 Score: \n{f1_score}\n')

# Model Evaluation - Test Set
model_evaluation = ModelEvaluation(classifier, study=optuna_pipeline, val=False)

report = model_evaluation.get_classification_report()
conf = model_evaluation.get_confusion_matrix(plot=False)
f1_score = model_evaluation.get_f1_score()

logging.info(f'Test Set -> Report: \n{report}\n')
logging.info(f'Test Set -> Confusion Matrix: \n{conf}\n')
logging.info(f'Test Set -> F1 Score: \n{f1_score}')

model_evaluation.save_outputs(directory='outputs')
