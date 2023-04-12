import json
import os
import logging
import urllib
from flask import Flask, jsonify, render_template, request, url_for;
from cassandra.cluster import Cluster
from io import StringIO
import pandas as pd
import csv

app = Flask(__name__)

# Define the Cassandra host address
cassandra_host = '127.0.0.1'
cassandra_port = 6000
# # Connect to Cassandra cluster
cluster = Cluster([cassandra_host], port = cassandra_port)
session = cluster.connect()

os.environ['CASSANDRA_LOADER_HOME'] = '/Users/ranjotaballal/Desktop/Cassandra-Data-Custodian/cassandra-loader'

 #create a logger
logger = logging.getLogger('mylogger')
#set logger level
logger.setLevel(logging.INFO)
#or you can set the following level
#logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('mylog.log')
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Ca = CassandraConnect()
# Ca.connect()
# session = Ca.session

if __name__ == '__main__':
    app.run(debug=True)
     # app.run(host='104.167.192.10', threaded=True, use_reloader=False)


@app.route("/")
def signIn():
     return render_template("sign-in.html")

@app.route("/studentInfo", methods=['POST', 'GET'])
def save_info():
    if request.data != None or request.data != '':
     request_data = json.loads(request.data)

     id = int(request_data['id'])
     first_name = str(json.dumps(request_data['firstName']))
     last_name = str(json.dumps(request_data['lastName']))
     email_id = str(json.dumps(request_data['emailId']))
     password = str(json.dumps(request_data['password']))
     year_of_birth = int(request_data['birthYear'])
     academic_period = str(json.dumps(request_data['academicPeriod']))
     georgian_campus = str(json.dumps(request_data['georgianCampus']))
     groups = str(json.dumps(request_data['groups']))
     program_code = str(json.dumps(request_data['programCode']))
     isAdmin =  True if str(request_data['isAdmin']) == 'True' else  False 
     isActiveUser =  True if str(request_data['isActiveUser']) == 'True' else  False


    # Create a keyspace and table to store form responses
     session.execute("""CREATE KEYSPACE IF NOT EXISTS testprojectdb WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };""")

     session.execute("""
          CREATE TABLE IF NOT EXISTS testprojectdb.responses (
               id int,
               first_name text,
               last_name text,
               email_id text,
               password text,
               year_of_birth int,
               academic_period text,
               georgian_campus text,
               groups text,
               program_code text,
               isAdmin boolean,
               isActiveUser boolean,
               PRIMARY KEY (id)
          );
     """)

     session.execute("""
            INSERT INTO testprojectdb.responses (id, first_name, last_name, email_id, password, year_of_birth, academic_period, georgian_campus, groups, program_code, isAdmin, isActiveUser  )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (id, first_name, last_name, email_id, password, year_of_birth, academic_period, georgian_campus, groups, program_code, isAdmin, isActiveUser))
     
     if isAdmin:
          redrectUrl = url_for("admintableList")
     else:
          redrectUrl = url_for("tableList")

     return jsonify({'redirect': redrectUrl, 'message': 'Data inserted successfully!!'});

@app.route('/userTable')
def userTable():
    return render_template("user-table.html")

@app.route('/userTableInfo', methods=['POST', 'GET'])
def userTableInfo():
     user_data = session.execute("SELECT * FROM testprojectdb.responses")
     return_data = [];
     for row in user_data:
          return_data.append(
               {'id': str(row[0]),
                'first_name':row[3].replace('"',''),
                'last_name':row[8].replace('"',''),
                'email_id':row[2].replace('"',''),
                'year_of_birth':str(row[11]),
                'password': row[9].replace('"',''),
                'academic_period':row[1].replace('"',''),
                'georgian_campus':row[4].replace('"',''),
                'groups':row[5].replace('"',''),
                'program_code':row[10].replace('"',''),
                'isAdmin': str(row[7]),
                'isActiveUser': str(row[6])  
               }
          )
    
     return jsonify(return_data);

@app.route('/updateUser', methods=['POST', 'GET'])
def updateUserTable():

     id = request.args.getlist('id')[0]
     data = urllib.parse.unquote(request.get_data(as_text=True),encoding='big5')
     data_list =json.loads(json.loads(json.dumps(data)))

     id_val = int(data_list['data'][id]['id'])
     first_name = '"' + data_list['data'][id]['first_name'] + '"'
     last_name = '"' + data_list['data'][id]['last_name'] + '"'
     email_id =  '"' + data_list['data'][id]['email_id'] + '"'
     year_of_birth = int(data_list['data'][id]['year_of_birth']) 
     isAdmin = True if data_list['data'][id]['isAdmin'] == 'True' else  False
     isActiveUser =  True if data_list['data'][id]['isActiveUser'] == 'True' else  False
     academic_period = '"' + data_list['data'][id]['academic_period'] + '"'
     georgian_campus = '"' + data_list['data'][id]['georgian_campus'] + '"'
     groups =  '"' + data_list['data'][id]['groups'] + '"'
     program_code = '"' + data_list['data'][id]['program_code'] + '"'

     session.execute("""
            INSERT INTO testprojectdb.responses (id, first_name, last_name, email_id, year_of_birth, academic_period, georgian_campus, groups, program_code, isAdmin, isActiveUser  )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (id_val, first_name, last_name, email_id, year_of_birth, academic_period, georgian_campus, groups, program_code, isAdmin, isActiveUser))

     return jsonify({'redirect': url_for("userTable"), 'message': 'Data inserted successfully!!'});


