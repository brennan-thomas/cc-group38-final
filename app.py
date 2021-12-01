# Sample flask app showing database connection and query

from flask import Flask
import mysql.connector

app = Flask(__name__)

# Root web page
@app.route("/")
def hello_world():

    # Connect to MySQL database on Azure
    cnx = mysql.connector.connect(user="admin", password="admin", host="test-final-db.mysql.database.azure.com", port=3306, database="final", ssl_ca="ssl_cert.pem", ssl_disabled=False)
    
    # Run query to get all records in table "test"
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM test")
    query_result = cursor.fetchall()

    # Format HTML string with results and return
    query_result = '<br>'.join(map(str, query_result))
    return_string = "<b>ID, Name in table \"test\"</b><br>" + query_result
    return return_string
