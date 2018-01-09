from peewee import *


db = SqliteDatabase('site.db')

class Subscriber(Model):
    """
    A person who has subscribed to notifications
    """
    id = IntegerField()
    email = CharField()
    verified = BooleanField()

    class Meta:
        database = db

class Animal(Model):
    """
    An animal someone wants updates about
    """
    id = IntegerField()
    animal_id = IntegerField()
    name = CharField()

    class Meta:
        database = db


class Subscription(Model):
    """
    Linking table between Animals and Subscribers

    One subscriber has many animals
    """
    subscriber = ForeignKeyField(Subscriber, related_name='id')
    animal = ForeignKeyField(Animal, related_name='id')

