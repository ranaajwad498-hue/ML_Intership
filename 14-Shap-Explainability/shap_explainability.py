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
            print("Shape of X_Train:", self.xtrain.shape)
            print("Shape of X_Test:", self.xtest.shape)
            print("Shape of Y_Test:", self.ytest.shape)
        except FileNotFoundError as e:
            print(f"Failed to load file: {e.filename} does not exist.")

    def create_explainer(self):
        print("Creating SHAP Explainer...")
        preprocessor = self.model.named_steps['preprocessing']
        classifier = self.model.named_steps['classifier'] 
        xtest_transformed = preprocessor.transform(self.xtest)
        self.feature_names = preprocessor.get_feature_names_out()
        self.xtest_trans_df= pd.DataFrame(xtest_transformed, columns=self.feature_names)
        self.explainer = shap.TreeExplainer(classifier)
        self.shap_values = self.explainer(self.xtest_trans_df)
        print("SHAP values computed successfully with TreeExplainer!")

    def create_summary_plot(self):
        print("Creating SHAP Summary Plot...")
        if len(self.shap_values.shape) == 3:
            shap_data = self.shap_values[:, :, 1]
        else:
            shap_data = self.shap_values
        shap.summary_plot(shap_data, self.xtest_trans_df, show=False)
        plt.savefig("charts/shap_summary_plot.png",bbox_inches='tight', dpi=300)

    def create_feature_importance_plot(self):
        print("Creating SHAP Bar Plot...")
        if len(self.shap_values.shape) == 3:
            self.shap_data = self.shap_values[:, :, 1]
        else:
            self.shap_data = self.shap_values
        shap.plots.bar(self.shap_data,show= False)
        plt.savefig("charts/shap_feature_importance.png",bbox_inches='tight', dpi=300)

    def explain_single_child(self):
        y_pred=pd.DataFrame([{
            'Age (months)':7,  'Gender':"Male", 'Mother_Education':"Primary", 'Household_Wealth_Index':"Low",  
            'Height_cm':77.5 , 'Weight_kg':13.7
        }])
        predict= self.model.predict(y_pred)
        print("Index of Record:",self.xtest.index[20])
        print("Prediction Result:",predict)
        print("Actual Result:",self.ytest.iloc[20])
        print("Prediction Probabity:",self.model.predict_proba(y_pred))
        prep_step = self.model.named_steps['preprocessing']
        classifier_step = self.model.named_steps['classifier']
        y_pred_trans = prep_step.transform(y_pred)
        feature_names = prep_step.get_feature_names_out()
        y_pred_df = pd.DataFrame(y_pred_trans, columns=feature_names)
        explainer = shap.TreeExplainer(classifier_step)
        explanation = explainer(y_pred_df)
        if len(explanation.shape) == 3:
            child_shap_values = explanation[0, :, 1].values
        else:
            child_shap_values = explanation[0].values
        self.shap_data = pd.DataFrame({
            'Feature': self.feature_names,
            'SHAP_Value': child_shap_values
        })
        increasing_risk =self.shap_data[self.shap_data['SHAP_Value'] > 0].head(3)
        decreasing_risk = self.shap_data[self.shap_data['SHAP_Value'] < 0].tail(3)
        print("--- Top factors increasing risk ---")
        print(increasing_risk.to_string(index=False))
        print("\n--- Top factors decreasing risk ---")
        print(decreasing_risk.to_string(index=False))

    def create_waterfall_plot(self, sample_index=0):
        print("Creating Waterfall Plot...")
        if len(self.shap_values.shape) == 3:
            shap_data = self.shap_values[:, :, 1]
        else:
            shap_data = self.shap_values
        shap.plots.waterfall(shap_data[sample_index], show=False)
        plt.savefig(f"charts/shap_waterfall_sample.png", bbox_inches='tight', dpi=300)
        plt.close()

    def save_explanations(self, sample_index=0):
        """Save SHAP explanations to CSV"""
        print('Saving explanations...')
        if len(self.shap_values.shape) == 3:
            self.shap_data = self.shap_values[:, :, 1]
        else:
            self.shap_data = self.shap_values
        shap_data = self.shap_data 
        feature_values = self.xtest_trans_df.iloc[sample_index].values
        if len(shap_data.shape) == 2:
            shap_values_sample = shap_data[sample_index]
        else:
            shap_values_sample = shap_data[sample_index]
    
        df = pd.DataFrame({
            "Feature Name": self.feature_names,
            "Feature Value": feature_values,
            "SHAP Value": shap_values_sample,
            "Absolute SHAP": shap_values_sample
        })
        df.to_csv("shap_feature_contributions.csv", index=False)
        print(f"Explanations saved to shap_feature_contributions.csv")

    def display_final_report(self):
        print("===== Child Malnutrition Model Explainability =====")
        self.load_model_and_data()
        self.create_explainer()
        self.create_summary_plot()
        self.create_feature_importance_plot()
        self.explain_single_child()
        self.explain_single_child()
        self.create_waterfall_plot()
        self.save_explanations()

child = ChildRiskSHAPExplainer("x_train.csv", "x_test.csv", "y_test.csv", "Random Forest Model.pkl")
child.display_final_report()
