import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

raw_data= pd.read_csv("malnutrition_children_ethiopia.csv")
cleaned_data = raw_data.drop(columns=["ID"])

le= LabelEncoder()
string_data = cleaned_data.select_dtypes(include="object")
for col in string_data:
    cleaned_data[col]=le.fit_transform(cleaned_data[col])


x= cleaned_data.drop(columns=['Stunting',
       'Underweight', 'Overweight', 'Anemia', 'Malaria', 'Diarrhea', 'TB',
       'Nutrition_Status'])
y = cleaned_data[['Stunting',
       'Underweight', 'Overweight', 'Anemia', 'Malaria', 'Diarrhea', 'TB',
       'Nutrition_Status']]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

cleaned_data.to_csv("Cleaned Data.csv" ,index=False)
x_test.to_csv("x_test.csv",index= False)
x_train.to_csv("x_train.csv",index= False)
y_test.to_csv("y_test.csv",index= False)
y_train.to_csv("y_train.csv",index= False)

# print(cleaned_data.columns)
# print("X_train columns:", pd.read_csv('x_train.csv').columns.tolist())
# print("y_train columns:", pd.read_csv('y_train.csv').columns.tolist())