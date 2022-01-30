# Regra que retorna ao testar quantas posições operacionais serão necessárias
from abc import ABC,abstractmethod


class Rules(ABC):
    @abstractmethod
    def test(movimentos):
        pass

class RulesPandemia(Rules):
    def test(movimentos):
        if movimentos['DEP'] + movimentos['ARR'] > 15:
            return '\t'.join(['TWR','GND','CLR','SUP'])
        elif movimentos['DEP'] > 7:
            return '\t'.join(['TWR','GND','CLR'])+'\t'
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