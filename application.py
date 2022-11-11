from flask import Flask, request, json, session, flash, url_for
from flask import render_template
from werkzeug.utils import redirect

app = Flask(__name__)
app.debug = True

alive = 0
data = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signin", methods=['GET','POST'])
def signin():
    return render_template('signin.html')

@app.route("/singin", methods=['GET','POST'])
def guest():
    return redirect("/")
@app.route("/register", methods=['GET','POST'])
def register():
    return render_template('register.html')


def validateUser(username, password, confirmPassword):
    return True

@app.route("/keep_alive")
def keep_alive():
    global alive, data
    alive +=1
    keep_alive_count = str(alive)
    data['keep_alive'] = keep_alive_count
    parsed_json = json.dumps(data)
    print(parsed_json)
    return str(parsed_json)

app.run( port = 5000)


if __name__ == '__application__':
    app.run()
