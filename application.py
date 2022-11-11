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


def login_user(user, remember):
    pass


class User:
    query = None


class SigninForm:
    def __init__(self):
        self.password = None
        self.username = None

    def validate_on_submit(self):
        pass


@app.route("/signin", methods=['GET','POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=True)
            session.permanent = True
            if user.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('signin.html', form=form, title='Login')

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
