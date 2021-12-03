# Sample flask app showing database connection and query

from flask import Flask, request, session, redirect, url_for, flash, render_template_string, render_template
import markdown.extensions.fenced_code
import mysql.connector
import sqlalchemy
import pandas as pd
import os

# Database credentials
database_username = 'admin'
database_password = 'admin'
database_ip       = 'test-final-db.mysql.database.azure.com:3306'
database_name     = 'final'
ssl_args = {'ssl_ca': 'ssl_cert.pem'}

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

# Connect to MySQL database on Azure
cnx = mysql.connector.connect(user="admin", password="admin", host="test-final-db.mysql.database.azure.com", port=3306, database="final", ssl_ca="ssl_cert.pem", ssl_disabled=False)
    
# Root web page
@app.route("/")
def home():
    return """<h1>Home</h1>
    <h3>Task 1: Cool_Group_Name </h3>
    <h3>Task 2: <a href="/task2">Questions Answered</a></h3>
    <h3>Task 3: <a href="/set_info">Dynamic Username/Password</a></h3>
    <h3>Tasks 4/5: <a href="/task4">Data Pull</a> (Query may take some time, please be patient.)</h3>
    <h3>Task 6: <a href="/task6">Web Page Data Display1</a></h3></h3>
    <h3>Task 7: <a href="/task7">Web Page Data Display2</a></h3></h3>
    <h3>Task 8: <a href="/task8">Data Upload</a></h3>
    <h3>Task 9: <a href="/task9">Questions Answered</a></h3>
    """

@app.route("/task6")
def task6():

    PEOPLE_FOLDER = os.path.join('static', 'people_photo')
    app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'purchases.png')
    full_filename2 = os.path.join(app.config['UPLOAD_FOLDER'], 'spending.png')
    full_filename3 = os.path.join(app.config['UPLOAD_FOLDER'], 'commodity.png')

    return render_template("index.html", user_image = full_filename, user_image2 = full_filename2, user_image3 = full_filename3)


@app.route("/task7")
def task7():

    PEOPLE_FOLDER = os.path.join('static', 'people_photo')
    app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'income.png')
    full_filename2 = os.path.join(app.config['UPLOAD_FOLDER'], 'household.png')
    full_filename3 = os.path.join(app.config['UPLOAD_FOLDER'], 'marital.png')
    full_filename4 = os.path.join(app.config['UPLOAD_FOLDER'], 'homeowner.png')

    return render_template("index.html", user_image = full_filename, user_image2 = full_filename2, user_image3 = full_filename3, user_image4 = full_filename4)


@app.route("/task4")
def task4():
    # Get houshold number from request, default to 10
    hshd_num = request.args.get("household")
    if hshd_num is None:
        hshd_num = "10"

    # SQL query to join the three tables
    sql_query = "select households.HSHD_NUM, transactions.BASKET_NUM, transactions.PURCHASE_, transactions.PRODUCT_NUM, products.DEPARTMENT, products.COMMODITY, transactions.SPEND, transactions.UNITS, transactions.STORE_R, transactions.WEEK_NUM, transactions.YEAR, households.L, households.AGE_RANGE, households.MARITAL, households.INCOME_RANGE, households.HOMEOWNER, households.HSHD_COMPOSITION, households.HH_SIZE, households.CHILDREN from households inner join transactions on households.HSHD_NUM=transactions.HSHD_NUM inner join products on transactions.PRODUCT_NUM=products.PRODUCT_NUM where households.HSHD_NUM={};".format(hshd_num)

    # Create database engine for pandas API
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                format(database_username, database_password, 
                                                        database_ip, database_name), connect_args=ssl_args)

    # Execute the query and return the result as a dataframe, convert to HTML table
    result = pd.read_sql(sql_query, database_connection).sort_values(["HSHD_NUM", "BASKET_NUM", "PURCHASE_", "PRODUCT_NUM", "DEPARTMENT", "COMMODITY"], ignore_index=True)
    html_result = result.to_html(classes='table table-striped', table_id="results")

    # Return HTML for page
    form = '''
        <form>
            <input type="text" name="household">
            <input type="submit" name="query" value="Query">
        </form>
        Queries may take some time, please be patient.<br>
        Returned {} entries.<br>
        <input type="text" id="searchTable" onkeyup="searchTable()" placeholder="Search table...">
        '''.format(len(result.index))

    # Add Javascript for searching the table
    form += '''        <script>
        function searchTable() {
        // Declare variables
        var input, filter, table, tr, td, i, j, txtValue, found;
        input = document.getElementById("searchTable");
        filter = input.value.toUpperCase();
        table = document.getElementById("results");
        tr = table.getElementsByTagName("tr");

        // Loop through all table rows, and hide those who don't match the search query
        for (i = 0; i < tr.length; i++) {
            found = false;
            td = tr[i].getElementsByTagName("td");
            if (!(td[0])) continue;
            for (j = 0; j < td.length; j++) {
                txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                }
            }
            if (found) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
        }
        </script>
        <a href="/">Return Home</a>'''
    return_html = form + html_result
    return return_html

