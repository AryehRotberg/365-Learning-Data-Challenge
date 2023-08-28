from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation


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

optuna_pipeline = model_training.create_optuna_pipeline(n_trials=550)
scores = model_training.get_study_values(optuna_pipeline)
classifier = model_training.get_best_classifier(scores)

# Model Evaluation
model_evaluation = ModelEvaluation(classifier)

report = model_evaluation.get_classification_report()
conf = model_evaluation.get_confusion_matrix(plot=False)
f1_score = model_evaluation.get_f1_score()

print(report, '\n')
print(conf, '\n')
print(f1_score, '\n')

model_evaluation.save_outputs(directory='outputs')