@app.route('/tableList')
def tableList():
    return render_template("table-list.html")

@app.route('/admintableList')
def admintableList():
    return render_template("admin-list.html")
    
@app.route('/tableListInfo', methods=['POST', 'GET'])
def tableListInfo():

     if request.data != None or request.data != '':
          request_data = json.loads(request.data)

     email_id = str(json.dumps(request_data['emailId']))
     if "true" in str(json.dumps(request_data['isAdmin'])):
          account_type = str(json.dumps(request_data['accountType']))
     else: 
          if '@mygeorgian.ca' in email_id  or '@student.georgianc.on.ca' in email_id:
               account_type = 'student'
          elif '@georgiancollege.ca' in email_id:
               account_type = 'faculty'
          else:
               account_type = 'public'

     if 'student' in account_type: #student account
        # session.execute("ALTER ROLE student_role WITH OPTIONS = { 'email' : email }")
        # session.execute("GRANT SELECT ON KEYSPACE gc_student_db TO student_role")
        accountType = "Student Account"
        #rows = session.execute('SELECT table_name FROM system_schema.tables WHERE keyspace_name = %s', ['student_role'])
        rows = session.execute('SELECT table_name FROM system_schema.tables WHERE keyspace_name = %s', ['gc_student_db'])
        # Render table information in template
        table_names = [row.table_name for row in rows]
     elif 'faculty' in account_type: #Faculty account
        # session.execute("ALTER ROLE faculty_role WITH OPTIONS = { 'email' : email }")
        # session.execute("GRANT SELECT ON KEYSPACE gc_faculty_db TO faculty_role")
        accountType = "Faculty Account"
        rows = session.execute('SELECT table_name FROM system_schema.tables WHERE keyspace_name = %s', ['gc_faculty_db'])
        #rows = session.execute('SELECT table_name FROM system_schema.tables WHERE keyspace_name = %s', ['testprojectdb'])
        # Render table information in template
        table_names = [row.table_name for row in rows]
     else: #Public account
        # session.execute("ALTER ROLE public_role WITH OPTIONS = { 'email' : email }")
        # session.execute("GRANT SELECT ON KEYSPACE gc_public_db TO public_role")
        accountType = "Public Account"
        rows = session.execute('SELECT table_name FROM system_schema.tables WHERE keyspace_name = %s', ['gc_public_db'])
        #rows = session.execute('SELECT table_name FROM system_schema.tables WHERE keyspace_name = %s', ['testprojectdb'])
        # Render table information in template
        table_names = [row.table_name for row in rows]
     
     return jsonify({'tableNames': table_names, 'accountType': accountType});

@app.route('/viewTable')
def viewTable():
    return render_template("view-table.html")

@app.route('/index')
def signUp():
    return render_template("index.html")

@app.route('/verifySignIn', methods=['POST', 'GET'])
def verifySignIn():

   if request.data != None or request.data != '':
          request_data = json.loads(request.data)

   email_id = request_data['username']
   password = request_data['password']

   query = "SELECT isAdmin, isActiveUser from testprojectdb.responses WHERE email_id='" + '"' + email_id + '"' + "' and password='" + '"' + password + '"' + "' ALLOW FILTERING"
   user_info = session.execute(query)
   user_data = []

   for row in user_info:
     user_data.append({
          'isAdmin': row[0],
          'isActiveUser': row[1]
     })


   if user_data and user_data[0]['isAdmin']:
     redirectUrl = url_for("admintableList")
   else:
     redirectUrl = url_for("tableList")

   return jsonify({'redirect': redirectUrl, 'userInfo': user_data, 'message': 'User sign in successful!!'});



