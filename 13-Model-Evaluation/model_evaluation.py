import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix,precision_score, recall_score, f1_score,ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import joblib

class ChildRiskModelEvaluator:
    def __init__(self, xtest_file, ytest_file, model_file):
        self.xtest_file= xtest_file
        self.ytest_file= ytest_file
        self.model_file= model_file
        self.xtest= None
        self.ytest= None
        self.model= None

    def load_model_and_data(self):
        try:
            self.xtest = pd.read_csv(self.xtest_file)
            self.ytest = pd.read_csv(self.ytest_file).squeeze("columns")
            self.model = joblib.load(self.model_file)
            print("Test data and Model loaded successfully.")

        except FileNotFoundError as e:
            print(f"Failed to load file: {e.filename} does not exist.")
        print("Shape of X_Test:", self.xtest.shape)
        print("Shape of Y_Test:", self.ytest.shape)

    def make_predictions(self):
        self.y_pred= self.model.predict(self.xtest)
        print("Predictions made successfully.",self.y_pred)
        print("Probabilities of predictions:", self.model.predict_proba(self.xtest))

    def calculate_accuracy(self):
        self.accuracy= accuracy_score(self.ytest, self.y_pred)
        print("Accuracy of the model:", self.accuracy)

    def calculate_precision(self):
       self.precision= precision_score(self.ytest, self.y_pred)
       print("Precision of the model:", self.precision)

    def calculate_recall(self):
        self.recall= recall_score(self.ytest, self.y_pred)
        print("Recall of the model:", self.recall)

    def calculate_f1_score(self):
        self.f1= f1_score(self.ytest, self.y_pred)
        print("F1 Score of the model:", self.f1)

    def generate_confusion_matrix(self):
        self.cm= confusion_matrix(self.ytest, self.y_pred)
        print("Confusion Matrix:\n", self.cm)

    def display_classification_report(self):
        report= classification_report(self.ytest, self.y_pred)
        print("Classification Report:\n", report)

    def create_confusion_matrix_chart(self):
        disp= ConfusionMatrixDisplay(confusion_matrix=self.cm , display_labels=["No Risk", "At Risk"])
        disp.plot()
        plt.title("Confusion Matrix")
        plt.savefig("charts/confusion_matrix.png")
        plt.show()

    def write_observations(self):
        print("Observations:")
        print(f"1. The model correctly identified {self.precision} of high-risk children.")
        print(f"2.The model missed {self.recall} high-risk children.")
        print("3. Recall is higher than precision, so the model identifies more high-risk children but produces some false alerts. ")
        print("4.The F1-score shows a reasonable balance between precision and recall.",self.f1)
        print("5. The model performs better for one class than the other.")

    def save_evaluation_results(self):
        df= pd.DataFrame({
            "Actual Result": self.ytest,
            "Predicted Result": self.y_pred,
            "Correct Prediction": self.ytest == self.y_pred,
            "Low Risk Probability": self.model.predict_proba(self.xtest)[:, 0],
            "High Risk Probability": self.model.predict_proba(self.xtest)[:, 1]
        })
        df.to_csv("model_evaluation_results.csv", index=False)

    def display_final_report(self):
        self.load_model_and_data()
        self.make_predictions()
        self.calculate_accuracy()
        self.calculate_precision()
        self.calculate_recall()
        self.calculate_f1_score()
        self.generate_confusion_matrix()
        self.display_classification_report()
        self.create_confusion_matrix_chart()
        self.write_observations()
        self.save_evaluation_results()

child= ChildRiskModelEvaluator("x_test.csv", "y_test.csv", "Random Forest Model.pkl")
child.display_final_report()
