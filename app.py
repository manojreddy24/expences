import hashlib
from flask import *
import pymysql
from datetime import *
import random
import string
import smtplib
import base64
from io import BytesIO
import pytz
import os

from email.mime.text import MIMEText
app.permanent_session_lifetime=timedelta(seconds=15)
app = Flask(__name__,template_folder="templates",static_folder="static")
app.secret_key="manbigdat"
# Connect to PHPMyAdmin cloud database
connection = pymysql.connect(
    host='sql9.freesqldatabase.com',
    user='sql9618784',
    password='ej2mLj1XvS',
    db='sql9618784'

)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'itsmymail425@gmail.com'
EMAIL_HOST_PASSWORD = 'llhattqaxodqhyjp'
EMAIL_PORT = 587

# @app.before_request
# def before_request():
#     session.permanent = True
#     app.permanent_session_lifetime = timedelta(seconds=15)
#     session.modified = True
#
#     if 'last_activity' in session:
#         elapsed_time = timedelta(seconds=15)
#         last_activity = session['last_activity']
#         print(last_activity)
#         # Get the client's timezone from the request headers
#         client_timezone = request.headers.get('Timezone')
#
#         # Get the current time in the client's timezone
#         current_time = datetime.now(pytz.timezone(client_timezone))
#
#         if (current_time - last_activity) > elapsed_time:
#             # Session has expired, redirect to the login page
#             return "Session expired"
#     session['last_activity'] = datetime.now(pytz.timezone(client_timezone))
#
#


# @app.route('/dairy_login')
def dairy_login():
    try:
        with connection.cursor() as cursor:
            sql = "CREATE TABLE IF NOT EXISTS dairy_login (id INT NOT NULL AUTO_INCREMENT, username VARCHAR(200) NOT NULL, password VARCHAR(100) NOT NULL, dairycode INT NOT NULL, email VARCHAR(100) NOT NULL UNIQUE, verification_code VARCHAR(255), verified BOOLEAN NOT NULL DEFAULT FALSE, PRIMARY KEY (id), INDEX(username), INDEX(email))"
            cursor.execute(sql)
            connection.commit()
        return "Table created: dairy_login"
    except pymysql.err.OperationalError as e:
        return "Error creating table: " + str(e)

# expences
# @app.route('/expences', methods=['GET', 'POST'])
def create_expense_table():
    try:
        with connection.cursor() as cursor:
            sql = """CREATE TABLE IF NOT EXISTS expenses (id INT NOT NULL AUTO_INCREMENT,username VARCHAR(200) NOT NULL,email VARCHAR(100) NOT NULL, expense_date DATE,amount DECIMAL(10, 2) NOT NULL,category VARCHAR(100) NOT NULL,notes TEXT,timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,image LONGBLOB ,PRIMARY KEY (id),INDEX(username),INDEX(email),INDEX(TIMESTAMP),FOREIGN KEY (username) REFERENCES dairy_login(username),FOREIGN KEY (email) REFERENCES dairy_login(email))"""
            cursor.execute(sql)
            connection.commit()
        return "Table created: expenses"
    except pymysql.err.OperationalError as e:
        return "Error creating table: " + str(e)


# @app.route('/view_table')
def view_table():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM dairy_login"
        cursor.execute(sql)
        result = cursor.fetchall()
        return render_template('view_table.html', result=result)

# @app.route('/drop')
def drop():
    try:
        with connection.cursor() as cursor:
            sql = "DROP TABLE IF EXISTS dairy_login"
            cursor.execute(sql)
            connection.commit()
        return "Table dropped: dairy_login"
    except pymysql.err.OperationalError as e:
        return "Error dropping table: " + str(e)

def generate_code():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

