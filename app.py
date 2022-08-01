from flask import Flask, render_template, jsonify, request, json
import time
import threading
from gateway import Gateway
from os.path import exists

app = Flask(__name__)
config_file = "config.json"
users_file = "./users.json"

gateway = Gateway(config_file)

@app.route("/login")
def login():
    return render_template('login.html', template_name="Jinja2")

@app.route("/config")
def configure():
    units = []
    if exists(config_file):
        with open(config_file, 'r') as f:
            units = json.load(f)
            gateway.units = units
            # print(units)
    return render_template('config.html', units=units, template_name="Jinja2")

@app.route("/save", methods=['POST'])
def save():
    units = json.loads(request.data)
    with open(config_file, 'w') as f:
        json.dump(units, f)
    return jsonify(success=True) 

def modbus_worker():
    gateway.loop()

if __name__ == '__main__':
    thread = threading.Thread(target=modbus_worker)
    thread.daemon = True
    thread.start()

    app.run(debug=True)
