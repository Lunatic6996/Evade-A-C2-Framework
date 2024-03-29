import psycopg2
from psycopg2 import sql

# Connection string
conn_string = "host=127.0.0.1 port=5432 dbname=evade-c2 user=postgres password=postgres sslmode=prefer connect_timeout=10"

# Connect to the PostgreSQL database
connection = psycopg2.connect(conn_string)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Define the table creation query and execute it
table_name = "agent_id"  # Changed to lowercase for consistency
columns = [
    ("agent_id", "SERIAL PRIMARY KEY"),
    ("Time_created", "TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"),
    ("protocol", "VARCHAR(50)")
]
create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({});").format(
    sql.Identifier(table_name),
    sql.SQL(', ').join([sql.SQL("{} {}").format(sql.Identifier(name), sql.SQL(dtype)) for name, dtype in columns])
)
cursor.execute(create_table_query)
connection.commit()

# Insert data into the table (corrected column names to uppercase)
insert_script = 'INSERT INTO agent_id (agent_id, "Time_created", protocol) VALUES (1, CURRENT_TIMESTAMP, \'HTTPs\')'
insert_script2 = 'INSERT INTO agent_id (agent_id, "Time_created", protocol) VALUES (2, CURRENT_TIMESTAMP, \'HTTPs\')'
insert_script3 = 'INSERT INTO agent_id (agent_id, "Time_created", protocol) VALUES (3, CURRENT_TIMESTAMP, \'TCP\')'
cursor.execute(insert_script)
cursor.execute(insert_script2)
cursor.execute(insert_script3)
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

print(f"Table {table_name} has been created")
