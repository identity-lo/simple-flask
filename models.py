from peewee import *

db = SqliteDatabase("mydatabase.db")

class User(Model):
    username = TextField()
    email = TextField()
    password = TextField()
    photo = TextField(default="")

    class Meta:
        database = db

class Post(Model):
    title = TextField()
    description = TextField()
    author = TextField(ForeignKeyField(User))
    class Meta:
        database = db