import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler 
from sklearn.model_selection import train_test_split
class ChildDataPreprocessor:
    def __init__(self, file_path="child_malnutrition_features.csv"):
        self.file_path=file_path
        

    def load_data(self):
        self.df = pd.read_csv(self.file_path)
        print("Dataset Shape:", self.df.shape)
        print("First 5 Rows:")
        print(self.df.head())
        print("Columns:\n",self.df.columns.tolist())
        if not self.df.empty:
            print(f"Success! Loaded {len(self.df)} rows and {len(self.df.columns)} columns.")
        else:
            print("Warning! The loaded DataFrame is empty.")
        return self.df

    def inspect_data(self):
        print("-"*50)
        print(f"Total Number of Rows:{len(self.df)} \n Total number of Columns: {len(self.df.columns)}")
        print("-"*50)
        print("Data Type of Each Column \n",self.df.dtypes)
        print("-"*50)
        print("Missing Values in Each Columns:\n", self.df.isnull().sum())
        print("-"*50)
        print("Duplicate Records:\n", self.df.duplicated().sum())
        print("-"*50)
        self.numeric_columns = self.df.select_dtypes(include='int64').columns.tolist()
        print("Numeric column names:",self.numeric_columns)
        self.categorical_columns = self.df.select_dtypes(include="str").columns.tolist()
        print("Categorical columns names:",self.categorical_columns)

    def clean_data(self):
        self.df=self.df.drop_duplicates()
        self.df= self.df.drop(columns=['ID' ,'Anemia', 'Malaria', 'Diarrhea', 'TB'])
        numeric_columns=self.df.select_dtypes(include="int64")
        for col in numeric_columns:
            self.df[col] = self.df[col].fillna(self.df[col].mean())
        categorical_columns= self.df.select_dtypes(include="str")
        for col in categorical_columns:
            self.df[col] = self.df[col].fillna(self.df[col].mode()[0])
            return self.df.shape

    def select_target(self):
        self.target = "Nutrition_Status"

    def split_features_target(self):
        self.select_target()
        X = self.df.drop(columns=[self.target])
        Y = self.df[self.target]
        self.X = X
        self.Y = Y
        print("Trainig Data Shape (X):", X.shape)
        print("Testing Data Shape (Y):", Y.shape)
        return len(self.X.columns)

    def encode_categorical_features(self):
        self.X = pd.get_dummies(self.X)
        if self.Y.dtype == "str":
            self.label_encoder = LabelEncoder()
            self.Y = self.label_encoder.fit_transform(self.Y)
        return len(self.X.columns)
         
    def scale_numerical_features(self):
        numeric_columns=self.df.select_dtypes(include="int64")
        minmax= MinMaxScaler()
        self.X = minmax.fit_transform(self.X[numeric_columns])

    def split_training_testing_data(self):
        self.X_train, self.X_test, self.Y_train, self.Y_test =train_test_split (self.X, self.Y, test_size=0.2, random_state= 42, stratify=self.Y)

    def display_report(self):
        print("Orignal Shape of our DataSet:",self.df.shape)
        print("Cleaned DataSet Shape:", self.clean_data())
        print("Number of Input Feature:",self.split_features_target() )
        print("Number of Encoded Feature:", self.encode_categorical_features())
        self.select_target()
        print("Target Class:",self.target)
       


child = ChildDataPreprocessor()
df = child.load_data()
child.display_report()
# child.split_features_target()



