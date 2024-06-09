from databases.select import rel_select as relatorio12
from databases.select import *
import pyodbc
from databases.database import connection_string
import pandas as pd

connection = pyodbc.connect(connection_string)
def get_column_names(table_name):
    query = f"""
    SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = '{table_name}';
    """
    return pd.read_sql(query, connection)

# Obter os nomes das colunas das tabelas de interesse
tabelas = ['ItensCot_Temp','ItensCotServ_Temp', 'AprovacaoPedMat', 'fn_ListEmpObr','OrdemCompra','ItensOrdemCompra','Aprovacao']
colunas = {}

for tabela in tabelas:
    colunas[tabela] = get_column_names(tabela)

# Mostrar os nomes das colunas
for tabela, colunas_tabela in colunas.items():
    print(f"Tabela: {tabela}")
    print(colunas_tabela)
    print("\n")

# Fechar a conexão
connection.close()