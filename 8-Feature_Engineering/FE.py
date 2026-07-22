import pandas as pd 

class ChildFeatureEngineer:
    def __init__(self , df):
        self.df=df

    def display_columns(self):
        print(self.df.columns)

    def display_first_records(self):
        print(self.df.head())

    def create_bmi(self):
        self.df["BMI"] = self.df["Weight_kg"] / ((self.df["Height_cm"] / 100) ** 2)
        self.df["BMI"] = self.df["BMI"].round(2)
        return self.df

    def create_weight_status(self):
        self.create_bmi()
        bins = [1, 20, 40, 60]
        labels = ["Under_Weight", "Normal", "Over_Weight"]
        self.df["Weight_Status"] = pd.cut(self.df["BMI"], bins=bins, labels=labels)
        return self.df

    def create_age_group(self):

        bins= [-1, 12, 24, 60]
        labels = ["Infant", "Toddler", "Preschool"]
        self.df["Age_Group"] = pd.cut(self.df["Age (months)"], bins= bins, labels=labels)
        return self.df

    def create_risk_score(self):
        self.create_weight_status()
        self.create_age_group()
        self.create_bmi()
        nutrtion_score = {"Under_Weight":35, "Normal":0, "Over_Weight":40}
        self.df["weight_score"]= self.df["Weight_Status"].map(nutrtion_score).astype(int)

        age_score = {"Infant":30, "Toddler":20, "Preschool":10}
        self.df["Age_Score"]= self.df["Age_Group"].map(age_score).astype(int)

        def bmi_score(bmi):
            if bmi < 15:
                return 30
            elif bmi < 25:
                return 10
            else:
                return 25
        self.df["BMI_Score"] = self.df["BMI"].apply(bmi_score)

        self.df["Risk_Score"]= self.df["BMI"] + self.df["nutrtion_score"] + self.df["Age_Score"]
        return self.df["Risk_Score"]
        

    def save_dataset(self):
        self.create_bmi()
        self.create_weight_status()
        self.create_age_group()
        self.create_risk_score()
        add_feature = self.df
        add_feature.to_csv("child_malnutrition_features.csv")

    def display_report(self):
        print("                     ===== Child Nutrition Feature Engineering =====")
        self.create_bmi()
        self.create_weight_status()
        self.create_age_group()
        self.create_risk_score()
        print(self.df)
        self.save_dataset()
        print("Dataset Saved Successfully")
        

df = pd.read_csv("malnutrition_children_ethiopia.csv")
child = ChildFeatureEngineer(df)
child.display_report()

