from datetime import datetime, timedelta
from lib.previsao import Previsao
from lib.rules import *
from lib.siros_parser import SirosParser

def main():
    """Main entry point for the SIROS application."""
    aerodromo = 'SBKP' # Aerodromo a ser processado
    # Na criação do objeto o parametro aerodromo trata do objeto de referencia para definir as partidas e chegadas
    robot = SirosParser(aerodromo)
    # A propriedade maintain define se o arquivo CSV baixado será excluido ou não após a execução,
    # evite definir False para o modelo ou o mesmo será removido
    robot.maintain = False
    # begin e end são os períodos de pesquisa, para calculo da escala do turno o recomendável é iniciar hoje e terminar amanhã
    try:
        print("🌐 Attempting to fetch data from SIROS website...")
        voos = robot.parse(begin=datetime.now().strftime('%d/%m/%Y'),end=(datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y'))
    except Exception as e:
        print(f"❌ Failed to fetch from SIROS: {e}")
        print("📁 Falling back to sample data for demonstration...")
        # Caso queira apenas testar o processamento do CSV, há um modelo de arquivo para testes e chama o método parseCSV
        voos = robot.parseCSV('modelo.csv')
    # Tratamento da previsão de movimentos
    previsao = Previsao(aerodromo)
    # Turnos de serviço em 2 parametros:
    #   turnos: List de int com os horários de 0 a 23 para a hora local de inicio do turno
    #   duracao: int com a duração em horas do turno de serviço
    previsao.setTurnos(turnos=[7,15,23],duracao=8)
    # parseVoos trata os registros processados pelo SirosParser.parseCSV (também chamado pelo parse)
    previsao.parseVoos(voos)
    # Lista o resultado de hora em hora com HORA | ARR | DEP | TOTAL
    previsao.dump()
    # Lista o resultado de movimentos para o turno HORA | ARR | DEP | TOTAL
    previsao.dump_turno()
    # Lista HORA | ARR | DEP | TOTAL | POSIÇÕES OPERACIONAIS
    # @rules implementação da class Rules com o método test retornando uma String com as posições operacionais
    previsao.dump_distribuicao(rules=RulesBita)
    # Aguarda tecla para finalizar
    input("Pressione qualquer tecla para fechar...")


if __name__ == '__main__':
    main()