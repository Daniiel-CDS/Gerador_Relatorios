import peewee as pw
from databases.database import db

def create_dynamic_model(table_name):
    class Meta:
        database = db
        table_name = table_name

    attrs = {'Meta': Meta}
    return type(table_name, (pw.Model,), attrs)