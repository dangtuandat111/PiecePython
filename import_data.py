import os
import mysql.connector

# List of SQL file paths
sql_directory = "D:\REMOVE"

# Database connection configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "es2020"
}

# Establish a database connection
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # List files in the directory
    for filename in os.listdir(sql_directory):
        if filename.endswith(".sql"):
            sql_file_path = os.path.join(sql_directory, filename)

            # Read the SQL file
            with open(sql_file_path, 'r', encoding="utf-8") as file:
                sql_commands = file.read()

            # Split the file into individual SQL statements
            sql_statements = sql_commands.split(';')

            # Execute each SQL statement
            for statement in sql_statements:
                try:
                    # Execute the SQL statement
                    if statement.strip():  # Check for non-empty statements
                        cursor.execute(statement)
                        print(f"Executed SQL statement from {filename}: {statement}")
                except mysql.connector.Error as e:
                    print(f"Error executing SQL statement: {e}")

    # Commit the transaction (if needed)
    connection.commit()

except mysql.connector.Error as e:
    print(f"Error connecting to the database: {e}")

finally:
    # Close the database connection
    if connection.is_connected():
        cursor.close()
        connection.close()