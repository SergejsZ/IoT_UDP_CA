from .application import db
import pymongo

ACCESS = {
    'guest': 0,
    'user': 1,
    'admin': 2
}


def bool_to_int(v):
    if 'true' in str(v):
        return 1
    elif 'false' in str(v):
        return 0
    else:
        raise ValueError


class User(db.Document):
    name = db.StringField()
    email = db.StringField()
    password = db.BinaryField()
    access_lvl = db.IntField()

    def __init__(self, _id, name, email, password, access_lvl=ACCESS['user']):
        self._id = _id
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


def getUserRowIfExists(email):
    get_user_row = User.objects(email=email).first()
    if (get_user_row != None):
        return get_user_row
    else:
        print("user doesn't exists")
        return False


def addUserAndLogin(name, email, password):
    row = getUserRowIfExists(email)
    print("Adding User " + name)
    User(name=name, email=email, password=password, access_lvl=ACCESS['user'])


def userLogout(email):
    row = getUserRowIfExists(email)
    if (row != False):
        row.update(login=0)
        print("user " + row.name + " logged out")


