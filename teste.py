from databases.select import rel_select 
import pandas as pd
import pyodbc
from databases.database import connection_string

data_inicio ='2024-04-01 '
data_termino = '2024-06-10'
prazocompra = 0
origem = '0'
pedidoatendimento = '0'
simulacao = 0
empresaobra = '245|237OB'
connection = pyodbc.connect(connection_string)
df = pd.read_sql(rel_select(data_inicio=data_inicio, data_termino=data_termino, empresaobra=empresaobra, pedidoatendimento=pedidoatendimento, origem=origem, prazocompra=prazocompra, simulacao=simulacao), connection)
df = df[['CodObra','Pedido','Cotação','UnidIns','Insumo', 'QtdeIns','Data do Pedido', 'Usr. Conf.', 'Excluído']]
print(df.head())