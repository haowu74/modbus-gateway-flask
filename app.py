from flask import Flask, render_template, jsonify
import time
import threading
import sys
from gateway import Gateway

app = Flask(__name__)
config_file = "config.json"
gateway = Gateway()

@app.route("/config")
def configure():
    return render_template('config.html', template_name="Jinja2")

@app.route("/save", methods=['POST'])
def save():
    print("Saved")
    return jsonify(success=True) 

def modbus_worker():
    gateway.loop()

if __name__ == '__main__':
    thread = threading.Thread(target=modbus_wworker)
    thread.daemon = True
    thread.start()
    app.run(debug=True)
