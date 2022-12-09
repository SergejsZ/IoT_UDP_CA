import bcrypt
from flask import render_template

from __init__ import db
from pymongo import MongoClient

ACCESS = {
    'guest': 0,
    'user': 1,
    'admin': 2
}


# def bool_to_int(v):
#     if 'true' in str(v):
#         return 1
#     elif 'false' in str(v):
#         return 0
#     else:
#         raise ValueError


class User(db.Document):
    user_id = db.FieldString()
    name = db.FieldString()
    email = db.FieldString()
    password = db.FieldBinary()
    access_lvl = db.FieldInt()

    def __init__(self, user_id, name, email, password, access_lvl=ACCESS['user']):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.access_lvl = access_lvl

    def is_admin(self):
        return self.access == ACCESS['admin']

    def allowed(self, access_level):
        return self.access >= access_level


def delete_all():
    try:
        User.objects({}).delete()
        print("Delete All Done!")
    except Exception as e:
        print("failed " + str(e))


def register_user(name, email, password1, password2):
    email_found = User.find_one({"email": email})
    if email_found:
        message = 'This email already exists in database'
        return render_template('register.html', message=message)
    if password1 != password2:
        message = 'Passwords should match!'
        return render_template('register.html', message=message)
    else:
        hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
        user_input = {'name': name, 'email': email, 'password': hashed, 'access_lvl': 1}
        User.insert(user_input)


def get_user_row_if_exists(user_id):
    get_user_row = User.objects(user_id=user_id).first()
    if get_user_row is not None:
        return get_user_row
    else:
        print("user doesn't exists")
        return False


def add_user_and_login(name, user_id, email, password):
    row = get_user_row_if_exists(user_id)
    print("Adding User " + name)
    User(user_id=user_id, name=name, email=email, password=password, access_lvl=ACCESS['user']).save()


def user_logout(email):
    row = get_user_row_if_exists(email)
    if row is not False:
        row.update(login=0)
        print("user " + row.name + " logged out")


def view_all():
    for user in User.objects():
        print(str(user.id) + " | " +
              str(user.user_id) + " | " +
              user.name + " | " +
              str(user.email) + " | " +
              str(user.password) + " | ")

        