BLOCK_SIZE = 16
def hash_password(password):
    # Convert password to bytes and hash using SHA-256 algorithm
    hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        dairycode = request.form['dairycode']

        code = generate_code()
        email = request.form['email']

        # Check if password and confirmation match
        if password != confirm_password:
            flash("Passwords do not match. Please try again.")
            return redirect(url_for('register'))

        # Hash the password
        hashed = hash_password(password)
        dairycode = hash_password(dairycode)
        sq1 = "INSERT INTO dairy_login (username,password,email,dairycode) VALUES (%s,%s,%s,%s)"
        val = (username, hashed, email,dairycode)
        with connection.cursor() as cursor:
            cursor.execute(sq1,val)
            connection.commit()

        send_verification_email(email, code)
        # flash('An email with verification code has been sent to your email address.')


        # Store user credentials in MySQL database
        return redirect(url_for('verify', email=email))
    return render_template('register.html')

# Send email to user with verification code
def send_verification_email(to_email, code):
    message = f'Your verification code is: {code}'
    msg = MIMEText(message)
    msg['Subject'] = 'Verification code for your account'
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = to_email
    with connection.cursor() as cursor:
        sql = "UPDATE dairy_login SET verification_code = %s WHERE email = %s"
        up_code=hash_password(code)
        val = (up_code, to_email)
        cursor.execute(sql, val)
        connection.commit()

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(EMAIL_HOST_USER, to_email, msg.as_string())




# Verify user's email address
@app.route('/verify/<email>', methods=['GET', 'POST'])
def verify(email):
    if request.method == 'POST':
        code = request.form['code']
        sq1 = "SELECT * FROM dairy_login WHERE email = %s AND verification_code = %s"
        up_code=hash_password(code)
        val = (email, up_code)
        with connection.cursor() as cursor:
            cursor.execute(sq1, val)
            data = cursor.fetchone()
            if data:
                sq2 = "UPDATE dairy_login SET verified = %s WHERE email = %s"
                val2 = (True, email)
                cursor.execute(sq2, val2)
                connection.commit()
                flash('Your email address has been verified.')
                return redirect(url_for('login'))
            else:
                flash('Invalid verification code. Please try again.')
    return render_template('verify.html', email=email)

@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    # session.pop('username', None)
    return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = hash_password(password)
        # print("username",username)
        # print("password",hashed)
        sql="select * from dairy_login where username='{}' and password='{}'".format(username,hashed)
        # print("sql",sql)

        with connection.cursor() as cursor:
            cursor.execute(sql)
            data = cursor.fetchone()
            # print("data",data[4])
            session['email'] = data[4]


            if data:
                session['username'] = username  # Store the username in the session
                # print("session",session['username'])



                return render_template('dairycode.html', username=session['username'])  # Pass the username to the template
            else:
                flash("Invalid username or password")
                return redirect(url_for('login'))


    return render_template('login.html')

@app.route('/dairycode', methods=['GET', 'POST'])
def dairycode():
    if 'username' in session:  # Check if the username is stored in the session
        username = session['username']  # Retrieve the username from the session
        if request.method=="POST":
            code=request.form['code']
            # print("code",code)
            with connection.cursor() as cursor:
                sql="select * from dairy_login where username='{}' and dairycode={}".format(username,code)
                cursor.execute(sql)
                data = cursor.fetchone()
                # print("data",data)

                if data:
                    session['dairycode'] = code  # Store the username in the session
                    return render_template('index.html', username=username)  # Pass the username to the template
                else:
                    flash("Invalid dairycode")
                    return redirect(url_for('dairycode'))

        return render_template('dairycode.html')  # Pass the username to the template
    else:
        return redirect(url_for('login'))


@app.route('/index')
def index():
    if 'username' and 'dairycode' in session:  # Check if the username is stored in the session
        username = session['username']  # Retrieve the username from the session
        dairycode = session['dairycode']
        # print("dairycode",dairycode)
        return render_template('index.html', username=username)  # Pass the username to the template
    else:
        return redirect(url_for('login'))
