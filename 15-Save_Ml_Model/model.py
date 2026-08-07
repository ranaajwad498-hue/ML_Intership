import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
import joblib

class ChildRiskModelManager:
    def __init__(self,xtrain, xtest, ytrain, ytest):
        self.xtrain_file= xtrain
        self.ytrain_file= ytrain
        self.xtest_file= xtest
        self.ytest_file= ytest
        self.xtrain=None
        self.ytrain=None
        self.xtest=None
        self.ytest=None

    def load_training_data(self):
        try:
            self.xtrain= pd.read_csv(self.xtrain_file)
            self.ytrain= pd.read_csv(self.ytrain_file).values.ravel()
            print("Shape of X_train File:",self.xtrain.shape)
            print("Shape of Y_train File:",self.ytrain.shape)
        except FileNotFoundError as e:
            print(f"Failed to load File: {e.filename}File not Found")

    def create_model(self):
        print("Random Forest Classifier is Creating.....")
        numeric_col=["Age (months)", 'Height_cm', 'Weight_kg']
        ordinal_cols = ["Mother_Education", "Household_Wealth_Index"]
        nominal_cols = ["Gender"]

        edu_order=["No education", "Primary", "Secondary", "Higher"]
        wealth_order= ["Low", "Middle", "High"]

        preprocessor= ColumnTransformer(transformers=[
            ("num", StandardScaler(), numeric_col),
            ("ord", OrdinalEncoder(categories=[edu_order,wealth_order]), ordinal_cols),
            ("nom", OneHotEncoder(drop="if_binary"),nominal_cols),
        ])

        self.model=Pipeline(steps=[
            ("preprocessing", preprocessor),
            ("classifier", RandomForestClassifier(random_state=42, max_samples=None, min_samples_split=2, min_samples_leaf=2))
        ])
        print("Model is Created Successfully")

    def train_model(self):
        print("Model Training is Started.....")
        self.model.fit(self.xtrain, self.ytrain)
        print("Model Trained Successfully")

    def save_model(self):
        print("Saving a Model..... ")
        joblib.dump(self.model, "Random_Forest_Classifier.joblib")
        print("Model is Saved Succssfully")

    def load_saved_model(self):
        print("Model is Loading.....")
        self.load_model= joblib.load("Random_Forest_Classifier.joblib")
        print("Model is Loaded Successfully")

    def load_test_data(self):
        print("Loading Test Data....")
        try:
            self.xtest=pd.read_csv("x_test.csv")
            self.ytest=pd.read_csv("y_test.csv")
            print("Files are Loaded Successfully")
            print("Shape of X_Test File:",self.xtest.shape)
            print("Shape of Y_Test File:",self.ytest.shape)
        except FileNotFoundError as e:
            print(f"Failed to Load File:{e.filename} is not Found")

    def make_predictions(self):
        self.pred= self.load_model.predict(self.xtest)
        print("Prediction:",self.pred)

    def predict_single_child(self):
        print("Predicting New Child")
        new_child= pd.DataFrame([{'Age (months)':11,  'Gender':"Male", 'Mother_Education':"Higher", 
                                  'Household_Wealth_Index':"Low",  'Height_cm':83.7, 'Weight_kg':17
        }])
        pred= self.load_model.predict(new_child)
        if pred ==1:
            pred= "Stunted"
        else:
            pred="Not Stunted"

        print("Record Number is:",self.xtest.index[15])
        print("Actual Risk:",self.ytest.loc[15])
        print("Child is:",pred)
        print("Prediction probability", self.load_model.predict_proba(new_child))

    def evaluate_loaded_model(self):
        print("Accuracy of the Model:",accuracy_score(self.ytest, self.pred))
        print("Precision Score:",precision_score(self.ytest, self.pred))
        print("Recall Score:",recall_score(self.ytest, self.pred))
        print("F1 Score:",f1_score(self.ytest, self.pred))

    def save_model_info(self):
        with open("model_information.txt", "w") as file:
            file.write("Model name: Random Forest Classifier\n")
            file.write("Model file name: Random_Forest_Classifier.joblib\n")
            file.write("Model file size: 10.4 MB\n")
            file.write("Date of training: 07/08/2026\n")
            file.write(f"Features used:{self.xtest.columns}\n")
            file.write(f"Target classes;{self.ytest.columns}\n")
            file.write(f"Accuracy of the Model:{accuracy_score(self.ytest, self.pred)}\n")
            file.write(f"Precision Score:{precision_score(self.ytest, self.pred)}\n")
            file.write(f"Recall Score:{recall_score(self.ytest, self.pred)}\n")
            file.write(f"F1 Score:{f1_score(self.ytest, self.pred)}\n")

    def run(self):
        print("===== Child Malnutrition Model Management =====")
        self.load_training_data()
        self.create_model()
        self.train_model()
        self.save_model()
        self.load_saved_model()
        self.load_test_data()
        self.make_predictions()
        self.predict_single_child()
        self.evaluate_loaded_model()
        self.save_model_info()

child= ChildRiskModelManager("x_train.csv", "x_test.csv", "y_train.csv", "y_test.csv")
child.run()

        