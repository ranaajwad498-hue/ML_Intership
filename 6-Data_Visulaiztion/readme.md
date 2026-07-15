# Child Nutrition Data Visualization

An Object-Oriented Python application designed to analyze and visualize child health and malnutrition data. This tool processes demographic, physical, and nutritional metrics to generate clear, actionable visual insights.

---

## Dataset Used

The application utilizes a dataset containing health indicators for children:
* **File Name:** `malnutrition_children_ethiopia.csv`
* **Key Fields Extracted:**
    * `Gender`: Categorical data indicating child gender (used for population distribution).
    * `Nutrition_Status`: Categorical indicator representing the risk category of the child.
    * `Age (months)`: Numerical continuous/discrete value representing child age.
    * `Height_cm` & `Weight_kg`: Continuous numerical measurements used to evaluate physical growth patterns.

---

## Class Structure

The codebase is built using **Object-Oriented Programming (OOP)** principles, centered around a single, cohesive class that manages the dataset and generates visualizations.

### The `children` Class

| Method / Attribute | Type | Description |
| :--- | :--- | :--- |
| `df` | Instance Attribute | Holds the Pandas DataFrame containing the child health records. |
| `__init__(self, df)` | Constructor | Initializes the class instance with the loaded DataFrame. |
| `display_columns(self)` | Instance Method | References the DataFrame columns (Note: contains a minor typo `colums` in source code). |
| `create_gender_chart(self)` | Instance Method | Generates and saves a bar chart showing the frequency of children by gender. |
| `create_risk_category_chart(self)` | Instance Method | Generates and saves a pie chart representing nutrition status distribution. |
| `create_age_distribution_chart(self)` | Instance Method | Generates and saves a histogram showing the frequency distribution of ages. |
| `create_height_weight_chart(self)` | Instance Method | Generates and saves a scatter plot analyzing physical development (Height vs Weight). |
| `create_all_charts(self)` | Orchestrator | Execution pipeline that prints status updates and runs the main visualization suite. |

---

## Charts Created & Selection Rationale

The program automatically saves all generated visualizations to a `charts/` directory. Each chart type was carefully chosen to best represent the underlying data structure:

### 1. Gender Distribution Bar Chart
* **Filename:** `charts/gender_chart.png`
* **Why Selected:** A **Bar Chart** is the gold standard for comparing the frequency or count of distinct, nominal categories (Male vs. Female). It allows the viewer to instantly assess if there is a gender imbalance in the dataset.

### 2. Nutrition Status Pie Chart
* **Filename:** `charts/risk_category_distribution.png`
* **Why Selected:** A **Pie Chart** is ideal for displaying part-to-whole relationships when there are relatively few categories. It allows immediate visualization of the percentage distribution of different "Nutrition Status" risk groups across the entire sample size.

### 3. Age Distribution Histogram
* **Filename:** `charts/age_distribution.png`
* **Why Selected:** A **Histogram** is the most effective tool for visualizing the shape, spread, and skewness of continuous numerical data (Age in months). It groups age values into bins to highlight which age brackets are most heavily represented.

### 4. Height vs. Weight Scatter Plot (Bonus Task)
* **Filename:** `charts/Height_Weight.png`
* **Why Selected:** A **Scatter Plot** is specifically designed to show relationships and correlations between two continuous numerical variables. Plotting Height against Weight makes it easy to spot trends, clusters, or outliers in physical development.

---

## Technical Reference

The project leverages the power of two core scientific Python libraries: **Pandas** and **Matplotlib**.

### Pandas Functions Used
* `pd.read_csv()`: Used to load the raw CSV dataset into a structured DataFrame object.
* `value_counts()`: Counts the unique occurrences in categorical columns (`Gender` and `Nutrition_Status`) to prepare frequency arrays for plotting.

### Matplotlib (`matplotlib.pyplot`) Functions Used
* `plt.bar()`: Renders the categorical bar chart.
* `plt.pie()`: Renders the circular pie chart, using `autopct="%1.0f%%"` to display percentage values.
* `plt.hist()`: Groups continuous data and renders the histogram distribution.
* `plt.scatter()`: Renders individual data points on a 2D Cartesian plane.
* `plt.grid(True)`: Toggles background grids on the bar chart and histogram to make reading values easier.
* `plt.title()`, `plt.xlabel()`, `plt.ylabel()`: Standard labeling functions to give context to charts.
* `plt.savefig()`: Exports and saves the generated figures to disk as `.png` files.
* `plt.show()`: Displays the active figure on-screen during execution.