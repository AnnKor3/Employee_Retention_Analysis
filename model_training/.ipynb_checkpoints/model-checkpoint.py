import logging
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import catboost
import lightgbm
import xgboost as xgb
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import shap
import matplotlib.pyplot as plt

class Model:
    
    def __init__(self):
        pass

    def training(self,X_train,y_train,X_test,y_test):
        pipe = Pipeline([
        ("classifier", AdaBoostClassifier())])
        sp = [
        {"classifier": [catboost.CatBoostClassifier(silent=True),AdaBoostClassifier(),GradientBoostingClassifier(),xgb.XGBClassifier(), lightgbm.LGBMClassifier()],
        "classifier__n_estimators": [100,120,150,300]}]

        grid = GridSearchCV(pipe, sp, cv=10, verbose=0)
        ml_grid = grid.fit(X_train,y_train)
        pred = ml_grid.predict(X_test)
        X_test['Prediction'] = pred
        logging.info( ml_grid.best_params_)
        logging.info( accuracy_score(y_test,pred))

        # shap
        explainer = shap.TreeExplainer(ml_grid.best_estimator_.steps[0][1])
        shap_values = explainer.shap_values(X_test)
        shap.summary_plot(shap_values, X_test,feature_names=X_test.columns)
        fig = shap.summary_plot(shap_values, X_test,feature_names=X_test.columns,show=False)
        plt.savefig('outputs\\general_importance.png')
        return [X_test, shap_values]

