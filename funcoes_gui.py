import pyodbc
import sys
import os
from databases import connection_string
import pandas as pd


def empresa_btn(empobra):
    empobras = empobra.get()
    return empobras

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
    

