# 🚒 San Francisco Fire Incidents Analysis

This repository contains the analysis of the public dataset of fire incidents in San Francisco, following all the required steps from the challenge **Case Study - Data of Fire v1.1**.

## 📊 Steps Completed

1. **Download and exploration** of the official dataset.
2. **Cleaning**: removed duplicates and rows with missing values.
3. **SQLite Database**: loaded the dataset into an SQLite database to allow SQL queries.
4. **Exploratory Data Analysis**: visualized the temporal distribution and other key insights.
5. **Data Warehouse Modeling**: built a simple star schema using SQLite.
6. **Notebook Documentation**: the notebook contains all steps and visualizations.

## 🏗️ Data Warehouse Model

A basic star schema was built using SQLite, including:

- `dim_date`: calendar date with year, month, day, and weekday.
- `dim_district`: neighborhoods in San Francisco.
- `dim_battalion`: fire department battalions.
- `fact_fire_incidents`: fact table storing the number of alarms, linked to date, district, and battalion.

The resulting file `fire_dw.db` is included in this repository.

## 📁 Files Included

- `Challenge.ipynb` — Google Colab/Jupyter Notebook with complete analysis.
- `fire_incidents.db` — SQLite database with cleaned incident data.
- `fire_dw.db` — SQLite database with dimensional model (Data Warehouse).
- `README.md` — Project documentation.

## ▶️ How to Run

1. Clone this repository or download it as ZIP.
2. Open the notebook `Challenge.ipynb` using Google Colab or Jupyter Notebook.
3. Run all cells in order to replicate the analysis.

## 🔗 Source Dataset

- [San Francisco Fire Incidents – DataSF](https://data.sfgov.org/Public-Safety/Fire-Incidents/wr8u-xric)

---

> ✅ This project fulfills all requirements from the case study: data cleaning, database usage, basic SQL queries, visualizations, and a dimensional warehouse model.

