import pandas as pd
import matplotlib.pyplot as plt
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
            # print("Shape of X_Train:", self.xtrain.shape)
            # print("Shape of X_Test:", self.xtest.shape)
            # print("Shape of Y_Test:", self.ytest.shape)
        except FileNotFoundError as e:
            print(f"Failed to load file: {e.filename} does not exist.")

    def create_explainer(self):
        print("Creating SHAP Explainer...")
        preprocessor = self.model.named_steps['preprocessing']
        classifier = self.model.named_steps['classifier'] 
        xtest_transformed = preprocessor.transform(self.xtest)
        feature_names = preprocessor.get_feature_names_out()
        self.xtest_trans_df= pd.DataFrame(xtest_transformed, columns=feature_names)
        self.explainer = shap.TreeExplainer(classifier)
        self.shap_values = self.explainer(self.xtest_trans_df)
        print("SHAP values computed successfully with TreeExplainer!")

    def create_summary_plot(self):
        print("Creating SHAP Summary Plot...")
        if len(self.shap_values.shape) == 3:
            shap.summary_plot(self.shap_values[:, :, 1], self.xtest_trans_df)
        else:
            shap.summary_plot(self.shap_values, self.xtest_trans_df)
        plt.savefig("charts/shap_summary_plot.png")



child = ChildRiskSHAPExplainer("x_train.csv", "x_test.csv", "y_test.csv", "Random Forest Model.pkl")
child.load_model_and_data()
child.create_explainer()
child.create_summary_plot()
