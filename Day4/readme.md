# Child Nutrition Data Analysis Program

A Python-based data analysis tool built using Object-Oriented Programming (OOP) principles and the **Pandas** library. This application loads child health data from a CSV file, stores it efficiently in a DataFrame, and analyzes metrics based on age thresholds (specifically identifying children under 24 months).

## 🚀 Features
* **OOP Architecture:** Built entirely inside a clean, reusable `ChildNutritionAnalyzer` class.
* **Pandas Integration:** Utilizes Pandas DataFrames for quick data manipulation and filtering.
* **Data Filtering:** Isolates and extracts records for toddlers under 2 years of age (24 months).
* **Summary Reporting:** Generates quick analytical insights directly to the terminal.

---

## 🛠️ Project Structure
```text
child-nutrition-pandas-oop/
│
├── children.csv                 # Data source containing 20+ child records
├── ChildNutritionAnalyzer.py    # Main OOP Python script 
└── README.md                    # Project documentation