@app.route('/viewTableInfo', methods=['POST', 'GET'])
def viewTableInfo():
     table_name = request.args.getlist('tableName')[0]
     email_id = request.args.getlist('emailId')[0]
     accountType =  request.args.getlist('accountType')[0]
     isAdmin =  request.args.getlist('isAdmin')[0]

     if "true" in isAdmin:
          if 'student' in accountType:
               keyspace = 'gc_student_db'
          elif 'faculty' in accountType:
               keyspace = 'gc_faculty_db'
          else:
               keyspace = 'gc_public_db'
     else: 
          if '@mygeorgian.ca' in email_id  or '@student.georgianc.on.ca' in email_id:
               keyspace = 'gc_student_db'
          elif '@georgiancollege.ca' in email_id:
               keyspace = 'gc_student_db'
          else:
               keyspace = 'gc_student_db'

     table_names_query = "SELECT JSON * FROM " + str(keyspace) + '.' + str(table_name)

     logger.info(table_names_query)
    
     view_table = session.execute(table_names_query);
     table_values = [];
     for row in view_table:
          table_values.append(json.loads(row.json));

     return jsonify(table_values);

@app.route('/loadData')
def loadData():
    return render_template("load-data.html")

@app.route('/uploadTable', methods=['POST', 'GET'])
def loadTable():
    account_type = request.args.get('accountType')
    keyspace = ''

    if account_type == 'student':
        keyspace = 'gc_student_db'
    elif account_type == 'faculty':
        keyspace = 'gc_faculty_db'
    else:
        keyspace = 'gc_public_db'

    for csv_file in request.files.getlist('csv_file'):
        file_name = csv_file.filename
        table_name = file_name.replace('.csv', '')
        
        if not table_name.startswith(keyspace):
          table_name = account_type + '_' + table_name

        csv_content = csv_file.read().decode('utf-8-sig')
        headers = next(csv.reader(csv_content.splitlines(), delimiter=',', quotechar='"'))

        headers = [header.replace(" ", "_") for header in headers]  # replace spaces with underscores
        headers = [header.replace('.', '').lower() for header in headers]
        data_types = [f"{column_name} text" for column_name in headers]  # set data type as text

        # Build the CREATE TABLE query to create the table schema
        query1 = f"DROP TABLE IF EXISTS {keyspace}.{table_name};"
        query2 = f"CREATE TABLE IF NOT EXISTS {keyspace}.{table_name} ("
        query2 += ", ".join(data_types)
        query2 += ", PRIMARY KEY(" + headers[0] + ")"
        query2 += ");"

        # Execute the CREATE TABLE query to create the table schema
        try:
            session.execute(query1)
            session.execute(query2)
        except Exception as e:
            logger.info(f"Error creating table {table_name}: {e}")
            continue

        # Load the data into the Cassandra table using pandas
        data = pd.read_csv(StringIO(csv_content))
        data.columns = headers
        data = data.astype(str)  # cast all columns to string type
        data = data.set_index(headers[0])  # set primary key as index
        data = data.where(pd.notnull(data), None)  # replace NaN values with None for compatibility with Cassandra

        for _, row in data.iterrows():
            values = ", ".join([f"'{value}'" if value is not None else "NULL" for value in row])
            query3 = f"INSERT INTO {keyspace}.{table_name} ({', '.join(headers)}) VALUES ('{row.name}', {values});"
            try:
                session.execute(query3)
            except Exception as e:
                logger.info(f"Error loading data into table {table_name}: {e}")
                continue
               
        # Emit an event to the client for each file upload
     #    emit('file_uploaded', {'file_name': file_name, 'table_name': table_name}, namespace='/upload')


    return "Success"


@app.route('/adminTableListInfo', methods=['POST', 'GET'])
def adminTableListInfo():

     if request.data != None or request.data != '':
          request_data = json.loads(request.data)

     account_type = str(json.dumps(request_data['accountType']))
     if 'student' in account_type: #student account
        accountType = "Student Account"
        rows = session.execute('SELECT table_name FROM system_schema.tables WHERE keyspace_name = %s', ['gc_student_db'])
        # Render table information in template
        table_names = [row.table_name for row in rows]
     elif 'faculty' in account_type: #Faculty account
        accountType = "Faculty Account"
        rows = session.execute('SELECT table_name FROM system_schema.tables WHERE keyspace_name = %s', ['gc_faculty_db'])
        # Render table information in template
        table_names = [row.table_name for row in rows]
     else: #Public account
        accountType = "Public Account"
        rows = session.execute('SELECT table_name FROM system_schema.tables WHERE keyspace_name = %s', ['gc_public_db'])
        # Render table information in template
        table_names = [row.table_name for row in rows]
     
     return jsonify({'tableNames': table_names, 'accountType': accountType});

