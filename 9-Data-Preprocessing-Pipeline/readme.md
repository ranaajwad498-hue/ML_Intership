# Child Malnutrition Data Preprocessing Pipeline

This document explains the data preprocessing pipeline implemented in
`child_data_preprocessor.py`, which prepares the child malnutrition dataset
for machine learning model training.

## Dataset Used

The pipeline loads `child_malnutrition_features.csv`, a tabular dataset
containing child health and demographic features (e.g. anthropometric
measurements, household/environmental factors, and disease indicators)
used to assess nutritional status.

## Target Column Selected

The target (label) column is **`Nutrition_Status`**, which represents the
nutritional classification of the child (e.g. normal, malnourished). This
is the variable the model is trained to predict, and it is separated from
the feature set before training.

## Missing-Value Strategy

Missing values are handled differently depending on column type:

- **Numeric columns (`int64`)** — missing values are filled with the
  **column mean**.
- **Categorical columns (`object`/string)** — missing values are filled
  with the **column mode** (most frequent value).

This preserves the overall distribution of each column instead of dropping
rows, which would reduce the size of an already limited dataset.

## Encoding Method

- **Features (X)**: categorical columns are converted using
  **one-hot encoding** via `pandas.get_dummies()`, turning each category
  into its own binary column.
- **Target (Y)**: if the target column is categorical (`object` dtype), it
  is converted to numeric labels using **`LabelEncoder`** from
  scikit-learn.

## Scaling Method

Numeric feature columns are scaled using **`MinMaxScaler`**, which rescales
values to a **[0, 1] range**. The scaler is:

- **Fit only on the training set** (`fit_transform` on `X_train`)
- **Applied (not re-fit) on the test set** (`transform` on `X_test`)

## Training and Testing Split

The dataset is split using **`train_test_split`** with:

- **Test size:** 20% (`test_size=0.2`)
- **Train size:** 80%
- **`random_state=42`** for reproducibility
- **`stratify=Y`** to preserve the original class distribution of
  `Nutrition_Status` in both the train and test sets

## Final Number of Features

The final feature count is determined **after** one-hot encoding is
applied (since encoding expands categorical columns into multiple binary
columns). The exact number depends on the cardinality of the categorical
variables in the dataset and is printed at runtime as:

```
Number of Encoded Feature: <count>
```

## Scikit-learn Functions Used

| Function | Purpose |
|---|---|
| `LabelEncoder` | Encodes the categorical target column into numeric labels |
| `MinMaxScaler` | Scales numeric features to a [0, 1] range |
| `train_test_split` | Splits data into training and testing sets with stratification |

(`pandas.get_dummies()` is used for feature encoding but is a pandas
function rather than scikit-learn.)

## How Data Leakage Was Avoided

Several safeguards are built into the pipeline to prevent information from
the test set influencing training:

1. **Split before scaling** — the train/test split happens *before*
   `MinMaxScaler` is applied, so scaling statistics (min/max) are computed
   only from training data.
2. **Fit only on training data** — `MinMaxScaler.fit_transform()` is called
   on `X_train` only; `X_test` is transformed using the *already-fitted*
   scaler (`transform()`, not `fit_transform()`), so test data never
   influences the scaling parameters.
3. **Stratified split** — stratifying by the target ensures the class
   distribution is representative in both sets, avoiding evaluation bias
   from an imbalanced split.
4. **Duplicate removal before splitting** — duplicate rows are dropped
   during cleaning, reducing the risk of identical records appearing in
   both the training and test sets.