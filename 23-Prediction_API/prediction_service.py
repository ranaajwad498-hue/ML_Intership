import joblib



class predictionservices():


    def load_model():
        try:
            model = joblib.dump("ml_models/Random_Forest_Classifier.joblib")
            print("Model is Loaded Successfuly")
        except FileNotFoundError as e:
            print("Failed to load Model")

    def prepare_input():
        

        


    