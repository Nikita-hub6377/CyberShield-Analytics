import pandas as pd
import mysql.connector

# Load processed CSV file
df = pd.read_csv("data/processed/cybersecurity_processed.csv")

print("CSV loaded successfully!")
print("Total rows in CSV:", len(df))

# Connect to MySQL
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Nikita@123",
    database="cybershield_analytics"
)

cursor = connection.cursor()

print("Connected to MySQL successfully!")

# Remove old data from the table to avoid duplicate imports
cursor.execute("DELETE FROM incidents")
connection.commit()

# SQL query for inserting data
insert_query = """
INSERT INTO incidents (
    incident_id,
    country,
    year,
    attack_type,
    target_industry,
    financial_loss_million,
    affected_users,
    attack_source,
    vulnerability_type,
    defense_mechanism,
    resolution_time_hours,
    financial_loss_score,
    affected_users_score,
    resolution_time_score,
    risk_score,
    risk_level
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s
)
"""

# Insert each row
for _, row in df.iterrows():
    values = tuple(row.values.tolist())
    cursor.execute(insert_query, values)

connection.commit()

print("All data imported successfully!")
print("Total rows imported:", len(df))

# Verify data
cursor.execute("SELECT COUNT(*) FROM incidents")
count = cursor.fetchone()[0]

print("Total rows currently in MySQL:", count)

# Close connection
cursor.close()
connection.close()

print("MySQL connection closed.")