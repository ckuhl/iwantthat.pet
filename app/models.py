from peewee import *


Database = SqliteDatabase('database.sqlite3',
        pragmas=(('foreign_keys', 'on'),))

class BaseModel(Model):
    class Meta:
        database = Database


class Subscriber(BaseModel):
    """
    A person who has subscribed to notifications
    """
    sub_id = PrimaryKeyField()
    email = CharField()
    verified = BooleanField()


class Animal(BaseModel):
    """
    An animal someone wants updates about
    """
    animal_id = PrimaryKeyField()
    rspca_id = IntegerField()
    name = CharField()


class Subscription(BaseModel):
    """
    Linking table between Animals and Subscribers

    One subscriber has many animals
    """
    sub_id = ForeignKeyField(Subscriber, related_name='subs')
    animal_id = ForeignKeyField(Animal, related_name='subs')

