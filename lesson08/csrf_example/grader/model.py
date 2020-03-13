import os

from peewee import Model, CharField, IntegerField
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.db'))

class Grade(Model):
    student = CharField(max_length=128)
    assignment = CharField(max_length=128)
    grade = CharField(max_length=128) 

    class Meta:
        database = db
