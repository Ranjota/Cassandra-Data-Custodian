from cassandra.cluster import Cluster
import csv
import os

# Connect to the Cassandra cluster
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect()

# Select the keyspace
keyspace = 'gc_public_db'

# Get a list of CSV files in the folder
folder_path = 'C:\\Users\\Yuvansh\\Desktop\\inserting_data_cass\\datasets\\public_datasets'
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Loop through each CSV file and create a table for it and insert the data
for file_name in csv_files:
    # Get the table name from the file name
    table_name = file_name.replace('.csv', '')

    # Read the CSV file to get the column names and data types
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r', encoding='ISO-8859-1') as f:
        reader = csv.reader(f)
        headers = next(reader)
        headers = [header.replace(" ", "_") for header in headers]  # replace spaces with underscores
        headers = [header.replace('.', '').lower() for header in headers]
        data_types = [f"{column_name} varchar" for column_name in headers]

    # Build the CREATE TABLE query to create the table schema
    query1 = f"DROP TABLE IF EXISTS {keyspace}.{table_name};"
    query2 = f"CREATE TABLE IF NOT EXISTS {keyspace}.{table_name} ("
    query2 += ", ".join(data_types)
    query2 += ", PRIMARY KEY(" + headers[0] + ", " + ", ".join([f"{column_name}" for column_name in headers[1:]]) + ")"
    query2 += ");"

    # Execute the CREATE TABLE query to create the table schema
    try:
        session.execute(query1)
        session.execute(query2)
    except:
        # print(f"Error creating table {table_name}: {str(e)}")
        continue

    # Insert the data from the CSV file into the table
    with open(file_path, 'r', encoding='ISO-8859-1') as f:
        reader = csv.reader(f)
        next(reader) # skip headers
        for row in reader:
            if any(row):
                query = f"""INSERT INTO {keyspace}.{table_name} ({', '.join(['"' + h + '"' for h in headers])}) VALUES ({', '.join(['%s']*len(row))})"""
                print(query)
                row = [value.strip() for value in row]
                session.execute(query, row)