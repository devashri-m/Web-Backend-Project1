from flask import Flask, render_template, request, redirect, session, abort, make_response, jsonify
import pymysql
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
import re
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

# CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

upload_folder = 'C:/Users/devashri\Desktop/flask_api_project/upload_folder'
app.config["SECRET_KEY"] = 'af8d0c819f19479bb50f8e28c4b17f2c';
app.config['UPLOAD_PATH'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = {'.jpeg', '.pdf', '.png'}

# To connect MySQL database
conn = pymysql.connect(
    host='localhost',
    user='devashri',
    password="Shree@199",
    db='web_backend_project',
    cursorclass=pymysql.cursors.DictCursor
)
cur = conn.cursor()


# JWT token for APIs are validated
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            data = request.headers["Authorization"]
            token = str.replace(str(data), "Bearer ", "")  # Token is extracted
        if not token:
            return make_response(jsonify({'Alert!': 'token is missing', 'statusCode': 401}),
                                 401)  # HTTP Status code 401 unauthorized
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])  #payload decoded from token
        except:
            return make_response(jsonify({'Alert!': 'Token is invalid', 'statusCode': 401}), 401)
        return func(*args, **kwargs)

    return decorated


# To Register users with Username, Password and Email address
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email':
        print('reached')
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cur.execute('SELECT * FROM users WHERE username = % s', (username,))
        user = cur.fetchone()
        print(user)
        conn.commit()
        if user:
            return abort(400, {'message': 'User already exist !'})  # HTTP Bad Request Error Code 400
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return abort(400, {'message': 'Invalid email address !'})
        elif not re.match(r'[A-Za-z0-9]+', username):
            return abort(400, {'message': 'name must contain only characters and numbers !'})
        else:
            cur.execute('INSERT INTO users VALUES (NULL, % s, % s, % s)',
                        (username, password, email))
            conn.commit()
            msg = 'You have successfully registered !'
            response_code = 201  # HTTP Created 201 Status code
            return make_response(jsonify({'message': msg, 'statusCode': response_code}), 201)
    elif request.method == 'POST':
        return abort(400, {'message': 'Please fill out the form !'})


# Login Users with Username and Password
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password,))
        conn.commit()
        user = cur.fetchone()
        if user:
            session['loggedin'] = True
            # Create JWT for Login 
            token = jwt.encode({
                'username': username,
                'expiration': str(datetime.utcnow() + timedelta(minutes=10))
            }, app.config['SECRET_KEY'])

            msg = 'Logged in successfully !'
            return jsonify({'token': token, 'message': msg})
        else:
            msg = 'Incorrect username / password !'
            return make_response({'message': msg}, 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed"'})


# To enter student details for university admission
@app.route('/student_admission', methods=['POST'])
@token_required
def student_admission():
    if request.method == 'POST' and 'fullName' in request.form and 'phoneNumber' in request.form and 'email' in request.form and 'state' in request.form and 'city' in request.form and 'area' in request.form and 'postalcode' in request.form and 'date_of_birth' in request.form and 'Current_CGPA' in request.form:
        fullname = request.form['fullName']
        phonenumber = request.form['phoneNumber']
        email = request.form['email']
        date = request.form['date_of_birth']
        cgpa = request.form['Current_CGPA']
        city = request.form['city']
        state = request.form['state']
        area = request.form['area']
        postalcode = request.form['postalcode']

        cur.execute('INSERT INTO student_admissions VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s)',
                    (fullname, phonenumber, email, date, cgpa, area, city, state, postalcode,))
        conn.commit()
        return make_response('Admission Form Submitted Successfully', 201)
    else:
        return make_response('Invalid request fields', 400)


# Upload file for upload extensions 
@app.route('/upload', methods=['POST'])
@token_required
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400, {'message': 'Unsupported file extension !'})
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        return make_response('Upload Successful', 200)


@app.route('/public', methods=['GET'])
def public():
    return make_response('No Login Required!!!', 200)


# Request APTs in 5000 port with host=localhost
if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))
