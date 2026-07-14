import pandas as pd

class ChildDataCleaner:
    def __init__(self, df):
        self.df = df
        
        
    def display_first_records(self):
        print(self.df.head())

    def display_dataset_shape(self):
        return self.df.shape

    def display_columns(self):
        print(self.df.columns)

    def display_dataset_info(self):
        print(self.df.info())

    def find_missing_values(self):
        print(self.df.isnull())

    def count_total_missing_values(self):
        print(self.df.isnull().sum())
        
    def clean_numerical_columns(self):
        total = self.df[["ID", "Age (months)","Height_cm", "Weight_kg","Stunting", "Underweight", "Overweight", "Anemia", "Malaria", "Diarrhea", "TB"]].isnull().sum().sum()
        self.df["ID"] =self.df["ID"].fillna(self.df["ID"].mean())
        self.df["Age (months)"] =self.df["Age (months)"].fillna(self.df["Age (months)"].mean())
        self.df["Height_cm"] =self.df["Height_cm"].fillna(self.df["Height_cm"].mean())
        self.df["Weight_kg"] =self.df["Weight_kg"].fillna(self.df["Weight_kg"].mean())
        self.df["Stunting"] =self.df["Stunting"].fillna(self.df["Stunting"].mean())
        self.df["Underweight"] =self.df["Underweight"].fillna(self.df["Underweight"].mean())
        self.df["Overweight"] =self.df["Overweight"].fillna(self.df["Overweight"].mean())
        self.df["Anemia"] =self.df["Anemia"].fillna(self.df["Anemia"].mean())
        self.df["Malaria"] =self.df["Malaria"].fillna(self.df["Malaria"].mean())
        self.df["Diarrhea"] =self.df["Diarrhea"].fillna(self.df["Diarrhea"].mean())
        self.df["TB"] =self.df["TB"].fillna(self.df["TB"].mean())
        return total


    def clean_categorical_columns(self):
        total= self.df[["Gender", "Region", "Mother_Education", "Household_Wealth_Index", "Nutrition_Status"]].isnull().sum().sum()
        
        self.df["Gender"]= self.df["Gender"].fillna(self.df["Gender"].mode()[0])
        self.df["Region"]= self.df["Region"].fillna(self.df["Region"].mode()[0])
        self.df["Mother_Education"]= self.df["Mother_Education"].fillna(self.df["Mother_Education"].mode()[0])
        self.df["Household_Wealth_Index"]= self.df["Household_Wealth_Index"].fillna(self.df["Household_Wealth_Index"].mode()[0])
        self.df["Nutrition_Status"]= self.df["Nutrition_Status"].fillna(self.df["Nutrition_Status"].mode()[0])
        return total
        

    def clean_data(self):
        self.clean_numerical_columns()
        self.clean_categorical_columns()
       
    def report(self):
        print("         ===== Child Malnutrition Data Cleaning =====")
        print("Total Records: ", self.display_dataset_shape())
        print("Cleaning numerical columns..." ,self.clean_numerical_columns())
        print("Cleaning categorical columns...",self.clean_categorical_columns())
        child.clean_data()
        print("Missing Values After Cleaning:", self.df.isnull().sum().sum())
        print("Data cleaning completed successfully.")

    def save_cleaned_data(self):
        self.clean_numerical_columns()
        self.clean_categorical_columns()
        cleaned_file  =  self.df
        cleaned_file.to_csv("cleaned_child_malnutrition_data.csv",index=False)

df = pd.read_csv("malnutrition_children_ethiopia.csv")

child = ChildDataCleaner(df)
child.report()
# child.save_cleaned_data()


