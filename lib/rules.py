# Regra que retorna ao testar quantas posições operacionais serão necessárias
from abc import ABC,abstractmethod


class Rules(ABC):
    @abstractmethod
    def test(movimentos):
        pass

class RulesBita(Rules):
    def test(movimentos):
        posicoes = ['TWR']
        # GND
        if movimentos['DEP'] + movimentos['ARR'] >= 8:
            posicoes += ['GND']
        # Verifica deps
        if movimentos['DEP'] > 14:
            posicoes += ['CLR','ASSCLR','CORD','SUP']
        elif movimentos['DEP'] > 10:
            posicoes += ['CLR','CORD','SUP']
        # Verifica assistente de twr
        if movimentos['DEP'] + movimentos['ARR'] > 20:
            posicoes += ['ASSTWR']
        elif len(posicoes)==1 and movimentos['DEP'] + movimentos['ARR'] > 5:
            posicoes += ['ASSTWR']
        return '\t'.join(posicoes)+'\t\t'

class RulesPandemia(Rules):
    def test(movimentos):
        if movimentos['DEP'] > 10:
            return '\t'.join(['TWR','GND','CLR','SUP'])
        else:
            return '\t'.join(['TWR','GND'])+'\t\t'

class RulesGeral(Rules):
    def test(movimentos):
        if movimentos['DEP'] + movimentos['ARR'] > 15:
            return '\t'.join(['TWR','ASSTWR','GND','CLR','ASSCLR','CORD','SUP'])
        elif movimentos['DEP'] > 7:
            return '\t'.join(['TWR','GND','CLR'])+'\t'
        else:
            return '\t'.join(['TWR','GND'])+'\t\t'