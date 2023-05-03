import data_processing.processing as Processing
from data_processing.processing import Data_Processing
from model_training.model import Model

def run():
    processing = Data_Processing()
    model = Model()
    # data preparation
    X_train, X_test, y_train, y_test = processing.get_split_data()
    # model training and shap values - generate img with general feature importance for test dataset
    X_test, shap_values = model.training(X_train, y_train, X_test, y_test)
    # adding a new column with 'top 10 features' for each particular prediction; get 10 most likely reasons of potencial leave for each employee separately 
    X_test = processing.get_top10_features_for_each_prediction(X_test, shap_values)
    # generate excel file with positive predictions only and newly added column 'top 10 features'
    processing.generate_excel_with_predictions(X_test)
    
if __name__ == '__main__':
    run()