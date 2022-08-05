from flask import Flask, render_template, jsonify, request, json, redirect, url_for, make_response
import time
import threading
from gateway import Gateway
from os.path import exists
from hashlib import blake2b
import random
import jwt

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
    try:
        token = cookies.get("JWT")
        decoded = jwt.decode(token, JWT_KEY, algorithms=[JWT_ALGO])
        return True
    except:
        return False

@app.route("/logout", methods=["POST"])
def logout():
    res = redirect(url_for("logout"))
    res.delete_cookie("JWT")
    return res

@app.route("/login")
def login():
    if jwtVerify(request.cookies):
        return redirect(url_for("configure"))
    else:
        return render_template('login.html', template_name="Jinja2")

@app.route("/config")
def configure():
    if jwtVerify(request.cookies):
        units = []
        if exists(config_file):
            with open(config_file, 'r') as f:
                units = json.load(f)
                gateway.units = units
                # print(units)
        return render_template('config.html', units=units, template_name="Jinja2")
    else:
        return redirect(url_for("login"))

@app.route("/save", methods=['POST'])
def save():
    units = json.loads(request.data)
    with open(config_file, 'w') as f:
        json.dump(units, f)
    return jsonify(success=True)

@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    username = request.form['username']
    password = request.form['password']
    with open(users_file, 'r') as f:
        users = json.load(f)
        for key in users:
            h = blake2b()
            h.update(str.encode(username))
            if key == h.hexdigest():
                h = blake2b()
                h.update(str.encode(password))
                if users[key] == h.hexdigest():
                    res = redirect(url_for('configure'))
                    res.set_cookie("JWT", jwtSign(username))
                    return res
                    #return redirect(url_for('configure'))
    return render_template('login.html')

def modbus_worker():
    gateway.loop()

if __name__ == '__main__':
    thread = threading.Thread(target=modbus_worker)
    thread.daemon = True
    thread.start()

    app.run(debug=True)
