from flask import Flask, render_template, jsonify
import time
import threading
import sys

app = Flask(__name__)
config_file = "config.json"

@app.route("/config")
def configure():
    return render_template('config.html', template_name="Jinja2")

@app.route("/save", methods=['POST'])
def save():
    print("Saved")
    return jsonify(success=True) 

def gateway():
    while True:
        time.sleep(5)
        print('Hi there!')

if __name__ == '__main__':
    thread = threading.Thread(target=gateway)
    thread.daemon = True
    thread.start()
    app.run(debug=True)