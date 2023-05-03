import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
from sklearn.model_selection import train_test_split

class Data_Processing:
    
    def __init__(self):
        pass

    def load_data(self):
        # ..\data\\WA_Fn-UseC_-HR-Employee-Attrition.csv
        return pd.read_csv('data\\WA_Fn-UseC_-HR-Employee-Attrition.csv')

    def get_X(self, df_):
        df = df_.copy()
        X = df[['Age', 'BusinessTravel', 'DailyRate', 'Department',
           'DistanceFromHome', 'Education', 'EducationField', 'EmployeeCount',
           'EmployeeNumber', 'EnvironmentSatisfaction', 'Gender', 'HourlyRate',
           'JobInvolvement', 'JobLevel', 'JobRole', 'JobSatisfaction',
           'MaritalStatus', 'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked',
            'OverTime', 'PercentSalaryHike', 'PerformanceRating',
           'RelationshipSatisfaction', 'StandardHours', 'StockOptionLevel',
           'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance',
           'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion',
           'YearsWithCurrManager']]

        X = pd.get_dummies(X, columns=[ 'Gender', 'OverTime'], drop_first=True)
        X = pd.get_dummies(X, columns=['BusinessTravel', 'Department', 'EducationField', 'JobRole','MaritalStatus'])
        return X

    def get_y(self, df):
        y = df['Attrition']
        y = y.map({"Yes":1, "No":0})
        return y

    def split_data(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
        return  X_train, X_test, y_train, y_test

    def get_split_data(self):
        df = self.load_data()
        X = self.get_X(df)
        y = self.get_y(df)
        return self.split_data(X, y)

    def get_top10_features_for_each_prediction(self, X_test, shap_values):
        l = list()

        for i in range(len(shap_values)):  
            d = dict(zip(X_test.columns,shap_values[i]))
            a = sorted(d.items(), key=lambda x:x[1])
            l.append(a[-5:]+a[:5])

        X_test['top 10 features'] = l
        X_test['top 10 features'] = X_test['top 10 features'].map(lambda x: str(x).replace('(','').replace('[','').replace(')','').replace(']','').replace("',",':').replace("'",'')) 
        return X_test

    def generate_excel_with_predictions(self, X_test):
        X_test[X_test['Prediction']==1].to_excel('outputs\\predictions.xlsx')