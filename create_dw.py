
import sqlite3
import pandas as pd

DB_NAME = "fire_incidents.db"

conn = sqlite3.connect(DB_NAME)
df = pd.read_sql("SELECT * FROM fire_incidents", conn)

# ---------------------------
# 1. Crear dimensión fecha
# ---------------------------
df['incident_date'] = pd.to_datetime(df['incident_date'], errors='coerce')
df_date = df[['incident_date']].dropna().drop_duplicates().copy()
df_date['date_id'] = df_date['incident_date'].dt.strftime('%Y%m%d').astype(int)
df_date['full_date'] = df_date['incident_date'].astype(str)
df_date['year'] = df_date['incident_date'].dt.year
df_date['month'] = df_date['incident_date'].dt.month
df_date['day'] = df_date['incident_date'].dt.day
df_date['weekday'] = df_date['incident_date'].dt.day_name()

df_date[['date_id', 'full_date', 'year', 'month', 'day', 'weekday']].to_sql('dim_date', conn, if_exists='replace', index=False)

# ---------------------------
# 2. Crear dimensión ubicación
# ---------------------------
location_cols = ['neighborhood_district', 'battalion', 'station_area', 'zipcode']
df_location = df[location_cols].drop_duplicates().dropna().copy()
df_location.reset_index(drop=True, inplace=True)
df_location['location_id'] = df_location.index + 1
df_location.to_sql('dim_location', conn, if_exists='replace', index=False)

# ---------------------------
# 3. Crear dimensión tipo de incidente
# ---------------------------
type_cols = ['incident_type_description', 'call_type', 'alarm_dttm', 'final_priority']
df_type = df[type_cols].drop_duplicates().dropna().copy()
df_type.reset_index(drop=True, inplace=True)
df_type['type_id'] = df_type.index + 1
df_type.to_sql('dim_incident_type', conn, if_exists='replace', index=False)

# ---------------------------
# 4. Crear tabla de hechos
# ---------------------------
df_fact = df.copy()

# Asignar date_id
df_fact['incident_date'] = pd.to_datetime(df_fact['incident_date'], errors='coerce')
df_fact = df_fact.merge(df_date[['incident_date', 'date_id']], on='incident_date', how='left')

# Asignar location_id
df_fact = df_fact.merge(df_location, on=location_cols, how='left')

# Asignar type_id
df_fact = df_fact.merge(df_type, on=type_cols, how='left')

# Seleccionar columnas relevantes
df_fact_table = df_fact[['incident_number', 'date_id', 'location_id', 'type_id',
                         'fire_fatalities', 'civilian_fatalities', 'estimated_property_loss']].copy()

df_fact_table['fatalities'] = df_fact_table[['fire_fatalities', 'civilian_fatalities']].sum(axis=1)
df_fact_table = df_fact_table[['incident_number', 'date_id', 'location_id', 'type_id',
                               'fatalities', 'estimated_property_loss']]

df_fact_table.rename(columns={'incident_number': 'incident_id'}, inplace=True)

df_fact_table.to_sql('fact_fire_incidents', conn, if_exists='replace', index=False)

conn.close()
print("✅ Data Warehouse creado exitosamente.")