app.config['UPLOAD_FOLDER'] = 'static'
@app.route('/expense_entry', methods=['GET', 'POST'])
def expense_entry():
    if 'username'  and 'dairycode' in session:  # Check if the username is stored in the session
        username = session['username']
        email=session['email']
        if request.method == 'POST':
            category = request.form['category']
            amount = float(request.form['amount'])
            notes = request.form['notes']
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            date = request.form['date']
            image = request.files['image']
            image_data = image.read()
            # print("image_data",image_data)





            # Insert the expense data into the expenses table
            with connection.cursor() as cursor:
                sql = "INSERT INTO expenses (username,email, category, amount, timestamp, notes,expense_date,image ) VALUES (%s,%s,%s, %s, %s, %s,%s,%s)"
                cursor.execute(sql, (username,email, category, amount, timestamp, notes,date,image_data ))
                connection.commit()

            return redirect(url_for('view_expenses'))

        return render_template('expense_entry.html')
    else:
        return redirect(url_for('login'))



@app.route('/expences_view', methods=['GET'])
def view_expenses():
    if 'username' and 'dairycode' in session:  # Check if the username is stored in the session

        username = session['username']


        # Retrieve the expenses from the database
        with connection.cursor() as cursor:
            sql = "SELECT * FROM expenses WHERE username = '{}' ORDER BY expense_date DESC".format(username)

            cursor.execute(sql)
            # print("cursor",sql)
            expenses = cursor.fetchall()



        return render_template('expences_view.html', expenses=expenses, username=username)
    else:
        return redirect(url_for('login'))

@app.route('/edit_expense', methods=['GET', 'POST'])
def edit_expense():
    if 'username' and 'dairycode' in session:  # Check if the username is stored in the session
        if request.method == 'POST':
            expense_id = request.form['expense_id']
            category = request.form['category']
            amount = float(request.form['amount'])
            date = request.form['date']
            notes = request.form['notes']
            image = request.files['image']
            image_data = image.read()
            # print("image_data", image_data)

            with connection.cursor() as cursor:
                sql = "UPDATE expenses SET category = %s, amount = %s, expense_date = %s, notes = %s , image= %s WHERE id = %s"
                # print(sql)
                cursor.execute(sql, (category, amount, date, notes, image_data,expense_id))
                connection.commit()

            return redirect('/expences_view')

        else:
            expense_id = request.args.get('id')

            with connection.cursor() as cursor:
                sql = "SELECT * FROM expenses WHERE id = %s"
                cursor.execute(sql, (expense_id,))
                expense = cursor.fetchone()

            return render_template('edit_expense.html', expense=expense)
    else:
        return redirect(url_for('login'))

@app.route('/delete_expense', methods=['GET'])
def delete_expense():
    if 'username' and 'dairycode' in session:  # Check if the username is stored in the session
        if request.method == 'GET':
            expense_id = request.args.get('id')

        with connection.cursor() as cursor:
            sql = "DELETE FROM expenses WHERE id = %s"
            cursor.execute(sql, (expense_id))
            connection.commit()

        return redirect('/expences_view')
    else:
        return redirect(url_for('login'))

@app.route('/view_image', methods=['GET', 'POST'])
def view_image():
    if 'username' and 'dairycode' in session:
        if request.method == 'GET':
            expense_id = request.args.get('id')

        with connection.cursor() as cursor:
            sql = "SELECT image FROM expenses WHERE id = %s"
            cursor.execute(sql, (expense_id))
            image = cursor.fetchone()
            # print("image",image[0])
        if image[0] is None:
            image_data = None
            return 'Image not found.'
        # Decode the base64-encoded image data
        encoded_image = image[0]
        image_data = base64.b64encode(encoded_image).decode('utf-8')

        return render_template('view_image.html', image_data=image_data, expense_id=expense_id)
    else:
        return redirect(url_for('login'))

