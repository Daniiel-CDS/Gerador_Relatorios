from databases.select import rel_select
from databases.select import *
import pyodbc
from databases.database import connection_string
import pandas as pd
import datetime 
from GUI.gui import data1, data2, valor
data_e_hora_atuais = datetime.datetime.now()
data = data_e_hora_atuais.strftime("%d-%m-%Y %H_%M")
data = str(data)

print(data1, data2, valor)

data_inicio = data1
data_termino = data2
prazocompra=0
origem = '0'
pedidoatendimento = '0'
simulacao = 0
empresaobra = valor[1]
# Conectando ao banco de dados
print("Conectando ao banco de dados...")
connection = pyodbc.connect(connection_string)
print("Conexão estabelecida.")
print(data)

# Criando um cursor para executar consultas SQL
cursor = connection.cursor()
print("Cursor criado.")

# Executando a query e pegando os resultados em um DataFrame
print("Executando a query SQL...")
try:
    df = pd.read_sql(rel_select(data_inicio=data_inicio,data_termino=data_termino,empresaobra=empresaobra,pedidoatendimento=pedidoatendimento,origem=origem,prazocompra=prazocompra,simulacao=simulacao), connection)
    print("Query executada com sucesso.")
except Exception as e:
    print(f"Erro ao executar a query: {e}")

# Verificar se o DataFrame contém dados
if not df.empty:
    print("Dados encontrados, exportando para Excel...")
    # Exportar para Excel
    output_file_path = 'relatorio'+ str(data) +  '.xlsx'
    df.to_excel(output_file_path, index=False)
    print(f"Relatório exportado para {output_file_path}")
else:
    print("Nenhum dado encontrado para o período especificado.")

# Fechando a conexão
connection.close()
print("Conexão fechada.")