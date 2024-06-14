from databases.select import rel_select as relatorio12
from databases.select import *
import pyodbc
from databases.database import connection_string
import pandas as pd

connection = pyodbc.connect(connection_string)
def get_column_names():
    connection = pyodbc.connect(connection_string)
    listaempresas = []
    query = f"""
   select descr_obr,cod_obr from obras where Empresa_obr=245;
    """
    query = pd.read_sql(query, connection)
    for i in query.values:
        listaempresas.append({'desc': i[0], 'cod': i[1]})
    print('Essa é a lista empresas dicionario', listaempresas)
    return listaempresas
connection.close()