import pandas as pd
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report,f1_score,precision_score,recall_score,ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import joblib


class ChildRiskModelComparison:
    def __init__(self,xtrain, xtest, ytrain, ytest):
        self.xtrainfile=xtrain
        self.xtestfile=xtest
        self.ytrainfile=ytrain
        self.ytestfile=ytest
        self.xtrain=None
        self.xtest=None
        self.ytrain=None
        self.ytest=None
        
    def load_data(self):
        self.xtrain=pd.read_csv("x_train.csv")
        self.xtest=pd.read_csv("x_test.csv")
        self.ytrain=pd.read_csv("y_train.csv").values.ravel()
        self.ytest=pd.read_csv("y_test.csv").values.ravel()
        print("Shape of X_test File",self.xtest.shape)
        print("Shape of X_train File",self.xtrain.shape)
        print("Shape of Y_test File",self.ytest.shape)
        print("Shape of Y_train File",self.ytrain.shape)

    def fe(self):
        numeric_col=["Age (months)", 'Height_cm', 'Weight_kg']
        ordinal_cols = ["Mother_Education", "Household_Wealth_Index"]
        nominal_cols = ["Gender"]

        edu_order=["No education", "Primary", "Secondary", "Higher"]
        wealth_order= ["Low", "Middle", "High"]

        self.preprocessor= ColumnTransformer(transformers=[
            ("num", StandardScaler(), numeric_col),
            ("ord", OrdinalEncoder(categories=[edu_order,wealth_order]), ordinal_cols),
            ("nom", OneHotEncoder(drop="if_binary"),nominal_cols),
        ])
    
    def create_decision_tree_model(self):
        print("Decison Tree Model")
        self.dt_model= Pipeline(steps=[
           ("preprocessing", self.preprocessor),
           ("classfier", DecisionTreeClassifier(random_state=42, max_depth=10, min_samples_split=5, min_samples_leaf=10))
        ])

    def create_random_forest_model(self):
        print("Random Forest Model")
        self.rf_model= Pipeline([
            ("preprocessing", self.preprocessor),
            ("classfier", RandomForestClassifier(n_estimators=500,random_state=42 ,max_depth=10, min_samples_split=5,min_samples_leaf=10))
        ])

    def  train_models(self):
        print("Training Decision Tree Model.....")
        self.dt_model.fit(self.xtrain, self.ytrain)
        print("Decision Tree trained successfully. ")
        print("Trainig Random Forest Model.....")
        self.rf_model.fit(self.xtrain, self.ytrain)
        print("Random Forest Model Trained Successfully")
        
    def make_predictions(self):
        self.dt_prediction= self.dt_model.predict(self.xtest)
        print("Prediction using Decision Tree Model:\n",self.dt_prediction)
        self.rf_prediction= self.rf_model.predict(self.xtest)
        print("Prediction using Random Forest Model:\n",self.rf_prediction )

    def evaluate_decision_tree(self):
        print("Decison Tree Classifier\nTraining Accuracy Score:", self.dt_model.score(self.xtrain, self.ytrain))
        print("Testing Accuracy Score:",accuracy_score(self.ytest, self.dt_prediction))
        print("Precision Score:", precision_score(self.ytest, self.dt_prediction))
        print("Recall Score:",recall_score(self.ytest, self.dt_prediction))
        print("F1 Score:",f1_score(self.ytest, self.dt_prediction))
        print(confusion_matrix(self.ytest, self.dt_prediction))
        print(classification_report(self.ytest, self.dt_prediction))

    def evaluate_random_forest(self):
        print("Random Forest Classifier\nTraining Accuracy Score:", self.rf_model.score(self.xtrain, self.ytrain))
        print("Testing Accuracy Score:",accuracy_score(self.ytest, self.rf_prediction))
        print("Precision Score:", precision_score(self.ytest, self.rf_prediction))
        print("Recall Score:",recall_score(self.ytest, self.rf_prediction))
        print("F1 Score:",f1_score(self.ytest, self.rf_prediction))
        print(confusion_matrix(self.ytest, self.rf_prediction))
        print(classification_report(self.ytest, self.rf_prediction))

    def compare_models(self):
        print("Decison Tree Testing Accuracy Score:",accuracy_score(self.ytest, self.dt_prediction))
        print("Random Forest Classifier Testing Accuracy Score:",accuracy_score(self.ytest, self.dt_prediction))
        print("Decison Tree F1 Score:",accuracy_score(self.ytest, self.rf_prediction))
        print("Random Forest F1 Accuracy Score:",accuracy_score(self.ytest, self.rf_prediction))

    def display_feature_importance(self):
        dt_importances = self.dt_model.named_steps["classfier"].feature_importances_
        rf_importances = self.rf_model.named_steps["classfier"].feature_importances_
        print("Feature Importances in Decision Tree:\n", dt_importances)
        print("Feature Importances in Random Forest:\n", rf_importances)

    def create_evaluation_charts(self):
        cm = confusion_matrix(self.ytest, self.dt_prediction)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Not Stunted', 'Stunted'])
        disp.plot(cmap=plt.cm.Blues) 
        plt.title("Confusion Matrix of Decision Tree")
        plt.savefig("charts/decision_tree_confusion_matrix.png", dpi=300, bbox_inches='tight')
        plt.show()
        # Random Forest Model
        cm = confusion_matrix(self.ytest, self.rf_prediction)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Not Stunted', 'Stunted'])
        disp.plot(cmap=plt.cm.Greens) 
        plt.title("Confusion Matrix of Random Forest")
        plt.savefig("charts/random_forest_confusion_matrix.png", dpi=300, bbox_inches='tight')
        plt.show()

    def save_predictions(self):
        print("Saving Actual Data and Prediction Data")
        data = {
            "Actual Data": self.ytest, 
            "DT_Prediction Data": self.dt_prediction,
            "RF_Prediction Data": self.rf_prediction,
        }
        data = pd.DataFrame(data)
        data.to_csv("model_comparison_predictions.csv", index=False)

    def save_models(self):
        joblib.dump(self.dt_model, "Decision Tree Model.pkl")
        joblib.dump(self.rf_model, "Random Forest Model.pkl")
    
    def pipline(self):
        self.load_data()
        self.fe()
        self.create_decision_tree_model()
        self.create_random_forest_model()
        self.train_models()
        self.make_predictions()
        self.evaluate_decision_tree()
        self.evaluate_random_forest()
        self.compare_models()
        self.display_feature_importance()
        self.create_evaluation_charts()
        self.save_predictions()
        self.save_models()


child = ChildRiskModelComparison("x_train.csv", "x_test.csv", "y_train.csv", "y_test.csv")
child.pipline()