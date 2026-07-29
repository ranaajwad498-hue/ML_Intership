import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

class ChildRiskLogisticRegression():
    def __init__(self, xtrain="x_train.csv", xtest="x_test.csv", ytrain="y_train.csv", ytest="y_test.csv"):
        self.xtrain_file = xtrain  
        self.xtest_file  = xtest    
        self.ytrain_file = ytrain  
        self.ytest_file  = ytest    
        self.xtrain = None
        self.xtest  = None
        self.ytrain = None
        self.ytest  = None
        self.model  = None
        self.prediction = None

    def load_data(self):
        print("Load data ")
        self.xtrain = pd.read_csv(self.xtrain_file)  
        self.xtest = pd.read_csv(self.xtest_file)
        self.ytrain = pd.read_csv(self.ytrain_file)
        self.ytest = pd.read_csv(self.ytest_file)

    def create_model(self):
        self.model = LogisticRegression(max_iter=1000)
        return self.model

    def train_model(self):
        print("Model Training is Loading....")
        self.model.fit(self.xtrain, self.ytrain.values.ravel()) 
        print("Model Trained Successfully")

    def make_predictions(self):
        self.prediction = self.model.predict(self.xtest)
        print("Prediction Result:\n", self.prediction)
        print("Actual Result\n", self.ytest)
        print("Prediction Probability\n", self.model.predict_proba(self.xtrain))
        return self.prediction

    def evaluate_model(self):
        print("Accuracy Score:", accuracy_score(self.ytest, self.prediction))
        print("Confusion Matrix:\n", confusion_matrix(self.ytest, self.prediction))
        print("Classification Report\n", classification_report(self.ytest, self.prediction))

    def pipeline(self):  
        print("===== Logistic Regression Model Evaluation =====")
        self.load_data()
        self.create_model()
        self.train_model()
        self.make_predictions()
        print("Model: Logistic Regression ")
        self.evaluate_model()
        self.predict_single_child()
        self.save_predictions()
        self.save_model()


    def predict_single_child(self ):
        new_child = pd.DataFrame([{'Age (months)':54,'Gender':0,'Region':3,'Mother_Education':1,
                                   'Household_Wealth_Index':1,'Height_cm':65,'Weight_kg':55}])
        
        prediction = self.model.predict(new_child)
        self.probability = self.model.predict_proba(new_child)
        if  prediction == 0:
             prediction="Normal"
        else:
             prediction="At_risk"
        print(f"This children is:{ prediction}")
        print("Proablity of this Child",self.probability)
        return  self.prediction,  self.probability

    def save_predictions(self):
        logistic_regression_predictions = {
        "Prediction": self.prediction, 
        "Actual Result": self.ytest.values.ravel(),  
    }
        logistic_regression_predictions = pd.DataFrame(logistic_regression_predictions)
        logistic_regression_predictions.to_csv("logistic_regression_predictions.csv", index=False)

    def save_model(self):
        joblib.dump(self.model,"logistic_regression_model.pkl")

child = ChildRiskLogisticRegression("x_train.csv", "x_test.csv", "y_train.csv", "y_test.csv")
child.pipeline() 
