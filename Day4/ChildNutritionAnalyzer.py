import pandas as pd
class ChildNutritionAnalyzer:
    def __init__(self,child_data):
        self.child_data= child_data


    child_data ={
    "Child_ID":     [1,2,3,4,5,
                     6,7,8,9,10,
                     11,12,13,14,15,
                     16,17,18,19,20],

    "Child_Name":   ["Ahmad", "Aslam", "Akram", "Ali", "Amana",
                      "Areeba", "Fatima", "Eman", "Saqib", "Ayesha", 
                      "Hasssan", "Ayyaz", "Haseeb", "Mahmod", "Bilal", 
                      "Mahnoor", "Talha","Haroon", "Hussian", "Nouman"],
    
    "age_months":   [11, 33, 15, 26,17,
                     12, 29, 10, 19, 20,
                     21, 22, 24, 25, 15, 
                     31, 30, 26, 28, 20],

    "Gender":       ["Male", "Male", "Male", "Male", "Female", 
                     "Female", "Female", "Female", "Male", "Female", 
                     "Male", "Male", "Male", "Male", "Male", 
                     "Female", "Male", "Male", "Male", "Male"],

    "Weight_Kg":    [10.1, 11.3, 9.3, 7.4, 12,
                      15, 13, 6, 12.3, 11, 
                      15, 9.4, 4.6, 13.5, 15.3,
                        16, 8, 7, 9 ,17],

    "Height_Cm":    [67, 68, 57, 49, 60, 
                     57, 87, 78, 58, 49, 
                     57, 48, 70, 65, 45, 
                     73, 82, 71, 55, 76]

    }
    df = pd.DataFrame(child_data)
    df.to_csv("children.csv")


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





