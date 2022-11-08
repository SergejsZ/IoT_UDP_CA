from flask import Flask, render_template
import json

app = Flask(__name__)

alive = 0
data = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/keep_alive")
def keep_alive():
    global alive, data
    alive +=1
    keep_alive_count = str(alive)
    dta['keep_alive'] = keep_alie_count
    parsed_json = json.dumps(data)
    print(parsed_json)
    return str(parsed_json)

app.run( port = 5000)