# Web page for data upload
@app.route("/task8", methods=["GET", "POST"])
def task8():
    # Uploaded files
    if request.method == 'POST':
        print(request.files)
        if 'trans' in request.files and request.files['trans'].filename != '':
            insert_csv(request.files['trans'], 'transactions')
        if 'house' in request.files and request.files['house'].filename != '':
            insert_csv(request.files['house'], 'households')
        if 'prod' in request.files and request.files['prod'].filename != '':
            insert_csv(request.files['prod'], 'products')
        return "Data Uploaded!"

    # Form to upload CSV files
    upload_form = '''
                <!doctype html>
                <title>Upload CSV Data</title>
                <h1>Upload CSV Data</h1>
                Uploading large amounts of data may take a long time. Please be patient and do not refresh the page while uploading.<br><br>
                <form method=post enctype=multipart/form-data>
                    <div>Transactions CSV</div><input type=file name=trans><br>
                    <div>Households CSV</div><input type=file name=house><br>
                    <div>Products CSV</div><input type=file name=prod><br>
                    <input type=submit value=Upload>
                </form>
                <a href="/">Return Home</a>
                '''
    return upload_form
    
# Insert a CSV file into a specified table in the database
def insert_csv(csv, table):
    # Create dataframe from CSV
    df = pd.read_csv(csv).rename(columns=lambda x: x.strip()) # remove whitespace from column names

    # Create database engine for pandas API
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name), connect_args=ssl_args)

    # Insert dataframe into table
    df.to_sql(name=table, 
              schema='final',
              con=database_connection,
              if_exists='append',
              index=False)


@app.route("/task9")
def task9():
    readme_file = open("task9.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )
    return md_template_string


@app.route("/task2")
def task2():
    readme_file = open("task2.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )
    return md_template_string


@app.route('/set_info', methods=['GET', 'POST'])
def set_info():
    if request.method == 'POST':
        # Save the form data to the session object

        try:
            if session['username']: #and session['password']:
                if (session['password'] == request.form['password'] and session['username'] == request.form['username']):
                    return redirect(url_for('get_info'))
                else:
                    flash('Wrong Combination')
        except:
            return redirect(url_for('set_info'))
        return redirect(url_for('set_info'))

    return """
        <form method="post">
            <label for="username">Enter your username:</label>
            <input type="username" id="username" name="username" required />
            <br>
            <label for="password">Enter your password:</label>
            <input type="password" id="password" name="password" required />
            <br>
            <button type="submit">Submit</button>
            <br>
            
        </form>
        <h3>Welcome! If you are new click <a href="capture_info">here.</a></h3>
        <br><br><a href="/">Return Home</a>
        """

@app.route('/capture_info', methods=['GET', 'POST'])
def capture_info():
    if request.method == 'POST':
        # Save the form data to the session object
        session['password'] = request.form['password']
        session['username'] = request.form['username']
        session['firstname'] = request.form['firstname']
        session['lastname'] = request.form['lastname']
        session['email'] = request.form['email']
        return redirect(url_for('set_info'))

    return """
        <form method="post">
        <form method="post">
            <label for="username">Enter your username:</label>
            <input type="username" placeholder="" name="username" required />
            <br>
            <label for="password">Enter your password:</label>
            <input type="password" placeholder="" name="password" required />
            <br>
            <label for="firstname">Enter your First Name:</label>
            <input type="text" placeholder="" name="firstname" required />
            <br>
            <label for="lastname">Enter your Last Name:</label>
            <input type="text" placeholder="" name="lastname" required />
            <br>
            <label for="email">Enter your email:</label>
            <input type="email" placeholder="" name="email" required />
            <br>
            <button type="submit">Submit</button>
        </form>
        <br>
        <br><a href="/">Return Home</a>
        """

@app.route('/get_info')
def get_info():
    return render_template_string("""
        {% if session['username'] %}
            <h1>Welcome {{ session['firstname'] }}!</h1>
            <h2>Here is your info:</h2>
            {{ session['firstname'] }} {{ session['lastname'] }} <br>
            {{ session['username'] }} <br>
            {{ session['email'] }}
            <h3>Delete your info <a href="delete_info">here.</a></h3>
            <h3>Log out <a href="set_info">here.</a></h3>
            <br>
        {% else %}
            <h1>Welcome! Please enter your info <a href="{{ url_for('set_info') }}">here.</a></h1>
        {% endif %}
        <br><br><a href="/">Return Home</a>
    """)


@app.route('/delete_info')
def delete_info():
    # Clear the info stored in the session object
    session.pop('password', default=None)
    session.pop('username', default=None)
    session.pop('first_name', default=None)
    session.pop('last_name', default=None)
    session.pop('email', default=None)
    return '''<h1>Session deleted!</h1><br><h3>Return <a href="set_info">here.</a></h3><br><br><a href="/">Return Home</a>'''