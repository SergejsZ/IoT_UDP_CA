import bcrypt
from flask import render_template

# from __init__ import db
import pymongo
from config import config
client = pymongo.MongoClient(config.get("mongodb_uri"))
db = client.get_database('T4U')
users = db.users
buss = db.buses
tickets = db.tickets


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


def delete_all():
    try:
        users.objects({}).delete()
        print("Delete All Done!")
    except Exception as e:
        print("failed " + str(e))


def register_user(name, email, password1, password2):
    email_found = users.find_one({"email": email})
    if email_found:
        message = 'This email already exists in database'
        return render_template('register.html', message=message)
    if password1 != password2:
        message = 'Passwords should match!'
        return render_template('register.html', message=message)
    else:
        hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
        user_input = {'name': name, 'email': email, 'password': hashed, 'access_lvl': 1}
        users.insert_one(user_input)


def get_user_row_if_exists(user_id):
    get_user_row = users.objects(user_id=user_id).first()
    if get_user_row is not None:
        return get_user_row
    else:
        print("user doesn't exists")
        return False


def add_user_and_login(name, user_id, email, password):
    row = get_user_row_if_exists(user_id)
    print("Adding User " + name)
    users(user_id=user_id, name=name, email=email, password=password, access_lvl=ACCESS['user']).save()


def user_logout(email):
    row = get_user_row_if_exists(email)
    if row is not False:
        row.update(login=0)
        print("user " + row.name + " logged out")


def view_all():
    for user in users.objects():
        print(str(user.id) + " | " +
              str(user.user_id) + " | " +
              user.name + " | " +
              str(user.email) + " | " +
              str(user.password) + " | ")

        