@app.route('/download_image', methods=['GET', 'POST'])
def download_image():
    if 'username' and 'dairycode' in session:
        if request.method == 'GET':
            expense_id = request.args.get('id')

        with connection.cursor() as cursor:
            sql = "SELECT image FROM expenses WHERE id = %s"
            cursor.execute(sql, (expense_id))
            image = cursor.fetchone()

        if image[0] is None:
            return 'Image not found.'

        # Decode the base64-encoded image data
        encoded_image = image[0]
        image_data = base64.b64decode(encoded_image)

        # Create a BytesIO object so that we can write the file contents to it
        img_io = BytesIO(image_data)



        # Seek back to the start of the stream
        img_io.seek(0)

        # Send the file contents and headers to the browser so that it downloads the file as "image.png"
        return send_file(img_io, mimetype='application/octet-stream', as_attachment=True,download_name='image.jpg')
    else:
        return redirect(url_for('login'))

# @app.route('/main_table')
def main_table():
    try:
        with connection.cursor() as cursor:
            sql = "CREATE TABLE IF NOT EXISTS main_dairy (id INT NOT NULL AUTO_INCREMENT, username VARCHAR(200) NOT NULL, email VARCHAR(100) NOT NULL, title VARCHAR(200) NOT NULL, content TEXT NOT NULL, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, images VARCHAR(255), PRIMARY KEY (id), FOREIGN KEY (username) REFERENCES dairy_login(username), FOREIGN KEY (email) REFERENCES dairy_login(email))"
            cursor.execute(sql)
            connection.commit()
        return "Table created: main_dairy"
    except pymysql.err.OperationalError as e:
        return "Error creating table: " + str(e)


@app.route('/create_diary', methods=['GET', 'POST'])
def create_diary():
    if 'username' and 'dairycode' in session:


        if request.method == 'POST':
            # Retrieve form data
            title = request.form['title']
            content = request.form['content']
            username = session['username']
            email = session['email']
            date=request.form['date']

        # Get system timestamp
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Connect to MySQL and execute the INSERT query
            with connection.cursor() as cursor:
                sql = "INSERT INTO main_dairy (username, email, title, content, timestamp,date) VALUES (%s, %s, %s, %s, %s,%s)"
                cursor.execute(sql, (username, email, title, content, current_timestamp,date))
            connection.commit()



            return redirect('/diary')  # Redirect to the diary page after successful entry creation

        return render_template('create_diary.html')
    else:
        return redirect(url_for('login'))

@app.route('/diary', methods=['GET', 'POST'])
def diary():
    if 'username' and 'dairycode' in session:
        username = session['username']
        with connection.cursor() as cursor:
            sql = "SELECT * FROM main_dairy WHERE username = %s ORDER BY timestamp DESC"
            cursor.execute(sql, (username))
            diary = cursor.fetchall()

        return render_template('diary.html', diary=diary, username=username)
    else:
        return redirect(url_for('login'))

@app.route('/edit_diary', methods=['GET', 'POST'])
def edit_diary():
    if 'username' and 'dairycode' in session:
        if request.method == 'POST':
            dairy_id=request.form['dairy_id']
            title = request.form['title']
            content = request.form['content']
            date=request.form['date']

            with connection.cursor() as cursor:
                sql="UPDATE main_dairy SET title=%s,content=%s,date=%s WHERE id=%s"
                cursor.execute(sql, (title, content,date,dairy_id))
                connection.commit()
            return redirect('/diary')
        else:
            dairy_id = request.args.get('id')

            with connection.cursor() as cursor:
                sql = "SELECT * FROM main_dairy WHERE id = %s"
                cursor.execute(sql, (dairy_id,))
                dairy = cursor.fetchone()

            return render_template('edit_diary.html', expense=dairy)
    else:
        return redirect(url_for('login'))

@app.route('/delete_diary', methods=['GET'])
def delete_diary():
    if 'username' and 'dairycode' in session:
        if request.method == 'GET':
            dairy_id = request.args.get('id')

        with connection.cursor() as cursor:
            sql = "DELETE FROM main_dairy WHERE id = %s"
            cursor.execute(sql, (dairy_id))
            connection.commit()

        return redirect('/diary')



if __name__ == '__main__':
    app.run(debug=True)
