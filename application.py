from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt
import qrcode
import base64

app = Flask(__name__)
app.secret_key = "testing"
client = pymongo.MongoClient("mongodb+srv://admin:0xIIagmADdNCgowK@cluster0.3aqrglf.mongodb.net/?retryWrites=true&w"
                             "=majority")
db = client.get_database('T4U')
users = db.users
bus = db.buses
tickets = db.tickets

ACCESS = {
    'guest': 0,
    'user': 1,
    'admin': 2
}


@app.route("/register", methods=['post', 'get'])
def register():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_found = users.find_one({"name": user})
        email_found = users.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('register.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('register.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('register.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed, 'access_lvl': ACCESS['user']}
            users.insert_one(user_input)

            user_data = users.find_one({"email": email})
            new_email = user_data['email']

            return redirect(url_for("logged_in", email=new_email))
    return render_template('register.html')


@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('logged_in.html', email=email)
    else:
        return redirect(url_for("index"))


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


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


@app.route("/buses", methods=["POST", "GET"])
def buses():
    all_bus = bus.find()
    id_bus = bus.find_one({}, {'_id': 1})
    user = users.find_one({}, {'name': 1, '_id': 0})
    print(id_bus)
    print(user)
    # input_data = "https://towardsdatascience.com/face-detection-in-10-lines-for-beginners-1787aa1d9127"
    # Creating an instance of qrcode
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)
    free_image = [id_bus, user]
    qr.add_data(free_image)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('qrcode001.png')
    with open("qrcode001.png", "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
    # img = qrcode.make(id_bus, user)
    # img.save('qrcode001.png')
    return render_template('buses.html', buses=all_bus, qr=my_string)


# end of code to run it
if __name__ == "__main__":
    app.run(debug=True)
