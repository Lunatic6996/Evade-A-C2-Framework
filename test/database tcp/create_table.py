import psycopg2
from psycopg2 import sql

# Connection string
conn_string = "host=127.0.0.1 port=5432 dbname=evade-c2 user=postgres password=postgres sslmode=prefer connect_timeout=10"

# Connect to the PostgreSQL database
connection = psycopg2.connect(conn_string)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Define the table creation query and execute it
table_name = "agent_connections"  # Updated table name
columns = [
    ("id", "SERIAL PRIMARY KEY"),
    ("agent_name", "VARCHAR(255)"),
    ("protocol", "VARCHAR(50)"),
    ("connection_time", "TIMESTAMP")
]
create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({});").format(
    sql.Identifier(table_name),
    sql.SQL(', ').join([sql.SQL("{} {}").format(sql.Identifier(name), sql.SQL(dtype)) for name, dtype in columns])
)
cursor.execute(create_table_query)
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

print(f"Table {table_name} has been created")
