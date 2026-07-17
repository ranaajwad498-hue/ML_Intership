import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
class ChildNutritionEDA:
    def __init__(self,df):
        self.df = df
        
    def display_first_records(self):
        return self.df.head()

    def display_dataset_shape(self):
        return self.df.shape
    
    def display_columns(self):
        print("Total Columns: ", len(self.df.columns))
        total_numeric = self.df.select_dtypes(include='int64').columns
        print("Total Numeric Columns:", len(total_numeric))
        total_catgory= self.df.select_dtypes(include= "str").columns
        print("Total Categorical Columns: ", len(total_catgory))
    
    def display_dataset_info(self):
        return self.df.info()
    

    def check_duplicate_records(self):
        return self.df.duplicated().sum()
            
    def display_summary_statistics(self):
        return self.df.describe()
    
    def display_unique_values(self):
        self.df =  self.df.drop(columns= ["ID"])
        for col in self.df:
            print(f"Uniques Values in {col}:", self.df[col].unique())

    def analyze_relationships(self):
        print("Nutrition Status According to Age\n",self.df.groupby('Age (months)')['Nutrition_Status'].value_counts().unstack().sort_values)
        print("Nutrition Status According to Gender\n",self.df.groupby("Gender")["Nutrition_Status"].value_counts().sort_values)
        print("Nutrition Status According to Weight\n",self.df.groupby("Weight_kg")["Nutrition_Status"].value_counts().unstack().sort_values)
        print("Nutrition Status According to Height\n",self.df.groupby("Height_cm")["Nutrition_Status"].value_counts().unstack().sort_values)
        
    
    def display_report(self):
        print("              ---        First Five Records \n", self.display_first_records())
        print("Shape of DataSet: ",self.display_dataset_shape())
        self.display_columns()
        print("             ---         All Information of Our DataSet          ----")
        print( self.display_dataset_info())
        print("             ----        Unique Values in Each Columns           ---- ")
        print(self.display_unique_values())
        print("Summary Statistics of our DataSet\n", self.display_summary_statistics() )
        print("Duplicate Reords: ", self.check_duplicate_records())
        print("Summary Statistics Generated Successfully")
        self.analyze_relationships()

    



df = pd.read_csv("malnutrition_children_ethiopia.csv")
child = ChildNutritionEDA(df)
print(df["Gender"].value_counts())
print(df.loc[df["Gender"] == "Male"].shape[0])
print(len(df["Gender"]))
# child.analyze_relationships()
