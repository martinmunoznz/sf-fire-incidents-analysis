
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# ----------------------------
# Global Parameters
# ----------------------------
DATA_URL = "https://data.sfgov.org/api/views/wr8u-xric/rows.csv?accessType=DOWNLOAD"
DB_NAME = "fire_incidents.db"

# ----------------------------
# Pipeline Functions
# ----------------------------

def descargar_dataset(url):
    print("📥 Downloading dataset...")
    try:
        return pd.read_csv(url, low_memory=False)
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return pd.DataFrame()

def limpiar_dataset(df):
    print("🧹 Cleaning dataset...")
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    df = df.drop_duplicates()
    df = df.dropna()
    return df

def guardar_en_sqlite(df, db_name):
    if df.empty:
        print("⚠️ No data to store.")
        return
    print("💾 Saving to SQLite database...")
    try:
        conn = sqlite3.connect(db_name)
        df.to_sql("fire_incidents", conn, if_exists="replace", index=False)
        conn.close()
        print("✅ Data saved successfully.")
    except Exception as e:
        print(f"❌ Error saving to SQLite: {e}")

def visualizar_distribucion_temporal(db_name):
    print("📊 Generating bar chart by year...")
    try:
        conn = sqlite3.connect(db_name)
        incidentes = pd.read_sql("""
            SELECT strftime('%Y', incident_date) AS year, COUNT(*) AS cantidad
            FROM fire_incidents
            GROUP BY year
            ORDER BY year
        """, conn)
        conn.close()

        if incidentes.empty:
            print("⚠️ No data available to plot.")
            return

        plt.figure(figsize=(10,5))
        plt.bar(incidentes["year"], incidentes["cantidad"], color='skyblue')
        plt.xlabel("Year")
        plt.ylabel("Number of Incidents")
        plt.title("Fire Incidents by Year")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("fire_incidents_by_year.png")
        plt.show()
        print("✅ Chart generated.")
    except Exception as e:
        print(f"❌ Error generating chart: {e}")

def crear_datawarehouse(db_name):
    print("🏗️ Creating dimensional model (Data Warehouse)...")
    conn = sqlite3.connect(db_name)
    df = pd.read_sql("SELECT * FROM fire_incidents", conn)

    # Dimensión fecha
    df['incident_date'] = pd.to_datetime(df['incident_date'], errors='coerce')
    df_date = df[['incident_date']].dropna().drop_duplicates().copy()
    df_date['date_id'] = df_date['incident_date'].dt.strftime('%Y%m%d').astype(int)
    df_date['full_date'] = df_date['incident_date'].astype(str)
    df_date['year'] = df_date['incident_date'].dt.year
    df_date['month'] = df_date['incident_date'].dt.month
    df_date['day'] = df_date['incident_date'].dt.day
    df_date['weekday'] = df_date['incident_date'].dt.day_name()
    df_date[['date_id', 'full_date', 'year', 'month', 'day', 'weekday']].to_sql('dim_date', conn, if_exists='replace', index=False)

    # Dimensión ubicación
    location_cols = ['neighborhood_district', 'battalion', 'station_area', 'zipcode']
    df_location = df[location_cols].drop_duplicates().dropna().copy()
    df_location.reset_index(drop=True, inplace=True)
    df_location['location_id'] = df_location.index + 1
    df_location.to_sql('dim_location', conn, if_exists='replace', index=False)

    # Dimensión tipo de incidente
    type_cols = ['incident_type_description', 'call_type', 'alarm_dttm', 'final_priority']
    df_type = df[type_cols].drop_duplicates().dropna().copy()
    df_type.reset_index(drop=True, inplace=True)
    df_type['type_id'] = df_type.index + 1
    df_type.to_sql('dim_incident_type', conn, if_exists='replace', index=False)

    # Tabla de hechos
    df_fact = df.copy()
    df_fact['incident_date'] = pd.to_datetime(df_fact['incident_date'], errors='coerce')
    df_fact = df_fact.merge(df_date[['incident_date', 'date_id']], on='incident_date', how='left')
    df_fact = df_fact.merge(df_location, on=location_cols, how='left')
    df_fact = df_fact.merge(df_type, on=type_cols, how='left')

    df_fact_table = df_fact[['incident_number', 'date_id', 'location_id', 'type_id',
                             'fire_fatalities', 'civilian_fatalities', 'estimated_property_loss']].copy()
    df_fact_table['fatalities'] = df_fact_table[['fire_fatalities', 'civilian_fatalities']].sum(axis=1)
    df_fact_table = df_fact_table[['incident_number', 'date_id', 'location_id', 'type_id',
                                   'fatalities', 'estimated_property_loss']]
    df_fact_table.rename(columns={'incident_number': 'incident_id'}, inplace=True)

    df_fact_table.to_sql('fact_fire_incidents', conn, if_exists='replace', index=False)
    conn.close()
    print("✅ Data Warehouse created successfully.")

# ----------------------------
# Orchestrator
# ----------------------------

def main():
    df_raw = descargar_dataset(DATA_URL)
    if df_raw.empty:
        print("⛔ Pipeline aborted: empty dataset.")
        return
    df_clean = limpiar_dataset(df_raw)
    guardar_en_sqlite(df_clean, DB_NAME)
    visualizar_distribucion_temporal(DB_NAME)
    crear_datawarehouse(DB_NAME)

# ----------------------------
# Run
# ----------------------------

if __name__ == "__main__":
    main()
