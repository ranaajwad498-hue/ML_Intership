# Machine Learning Model Persistence & Deployment Guide

This repository demonstrates how to train, serialize (save), deserialize (load), evaluate, and deploy a **Random Forest Classifier** pipeline using Python and `joblib`.

---

## 1. Model Used
This project utilizes the **Random Forest Classifier** (`sklearn.ensemble.RandomForestClassifier`). 

Random Forest is an ensemble learning method that constructs a multitude of decision trees during training and outputs the class that is the mode of the classes of the individual trees. It was selected for its high accuracy, resistance to overfitting, and ability to handle complex feature interactions.

---

## 2. Why Models Are Saved (Model Serialization)
Training machine learning models can be computationally expensive and time-consuming. Saving (serializing) a model provides several key benefits:

* **Eliminates Retraining:** Once trained, the model weights and structure are written to disk. You do not need to retrain the model every time you run an application.
* **Separates Training from Inference:** Training scripts can run on dedicated high-performance hardware, while the saved model artifact is transferred to lightweight application servers for predictions.
* **Ensures Reproducibility:** Allows freezing specific versions of a model for auditability, testing, and rollback purposes.
* **Decreases Latency:** Serving predictions from a loaded file takes milliseconds compared to minutes or hours spent fitting a dataset.

---

## 3. Difference Between Joblib and Pickle

| Feature | `joblib` | `pickle` |
| :--- | :--- | :--- |
| **Primary Focus** | Optimized for Python objects containing large NumPy arrays. | General Python object serialization. |
| **Performance** | Faster read/write speeds for large numerical matrices and tree models. | Slower when handling large array structures. |
| **Disk Memory Efficiency** | Highly efficient memory mapping for Scikit-Learn estimators. | Standard byte stream serialization. |
| **File Extension** | `.joblib` | `.pkl` |
| **Best Used For** | Scikit-Learn models, Random Forests, Preprocessing Pipelines. | Dictionaries, lists, and lightweight custom Python classes. |

---

## 4. Code Implementation

Below is the complete workflow covering model training, saving, loading, testing before/after prediction consistency, and evaluating performance post-reload.

```python
import joblib

# --- 4. HOW THE MODEL WAS SAVED ---
joblib.dump(model, MODEL_PATH)
print(f"Model successfully saved to: {MODEL_PATH}")

# --- 5. HOW THE MODEL WAS LOADED ---
loaded_model = joblib.load(MODEL_PATH)
print("Model successfully loaded into memory.")

# --- PREDICTION AFTER LOADING ---
pred_after_load = loaded_model.predict(sample_data)
print(f"Predictions after loading:  {pred_after_load}")

## 5. Evaluation Results After Reloading

After loading `random_forest_model.joblib` back into RAM, the model was evaluated on the test set (`X_test`, `y_test`). Based on the evaluated confusion matrix:

```text
Confusion Matrix:
[[209 198]
 [196 217]]

--- Evaluation Results (Loaded Model) ---
Accuracy: 0.5195

Classification Report:

              precision    recall  f1-score   support

           0       0.52      0.51      0.51       407
           1       0.52      0.53      0.52       413

    accuracy                           0.52       820
   macro avg       0.52      0.52      0.52       820
weighted avg       0.52      0.52      0.52       820

6. Using the Saved Model in Production (API & Mobile Apps)
Once the model is saved to .joblib, it can be integrated into production environments without needing the training code or training data.

Scenario A: Deployment via Python REST API (FastAPI)
In web backend applications, the model is loaded once when the API server starts up. Incoming HTTP POST requests feed raw data to an endpoint that returns real-time predictions.

Scenario B: Mobile Application Integration (Flutter / Android / iOS)
Client-Server Architecture ():
The mobile app (e.g., Flutter, Swift, React Native) collects user input and sends a JSON payload via an HTTP POST request to the deployed FastAPI endpoint.
The server executes joblib.load() inference and returns the result back to the mobile screen.
