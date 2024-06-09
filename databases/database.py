import peewee as pw
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('USERNAME')
DB_PASS = os.getenv('PASSWORD')
DB_HOST = os.getenv('HOST')
DB_DATABASE = os.getenv('DATABASE')

connection_string = f'DRIVER=SQL Server;SERVER={DB_HOST};DATABASE={DB_DATABASE};UID={DB_USER};PWD={DB_PASS};'
