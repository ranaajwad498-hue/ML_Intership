# Child Malnutrition Analysis & Feature Engineering

An Object-Oriented Python Framework for Cleaning, Feature Engineering, and Risk Assessment of Child Health and Malnutrition Data.

---

## 📋 Project Overview

This project is a Python program that helps track and analyze child malnutrition data. It takes basic information about children—like their age, weight, and height—and automatically calculates important health metrics. By grouping children by age, classifying their nutrition levels, and giving each child an overall health risk score, the program makes it easy to spot who needs urgent medical help.
---

## 📊 Dataset Overview

* **Dataset Name:** `malnutrition_children_ethiopia.csv`
* **Target Population:** Infants and young children across region-specific demographic surveys in Ethiopia.
* **Key Input Fields:**
  * `Age (months)`: Age of the child measured in months ($0–60+$ months).
  * `Weight_kg`: Weight of the child in kilograms ($\text{kg}$).
  * `Height_cm`: Height/length of the child in centimeters ($\text{cm}$).
  * `Malnutrition_Status`: Anthropometric clinical classification (`Severe`, `Moderate`, `None`).

---

## ⚙️ Class Methods & Feature Engineering

The pipeline is implemented through the `MalnutritionAnalyzer` class. Below is a detailed technical summary of all methods included in the pipeline:

| Method Name | Purpose & Description |
| :--- | :--- |
| `__init__(filepath)` | Initializes the class instance, loads `malnutrition_children_ethiopia.csv` into a Pandas DataFrame, and verifies data integrity. |
| `display_columns()` | Prints the full list of column names, data types, and non-null value counts to inspect dataset schema. |
| `display_first_records(n=5)` | Displays the first $n$ rows of the DataFrame for rapid validation after transformations. |
| `create_bmi()` | Calculates standard Body Mass Index ($\text{BMI}$) from weight and height measurements. |
| `create_age_group()` | Categorizes continuous age values (in months) into pediatric growth stages using `pd.cut()`. |
| `create_nutrition_status()` | Bins calculated $\text{BMI}$ values into standardized WHO/CDC clinical classification labels. |
| `create_risk_score()` | Constructs a weighted composite Risk Score ($0–100$) combining age, BMI, and malnutrition indicators. |
| `save_dataset(output_path)` | Exports the feature-engineered DataFrame into a structured CSV file for downstream modeling. |
| `display_report()` | Generates summary statistics, value distributions, and categorical counts for engineered features. |

---

## 🧮 Logic & Mathematical Formulas

### 1. Body Mass Index (`create_bmi`)
Height is converted from centimeters to meters before applying the standard exponentiation formula:

$$\text{BMI} = \frac{\text{Weight (kg)}}{\left(\frac{\text{Height (cm)}}{100}\right)^2}$$

### 2. Age Group Segmentation (`create_age_group`)
Continuous age values in months are mapped into discrete WHO pediatric brackets:

$$\text{Age Group} = \begin{cases} \text{Infant} & 0 \le \text{Age} \le 12 \text{ months} \\ \text{Toddler} & 12 < \text{Age} \le 36 \text{ months} \\ \text{Preschool} & 36 < \text{Age} \le 60 \text{ months} \\ \text{School Age / Older} & \text{Age} > 60 \text{ months} \end{cases}$$

### 3. Nutrition Status Classification (`create_nutrition_status`)
Categorizes BMI measurements into standard health status bins:

$$\text{Nutrition Status} = \begin{cases} \text{Underweight} & \text{BMI} < 18.5 \\ \text{Normal} & 18.5 \le \text{BMI} \le 24.9 \\ \text{Overweight} & 25.0 \le \text{BMI} \le 29.9 \\ \text{Obese} & \text{BMI} \ge 30.0 \end{cases}$$

### 4. Composite Risk Score Logic (`create_risk_score`)
The total health risk score ($0–100$) combines weighted sub-scores evaluating pediatric vulnerability, weight deficiency, and existing clinical malnutrition:

$$\text{Risk Score} = \text{Score}_{\text{BMI}} + \text{Score}_{\text{Age}} + \text{Score}_{\text{Malnutrition}}$$

* **BMI Sub-Score (Max 40 Points):**
  * $\text{Underweight / Obese} \rightarrow +40$
  * $\text{Overweight} \rightarrow +20$
  * $\text{Normal} \rightarrow +0$
* **Age Sub-Score (Max 30 Points):**
  * $\text{Infant } (\le 12\text{m}) \rightarrow +30$
  * $\text{Toddler } (12\text{--}36\text{m}) \rightarrow +15$
  * $\text{Preschool / Older} \rightarrow +5$
* **Malnutrition Sub-Score (Max 30 Points):**
  * $\text{Severe} \rightarrow +30$
  * $\text{Moderate} \rightarrow +15$
  * $\text{None} \rightarrow +0$

---

## 🛠️ Core Pandas & NumPy Functions Used

* **`pd.read_csv()`**: Loading raw dataset into DataFrame structures.
* **`pd.cut()`**: Binning continuous numeric variables (`Age`, `BMI`) into custom categorical ranges with predefined boundaries.
* **`np.select()`**: Evaluating multi-condition logical rules efficiently to generate point vectors for composite score calculation.
* **`df.head()` / `df.info()`**: Data auditing, schema verification, and inspection.
* **`df.to_csv()`**: Persisting updated datasets with newly generated feature columns.
* **`df.drop()`**: Cleanly dropping intermediate helper columns after composite scoring.

---

[SUCCESS] Processed dataset saved to 'child_malnutrition_features.csv'.