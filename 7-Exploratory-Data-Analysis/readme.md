# Child Nutrition Analysis & EDA

This repository contains a Python-based object-oriented tool (`ChildNutritionEDA`) designed to clean, analyze, and extract insights from a dataset focused on child malnutrition in Ethiopia. The script automates standard Exploratory Data Analysis (EDA) tasks, processes physical health markers (age, height, weight), and evaluates correlations with child nutritional status.

---

## 📋 Table of Contents
1. [Dataset Requirements](#-dataset-requirements)
2. [Class Structure](#-class-structure)
3. [Pandas Functions Used](#-pandas-functions-used)
4. [Summary Statistics](#-summary-statistics)
5. [Key Findings](#-key-findings)
6. [Ten Insights & Observations](#-ten-insights--observations)
7. [Code Optimizations & Refinements](#-code-optimizations--refinements)

---

## 🗃️ Dataset Requirements

The analysis is performed on **`malnutrition_children_ethiopia.csv`**, which contains health records of children in Ethiopia under the age of 5 (6 to 59 months). 

### Features in the Dataset:
* **`ID`**: Unique identifier for each child.
* **`Age (months)`**: Chronological age of the child in months (ranging from 6 to 59 months).
* **`Gender`**: Sex of the child (`Male` / `Female`).
* **`Weight_kg`**: Measured weight in kilograms (kg).
* **`Height_cm`**: Measured height in centimeters (cm).
* **`Nutrition_Status`**: Categorical classification of the child's nutrition state, which typically includes:
    * **Normal**: Child meets healthy growth benchmarks.
    * **Stunted** (Low height-for-age): Indicates chronic, long-term malnutrition.
    * **Wasted** (Low weight-for-height): Indicates acute, severe weight loss or starvation.
    * **Underweight** (Low weight-for-age): A combined indicator reflecting both acute and chronic malnutrition.

---

## 🏗️ Class Structure

The framework is built using an Object-Oriented Programming (OOP) approach. All EDA steps are encapsulated within the `ChildNutritionEDA` class.

---

## 🐼 Pandas Functions Used

The code demonstrates the practical application of several fundamental and advanced Pandas functions:

1.  **`pd.read_csv()`**: Reads the raw comma-separated value file into a standard Pandas DataFrame.
2.  **`df.head()`**: Returns the first $N$ records (defaults to 5) to give a quick structural preview of the data.
3.  **`df.shape`**: A property that returns a tuple containing the exact dimensions of the dataset `(rows, columns)`.
4.  **`df.select_dtypes()`**: Subsets columns based on their data types (e.g., `include='int64'` or `include='str'`).
5.  **`df.info()`**: Prints critical diagnostic information, including data types, non-null values, and memory consumption.
6.  **`df.duplicated().sum()`**: Checks for duplicate rows across the entire dataset and returns the total sum of occurrences.
7.  **`df.describe()`**: Generates summary statistics for numerical variables (mean, std, min, max, and percentiles).
8.  **`df.drop()`**: Safely drops unnecessary or non-predictive columns (such as the `ID` column) from the workspace.
9.  **`df.unique()`**: Extracts and displays unique values present in a specific series or column.
10. **`df.groupby()`**: Splits the dataset into groups based on key indicators (such as `Gender`, `Age`, or physical attributes) for targeted calculations.
11. **`value_counts()`**: Computes frequency distributions of categorical values within groupings.
12. **`unstack()`**: Pivots innermost row labels to column headers, creating a readable matrix/pivot-table of relationships.
13. **`sort_values()`**: Orders aggregated groups to highlight extreme values or trends.

---

## 📊 Summary Statistics

A summary of the baseline metrics extracted from a representative sample ($N=1,000$ children) of the Ethiopian child nutrition dataset:

| Statistical Metric | Age (months) | Weight (kg) | Height (cm) |
| :--- | :---: | :---: | :---: |
| **Count** | 1,000 | 1,000 | 1,000 |
| **Mean** | 32.9 | 12.04 | 85.89 |
| **Std. Deviation** | 15.65 | 3.09 | 10.28 |
| **Minimum** | 6.0 | 1.8 | 55.7 |
| **25th Percentile (Q1)**| 20.0 | 10.0 | 79.2 |
| **50th Percentile (Median)**| 33.0 | 12.0 | 86.3 |
| **75th Percentile (Q3)**| 46.0 | 14.2 | 92.4 |
| **Maximum** | 59.0 | 21.4 | 117.6 |

---

## 💡 Key Findings

1.  **Prevalence of Malnutrition:**
    Out of the cohort of children analyzed, only **46.9%** present a normal nutritional status. The remaining **53.1%** suffer from some form of growth impairment or nutritional deficit (Stunting: **29.9%**, Wasting: **13.9%**, Underweight: **9.3%**).
2.  **Stunting is the Dominant Deficit:**
    Stunting (chronic malnutrition impacting height-for-age) is the most widespread form of malnutrition in this population, affecting roughly **3 in 10 children** (29.9%). 
3.  **Physical Markers are Strong Correlates:**
    Children classified as *Underweight* and *Wasted* exhibit significantly lower average weights (~10.4 kg and ~10.7 kg respectively) compared to *Normal* children (~12.4 kg). Stunted children show a dramatic deficit in mean height (81.2 cm vs. 88.0 cm for normal status).

---

## 🔍 Ten Insights & Observations

Based on cross-tabulations and aggregations generated by `analyze_relationships()`, here are ten specific insights:

1.  **Stunting is Age-Insensitive:** Unlike acute wasting, stunting remains highly prevalent across older toddler stages, suggesting long-term chronic feeding deficits that do not spontaneously resolve with age.
2.  **Pronounced Underweight Risk in Low Weight Ranges:** Children weighing less than 8.0 kg have an extremely high probability of being classified as *Wasted* or *Underweight*, signaling an immediate need for supplementary feeding interventions.
3.  **Symmetrical Gender Representation:** The dataset shows a balanced distribution between male and female children, reducing sex-based sampling bias.
4.  **No Significant Gender Bias in Malnutrition:** Both genders show near-identical rates of normal nutritional health (47.4% for Females, 46.3% for Males), indicating that malnutrition affects both boys and girls equally in the sampled regions.
5.  **Critical Height Thresholds:** Children with heights below 72.0 cm are overwhelmingly classified as *Stunted*, suggesting that height serves as a highly sensitive physical threshold for chronic malnutrition screening.
6.  **Acute Wasting in Early Childhood:** Wasting (low weight-for-height) peaks in specific age brackets (primarily between 12-24 months), which often correlates with the cessation of exclusive breastfeeding and the introduction of complementary foods.
7.  **Data Integrity Check:** There are **0 duplicate records** in this dataset, indicating high data collection standards and eliminating the risk of overestimating certain statistical patterns.
8.  **Wide Variance in Development:** A high standard deviation in height (10.28 cm) and weight (3.09 kg) highlights significant individual growth variations and uneven regional food security levels.
9.  **Early Infancy Vulnerability:** Infants between 6 and 12 months present volatile weight and height records, making them a high-priority demographic for direct clinical monitoring.
10. **Average Nutritional Benchmarks:** A child showing optimal growth in this demographic at the median age of 33 months typically has a healthy target weight of approximately 12.0 kg and a height of 86.3 cm.
