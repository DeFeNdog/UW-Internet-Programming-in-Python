import os

from peewee import Model, CharField, FloatField, ForeignKeyField
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///mailroom.db'))


class Donor(Model):
    """
    This class defines the Donor model
    """
    code = CharField(max_length=255, primary_key=True, unique=True)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)

    class Meta:
        database = db


class Donation(Model):
    """
    This class defines Donations model.
    """
    donation = FloatField()
    donor = ForeignKeyField(Donor, field='last_name', null=False)

    class Meta:
        database = db
