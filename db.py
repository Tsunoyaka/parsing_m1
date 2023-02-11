from peewee import *
from decouple import config

db = PostgresqlDatabase(config('DB_NAME'))

class Hotel(Model):
    title = CharField(max_length=300)
    image = CharField(max_length=500, null=True)
    price = SmallIntegerField(null=True)
    date_ = CharField(max_length=20)

    class Meta:
        database = db 


if __name__ == '__main__':
    db.create_tables([Hotel])



