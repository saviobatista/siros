from datetime import datetime, timedelta


class Voo:
    version = 'ICAO;Operador Aéreo;Etapa;Voo;Equip;Assentos;Origem;Aeroporto Origem;Início;Partida Prevista;Chegada Prevista;dt_referencia;nr_voo;nr_etapa;Tipo;Destino;Aeroporto Destino;tx_codeshare\r\n'

    def __init__(self,dados,aerodromo):
        self.aerodromo = aerodromo # Aerodromo de referencia, em relação a onde haverá os calculos
        # REFERENCIA: CSV gerado em 2022-01-28 foi retirado uma linha qualquer para teste
        # GTI;ATLAS AIR INC;1;0061;B744;0;KMIA;MIAMI INTERNATIONAL AIRPORT - MIAMI, FLORIDA - ESTADOS UNIDOS DA AMÉRICA;28/01/2022;28/01/2022 20:40;29/01/2022 04:40;28/01/2022 00:00:00;0061;1;REGULAR DE CARGA INTERNACIONAL;SBKP;VIRACOPOS - CAMPINAS - SP - BRASIL;
        self.icao = dados[0] # GTI
        self.operador = dados[1] # ATLAS AIR INC
        self.etapa = dados[2] # 1
        self.voo = dados[3] # 0061
        self.equipamento = dados[4] # B744
        self.assentos = dados[5] # 0
        self.origem = dados[6] # KMIA
        self.aeroportoOrigem = dados[7] # MIAMI INTERNATIONAL AIRPORT - MIAMI, FLORIDA - ESTADOS UNIDOS DA AMÉRICA
        self.inicio = dados[8] # 28/01/2022
        self.partida = dados[9] # 28/01/2022 20:40
        self.chegada = dados[10] # 29/01/2022 04:40
        self.dtReferencia = dados[11] # 28/01/2022 00:00:00
        self.nrVoo = dados[12] # 0061
        self.nrEtapa = dados[13] # 1
        self.tipo = dados[14] # REGULAR DE CARGA INTERNACIONAL
        self.destino = dados[15] # SBKP
        self.aeroportoDestino = dados[16] # VIRACOPOS - CAMPINAS - SP - BRASIL
        self.txCodeshare = dados[17]
        if len(dados) > 18:
            self.extra = dados[18]
        else:
            self.extra = ''
        self.set_tipo()
        self.set_data()

    def set_tipo(self):
        if self.origem == self.aerodromo:
            self.tipo = 'DEP'
        elif self.destino == self.aerodromo:
            self.tipo = 'ARR'
        else:
            self.tipo = 'ERR'
            raise 'Não pertence ao aeródromo de referencia'
    
    def set_data(self):
        if self.tipo == 'DEP':
            self.data = datetime(int(self.partida[6:10]),int(self.partida[3:5]),int(self.partida[0:2]),int(self.partida[11:13]),int(self.partida[14:16]))
            # ao ser partida consideramos a hora de CLR que é em geral 20 minutos antes do EOBT do plano
            self.data -= timedelta(minutes=20)
        elif self.tipo == 'ARR':
            self.data = datetime(int(self.chegada[6:10]),int(self.chegada[3:5]),int(self.chegada[0:2]),int(self.chegada[11:13]),int(self.chegada[14:16]))
        