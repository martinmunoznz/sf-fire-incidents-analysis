import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# ----------------------------
# Parámetros Globales
# ----------------------------
DATA_URL = "https://data.sfgov.org/api/views/wr8u-xric/rows.csv?accessType=DOWNLOAD"
DB_NAME = "fire_incidents.db"

# ----------------------------
# Funciones del Pipeline
# ----------------------------

def descargar_dataset(url):
    print("Descargando datos...")
    return pd.read_csv(url, low_memory=False)

def limpiar_dataset(df):
    print("Limpiando datos...")
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    df = df.drop_duplicates()
    df = df.dropna()
    return df

def guardar_en_sqlite(df, db_name):
    print("Guardando en SQLite...")
    conn = sqlite3.connect(db_name)
    df.to_sql("fire_incidents", conn, if_exists="replace", index=False)
    conn.close()

def visualizar_distribucion_temporal(db_name):
    print("Generando gráfico temporal...")
    conn = sqlite3.connect(db_name)
    incidentes = pd.read_sql("""
        SELECT strftime('%Y', incident_date) AS year, COUNT(*) AS cantidad
        FROM fire_incidents
        GROUP BY year
        ORDER BY year
    """, conn)
    conn.close()

    plt.figure(figsize=(10,5))
    plt.bar(incidentes["year"], incidentes["cantidad"])
    plt.xlabel("Year")
    plt.ylabel("Number of Incidents")
    plt.title("Fire Incidents by Year")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ----------------------------
# Orquestador
# ----------------------------

def main():
    df_raw = descargar_dataset(DATA_URL)
    df_clean = limpiar_dataset(df_raw)
    guardar_en_sqlite(df_clean, DB_NAME)
    visualizar_distribucion_temporal(DB_NAME)

# ----------------------------
# Ejecutar
# ----------------------------

if __name__ == "__main__":
    main()
