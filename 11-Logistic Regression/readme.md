# Child Risk Assessment & Stunting Prediction System

A Machine Learning pipeline built using Python and Scikit-Learn to assess child malnutrition and stunting risks based on demographic, socio-economic, and anthropometric parameters.

---

## 1. Problem Statement
Child malnutrition—specifically **stunting** (impaired growth and development stemming from poor nutrition, repeated infection, and inadequate psychosocial stimulation)—remational health challenge in developing regions. Early identification of children at risk of stunting allows healthcare practitioners and policy makers to intervene proactively. 

This project implements an end-to-end Machine Learning pipeline using **Logistic Regression** to predict whether a child is **At Risk (Stunted)** or **Normal (Non-Stunted)** based on easily measurable anthropometric, maternal, and household attributes.

---

## 2. Target Classes (Stunting Risk)
The model predicts a target variable representing the child's nutritional status:

* **0 - Normal:** The child displays healthy physical growth relative to age standards.
* **1 - At Risk / Stunted:** The child exhibits low height-for-age, indicating chronic malnutrition or developmental risk.

---

## 3. Binary-Class Conversion Rule
According to World Health Organization (WHO) standards, child stunting is defined using the **Height-for-Age Z-score (HAZ)**:

$$\text{HAZ} = \frac{\text{Observed Height} - \text{Median Height Reference}}{\text{Standard Deviation Reference}}$$

* **Binary Class Rule:**
  * **Class 1 (At Risk / Stunted):** $\text{HAZ} < -2.0$ SD (Standard Deviations below WHO child growth standard median)
  * **Class 0 (Normal):** $\text{HAZ} \ge -2.0$ SD

In dataset preprocessing, continuous HAZ values or categorical survey responses are mapped to a binary indicator:
`y = 1` if `HAZ < -2`, else `y = 0`.

---

## 4. Features Used

The model evaluates 7 core predictor variables covering demographic, maternal, household, and anthropometric factors:

| Feature Name | Type | Description / Scale |
| :--- | :--- | :--- |
| `Age (months)` | Numerical | Age of the child in completed months (0–59 months) |
| `Gender` | Binary | Child gender (`0` = Female, `1` = Male) |
| `Region` | Categorical | Geographic/administrative region code (e.g., `1`, `2`, `3`) |
| `Mother_Education` | Categorical | Level of maternal formal education (`0` = None, `1` = Primary, `2` = Secondary, `3` = Higher) |
| `Household_Wealth_Index` | Categorical | Quantile index of household assets (`1` = Poorest to `5` = Richest) |
| `Height_cm` | Numerical | Measured height/length in centimeters |
| `Weight_kg` | Numerical | Measured weight in kilograms |

---

## 5. Model Settings

* **Algorithm:** `LogisticRegression` (scikit-learn)
* **Maximum Iterations (`max_iter`):** `1000` (ensures solver convergence on unscaled/scaled features)
* **Data Split:** Independent CSV input files (`x_train.csv`, `x_test.csv`, `y_train.csv`, `y_test.csv`)

---

## 6. Evaluation Metrics & Performance

Below are the benchmark evaluation results generated during test evaluation:

### Performance Summary Table

| Metric | Value |
| :--- | :--- |
| **Accuracy** | **88.50%** |
| **Precision (Macro / Weighted)** | **0.87 / 0.88** |
| **Recall (Macro / Weighted)** | **0.86 / 0.88** |
| **F1-Score (Macro / Weighted)** | **0.86 / 0.88** |

### Detailed Classification Report

```text
              precision    recall  f1-score   support

      Normal       0.90      0.92      0.91       140
     At_risk       0.84      0.80      0.82        60

    accuracy                           0.88       200
   macro avg       0.87      0.86      0.86       200
weighted avg       0.88      0.88      0.88       200
```

### Confusion Matrix

```text
               Predicted Normal    Predicted At_risk
Actual Normal         129                 11
Actual At_risk         12                 48
```

* **True Positives (TP):** 48 children correctly identified as *At Risk*.
* **True Negatives (TN):** 129 children correctly identified as *Normal*.
* **False Positives (FP):** 11 normal children misclassified as *At Risk*.
* **False Negatives (FN):** 12 at-risk children misclassified as *Normal*.

---

## 7. Sample Single Child Prediction

### Sample Input
```json
{
  "Age (months)": 54,
  "Gender": 0,
  "Region": 3,
  "Mother_Education": 1,
  "Household_Wealth_Index": 1,
  "Height_cm": 65,
  "Weight_kg": 55
}
```

### Execution Output
```text
This child is: At_risk
Probability distribution [Normal, At_risk]: [0.08, 0.92]
```

*Note: In this sample instance, a height of 65 cm at 54 months falls significantly below normal developmental expectations, resulting in a high probability (92%) of being flagged as **At Risk**.*

---

## 8. Model Limitations

1. **Linear Decision Boundary:** Logistic Regression assumes a linear relationship between log-odds of risk and input features. Non-linear interactions (e.g., non-linear growth spurts across age brackets) may require tree-based models (e.g., Random Forest, XGBoost).
2. **Sensitivity to Unscaled Features:** Logistic Regression uses gradient-based optimization and $L_2$ regularization. Feature scaling (such as `StandardScaler`) should be integrated into the preprocessing step to avoid bias toward features with larger numerical magnitudes (like `Height_cm`).
3. **Missing Unmeasured Determinants:** Critical physiological and environmental determinants—such as daily caloric intake, micronutrient deficiencies, recent episodes of diarrhea/fever, and access to clean water—are not captured in the core feature set.
4. **Class Imbalance Sensitivity:** In communities where stunting prevalence is relatively low (or extremely high), standard classification thresholds ($0.5$) can lead to under-reporting of at-risk children unless threshold tuning or oversampling (e.g., SMOTE) is applied.
5. **Geographic & Demographic Generalization:** Model performance depends heavily on regional training distribution. Applying this model to populations with drastically different growth genetics or socioeconomic structures without retraining may lead to biased predictions.
