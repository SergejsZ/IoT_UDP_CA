import json

from flask import Flask, render_template, request, url_for, redirect, session, abort
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import pymongo
import bcrypt
import qrcode
import base64
import os
import pathlib
import requests

# models
from . import user
# import bus

app = Flask(__name__)
app.secret_key = "testing"
client = pymongo.MongoClient("mongodb+srv://admin:0xIIagmADdNCgowK@cluster0.3aqrglf.mongodb.net/?retryWrites=true&w"
                             "=majority")
db = client.get_database('T4U')
users = db.users
buss = db.buses
tickets = db.tickets

GOOGLE_CLIENT_ID = "806422887626-sum7vf05g9277fk14dectaiaqee34mbo.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file,
                                     scopes=["https://www.googleapis.com/auth/userinfo.profile",
                                             "https://www.googleapis.com/auth/userinfo.email", "openid"],
                                     redirect_uri="https://dawidiot22.tk/callback"
                                     )

alive = 0
data = {}


@app.route("/sensor")
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data['keep_alive'] = keep_alive_count
    parsed_json = json.dumps(data)
    print(parsed_json)
    return render_template('sensor.html'), str(parsed_json)


@app.route("/register", methods=['post', 'get'])
def register():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        name = request.form.get("fullname")
        email = request.form.get("email")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user.register_user(name,email,password1,password2)

        user_data = users.find_one({"email": email})
        new_email = user_data['email']

        return redirect(url_for("logged_in", email=new_email))
    return render_template('register.html')


@app.route('/logged_in')
def logged_in():
    return render_template('logged_in.html')


@app.route("/", methods=["POST", "GET"])
def index():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        email_found = users.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('index.html', message=message)
        else:
            message = 'Email not found'
            return render_template('index.html', message=message)
    return render_template('index.html', message=message)


@app.route("/logout")  # the logout page and function
def logout():
    session.clear()
    return redirect("/")


@app.route("/buses", methods=["POST", "GET"])
def buses():
    # Get all bus records
    all_bus = buss.find()

    return render_template('buses.html', buses=all_bus)


def generate_qr():
    # QR Code Generator (Temp hardcoded)
    id_bus = buss.find_one({}, {'_id': 1})
    user = users.find_one({}, {'name': 1, '_id': 0})
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)
    free_image = [id_bus, user]
    qr.add_data(free_image)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('qrcode001.png')

    # Encoding the Image with base64
    with open("qrcode001.png", "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
        print(my_string)


# Google login auth
def login_is_required(function):  # a function to check if the user is authorized or not
    def wrapper(*args, **kwargs):
        if "google_id" not in session:  # authorization required
            return abort(401)
        else:
            return function()

    return wrapper


@app.route("/google_login")  # the page where the user can login
def google_login():
    authorization_url, state = flow.authorization_url()  # asking the flow class for the authorization (login) url
    session["state"] = state
    return redirect(authorization_url)


@app.route(
    "/callback")  # this is the page that will handle the callback process meaning process after the authorization
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")  # defing the results to show on the page
    session["name"] = id_info.get("name")
    return redirect("/logged_in")  # the final page where the authorized users will end up


@app.route("/mytickets", methods=['post', 'get'])
def mytickets():
    return render_template('mytickets.html')


# end of code to run it
if __name__ == "__main__":
    app.run(debug=True, port=5000)