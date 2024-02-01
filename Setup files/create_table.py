import psycopg2
from psycopg2 import sql

# Database connection parameters
dbname = "evade-c2"
user = "postgres"
password = "postgres"
host = "localhost"
port = "5432"

# Connect to the PostgreSQL database
connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Define the table creation query
table_name = "Agent_id"
columns = [
    ("agent_id", "SERIAL PRIMARY KEY"),
    ("Time_created", "TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"),
    ("protocol", "VARCHAR(50)")
]
create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({});").format(
    sql.Identifier(table_name),
    sql.SQL(', ').join([sql.SQL("{} {}").format(sql.Identifier(name), sql.SQL(dtype)) for name, dtype in columns])
)

# Execute the table creation query
cursor.execute(create_table_query)

# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

print(f"Table {table_name} has been created.")
