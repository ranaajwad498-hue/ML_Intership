import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

class ChildRiskLogisticRegression:
    def __init__(self, x_train= "x_train.csv", x_test="x_test.csv", y_train="y_train.csv", y_test="y_test.csv"):
        self.x_train_file=x_train
        self.x_test_file= x_test
        self.y_train_file=y_train
        self.y_test_file=y_test
        self.x_train=None
        self.x_test = None
        self.y_train= None
        self.y_test= None
        self.prediction= None

    def load_data(self):
        self.x_train=pd.read_csv(self.x_train_file)
        self.x_test=pd.read_csv(self.x_test_file)
        self.y_train=pd.read_csv(self.y_train_file)
        self.y_test=pd.read_csv(self.y_test_file)

    def create_model(self):
        self.base_model = LogisticRegression(max_iter=1000)
        self.model = MultiOutputClassifier(self.base_model)
        return self.model

    def train_model(self):
        self.model.fit(self.x_train, self.y_train)
        print("Model is Trained Successfully")

    def make_predictions(self):
        self.prediction=self.model.predict(self.x_test)
        print("Testing Data\n",self.prediction)
        print("Actual Data\n",self.y_test)
        return self.prediction

    def predict_proba(self):
        print("Probability:",self.model.predict_proba(self.x_test))

    def save_model(self):
        joblib.dump(self.model, "Trained Model.pkl")
        print("Model is Saved Successfully")

    def load_model(self):
        self.load = joblib.load("Trained Mode.pkl")
        return self.load

    def predict_single_child(self):
        print("Predicting New Child")
        new_child= pd.DataFrame([{
           "Age (months)":31,"Gender":0,"Region":2,"Mother_Education":3,"Household_Wealth_Index":0,"Height_cm":90,"Weight_kg":15
        }])
        self.prediction= self.model.predict(new_child)
        print("New Child",self.prediction)
        return self.prediction

    # def evaluate_model(self):
    #     for col in ['Stunting','Underweight', 'Overweight', 'Anemia', 'Malaria', 'Diarrhea', 'TB','Nutrition_Status']:
    #         accuracy = self.y_test[col]
    #         print(f"Accuracy Score of {col} is:",accuracy_score(accuracy, self.prediction))
            


pipline = ChildRiskLogisticRegression("x_train.csv", "x_test.csv", "y_train.csv", "y_test.csv")
pipline.load_data()
pipline.create_model()
pipline.train_model()
pipline.make_predictions()
pipline.predict_proba()
# pipline.evaluate_model()
pipline.predict_single_child()
