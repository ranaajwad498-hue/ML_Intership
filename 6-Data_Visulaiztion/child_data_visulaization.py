import matplotlib.pyplot as plt
import pandas as pd 

class children:
    def __init__(self,df):
        self.df= df

    def display_columns(self):
        self.df.colums

    def create_gender_chart(self):
        count =self.df["Gender"].value_counts()
        print(count)
        plt.bar(count.index, count.values)
        plt.grid(True)
        plt.xlabel("Gender")
        plt.ylabel("Number of Children")
        plt.savefig("charts/gender_chart.png")
        plt.show()


    def create_risk_category_chart(self):
        counts = self.df["Nutrition_Status"].value_counts()
        print(counts)
        plt.pie(counts, labels=counts.index, autopct="%1.0f%%")
        plt.title("Nutrition_Status")
        plt.savefig("charts/risk_category_distribution.png")
        plt.show()

    def create_age_distribution_chart(self):
        plt.hist(self.df["Age (months)"])
        plt.grid(True)
        plt.title("Chart of Child's Age Distibutation")
        plt.xlabel("Child Age (Months)")
        plt.ylabel("Number of Children")
        plt.savefig("charts/age_distribution.png")
        plt.show()
    
    def create_all_charts(self):
        print("             ===== Child Nutrition Data Visualization =====")
        print("Dataset loaded successfully.")
        print("Creating Chart 1: Children by Gender...")
        self.create_gender_chart()
        print("Creating Chart 2: Risk Category Distribution...")
        self.create_risk_category_chart()
        print("Creating Chart 3: Age Distribution...")
        self.create_age_distribution_chart()
        print("Height and Weight Chart")
        self.create_height_weight_chart()

#Bonus Task:
    def create_height_weight_chart(self):
        plt.scatter(self.df["Height_cm"], self.df["Weight_kg"])
        plt.xlabel("Height (cm)")
        plt.ylabel("Weight (kg)")
        plt.title("Height vs Weight")
        plt.savefig("charts/Height_Weight.png")
        plt.show()

df = pd.read_csv("malnutrition_children_ethiopia.csv")
child = children(df)
child.create_all_charts()

