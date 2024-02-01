import psycopg2
from psycopg2 import sql

# Database connection parameters
dbname = "evade-c2"
user = "postgres"
password = "postgres"
host = "localhost"
port = "5432"
conn = None
cur = None

try:
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    # Create a cur object to execute SQL queries
    cur = conn.cur()
    cur.execute('DROP TABLE IF EXISTS agents')
    # Define the table creation query and Execute the table creation query and commit the changes
    create_script = '''
    CREATE TABLE IF NOT EXISTS agents (
        id            SERIAL PRIMARY KEY,
        time_created  TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        protocol      VARCHAR(6) NOT NULL)
    '''
    cur.execute(create_script)
    conn.commit()

    #insert data into the database
    insert_script = 'INSERT INTO agents (id, time_created, protocol) VALUES (%s, CURRENT_TIMESTAMP, %s);'
    insert_values = [(1, 'TCP'), (2, 'HTTP'), (3, 'HTTPS')]
    for record in insert_values:
        cur.execute(insert_script,record)
    conn.commit()

    #delete data from the database
    delete_script = 'DELETE FROM agents WHERE id = %s'
    delete_record = ('1',)
    cur.execute(delete_script,delete_record)
    conn.commit()
    

except Exception as error:
    print(error)

finally:
    # Close the cur and connection
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()

print(f"Table agents has been created and data inserted.")
