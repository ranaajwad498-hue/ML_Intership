# Child Stunting Risk Prediction: Decision Tree vs. Random Forest

## 1. Problem Statement
Child stunting (impaired growth and development due to poor nutrition and repeated infections) is a critical public health issue. The objective of this project is to build and evaluate machine learning models capable of predicting whether a child is **Stunted** or **Not Stunted** based on anthropometric measurements and socioeconomic factors. 

Accurate prediction allows healthcare providers to implement early interventions for at-risk children.

---

## 2. Dataset Used
The dataset contains child-level demographic, anthropometric, and household data split into training and testing sets:

* **Numeric Features:** `Age (months)`, `Height_cm`, `Weight_kg`
* **Ordinal Features:** `Mother_Education` (`No education`, `Primary`, `Secondary`, `Higher`), `Household_Wealth_Index` (`Low`, `Middle`, `High`)
* **Nominal Features:** `Gender`
* **Target Label:** Binary classification (`Not Stunted` vs. `Stunted`)

---

## 3. Model Configurations & Settings

### Decision Tree Classifier
* **Preprocessing:** `StandardScaler` (numerical), `OrdinalEncoder` (ordinal), `OneHotEncoder(drop='if_binary')` (nominal)
* **Hyperparameters:**
  * `max_depth`: none
  * `min_samples_split`: 2
  * `min_samples_leaf`: 2
  * `random_state`: 42

### Random Forest Classifier
* **Preprocessing:** Identical preprocessing pipeline via `ColumnTransformer`
* **Hyperparameters:**
  * `n_estimators`: 500
  * `max_depth`: None
  * `min_samples_split`: 2
  * `min_samples_leaf`: 2
  * `random_state`: 42

---

## 4. Evaluation Metrics & Comparison

| Metric | Decision Tree | Random Forest |
| :--- | :---: | :---: |
| **Training Accuracy** | **90.97%** | **99.76%** |
| **Testing Accuracy** | **47.68%** | **52.20%** |
| **Precision** | **47.75%** | **52.52%** |
| **Recall** | **41.16%** | **53.03%** |
| **F1-Score** | **44.21%** | **52.77%** |

---


### 5 Visual Charts
The confusion matrix heatmaps are saved in the project output as:
* `decision_tree_confusion_matrix.png`
* `random_forest_confusion_matrix.png`

---

## 6. Feature Importance
Using `.named_steps['classfier'].feature_importances_`, feature importances reveal how much each variable contributed to reducing node impurity:

1. **Anthropometric Indicators:** `Height_cm` and `Age (months)` were the dominant predictors across both models, as stunting is directly tied to height-for-age z-scores.
2. **Socioeconomic Indicators:** `Household_Wealth_Index` and `Mother_Education` played secondary roles in guiding splits.
3. **Demographics:** `Gender` provided minimal predictive power.

---

## 7. Overfitting & Model Observations

* **Decision Tree:** Shows moderate underfitting/poor generalization. While train accuracy (90.97%) and test accuracy (47.68%) are relatively close, the overall test performance is barely better than random guessing (50%).
* **Random Forest:** Displays **significant overfitting**. The model achieves **~99.76%** accuracy on the training set but drops drastically to **~52.20%** on the test set—a performance gap of over 27 percentage points. 

Both models suffer from predicting the majority/positive class far too aggressively, leading to high False Positive rates.

---

## 8. Best Model Selection & Justification

**Neither model is currently suitable for deployment.** However, if forced to select based on balance:

* **Decision Tree** is slightly preferable for clinical identification if **Recall** is prioritized (41.16% recall vs. 53.03% in Random Forest), ensuring fewer stunted children are missed (fewer False Negatives).
* **Random Forest** provides marginally better overall test accuracy (47..68% vs 52.20%), but its severe underfitting makes it unreliable without hyperparameter re-tuning.

---

## 9. Model Limitations & Future Improvements

1. **Near-Random Performance:** Both models perform near a 50% baseline (coin flip), indicating current features or hyperparameters are insufficient to capture stunting dynamics.
2. **Class Imbalance / Feature Engineering:** The model requires explicit feature engineering (e.g., WHO Height-for-Age Z-scores calculated directly) rather than raw height and age values.

### Recommended Next Steps
* Compute standard WHO Growth Standard Z-scores ($HAZ$ / $WAZ$).
* Apply class balancing techniques (e.g., `class_weight='balanced'` or SMOTE).
* Perform hyperparameter search (e.g., `GridSearchCV`) to prune trees and prevent Random Forest overfitting.
* Experiment with non-tree algorithms like Logistic Regression or Support Vector Machines (SVM).
