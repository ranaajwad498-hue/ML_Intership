import pandas as pd
class ChildNutritionAnalyzer:
    def __init__(self,child_data):
        self.child_data= child_data

    df = pd.read_csv("children.csv")


    def display_all_children(self):
        print("                             ---         Children Details        ---")
        print(self.df)

    def get_total_children(self):
        print("Total number of children:", self.df.shape[0])

    def get_children_under_24_months(self):
        print("                            ---         Children Under Age 24 Months            ---")
        print(self.df.loc[self.df["age_months"] < 24])

    def count_children_under_24_months(self):
        print("Total number of children Under 24:" ,self.df[self.df["age_months"] < 24].shape[0])



analyzer = ChildNutritionAnalyzer("df")
analyzer.display_all_children()
analyzer.get_total_children()
analyzer.get_children_under_24_months()
analyzer.count_children_under_24_months()





