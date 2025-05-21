# 🔥 Fire Incident Analysis in San Francisco

This project builds a Python data pipeline to analyze fire incidents in the city of San Francisco.  
It includes data downloading, cleaning, local storage using SQLite, visualization of incident frequency by year, and automatic creation of a dimensional data warehouse.

---

## 📁 Project Structure
```
.
├── pipeline.py            # Main script with the full pipeline logic
├── Challenge.ipynb        # Jupyter Notebook for interactive exploration
├── fire_incidents.db      # SQLite database with cleaned and dimensional data (auto-generated)
└── README.md              # Project documentation
```

---

## ⚙️ Pipeline Overview

The pipeline performs the following automated tasks:

- Download the dataset from a public URL.
- Clean the data:
  - Standardize column names to snake_case
  - Remove duplicates and null values
- Store the cleaned data in a local SQLite database
- Create a dimensional Data Warehouse
- Visualize the number of fire incidents per year in a bar chart

---

## 🔗 Data Source

- Dataset: Fire Incidents - San Francisco  
- Format: CSV  
- [🔗 Download Dataset](https://data.sfgov.org/api/views/wr8u-xric/rows.csv?accessType=DOWNLOAD)

---

## 🧰 Requirements

Ensure you have Python 3.7 or higher installed.

Install the required libraries with:

```bash
pip install pandas matplotlib
```

---

## ▶️ How to Run the Pipeline

Simply run the script from the terminal:

```bash
python pipeline.py
```

This will:

- Download the fire incidents dataset
- Clean and preprocess the data
- Store the data into a local SQLite database named `fire_incidents.db`
- Build a full dimensional model
- Display a bar chart with the number of fire incidents per year

---

## 📊 Visualization Output

The generated plot shows:

- **X-axis**: Year of the incident (from `incident_date`)
- **Y-axis**: Number of fire incidents
- **Library**: matplotlib

---

## 🧪 Jupyter Notebook: `Challenge.ipynb`

This notebook mirrors the `pipeline.py` script and is ideal for:

- Step-by-step execution
- Debugging
- Exploring and transforming the data manually

---

## 📐 Data Model Design (Facts and Dimensions)

Starting from the cleaned `fire_incidents` dataset, the pipeline builds a dimensional data model automatically, designed for Business Intelligence and OLAP-style reporting.

### 🧱 Fact Table:
- `fact_fire_incidents`: Each row represents a fire incident.
  - **Measures**: number of fatalities, estimated property loss.
  - **Foreign Keys**: `date_id`, `location_id`, `type_id`

### 📊 Dimension Tables:
- `dim_date`: year, month, day, weekday
- `dim_location`: neighborhood, battalion, station area, zip code
- `dim_incident_type`: incident type description, call type, alarm datetime, priority level

These tables enable fast and flexible aggregation queries suitable for use in BI tools like Power BI or Superset.

---

## 💡 Potential Extensions

Here are a few ideas to take the project further:

- Filter incidents by neighborhood or incident type
- Build interactive dashboards using Plotly or Dash
- Export visualizations and datasets to PDF or Excel
- Upload the data to a cloud data warehouse like BigQuery
- Implement scheduled runs using Airflow or Prefect
- Model fact/dimension schema and load it into a BI system (e.g. Power BI, Superset)

---

## 📌 Author

This project was developed as part of a Python-based data engineering and visualization practice using real-world open data.
