import pandas as pd
# import model_evaluation.py
import joblib
import shap

class ChildRiskSHAPExplainer:
    def __init__(self, xtrain, xtest, ytest, model):
        self.xtrain_file = xtrain
        self.xtest_file = xtest
        self.ytest_file = ytest
        self.model_file = model
        self.xtrain = None
        self.xtest = None
        self.ytest = None
        self.model = None

    def load_model_and_data(self):
        try:
            self.xtrain = pd.read_csv(self.xtrain_file)
            self.xtest = pd.read_csv(self.xtest_file)
            self.ytest = pd.read_csv(self.ytest_file)
            self.model = joblib.load(self.model_file)
            print("Shape of X_Train:", self.xtrain.shape)
            print("Shape of X_Test:", self.xtest.shape)
            print("Shape of Y_Test:", self.ytest.shape)
        except FileNotFoundError as e:
            print(f"Failed to load file: {e.filename} does not exist.")

    def create_explainer(self):
        print("Creating SHAP Explainer...")
        preprocessor = self.model.named_steps['preprocessing']
        classifier = self.model.named_steps['classfier']  
        xtrain_transformed = preprocessor.transform(self.xtrain)
        xtest_transformed = preprocessor.transform(self.xtest)
        self.explainer = shap.TreeExplainer(classifier)
        self.shap_values = self.explainer(xtest_transformed)
        print("SHAP values computed successfully with TreeExplainer!")

    def create_summary_plot(self):
        print("Creating SHAP Summary Plot...")
        xtest_encoded = pd.get_dummies(self.xtest, columns=['Gender',"Mother_Education","Household_Wealth_Index"], drop_first=True)
        self.shap_values = self.explainer.shap_interaction_values(xtest_encoded)
        shap.plots.waterfall(self.shap_values[0], feature_names=xtest_encoded.columns)
        print("SHAP Summary Plot created successfully!")

child = ChildRiskSHAPExplainer("x_train.csv", "x_test.csv", "y_test.csv", "Random Forest Model.pkl")
child.load_model_and_data()
child.create_explainer()
child.create_summary_plot()
