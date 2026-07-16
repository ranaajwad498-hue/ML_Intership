import pandas as pd 
import matplotlib.pyplot as plt

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

    # def analyze_relationships(self):
    #     print("Most Malnutrition cases occur in Male children.")
    #     print("Children Weight Greator Than ")

    
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
        print()




df = pd.read_csv("malnutrition_children_ethiopia.csv")
child = ChildNutritionEDA(df)
child.display_report()

