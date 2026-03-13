import pandas as pd
import sqlite3

file_path = "2_tool_calling/world_population.csv"

# Databse initieren
db_file = "2_tool_calling/world_data.db"

# CSV inlezen (eerste 4 regels overslaan)
df = pd.read_csv(
    file_path,
    skiprows=4
)

# Lege kolommen verwijderen (zoals de laatste lege kolom)
df = df.dropna(axis=1, how="all")

# Verbinding maken met SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Tabel aanmaken als die nog niet bestaat
cursor.execute("""
CREATE TABLE IF NOT EXISTS population_data (
    country_iso_code TEXT PRIMARY KEY,
    country_name TEXT NOT NULL,
    population INTEGER
)
""")


for index, row in df.iterrows():
    print(row['2024'])

    cursor.execute("""
    INSERT INTO population_data (country_iso_code, country_name, population)
    VALUES (?, ?, ?)
    ON CONFLICT(country_iso_code) DO UPDATE SET
        country_name = excluded.country_name,
        population = excluded.population
    """, (row["Country Code"], row["Country Name"], row["2024"]))

conn.commit()
conn.close()