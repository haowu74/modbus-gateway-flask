from crypt import methods
from sre_constants import SUCCESS
from flask import Flask, render_template, jsonify, request, json, redirect, url_for, make_response, send_file, flash
import time
import threading
from gateway import Gateway
from os.path import exists
from hashlib import blake2b
import random
import jwt
import os

app = Flask(__name__)
config_file = "config.json"
users_file = "users.json"
gateway = Gateway(config_file)

HOST_NAME = "localhost"
HOST_PORT = 80
JWT_KEY = "!s3cur!ty321"
JWT_ISS = "isecurity.com.au"
JWT_ALGO = "HS512"

def jwtSign(username):
    rnd = "".join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz~!@#$%^_-") for i in range(24))
    now = int(time.time())
    return jwt.encode({
        "iat": now,
        "nbf": now,
        "exp": now + 3600,
        "jti": rnd,
        "iss": JWT_ISS,
        "data": {"username": username}
        }, JWT_KEY, algorithm=JWT_ALGO)

def jwtVerify(cookies):
    current_user = ""
    try:
        token = cookies.get("JWT")
        decoded = jwt.decode(token, JWT_KEY, algorithms=[JWT_ALGO])
        current_user = decoded['data']['username']
        return current_user
    except:
        return ""

@app.route("/logout", methods=["POST"])
def logout():
    res = redirect(url_for("logout"))
    res.delete_cookie("JWT")
    return res

@app.route("/login")
def login():
    if jwtVerify(request.cookies) != "":
        return redirect(url_for("configure"))
    else:
        return render_template('login.html', template_name="Jinja2")

@app.route("/")
@app.route("/config")
def configure():
    current_user = jwtVerify(request.cookies) 
    if current_user != "":
        units = []
        if exists(config_file):
            with open(config_file, 'r') as f:
                units = json.load(f)
                gateway.units = units
        is_admin = current_user == "admin"
        return render_template('config.html', units=units, is_admin=is_admin, template_name="Jinja2")
    else:
        return redirect(url_for("login"))

@app.route("/admin")
def admin():
    current_user = jwtVerify(request.cookies)
    if current_user == "admin":
        users = []
        usernames = []
        license_hint = getserial()
        islocked = True
        if exists(users_file):
            with open(users_file, 'r') as f:
                users = json.load(f)
                usernames = [x for x in users]
        return render_template('admin.html', usernames=usernames, islocked=islocked, license_hint=license_hint, template_name='Jinja2')
    else:
        return redirect(url_for("login"))

@app.route("/save", methods=['POST'])
def save():
    units = json.loads(request.data)
    with open(config_file, 'w') as f:
        json.dump(units, f)
        gateway.units = units
    return jsonify(success=True)

@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    username = request.form['username']
    password = request.form['password']
    with open(users_file, 'r') as f:
        users = json.load(f)
        for key in users:
            if key == username:
                h = blake2b()
                h.update(str.encode(password))
                if users[key] == h.hexdigest():
                    res = redirect(url_for('configure'))
                    res.set_cookie("JWT", jwtSign(username))
                    return res
                    #return redirect(url_for('configure'))
    return render_template('login.html')

@app.route('/download', methods=['POST'])
def download():
    return send_file(config_file, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload():
    print('upload')
    if 'file' not in request.files:
        return jsonify(success=False)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    print(file.filename)
    if file.filename == '':
        return jsonify(success=False)
    if file and file.filename == 'config.json':
        file.save(file.filename)
        print('config uploaded')
        return jsonify(success=True)
    return jsonify(success=False)

@app.route('/addnewuser', methods=['POST'])
def add_new_user():
    user = json.loads(request.data)
    username = user['username']
    password = user['password']
    with open(users_file, 'r+') as f:
        users = json.load(f)
        for key in users:
            if key == username:
                #user exist
                return jsonify(success=False)
            
        h = blake2b()
        h.update(str.encode(password))
        users[username] = h.hexdigest()
        f.seek(0)
        json.dump(users, f)
    return jsonify(success=True)

@app.route('/changepassword', methods=['POST'])
def change_password():
    user = json.loads(request.data)
    username = user['username']
    password = user['password']
    with open(users_file, 'r+') as f:
        users = json.load(f)
        for key in users:
            if key == username:
                #user found
                h = blake2b()
                h.update(str.encode(password))
                users[username] = h.hexdigest()
                f.seek(0)
                json.dump(users, f)
                return jsonify(success=True)
    return jsonify(success=False)

@app.route('/deleteuser', methods=['POST'])
def delete_user():
    user = json.loads(request.data)
    username = user['username']
    with open(users_file, 'r') as f:
        users = json.load(f)
        user_found = False
        for key in users:
            if key == username:
                #user found
                user_found = True
    if user_found:
        with open(users_file, 'w') as f:
            users.pop(username)
            json.dump(users, f)
            return jsonify(success=True)
    return jsonify(success=False)

def modbus_worker(islocked):
    gateway.loop(islocked)

def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        with open('/proc/cpuinfo','r') as f:
            for line in f:
                if line[0:6]=='Serial':
                    cpuserial = line[10:26]
    except:
        cpuserial = "ERROR000000000"
    return cpuserial

def check_license():
    # generate public and private key from the ((serial number) combining (our secret ))
    # encrypt our secret message using public key to get the license number
    # RPi uses private key to decrypt the license number
    # save the license code to a license file
    # every time start the web server, it checks the content of the license file. 
    return False

if __name__ == '__main__':
    islocked = not check_license()
    thread = threading.Thread(target=modbus_worker, args=(islocked,))
    thread.daemon = True
    thread.start()
    app.secret_key = 'isecurity_modbus'
    app.run(debug=True, host='0.0.0.0', port=3000)
