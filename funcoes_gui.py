import pyodbc
import sys
import os
from databases import connection_string
import pandas as pd


def empresa_btn(empobra):
    empobras = empobra.get()
    return empobras

def get_column_names(empresa=321):
    connection = pyodbc.connect(connection_string)
    lista_empresas = []
    query = f"""
   select descr_obr,cod_obr from obras where Empresa_obr={empresa};
    """
    query = pd.read_sql(query, connection)
    for i in query.values:
        lista_empresas.append({'desc_obr':i[0], 'cod_obr':i[1]})
    
    return lista_empresas


