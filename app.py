# Sample flask app showing database connection and query

from flask import Flask, request, session, redirect, url_for, flash, render_template_string
import mysql.connector
from collections import Counter
import markdown.extensions.fenced_code

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

# Connect to MySQL database on Azure
cnx = mysql.connector.connect(user="admin", password="admin", host="test-final-db.mysql.database.azure.com", port=3306, database="final", ssl_ca="ssl_cert.pem", ssl_disabled=False)
    
# Root web page
@app.route("/")
def home():

    # Run query to get all records in table "test"
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM test")
    query_result = cursor.fetchall()

    # Format HTML string with results and return
    query_result = '<br>'.join(map(str, query_result))
    return_string = "<b>ID, Name in table \"test\"</b><br>" + query_result

    return return_string + """<br><br>
    <h3>Task 1: Cool_Group_Name </h3>
    <h3>Task 2: <a href="/task2">Questions Answered</a></h3>
    <h3>Task 3: <a href="/set_info">Dynamic Username/Password</a></h3>
    <h3>Task 4: </h3>
    <h3>Task 5: </h3>
    <h3>Task 6: </h3>
    <h3>Task 7: </h3>
    <h3>Task 8: </h3>
    <h3>Task 9: <a href="/task9">Questions Answered</a></h3>
    """

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