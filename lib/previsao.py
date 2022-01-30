from datetime import datetime, timedelta

class Previsao:
    def __init__(self,aerodromo):
        self.aerodromo = aerodromo
        self.dias = {}
    
    def setTurnos(self, turnos, duracao):
        self.turnos = turnos
        self.duracao = duracao
    
    def parseVoos(self, voos):
        for voo in voos:
            self.addVoo(voo)

    def addVoo(self,voo):
        if voo.data < datetime.today().replace(hour=0, minute=0, second=0, microsecond=0): # Voos para dias anteriores são descartados
            return
        d = voo.data.strftime('%d/%m/%Y')
        if not d in self.dias:
            model = []
            for i in range(24):
                model.append({'DEP':0,'ARR':0})
            self.dias[d] = model
        h = int(voo.data.strftime('%H'))
        self.dias[d][h][voo.tipo] += 1
    
    def dump(self):
        print('PREVISAO DE MOVIMENTO')
        for dia in self.dias:
            print('+========== '+dia+' =========+')
            print('| HORA\t| ARR\t| DEP\t| TOTAL\t|')
            print('+-------------------------------+')
            h = 0
            for hora in self.dias[dia]:
                print('| '+str(h)+':00'+'\t| '+str(hora['ARR'])+'\t| '+str(hora['DEP'])+'\t| '+str(hora['ARR']+hora['DEP'])+'\t|')
                h += 1
            print('+-------------------------------+')
    
    def get_proximo_turno(self):
        agora = datetime.now().hour
        proximo = False
        for turno in self.turnos:
            if agora < turno and proximo == False:
                proximo = turno
        if proximo == False: # Não tem nenhum turno após a hora atual, então vai pro primeiro do proximo dia
            inicio = datetime.now().replace(hour=self.turnos[0], minute=0, second=0, microsecond=0) + timedelta(days=1)
        else:
            inicio = datetime.now().replace(hour=proximo, minute=0, second=0, microsecond=0)
        fim = inicio + timedelta(hours=self.duracao)
        return inicio, fim
    # Mostra a previsão de movimento para o próximo turno
    def dump_turno(self):
        print('PREVISAO DE MOVIMENTO PARA O TURNO')
        inicio, fim = self.get_proximo_turno()
        print('+===== '+inicio.strftime('%d/%m %H:%M')+' - '+fim.strftime('%H:%M')+' ====++')
        print('| HORA\t| ARR\t| DEP\t| TOTAL\t|')
        print('+-------------------------------+')
        for dia in self.dias:
            h = 0
            for hora in self.dias[dia]:
                data = datetime(int(dia[6:10]),int(dia[3:5]),int(dia[0:2]),h)
                if inicio <= data <= fim:
                    print('| '+str(h)+':00'+'\t| '+str(hora['ARR'])+'\t| '+str(hora['DEP'])+'\t| '+str(hora['ARR']+hora['DEP'])+'\t|')
                h += 1
        print('+-------------------------------+')
    
    # Gera uma lista de posições operacionais necessárias em cada hora
    def dump_distribuicao(self,rules):
        print('PREVISÃO DE DISTRIBUIÇÃO DE POSIÇÕES OPERACIONAIS')
        inicio, fim = self.get_proximo_turno()
        print('+========== TURNO: '+inicio.strftime('%d/%m/%Y %H:%M')+' ATÉ '+fim.strftime('%d/%m/%Y %H:%M')+' =======+')
        print('| HORA\t| ARR\t| DEP\t| TOTAL\t| POSIÇÕES\t\t\t|')
        print('+---------------------------------------------------------------+')
        for dia in self.dias:
            h = 0
            for hora in self.dias[dia]:
                data = datetime(int(dia[6:10]),int(dia[3:5]),int(dia[0:2]),h)
                if inicio <= data <= fim:
                    print('| '+str(h)+':00'+'\t| '+str(hora['ARR'])+'\t| '+str(hora['DEP'])+'\t| '+str(hora['ARR']+hora['DEP'])+'\t| '+rules.test(hora)+'\t|')
                h += 1
        print('+---------------------------------------------------------------+')
