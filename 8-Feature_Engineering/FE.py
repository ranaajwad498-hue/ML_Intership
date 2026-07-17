import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler , MinMaxScaler

df= pd.read_csv("malnutrition_children_ethiopia.csv")
print(df.head())
# Feature Engineering
# df_encoded = df.copy()
# label_encoder = LabelEncoder()
# print(df.head())
# label encodeing
# df_encoded["gender"] = label_encoder.fit_transform(df_encoded["Gender"]) # only use fit_transform in trainig data and transform in testing data
# print(df_encoded.head())

# label encoding (ordinal form)
# eduaction = {"No education": 0, "Higher":1, "Secondary":2}
# df_encoded["Edu_Rank"] = df_encoded["Mother_Education"].map(eduaction)
# print(df_encoded.head())


# one hot encodeing
# df_encoded = pd.get_dummies(df_encoded, columns=["Region"], prefix="Region")
# print(df_encoded.head())

# Frequency Encoding
# nutrition = df["Nutrition_Status"].value_counts().to_dict()
# df_encoded["nutrition_status"] = df_encoded["Nutrition_Status"].map(nutrition)
# print(df_encoded.head())

# Targeting Encoding
# education = df_encoded.groupby("Mother_Education")["Stunting"].mean().to_dict()
# df_encoded["edu"] = df_encoded["Mother_Education"].map(education)
# print(df_encoded.head())

# Frequency Scaling
# df_scaled = df.copy()

#   Standerdization
# standard_scaler = StandardScaler()
# df_scaled["Standard_height_cm"] = standard_scaler.fit_transform(df_scaled[["Height_cm"]]) # Note: double brackets

# #   Noramlization
# minmax_scaler = MinMaxScaler()
# df_scaled["MinMax_Height_cm"] = minmax_scaler.fit_transform(df_scaled[["Height_cm"]]) # Note: double brackets
# print(df_scaled[["Height_cm", "Standard_height_cm", "MinMax_Height_cm"]].head())



