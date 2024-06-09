data_inicio = '2024-01-05'
data_termino='2024-06-06'

#Parametros = DATA-IN ,DATA-TER, EMPRESAOBRA(), 
# ORIGEM(Origem dos dados (0=no período; 1=anterior ao período; 0,1=todos). ), 
# PEDIDOADIANTAMENTO(Buscar pedidos originados de adiantamento de contrato (0=não, 1=sim).),
# PRAZO COMPRA(Prazo para o fechamento da compra (apenas para o layout)
# SIMULACAO(Prazo para geração da O.C. (apenas para o layout 10). );


def rel_select(data_inicio, data_termino, empresaobra, pedidoatendimento, origem, prazocompra, simulacao):
    return f"""
    SELECT Resulta.*, 
        CAST('{data_inicio}' AS DATETIME) [DataInicial], 
        CAST('{data_termino}' AS DATETIME) [DataFinal], 
        CAST(CodEmp AS VARCHAR) + ' - ' + UPPER(Desc_Emp) [Empresa], 
        CodObra + ' - ' + UPPER(Descr_Obr) [Obra], 
        UPPER(Nome_Pes) [Fornecedor],
        COALESCE(PendenteEnt, PendEnt) AS PendDtEntrega
    FROM 
    ( 
        SELECT *, 
            CASE WHEN Cod_Ped IS NULL THEN 0 ELSE 1 END [PedidoAdiantamento] 
        FROM 
        ( 
            SELECT CodEmp, CodObra, Pedido, Cotação, UnidIns, CodIns, 
                UPPER(CodIns + ' - ' + Insumo) [Insumo], 
                Qtde_Temp [QtdeIns], 
                CAST([Data do Pedido] AS DATETIME) [Data do Pedido], 
                [Usr. Conf.], 
                CAST(DataCompra AS DATETIME) [DataCompra], 
                [Usr. Compra], 
                CAST(DataEntrega AS DATETIME) [DataEntrega], 
                [Usr. Entrega], 
                QtdeEntrega,
                CAST(DataSegEntrega AS DATETIME) [DataSegEntrega], 
                UsrSegEntrega, 
                QtdeSegEntrega,
                CAST(DataEntregaPed AS DATETIME) [DataEntregaPed], 
                Tipo, 
                Excluído, 
                CAST(DataAprovSimulacao AS DATETIME) [DataAprovSimulacao], 
                [Usr. Aprov.], 
                CAST(DataSimulacaoObra AS DATETIME) [DataSimulacaoObra], 
                [Usr. Sim. Obra], 
                CAST(DataPedido AS DATETIME) [DataPedido], 
                [Usr. Ped.], 
                DATEDIFF(DAY, DataEntregaPed, DataEntrega) [Atraso], 
                CASE WHEN [Data do Pedido] IS NULL AND Excluído = 'NÃO' THEN 1 ELSE 0 END [PendDtApPed],
                CASE WHEN DataAprovSimulacao IS NULL AND [DataSimulacao] IS NOT NULL THEN 1 ELSE 0 END [PendSimulacao],
                CASE WHEN DataSimulacaoObra IS NULL AND DataAprovSimulacao IS NOT NULL AND [Tab].TipoPedido NOT IN(2,11,12,13,15,16, 4)
                    THEN 1 ELSE 0 END [PendSimulacaoObra],
                CASE WHEN DataCompra IS NULL AND DataSimulacaoObra IS NOT NULL AND [Tab].Estagio_Ped = 4 THEN 1 ELSE 0 END [PendDtCompra],
                CASE WHEN DataEntrega IS NULL AND DataCompra IS NOT NULL THEN 1 ELSE 0 END PendEnt, 
                0 [TipoOrigem], 
                'NO PERÍODO' [Origem], 
                TipoPedido, 
                {prazocompra} [PrazoCompra], 
                CASE WHEN DataCompra IS NULL THEN 0 ELSE 1 END [TemOC], 
                CASE WHEN DATEDIFF(DAY, DataPedido, DataCompra) <= {prazocompra} THEN 1 ELSE 0 END [PedidoCompraPrazo], 
                CASE WHEN DATEDIFF(DAY, DataPedido, DataCompra) > {prazocompra} THEN 1 ELSE 0 END [PedidoCompraForaPrazo], 
                {simulacao} [PrazoSimulacao], 
                CASE WHEN DATEDIFF(DAY, DataAprovSimulacao, DataCompra) <= {simulacao} THEN 1 ELSE 0 END [SimulacaoCompraPrazo], 
                CASE WHEN DATEDIFF(DAY, DataAprovSimulacao, DataCompra) > {simulacao} THEN 1 ELSE 0 END [SimulacaoCompraForaPrazo], 
                DATEDIFF(DAY, DataPedido, DataEntrega) [TempoTotal], 
                CASE WHEN DATEDIFF(DAY, DataPedido, DataEntrega) <= {prazocompra} THEN 1 ELSE 0 END [EntregaPrazo], 
                CASE WHEN DATEDIFF(DAY, DataPedido, DataEntrega) > {prazocompra} THEN 1 ELSE 0 END [EntregaForaPrazo],
                CodForn_Ocp, 
                DATEDIFF(DAY, DataPedido, DataCompra) [PedidoXCompra], 
                DATEDIFF(DAY, DataPedido, DataEntrega) [PedidoXEntrega],
                OC,
                ISNULL(ValorOC, 0) [ValorOC], 
                DtVencParc_Proc 
            FROM 
            (
                SELECT Empresa_temp [CodEmp], Obra_temp [CodObra], NumPedido_temp [Pedido], Cotacao_temp [Cotação], 
                    Insumo_temp [CodIns], Unid_temp [UnidIns], Descr_Ins [Insumo], QtdeCot_temp AS Qtde_Temp, 
                    ISNULL(Aprovacao.DataConf_temp, ItensCot_Temp.DataConf_temp) [Data do Pedido], 
                    ISNULL(Aprovacao.QuemConf_temp, ItensCot_Temp.QuemConf_temp) [Usr. Conf.],
                    ISNULL(DataGer_Ocp, NULL) [DataCompra], ISNULL(Usuario_Ocp, NULL) [Usr. Compra], 
                    ISNULL(DtAtividade_Hen, NULL) [DataEntrega], ISNULL(Usuario_Hen, NULL) [Usr. Entrega],
                    ISNULL(Qtde_Hen,0) [QtdeEntrega], ISNULL(DtSegEnt, NULL) [DataSegEntrega], ISNULL(UsrSegEnt, NULL) [UsrSegEntrega],
                    ISNULL(QtdeSegEnt,0) [QtdeSegEntrega], DtEntrega_temp [DataEntregaPed], 
                    'MATERIAL' [Tipo], CASE Excluido_temp WHEN 0 THEN 'NÃO' ELSE 'SIM' END [Excluído], 
                    ISNULL (DtPedido_Ped,NULL) [DataPedido], ISNULL (Quem_Ped, NULL) [Usr. Ped.], Tipo_Ped [TipoPedido], 
                    CodForn_Ocp, OC, ValorOC, DtVencParc_Proc, Estagio_temp AS Estagio_Ped
                FROM fn_ListEmpObr('{empresaobra}',',') 
                    INNER JOIN ItensCot_Temp ON Empresa_temp = Empresa AND Obra_temp = Obra 
                    LEFT JOIN ( 
                        SELECT Empresa_ApPedM, Obra_ApPedM, Insumo_ApPedM, NumPedido_ApPedM, ItemPed_ApPedM, 
                            MAX(DataAprov_ApPedM) [DataConf_temp], 
                            ( 
                                SELECT MAX(APM.UsrAprov_ApPedM) 
                                FROM AprovacaoPedMat [APM] 
                                WHERE APM.Empresa_ApPedM = APM1.Empresa_ApPedM 
                                    AND APM.Obra_ApPedM = APM1.Obra_ApPedM 
                                    AND APM.Insumo_ApPedM = APM1.Insumo_ApPedM 
                                    AND APM.NumPedido_ApPedM = APM1.NumPedido_ApPedM 
                                    AND APM.ItemPed_ApPedM = APM1.ItemPed_ApPedM 
                                    AND APM.DataAprov_ApPedM = MAX(APM1.DataAprov_ApPedM) 
                            ) [QuemConf_temp] 
                        FROM AprovacaoPedMat [APM1] 
                        GROUP BY Empresa_ApPedM, Obra_ApPedM, Insumo_ApPedM, NumPedido_ApPedM, ItemPed_ApPedM 
                    ) [Aprovacao] ON Empresa_temp = Empresa_ApPedM AND Obra_temp = Obra_ApPedM AND Insumo_temp = Insumo_ApPedM 
                        AND NumPedido_temp = NumPedido_ApPedM AND ItemPed_temp = ItemPed_ApPedM 
                    LEFT JOIN ( 
                        SELECT Empresa_Ocp [EmpresaOC], Obra_Ocp [ObraOC], NumCot_Ocp [CotacaoOC], CodInsumo_Ioc [InsumoOC], 
                            MAX(NumeroOC_Ocp) [OC], MAX(DataGer_Ocp) [DataGer_Ocp], MAX(Usuario_Ocp) [Usuario_Ocp], 
                            MAX(CodForn_Ocp) [CodForn_Ocp], SUM(Qtde_Ioc * Preco_Ioc) [ValorOC],
                            (SELECT DISTINCT COALESCE(MAX(Parc_Proc.DtVencParc_Proc), MAX(DataProc_Pag)) AS DtVencParc_Proc
                                FROM Dados_Proc
                                    INNER JOIN Parc_Proc
                                        ON Dados_Proc.Empresa_Proc = Parc_Proc.Empresa_Proc
                                        AND Dados_Proc.Obra_Proc = Parc_Proc.Obra_Proc
                                        AND Dados_Proc.Num_Proc = Parc_Proc.Num_Proc
                                    LEFT JOIN ContasPagas
                                        ON ContasPagas.Empresa_pag = Dados_Proc.Empresa_proc
                                        AND ContasPagas.ObraProc_Pag = Dados_Proc.Obra_Proc
                                        AND ContasPagas.OrdemCompra_Pag = Dados_Proc.OrdemCompra_Proc
                                        AND ContasPagas.NumCot_Pag = Dados_Proc.NumCot_Proc
                                WHERE Dados_Proc.Empresa_Proc = Empresa_Ocp
                                    AND Dados_Proc.Obra_Proc = Obra_Ocp
                                    AND Dados_Proc.NumCot_Proc = NumCot_Ocp
                                    AND Dados_Proc.OrdemCompra_Proc = NumeroOC_Ocp
                            ) AS DtVencParc_Proc
                        FROM OrdemCompra
                            INNER JOIN ItensOrdemCompra
                                ON Empresa_Ocp = Empresa_Ioc
                                AND Obra_Ocp = Obra_Ioc
                                AND NumeroOC_Ocp = NumeroOC_Ioc
                        WHERE ISNULL(NumCot_Ocp, 0) <> 0
                        GROUP BY Empresa_Ocp, Obra_Ocp, NumCot_Ocp, CodInsumo_Ioc, NumeroOC_Ocp
                    ) [OC] ON EmpresaOC = Empresa_temp AND ObraOC = Obra_temp AND InsumoOC = Insumo_temp AND CotacaoOC = ISNULL(Cotacao_temp, 0)
                    LEFT JOIN (
                        SELECT Empresa_Hen, Obra_Hen, NumOc_Hen, NumIns_Hen, DtAtividade_Hen, Usuario_Hen, Qtde_Hen - QtdeCancelada_Hen [Qtde_Hen]
                        FROM HistoricoEntrega
                        WHERE Entrega_Hen = 1
                    ) AS HistoricoEntrega ON Empresa_Hen = Empresa_temp AND Obra_Hen = Obra_temp AND NumOc_Hen = OC AND NumIns_Hen = Insumo_temp
                    LEFT JOIN (
                        SELECT Empresa_Hen [EmpSegEnt], Obra_Hen [ObrSegEnt], NumOc_Hen [OcSegEnt], NumIns_Hen [InsSegEnt],
                            DataEntrega_hdt [DtSegEnt], Usuario_Hen [UsrSegEnt], Qtde_Hen [QtdeSegEnt]
                        FROM HistoricoEntrega
                            INNER JOIN (
                                SELECT Empresa_Hen [EmpUlt], Obra_Hen [ObrUlt], NumOc_Hen [OcUlt], NumIns_Hen [InsUlt], MAX(Entrega_hen) [UltEnt]
                                FROM HistoricoEntrega
                                GROUP BY Empresa_Hen, Obra_Hen, NumOc_Hen, NumIns_Hen
                            ) AS UltEntrega ON Empresa_Hen = EmpUlt AND Obra_Hen = ObrUlt AND NumOc_Hen = OcUlt AND NumIns_Hen = InsUlt AND Entrega_hen = UltEnt
                            INNER JOIN (
                                SELECT Empresa_hdt AS EmpHdt, Obra_HDt AS ObraHdt, NumOC_HDt AS OcHdt, MAX(NumProc_Hdt) AS ProcHdt
                                FROM HistoricoDtEntrega
                                GROUP BY Empresa_hdt, Obra_HDt, NumOC_HDt
                            ) AS UltDtEntrega ON Empresa_Hen = EmpHdt AND Obra_Hen = ObraHdt AND NumOc_Hen = OcHdt
                            INNER JOIN HistoricoDtEntrega
                                ON Empresa_hdt = EmpHdt AND Obra_HDt = ObraHdt AND NumOC_HDt = OcHdt AND NumProc_Hdt = ProcHdt
                        WHERE Entrega_hen <> 1
                    ) AS SegundaEntrega ON EmpSegEnt = Empresa_temp AND ObrSegEnt = Obra_temp AND OcSegEnt = OC AND InsSegEnt = Insumo_temp
                    INNER JOIN InsumosGeral ON ItensCot_Temp.Insumo_temp = InsumosGeral.Cod_Ins
                    LEFT JOIN Pedidos ON Empresa_Ped = Empresa_temp AND Obra_Ped = Obra_temp AND Cod_Ped = NumPedido_temp
                WHERE ISNULL(ISNULL((CAST(CONVERT(VARCHAR,Aprovacao.DataConf_temp,111)AS DATETIME)), (CAST(CONVERT(VARCHAR,ItensCot_Temp.DataConf_temp,111)AS DATETIME))), (CAST(CONVERT(VARCHAR,DtPedido_ped,111)AS DATETIME))) BETWEEN '{data_inicio}' AND '{data_termino}'
            UNION
            SELECT Empresa_ServTemp [CodEmp], Obra_ServTemp [CodObra], NumPedido_ServTemp [Pedido], Cotacao_ServTemp [Cotação],
                Serv_ServTemp [CodIns], Unid_ServTemp [UnidIns], Descr_Comp [Insumo], QtdeCot_ServTemp,
                ISNULL(Aprovacao.DataConf_ServTemp, ItensCotServ_Temp.DataConf_ServTemp) [Data do Pedido],
                ISNULL(Aprovacao.QuemConf_ServTemp, ItensCotServ_Temp.QuemConf_ServTemp) [Usr. Conf.],
                ISNULL((
                    SELECT MIN(SimulacoesConf.Data_Smlc)
                    FROM SimulacoesConf
                    WHERE (SimulacoesConf.Empresa_Smlc = Empresa_ServTemp)
                        AND (SimulacoesConf.NumCot_Smlc = Cotacao_ServTemp)
                        AND (SimulacoesConf.ObraCot_Smlc = Obra_ServTemp)
                ), NULL) [DataCompra],
                ISNULL((
                    SELECT MIN(SimulacoesConf.Usr_Smlc)
                    FROM SimulacoesConf
                    WHERE (SimulacoesConf.Empresa_Smlc = Empresa_ServTemp)
                        AND (SimulacoesConf.NumCot_Smlc = Cotacao_ServTemp)
                        AND (SimulacoesConf.ObraCot_Smlc = Obra_ServTemp)
                ), NULL) [Usr. Compra],
                ISNULL(DtCriacao_Med, NULL) [DataEntrega], ISNULL(Quem_Med, NULL) [Usr. Entrega], 0 [QtdeEntrega],
                NULL [DataSegEntrega], NULL [UsrSegEntrega], 0 [QtdeSegEntrega], NULL AS [DataEntregaPed],
                'SERVIÇO' [Tipo], CASE Excluido_ServTemp WHEN 0 THEN 'NÃO' ELSE 'SIM' END [Excluído],
                ISNULL(DtPedido_Ped, NULL) [DataPedido], ISNULL(Quem_Ped, NULL) [Usr. Ped.], Tipo_Ped [TipoPedido],
                (
                    SELECT MIN(CodForn_ItCotServ)
                    FROM ItensContratoCotServ
                    WHERE Empresa_ItCotServ = Empresa_ServTemp
                        AND Cotacao_ItCotServ = Cotacao_ServTemp
                        AND Serv_ItCotServ = Serv_ServTemp
                ) [CodForn],
                '' [OC], 0 [ValorOC], NULL [DtVencParc_Proc], Estagio_ServTemp AS Estagio_Ped
            FROM fn_ListEmpObr('{empresaobra}',',')
                INNER JOIN ItensCotServ_Temp ON Empresa_ServTemp = Empresa AND Obra_ServTemp = Obra
                LEFT JOIN (
                    SELECT Empresa_ApPedS, Obra_ApPedS, Serv_ApPedS, NumPedido_ApPedS, MAX(DataAprov_ApPedS) [DataConf_ServTemp],
                        (
                            SELECT MAX(APM.UsrAprov_ApPedS)
                            FROM AprovacaoPedServ [APM]
                            WHERE APM.Empresa_ApPedS = APM1.Empresa_ApPedS
                                AND APM.Obra_ApPedS = APM1.Obra_ApPedS
                                AND APM.Serv_ApPedS = APM1.Serv_ApPedS
                                AND APM.NumPedido_ApPedS = APM1.NumPedido_ApPedS
                                AND APM.DataAprov_ApPedS = MAX(APM1.DataAprov_ApPedS)
                        ) [QuemConf_ServTemp]
                    FROM AprovacaoPedServ [APM1]
                    GROUP BY Empresa_ApPedS, Obra_ApPedS, Serv_ApPedS, NumPedido_ApPedS
                ) [Aprovacao] ON Empresa_ServTemp = Empresa_ApPedS AND Obra_ServTemp = Obra_ApPedS AND Serv_ServTemp = Serv_ApPedS AND NumPedido_ServTemp = NumPedido_ApPedS
                INNER JOIN Composicoes ON ItensCotServ_Temp.Serv_ServTemp = Composicoes.Cod_Comp
                LEFT JOIN Pedidos ON Empresa_Ped = Empresa_ServTemp AND Obra_Ped = Obra_ServTemp AND Cod_Ped = NumPedido_ServTemp
                LEFT JOIN (
                    SELECT Empresa_Itens, Cotacao_ItCotServ, Serv_Itens, MAX(DtCriacao_Med) [DtCriacao_Med], MAX(Quem_Med) [Quem_Med],
                        SUM(Qtde_Item) AS QtdeMed, ItensContrato.Qtde_itens,
                        (SELECT SUM(icst.QtdeCot_ServTemp)
                        FROM ItensCotServ_temp AS icst
                         WHERE icst.Empresa_ServTemp = Empresa_Itens 
                           AND icst.Obra_ServTemp = Obra_SimcServ
                           AND icst.Serv_ServTemp = Serv_Itens 
                           AND icst.Cotacao_ServTemp = Cotacao_ItCotServ) AS QtdePed,
                        Obra_SimcServ
                    FROM ItensMedicao
                        INNER JOIN Medicoes
                            ON ItensMedicao.Empresa_Item = Medicoes.Empresa_Med
                            AND ItensMedicao.Contrato_Item = Medicoes.Contrato_Med
                            AND ItensMedicao.CodMed_Item = Medicoes.Cod_Med
                        INNER JOIN ItensContrato
                            ON ItensMedicao.Empresa_Item = ItensContrato.Empresa_Itens
                            AND ItensMedicao.Contrato_Item = ItensContrato.Contrato_Itens
                            AND ItensMedicao.Ins_Item = ItensContrato.Serv_Itens
                            AND ItensMedicao.ItensCont_Item = ItensContrato.Item_itens
                        INNER JOIN Contratos
                            ON Contratos.Empresa_cont = ItensContrato.Empresa_Itens
                            AND Contratos.Cod_cont = ItensContrato.Contrato_Itens
                        INNER JOIN ItensContratoCotServ
                            ON Empresa_Itens = Empresa_ItCotServ
                            AND Contrato_Itens = Contrato_ItCotServ
                            AND Item_Itens = Item_ItCotServ
                        INNER JOIN ItensSimuladosConfServ
                            ON ItensSimuladosConfServ.Empresa_SimcServ = ItensContrato.Empresa_Itens
                            AND ItensSimuladosConfServ.Cotacao_SimcServ = ItensContratoCotServ.Cotacao_ItCotServ
                            AND ItensSimuladosConfServ.CodForn_SimcServ = ItensContratoCotServ.CodForn_ItCotServ
                            AND ItensSimuladosConfServ.Serv_SimcServ = ItensContrato.Serv_Itens
                            AND ItensSimuladosConfServ.Obra_SimcServ = Contratos.Obra_cont
                    GROUP BY Empresa_Itens, Cotacao_ItCotServ, Serv_Itens, Qtde_itens, Obra_SimcServ
                ) AS Med ON Empresa_Itens = Empresa_ServTemp AND Cotacao_ItCotServ = Cotacao_ServTemp AND Serv_Itens = Serv_ServTemp
                AND Med.Obra_SimcServ = Obra_ServTemp AND (Med.QtdeMed = Qtde_itens OR Med.QtdeMed >= QtdePed)
            WHERE ISNULL(ISNULL((CAST(CONVERT(VARCHAR, Aprovacao.DataConf_ServTemp, 111) AS DATETIME)), 
                    (CAST(CONVERT(VARCHAR, ItensCotServ_Temp.DataConf_ServTemp, 111) AS DATETIME))), 
                    (CAST(CONVERT(VARCHAR, DtPedido_ped, 111) AS DATETIME))) BETWEEN '{data_inicio}' AND '{data_termino}'
        ) [Tab]
        LEFT JOIN (
            SELECT Empresa_Smlc, NumCot_Smlc, MIN(Data_Smlc) [DataAprovSimulacao], MIN(Usr_Smlc) [Usr. Aprov.]
            FROM SimulacoesConf
            GROUP BY Empresa_Smlc, NumCot_Smlc
        ) [SimulacoesConf1] ON CodEmp = SimulacoesConf1.Empresa_Smlc AND Cotação = SimulacoesConf1.NumCot_Smlc
        LEFT JOIN (
            SELECT Empresa_Smlc, NumCot_Smlc, ObraCot_Smlc, MIN(DataConf_Smlc) [DataSimulacaoObra], MIN(UsrConf_Smlc) [Usr. Sim. Obra]
            FROM SimulacoesConf
            GROUP BY Empresa_Smlc, NumCot_Smlc, ObraCot_Smlc
        ) [SimulacoesConf2] ON CodEmp = SimulacoesConf2.Empresa_Smlc AND Cotação = SimulacoesConf2.NumCot_Smlc AND CodObra = SimulacoesConf2.ObraCot_Smlc
        LEFT JOIN (
            SELECT Empresa_Sml, NumCot_Sml, MIN(Simulacoes.Data_Sml) [DataSimulacao]
            FROM Simulacoes
            GROUP BY Empresa_Sml, NumCot_Sml
        ) [Simulacoes] ON CodEmp = Simulacoes.Empresa_Sml AND Cotação = Simulacoes.NumCot_Sml
        WHERE [TipoPedido] <> 8

        UNION

        SELECT CodEmp, CodObra, Pedido, Cotação, UnidIns, CodIns, UPPER(CodIns + ' - ' + Insumo) [Insumo],
            Qtde_Temp [QtdeIns], CAST([Data do Pedido] AS DATETIME) [Data do Pedido], [Usr. Conf.],
            CAST(DataCompra AS DATETIME) [DataCompra], [Usr. Compra], CAST(DataEntrega AS DATETIME) [DataEntrega],
            [Usr. Entrega], QtdeEntrega, CAST(DataSegEntrega AS DATETIME) [DataSegEntrega], UsrSegEntrega,
            QtdeSegEntrega, CAST(DataEntregaPed AS DATETIME) [DataEntregaPed], Tipo, Excluído,
            CAST(DataAprovSimulacao AS DATETIME) [DataAprovSimulacao], [Usr. Aprov.], CAST(DataSimulacaoObra AS DATETIME) [DataSimulacaoObra],
            [Usr. Sim. Obra], CAST(DataPedido AS DATETIME) [DataPedido], [Usr. Ped.], DATEDIFF(DAY, DataEntregaPed, DataEntrega) [Atraso],
            CASE WHEN [Data do Pedido] IS NULL AND Excluído = 'NÃO' THEN 1 ELSE 0 END [PendDtApPed],
            CASE WHEN DataAprovSimulacao IS NULL AND [DataSimulacao] IS NOT NULL THEN 1 ELSE 0 END [PendSimulacao],
            CASE WHEN DataSimulacaoObra IS NULL AND DataAprovSimulacao IS NOT NULL AND [Tab].TipoPedido NOT IN (2,4) THEN 1 ELSE 0 END [PendSimulacaoObra],
            CASE WHEN DataCompra IS NULL AND DataSimulacaoObra IS NOT NULL AND [Tab].Estagio_Ped = 4 THEN 1 ELSE 0 END [PendDtCompra],
            CASE WHEN DataEntrega IS NULL AND DataCompra IS NOT NULL THEN 1 ELSE 0 END PendEnt, 1 [TipoOrigem],
            'ANTERIOR AO PERÍODO' [Origem], TipoPedido, {prazocompra} [PrazoCompra], CASE WHEN DataCompra IS NULL THEN 0 ELSE 1 END [TemOC],
            CASE WHEN DATEDIFF(DAY, DataPedido, DataCompra) <= {prazocompra} THEN 1 ELSE 0 END [PedidoCompraPrazo],
            CASE WHEN DATEDIFF(DAY, DataPedido, DataCompra) > {prazocompra} THEN 1 ELSE 0 END [PedidoCompraForaPrazo], {simulacao} [PrazoSimulacao],
            CASE WHEN DATEDIFF(DAY, DataAprovSimulacao, DataCompra) <= {simulacao} THEN 1 ELSE 0 END [SimulacaoCompraPrazo],
            CASE WHEN DATEDIFF(DAY, DataAprovSimulacao, DataCompra) > {simulacao} THEN 1 ELSE 0 END [SimulacaoCompraForaPrazo],
            DATEDIFF(DAY, DataPedido, DataEntrega) [TempoTotal], CASE WHEN DATEDIFF(DAY, DataPedido, DataEntrega) <= {prazocompra} THEN 1 ELSE 0 END [EntregaPrazo],
            CASE WHEN DATEDIFF(DAY, DataPedido, DataEntrega) > {prazocompra} THEN 1 ELSE 0 END [EntregaForaPrazo], CodForn_Ocp,
            DATEDIFF(DAY, DataPedido, DataCompra) [PedidoXCompra], DATEDIFF(DAY, DataPedido, DataEntrega) [PedidoXEntrega], OC, ISNULL(ValorOC, 0) [ValorOC], DtVencParc_Proc
        FROM
        (
            SELECT Empresa_temp [CodEmp], Obra_temp [CodObra], NumPedido_temp [Pedido], Cotacao_temp [Cotação], Insumo_temp [CodIns],
                Unid_temp [UnidIns], Descr_Ins [Insumo], QtdeCot_temp AS Qtde_Temp, ISNULL(Aprovacao.DataConf_temp, ItensCot_Temp.DataConf_temp) [Data do Pedido],
                ISNULL(Aprovacao.QuemConf_temp, ItensCot_Temp.QuemConf_temp) [Usr. Conf.], ISNULL(DataGer_Ocp, NULL) [DataCompra], ISNULL(Usuario_Ocp, NULL) [Usr. Compra],
                ISNULL(DtAtividade_Hen, NULL) [DataEntrega], ISNULL(Usuario_Hen, NULL) [Usr. Entrega], ISNULL(Qtde_Hen, 0) [QtdeEntrega], ISNULL(DtSegEnt, NULL) [DataSegEntrega],
                ISNULL(UsrSegEnt, NULL) [UsrSegEntrega], ISNULL(QtdeSegEnt, 0) [QtdeSegEntrega], DtEntrega_temp [DataEntregaPed], 'MATERIAL' [Tipo],
                CASE Excluido_temp WHEN 0 THEN 'NÃO' ELSE 'SIM' END [Excluído], 
                ISNULL(DtPedido_Ped, NULL) [DataPedido], ISNULL(Quem_Ped, NULL) [Usr. Ped.], Tipo_Ped [TipoPedido], 
                CodForn_Ocp, OC, ValorOC, DtVencParc_Proc, Estagio_temp AS Estagio_Ped
            FROM fn_ListEmpObr('{empresaobra}', ',') 
            INNER JOIN ItensCot_Temp ON Empresa_temp = Empresa AND Obra_temp = Obra
            LEFT JOIN ( 
                SELECT Empresa_ApPedM, Obra_ApPedM, Insumo_ApPedM, NumPedido_ApPedM, ItemPed_ApPedM, 
                    MAX(DataAprov_ApPedM) [DataConf_temp], 
                    ( 
                        SELECT MAX(APM.UsrAprov_ApPedM) 
                        FROM AprovacaoPedMat [APM] 
                        WHERE APM.Empresa_ApPedM = APM1.Empresa_ApPedM 
                            AND APM.Obra_ApPedM = APM1.Obra_ApPedM 
                            AND APM.Insumo_ApPedM = APM1.Insumo_ApPedM 
                            AND APM.NumPedido_ApPedM = APM1.NumPedido_ApPedM 
                            AND APM.ItemPed_ApPedM = APM1.ItemPed_ApPedM 
                            AND APM.DataAprov_ApPedM = MAX(APM1.DataAprov_ApPedM) 
                    ) [QuemConf_temp] 
                FROM AprovacaoPedMat [APM1] 
                GROUP BY Empresa_ApPedM, Obra_ApPedM, Insumo_ApPedM, NumPedido_ApPedM, ItemPed_ApPedM 
            ) [Aprovacao] ON Empresa_temp = Empresa_ApPedM AND Obra_temp = Obra_ApPedM AND Insumo_temp = Insumo_ApPedM 
                AND NumPedido_temp = NumPedido_ApPedM AND ItemPed_temp = ItemPed_ApPedM 
            LEFT JOIN ( 
                SELECT Empresa_Ocp [EmpresaOC], Obra_Ocp [ObraOC], NumCot_Ocp [CotacaoOC], CodInsumo_Ioc [InsumoOC], 
                    MAX(NumeroOC_Ocp) [OC], MAX(DataGer_Ocp) [DataGer_Ocp], MAX(Usuario_Ocp) [Usuario_Ocp], 
                    MAX(CodForn_Ocp) [CodForn_Ocp], SUM(Qtde_Ioc * Preco_Ioc) [ValorOC],
                    (
                        SELECT DISTINCT COALESCE(MAX(Parc_Proc.DtVencParc_Proc), MAX(DataProc_Pag)) AS DtVencParc_Proc
                        FROM Dados_Proc
                        INNER JOIN Parc_Proc ON Dados_Proc.Empresa_Proc = Parc_Proc.Empresa_Proc
                            AND Dados_Proc.Obra_Proc = Parc_Proc.Obra_Proc
                            AND Dados_Proc.Num_Proc = Parc_Proc.Num_Proc
                        LEFT JOIN ContasPagas ON ContasPagas.Empresa_pag = Dados_Proc.Empresa_proc
                            AND ContasPagas.ObraProc_Pag = Dados_Proc.Obra_Proc
                            AND ContasPagas.OrdemCompra_Pag = Dados_Proc.OrdemCompra_Proc
                            AND ContasPagas.NumCot_Pag = Dados_Proc.NumCot_Proc
                        WHERE Dados_Proc.Empresa_Proc = Empresa_Ocp
                            AND Dados_Proc.Obra_Proc = Obra_Ocp
                            AND Dados_Proc.NumCot_Proc = NumCot_Ocp
                            AND Dados_Proc.OrdemCompra_Proc = NumeroOC_Ocp
                    ) AS DtVencParc_Proc
                FROM OrdemCompra
                INNER JOIN ItensOrdemCompra ON Empresa_Ocp = Empresa_Ioc
                    AND Obra_Ocp = Obra_Ioc
                    AND NumeroOC_Ocp = NumeroOC_Ioc
                WHERE ISNULL(NumCot_Ocp, 0) <> 0
                GROUP BY Empresa_Ocp, Obra_Ocp, NumCot_Ocp, CodInsumo_Ioc, NumeroOC_Ocp
            ) [OC] ON EmpresaOC = Empresa_temp AND ObraOC = Obra_temp AND InsumoOC = Insumo_temp AND CotacaoOC = ISNULL(Cotacao_temp, 0)
            LEFT JOIN (
                SELECT Empresa_Hen, Obra_Hen, NumOc_Hen, NumIns_Hen, DtAtividade_Hen, Usuario_Hen, Qtde_Hen - QtdeCancelada_Hen [Qtde_Hen]
                FROM HistoricoEntrega
                WHERE Entrega_Hen = 1
            ) AS HistoricoEntrega ON Empresa_Hen = Empresa_temp AND Obra_Hen = Obra_temp AND NumOc_Hen = OC AND NumIns_Hen = Insumo_temp
            LEFT JOIN (
                SELECT Empresa_Hen [EmpSegEnt], Obra_Hen [ObrSegEnt], NumOc_Hen [OcSegEnt], NumIns_Hen [InsSegEnt],
                    DataEntrega_hdt [DtSegEnt], Usuario_Hen [UsrSegEnt], Qtde_Hen [QtdeSegEnt]
                FROM HistoricoEntrega
                INNER JOIN (
                    SELECT Empresa_Hen [EmpUlt], Obra_Hen [ObrUlt], NumOc_Hen [OcUlt], NumIns_Hen [InsUlt], MAX(Entrega_hen) [UltEnt]
                    FROM HistoricoEntrega
                    GROUP BY Empresa_Hen, Obra_Hen, NumOc_Hen, NumIns_Hen
                ) AS UltEntrega ON Empresa_Hen = EmpUlt AND Obra_Hen = ObrUlt AND NumOc_Hen = OcUlt AND NumIns_Hen = InsUlt AND Entrega_hen = UltEnt
                INNER JOIN (
                    SELECT Empresa_hdt AS EmpHdt, Obra_HDt AS ObraHdt, NumOC_HDt AS OcHdt, MAX(NumProc_Hdt) AS ProcHdt
                    FROM HistoricoDtEntrega
                    GROUP BY Empresa_hdt, Obra_HDt, NumOC_HDt
                ) AS UltDtEntrega ON Empresa_Hen = EmpHdt AND Obra_Hen = ObraHdt AND NumOc_Hen = OcHdt
                INNER JOIN HistoricoDtEntrega ON Empresa_hdt = EmpHdt AND Obra_HDt = ObraHdt AND NumOC_HDt = OcHdt AND NumProc_Hdt = ProcHdt
                WHERE Entrega_hen <> 1
            ) AS SegundaEntrega ON EmpSegEnt = Empresa_temp AND ObrSegEnt = Obra_temp AND OcSegEnt = OC AND InsSegEnt = Insumo_temp
            INNER JOIN InsumosGeral ON ItensCot_Temp.Insumo_temp = InsumosGeral.Cod_Ins
            LEFT JOIN Pedidos ON Empresa_Ped = Empresa_temp AND Obra_Ped = Obra_temp AND Cod_Ped = NumPedido_temp
            WHERE ISNULL(ISNULL((CAST(CONVERT(VARCHAR, Aprovacao.DataConf_temp, 111) AS DATETIME)), 
                (CAST(CONVERT(VARCHAR, ItensCot_Temp.DataConf_temp, 111) AS DATETIME))), 
                (CAST(CONVERT(VARCHAR, DtPedido_ped, 111) AS DATETIME))) < '{data_inicio}'
            
            UNION
            
            SELECT Empresa_ServTemp [CodEmp], Obra_ServTemp [CodObra], NumPedido_ServTemp [Pedido], Cotacao_ServTemp [Cotação],
                Serv_ServTemp [CodIns], Unid_ServTemp [UnidIns], Descr_Comp [Insumo], QtdeCot_ServTemp,
                ISNULL(Aprovacao.DataConf_ServTemp, ItensCotServ_Temp.DataConf_ServTemp) [Data do Pedido],
                ISNULL(Aprovacao.QuemConf_ServTemp, ItensCotServ_Temp.QuemConf_ServTemp) [Usr. Conf.],
                ISNULL((
                    SELECT MIN(SimulacoesConf.Data_Smlc)
                    FROM SimulacoesConf
                    WHERE (SimulacoesConf.Empresa_Smlc = Empresa_ServTemp)
                        AND (SimulacoesConf.NumCot_Smlc = Cotacao_ServTemp)
                        AND (SimulacoesConf.ObraCot_Smlc = Obra_ServTemp)
                ), NULL) [DataCompra],
                ISNULL((
                    SELECT MIN(SimulacoesConf.Usr_Smlc)
                    FROM SimulacoesConf
                    WHERE (SimulacoesConf.Empresa_Smlc = Empresa_ServTemp)
                        AND (SimulacoesConf.NumCot_Smlc = Cotacao_ServTemp)
                        AND (SimulacoesConf.ObraCot_Smlc = Obra_ServTemp)
                ), NULL) [Usr. Compra],
                ISNULL(DtCriacao_Med, NULL) [DataEntrega], ISNULL(Quem_Med, NULL) [Usr. Entrega], 0 [QtdeEntrega],
                NULL [DataSegEntrega], NULL [UsrSegEntrega], 0 [QtdeSegEntrega], NULL AS [DataEntregaPed],
                'SERVIÇO' [Tipo], CASE Excluido_ServTemp WHEN 0 THEN 'NÃO' ELSE 'SIM' END [Excluído],
                ISNULL(DtPedido_Ped, NULL) [DataPedido], ISNULL(Quem_Ped, NULL) [Usr. Ped.], Tipo_Ped [TipoPedido], 
                (
                    SELECT MIN(CodForn_ItCotServ)
                    FROM ItensContratoCotServ
                    WHERE Empresa_ItCotServ = Empresa_ServTemp
                        AND Cotacao_ItCotServ = Cotacao_ServTemp
                        AND Serv_ItCotServ = Serv_ServTemp
                ) [CodForn],
                '' [OC], 0 [ValorOC], NULL [DtVencParc_Proc], Estagio_ServTemp AS Estagio_Ped
            FROM fn_ListEmpObr('{empresaobra}', ',')
            INNER JOIN ItensCotServ_Temp ON Empresa_ServTemp = Empresa AND Obra_ServTemp = Obra
            LEFT JOIN (
                SELECT Empresa_ApPedS, Obra_ApPedS, Serv_ApPedS, NumPedido_ApPedS, MAX(DataAprov_ApPedS) [DataConf_ServTemp],
                    (
                        SELECT MAX(APM.UsrAprov_ApPedS)
                        FROM AprovacaoPedServ [APM]
                        WHERE APM.Empresa_ApPedS = APM1.Empresa_ApPedS
                            AND APM.Obra_ApPedS = APM1.Obra_ApPedS
                            AND APM.Serv_ApPedS = APM1.Serv_ApPedS
                            AND APM.NumPedido_ApPedS = APM1.NumPedido_ApPedS
                            AND APM.DataAprov_ApPedS = MAX(APM1.DataAprov_ApPedS)
                    ) [QuemConf_ServTemp]
                FROM AprovacaoPedServ [APM1]
                GROUP BY Empresa_ApPedS, Obra_ApPedS, Serv_ApPedS, NumPedido_ApPedS
            ) [Aprovacao] ON Empresa_ServTemp = Empresa_ApPedS AND Obra_ServTemp = Obra_ApPedS AND Serv_ServTemp = Serv_ApPedS AND NumPedido_ServTemp = NumPedido_ApPedS
            INNER JOIN Composicoes ON ItensCotServ_Temp.Serv_ServTemp = Composicoes.Cod_Comp
            LEFT JOIN Pedidos ON Empresa_Ped = Empresa_ServTemp AND Obra_Ped = Obra_ServTemp AND Cod_Ped = NumPedido_ServTemp
            LEFT JOIN (
                SELECT Empresa_Itens, Cotacao_ItCotServ, Serv_Itens, MAX(DtCriacao_Med) [DtCriacao_Med], MAX(Quem_Med) [Quem_Med],
                    SUM(Qtde_Item) AS QtdeMed, ItensContrato.Qtde_itens,
                    (SELECT SUM(icst.QtdeCot_ServTemp)
                     FROM ItensCotServ_temp AS icst
                     WHERE icst.Empresa_ServTemp = Empresa_Itens 
                       AND icst.Obra_ServTemp = Obra_SimcServ
                       AND icst.Serv_ServTemp = Serv_Itens 
                       AND icst.Cotacao_ServTemp = Cotacao_ItCotServ) AS QtdePed,
                    Obra_SimcServ
                FROM ItensMedicao
                    INNER JOIN Medicoes
                        ON ItensMedicao.Empresa_Item = Medicoes.Empresa_Med
                        AND ItensMedicao.Contrato_Item = Medicoes.Contrato_Med
                        AND ItensMedicao.CodMed_Item = Medicoes.Cod_Med
                    INNER JOIN ItensContrato
                        ON ItensMedicao.Empresa_Item = ItensContrato.Empresa_Itens
                        AND ItensMedicao.Contrato_Item = ItensContrato.Contrato_Itens
                        AND ItensMedicao.Ins_Item = ItensContrato.Serv_Itens
                        AND ItensMedicao.ItensCont_Item = ItensContrato.Item_itens
                    INNER JOIN Contratos
                        ON Contratos.Empresa_cont = ItensContrato.Empresa_Itens
                        AND Contratos.Cod_cont = ItensContrato.Contrato_Itens
                    INNER JOIN ItensContratoCotServ
                        ON Empresa_Itens = Empresa_ItCotServ
                        AND Contrato_Itens = Contrato_ItCotServ
                        AND Item_Itens = Item_ItCotServ
                    INNER JOIN ItensSimuladosConfServ
                        ON ItensSimuladosConfServ.Empresa_SimcServ = ItensContrato.Empresa_Itens
                        AND ItensSimuladosConfServ.Cotacao_SimcServ = ItensContratoCotServ.Cotacao_ItCotServ
                        AND ItensSimuladosConfServ.CodForn_SimcServ = ItensContratoCotServ.CodForn_ItCotServ
                        AND ItensSimuladosConfServ.Serv_SimcServ = ItensContrato.Serv_Itens
                        AND ItensSimuladosConfServ.Obra_SimcServ = Contratos.Obra_cont
                GROUP BY Empresa_Itens, Cotacao_ItCotServ, Serv_Itens, Qtde_itens, Obra_SimcServ
            ) AS Med ON Empresa_Itens = Empresa_ServTemp AND Cotacao_ItCotServ = Cotacao_ServTemp AND Serv_Itens = Serv_ServTemp
            AND Med.Obra_SimcServ = Obra_ServTemp AND (Med.QtdeMed = Qtde_itens OR Med.QtdeMed >= QtdePed)
            WHERE ISNULL(ISNULL((CAST(CONVERT(VARCHAR, Aprovacao.DataConf_ServTemp, 111) AS DATETIME)), 
                (CAST(CONVERT(VARCHAR, ItensCotServ_Temp.DataConf_ServTemp, 111) AS DATETIME))), 
                (CAST(CONVERT(VARCHAR, DtPedido_ped, 111) AS DATETIME))) < '{data_inicio}'
        ) [Tab]
        LEFT JOIN (
            SELECT Empresa_Smlc, NumCot_Smlc, MIN(Data_Smlc) [DataAprovSimulacao], MIN(Usr_Smlc) [Usr. Aprov.]
            FROM SimulacoesConf
            GROUP BY Empresa_Smlc, NumCot_Smlc
        ) [SimulacoesConf1] ON CodEmp = SimulacoesConf1.Empresa_Smlc AND Cotação = SimulacoesConf1.NumCot_Smlc
        LEFT JOIN (
            SELECT Empresa_Smlc, NumCot_Smlc, ObraCot_Smlc, MIN(DataConf_Smlc) [DataSimulacaoObra], MIN(UsrConf_Smlc) [Usr. Sim. Obra]
            FROM SimulacoesConf
            GROUP BY Empresa_Smlc, NumCot_Smlc, ObraCot_Smlc
        ) [SimulacoesConf2] ON CodEmp = SimulacoesConf2.Empresa_Smlc AND Cotação = SimulacoesConf2.NumCot_Smlc AND CodObra = SimulacoesConf2.ObraCot_Smlc
        LEFT JOIN (
            SELECT Empresa_Sml, NumCot_Sml, MIN(Simulacoes.Data_Sml) [DataSimulacao]
            FROM Simulacoes
            GROUP BY Empresa_Sml, NumCot_Sml
        ) [Simulacoes] ON CodEmp = Simulacoes.Empresa_Sml AND Cotação = Simulacoes.NumCot_Sml
        WHERE ([Data do Pedido] IS NULL 
            OR DataAprovSimulacao IS NULL 
            OR DataSimulacaoObra IS NULL 
            OR DataCompra IS NULL 
            OR DataEntrega IS NULL) 
            AND [TipoPedido] <> 8
    ) [Tabela]
    LEFT JOIN (
        SELECT Empresa_Ped, Obra_Ped, Cod_Ped
        FROM ItensCot_Temp
        INNER JOIN Pedidos ON Empresa_temp = Empresa_Ped AND Obra_temp = Obra_Ped AND NumPedido_temp = Cod_Ped
        INNER JOIN AdiantamentoContrato ON Empresa_temp = Empresa_AdCont AND Obra_temp = Obra_AdCont AND Cotacao_temp = NumCot_AdCont
        GROUP BY Empresa_Ped, Obra_Ped, Cod_Ped
    ) [PedidosAdiantamento] ON CodEmp = Empresa_Ped AND CodObra = Obra_Ped AND Pedido = Cod_Ped
) [Resulta]
INNER JOIN Empresas ON CodEmp = Codigo_Emp
INNER JOIN Obras ON CodEmp = Empresa_Obr AND CodObra = Cod_Obr
LEFT JOIN Pessoas ON CodForn_Ocp = Cod_Pes
LEFT JOIN (
    SELECT
        CASE WHEN Qtde_Ioc + QtdeAMais_Ioc - ISNULL(QtdeDescartada, 0) - ISNULL(Qtde_Ent, 0) > 0 THEN 1 ELSE 0 END [PendenteEnt],
        Empresa_Ioc, Obra_Ioc, CodInsumo_Ioc, NumeroOC_Ioc, Cotacao_Ioc
    FROM fn_ListEmpObr('{empresaobra}', ',')
    INNER JOIN ItensOrdemCompra ON Empresa = ItensOrdemCompra.Empresa_Ioc AND obra = ItensOrdemCompra.Obra_Ioc
    LEFT JOIN (
        SELECT Empresa_Ioc [Empresa_Descartada], Obra_Ioc [Obra_Descartada], NumeroOC_Ioc [NumeroOC_Descartada], CodInsumo_Ioc [CodInsumo_Descartada],
            (Qtde_Ioc + ISNULL(QtdeAMais_Ioc, 0)) - ISNULL(Qtde_Ent, 0) [QtdeDescartada]
            FROM fn_ListEmpObr('{empresaobra}', ',')
        INNER JOIN ItensOrdemCompra ON Empresa = Empresa_Ioc AND Obra = Obra_Ioc
        LEFT JOIN (
            SELECT Empresa_Ent, Obra_Ent, NumOC_Ent, Ins_Ent, SUM(Qtde_Ent) [Qtde_Ent]
            FROM (
                SELECT Empresa_Ent, Obra_Ent, NumOC_Ent, Ins_Ent, Qtde_Ent
                FROM fn_ListEmpObr('{empresaobra}', ',')
                INNER JOIN Entrada ON Empresa = Empresa_Ent AND Obra = Obra_Ent
                UNION ALL
                SELECT Empresa_Est, Obra_Est, NumOC_Est, Ins_Est, Qtde_Est
                FROM fn_ListEmpObr('{empresaobra}', ',')
                INNER JOIN FEstoque ON Empresa = Empresa_Est AND Obra = Obra_Est
                WHERE Status_Est = 1
            ) [Qtde]
            GROUP BY Empresa_Ent, Obra_Ent, NumOC_Ent, Ins_Ent
        ) [Qtde] ON Empresa_Ioc = Empresa_Ent AND Obra_Ioc = Obra_Ent AND NumeroOC_Ioc = NumOC_Ent AND CodInsumo_Ioc = Ins_Ent
        WHERE (Qtde_Ioc + ISNULL(QtdeAMais_Ioc, 0)) - ISNULL(Qtde_Ent, 0) > 0
    ) [Descartadas] ON Empresa_Ioc = Empresa_Descartada AND Obra_Ioc = Obra_Descartada AND NumeroOC_Ioc = NumeroOC_Descartada AND CodInsumo_Ioc = CodInsumo_Descartada
    LEFT JOIN (
        SELECT Empresa_Ent, Obra_Ent, NumOC_Ent, Ins_Ent, SUM(Qtde_Ent) [Qtde_Ent]
        FROM fn_ListEmpObr('{empresaobra}', ',')
        INNER JOIN Entrada ON Empresa = Empresa_Ent AND Obra = Obra_Ent
        GROUP BY Empresa_Ent, Obra_Ent, NumOC_Ent, Ins_Ent
    ) [Entrega] ON Empresa_Ioc = Empresa_Ent AND Obra_Ioc = Obra_Ent AND NumeroOC_Ioc = NumOC_Ent AND CodInsumo_Ioc = Ins_Ent
) AS EntregasPendentes ON Resulta.CodEmp = EntregasPendentes.Empresa_Ioc AND Resulta.CodObra = EntregasPendentes.Obra_Ioc AND Resulta.Cotação = EntregasPendentes.Cotacao_Ioc AND Resulta.OC = EntregasPendentes.NumeroOC_Ioc AND Resulta.CodIns = EntregasPendentes.CodInsumo_Ioc

WHERE TipoOrigem IN ({origem})
    AND CASE {pedidoatendimento} WHEN 0 THEN 1 WHEN 1 THEN -1 END NOT IN (PedidoAdiantamento)
ORDER BY CodEmp, CodObra, TipoOrigem, Pedido;
"""