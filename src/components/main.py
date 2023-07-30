from model_trainer import ModelTrainer
from data_transformation import DataTransformation


transformation = DataTransformation()
model_trainer = ModelTrainer()

transformation.transform_data(scaler='standard')
transformation.to_csv()

grid_search = model_trainer.get_gridsearch_dict()
scores = model_trainer.get_tuned_models_scores(grid_search, verbose=True)
classifier, params = model_trainer.get_best_classifier(scores)

model_trainer.save_best_classifier(classifier, params)
