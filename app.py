from flask import Flask, render_template, jsonify, request, json
import time
import threading
from os.path import exists

app = Flask(__name__)
config_file = "config.json"
users_file = "./users.json"

@app.route("/login")
def login():
    return render_template('login.html', template_name="Jinja2")

@app.route("/config")
def configure():
    units = []
    if exists(config_file):
        with open(config_file, 'r') as f:
            units = json.load(f)
            # print(units)
    return render_template('config.html', units=units, template_name="Jinja2")

@app.route("/save", methods=['POST'])
def save():
    units = json.loads(request.data)
    with open(config_file, 'w') as f:
        json.dump(units, f)
    return jsonify(success=True) 

def gateway():
    while True:
        time.sleep(5)
        print('Gateway worker.')

if __name__ == '__main__':
    thread = threading.Thread(target=gateway)
    thread.daemon = True
    thread.start()

    app.run(debug=True)