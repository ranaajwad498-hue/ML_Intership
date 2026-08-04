import pandas as pd
import joblib
import shap

class ChildRiskSHAPExplainer:
    def __init__(self, xtrain, xtest, ytest, model):
        self.xtrain_file= xtrain
        self.xtest_file= xtest
        self.ytest_file= ytest
        self.model_file= model
        self.xtrain=None
        self.xtest= None
        self.ytest= None
        self.model= None

    def load_model_and_data(self):
        try:
            self.xtrain= pd.read_csv(self.xtrain_file)
            self.xtest= pd.read_csv(self.xtest_file)
            self.ytest= pd.read_csv(self.ytest_file)
            self.model= joblib.load(self.model_file)
        except FileNotFoundError as e:
            print(f"Failed to load file: {e.filename} does not exist.")
        print("Shape of X_Train:", self.xtrain.shape)
        print("Shape of X_Test:", self.xtest.shape)
        print("Shape of Y_Test:", self.ytest.shape)

    def create_explainer(self):
        print("Createing SHAP Explainer")
        self.expalainer= shap.Explainer(self.model)
        self.shap_values= self.expalainer(self.xtest)


child= ChildRiskSHAPExplainer("x_train.csv", "x_test.csv", "y_test.csv", "Random Forest Model.pkl")
child.load_model_and_data()
child.create_explainer()