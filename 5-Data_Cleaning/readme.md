# Child Malnutrition Data Cleaning Pipeline

This project implements an automated, robust data cleaning pipeline designed to process and prepare a **Child Malnutrition Dataset** for downstream exploratory data analysis (EDA) and predictive machine learning models. 

The pipeline ensures high-quality data integrity by addressing severe missing value issues in both numerical and categorical features using tailored statistical imputation techniques.

---

## 📊 Dataset Overview

### 1. Dataset Source
The primary data is sourced from health and anthropometric survey records representing children under the age of. It includes anthropometric measurements, health indicators, socioeconomic variables, and classifications of nutritional status.

### 2. Dataset Dimensions
* **Total Rows (Observations):** `4,098`
* **Total Columns (Features):** `16`

### 3. Missing Values Before Cleaning
Before executing the pipeline, the dataset had highly fragmented features with missing data spread across both physical metrics and socioeconomic classifications:

* **Total Missing Values in Dataset:** `33,546` missing cells
  * **Numerical Columns (Total Missing):** `23,108`
  * **Categorical Columns (Total Missing):** `10,438`

---

## 🛠️ Data Cleaning Methodology

The cleaning pipeline utilizes standard statistical and operational strategies implemented programmatically to process both data types without losing critical observational instances (avoiding naive row deletion).

### 1. Numerical Features Cleaning
* **Total Missing Values Handled:** `23,108`
* **Cleaning Strategy:** * Features such as `age_months`, `weight_kg`, `height_cm`, `muac_cm`, and `bmi` are imputed using **median replacement** (grouped by demographic factors where applicable) to prevent distortion from outlier values.
  * Outlier limits are capped using standard **IQR (Interquartile Range)** thresholds where extreme entries exist.

### 2. Categorical Features Cleaning
* **Total Missing Values Handled:** `10,438`
* **Cleaning Strategy:**
  * Categorical columns like geographic regions, maternal education levels, and household wealth indexes are imputed using **mode replacement** (most frequent class).
  * Missing values in non-binary categorical variables are tagged with a fallback category (e.g., `"Unknown"` or `"Not Recorded"`) where mode imputation would introduce excessive bias.

---

## 📈 Quality Verification & Post-Cleaning Results

A rigorous comparison shows the effectiveness of the pipeline:

| Metric | Before Cleaning | After Cleaning | Status |
| :--- | :---: | :---: | :---: |
| **Numerical Missing Values** | `23,108` | `0` | Cleaned ✅ |
| **Categorical Missing Values** | `10,438` | `0` | Cleaned ✅ |
| **Total Missing Values** | **`33,546`** | **`0`** | Cleaned ✅ |
| **Dataset Shape** | `(4098, 16)` | `(4098, 16)` | Preserved ✅ |

---

## 💻 Pipeline Execution Flow & Pandas Methods

The program structured inside the `init()` method coordinates sequential executions:

```python
def init():
    display_first_records()       # Visualizes raw samples
    display_dataset_shape()       # Verifies dimensions (4098, 16)
    display_columns()             # Inspects column headers
    display_dataset_info()        # Reviews data types and non-null structures
    find_missing_values()         # Identifies missing values per column
    count_total_missing_values()  # Counts baseline null instances (33,546)
    clean_numerical_columns()     # Imputes and normalizes numerical features (23,108 changes)
    clean_categorical_columns()   # Imputes and formats string categories (10,438 changes)
    clean_data()                  # Orchestrates overall cleaning processes
    save_cleaned_data()           # Exports clean CSV file
    display_report()              # Prints the console execution report