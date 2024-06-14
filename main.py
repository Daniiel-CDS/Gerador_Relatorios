import logging
from databases.select import rel_select
from databases.select import *
import pyodbc
from databases.database import connection_string
import pandas as pd
import datetime 
import os

def execute_main(data1, data2, valor, valor_nome):
    data_e_hora_atuais = datetime.datetime.now()
    data = data_e_hora_atuais.strftime(fr"%d-%m-%Y %H-%M")
    data = str(data)
    log_file = f'loggerador.txt'
    logging.basicConfig(level=logging.INFO, filename=log_file, filemode='a',
                        format='%(asctime)s - %(levelname)s - %(message)s', encoding='UTF-8')
    

    data_inicio = data1
    data_termino = data2
    print(data_inicio, "começa\n", data_termino,'Fim' )
    print(f'data inicial é :{data_inicio}, e data final = {data_termino}')
    print('O valor é ', valor)
    logging.info(f'data inicial é :{data_inicio}, e data final = {data_termino}')
    prazocompra = 0
    origem = '0'
    pedidoatendimento = '0'
    simulacao = 0
    connection = pyodbc.connect(connection_string)
    empresaobra = valor

    print("Conectando ao banco de dados...")
    logging.info("Conectando ao banco de dados...")
    connection = pyodbc.connect(connection_string)
    print("Conexão estabelecida.")
    logging.info("Conexão estabelecida.")
    print(data)

    # Criando um cursor para executar consultas SQL
    cursor = connection.cursor()
    print("Cursor criado.")
    logging.info("Cursor criado.")

    # Executando a query e pegando os resultados em um DataFrame
    print("Executando a query SQL...")
    logging.info("Executando a query SQL...")
    try:
        df = pd.read_sql(rel_select(data_inicio=data_inicio, data_termino=data_termino, empresaobra=empresaobra, pedidoatendimento=pedidoatendimento, origem=origem, prazocompra=prazocompra, simulacao=simulacao), connection)
        print("Query executada com sucesso.")
        print(datetime.datetime.now().strftime('%H:%M:%S'))
        logging.info("Query executada com sucesso.")
    except Exception as e:
        # print(f"Erro ao executar a query: {e}")
        logging.info(f"Erro ao executar a query: {e}")

    # Verificar se o DataFrame contém dados
    if not df.empty:
        print(datetime.datetime.now().strftime('%H:%M:%S'))
        print("Dados encontrados, exportando para Excel...")
        logging.info("Dados encontrados, exportando para Excel...")
        # Exportar para Excel
        caminho = f'relatorios/{valor_nome}'
        caminho_usuario = os.path.expanduser('~') + fr'\Desktop'
        relatorios = caminho_usuario + fr'\relatorios'
        try:
            os.chdir(relatorios)
            print(f'o Diretorio {relatorios} já existia \nseguindo com o codigo')
        except FileNotFoundError as e:
            print(f'O caminho {e} não existia mas já foi criado')
            os.chdir(caminho_usuario)
            os.mkdir('relatorios')
        output_file_path = fr"{relatorios}\Relatorio_{str(data)}.xlsx"
        df = df[[ 'CodObra', 'Pedido', 'Cotação', 'UnidIns', 'Insumo',
       'QtdeIns', 'Data do Pedido', 'Usr. Conf.', 'DataCompra', 'Usr. Compra',
       'DataEntrega', 'Usr. Entrega','DataSegEntrega',
       'UsrSegEntrega', 'DataEntregaPed', 'Excluído',
       'DataAprovSimulacao', 'Usr. Aprov.', 'DataSimulacaoObra',
       'Usr. Sim. Obra', 'DataPedido', 'Usr. Ped.','OC', 'ValorOC', 'Fornecedor']]
        df.rename(columns={'QtdeIns': 'Quantidade'}, inplace = True)
        df.to_excel(output_file_path, index=False)
        print(f"Relatório exportado para {output_file_path}")
        logging.info(f"Relatório exportado para {output_file_path}")
        return True
    else:
        print("Nenhum dado encontrado para o período especificado.")
        logging.info("Nenhum dado encontrado para o período especificado.")
        return False

    # Fechando a conexão
    connection.close()
    print("Conexão fechada.")
    logging.info("Conexão fechada.")
if __name__ == "__main__":
    execute_main()
