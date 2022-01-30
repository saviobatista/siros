from hashlib import md5
import pathlib
import csv
from os import path, remove, removedirs, mkdir
from shutil import rmtree
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lib.voo import Voo

class SirosParser:
    checksum = '81d0f5467405879625a83802142b5f24' # MD5 da primeira linha do arquivo gerado, para validar a versão
    url = 'https://siros.anac.gov.br/'

    def __init__(self,aerodromo):
        self.timeout = 30
        self.aerodromo = aerodromo
        self.maintain = True

    def waitFor(self, locator):
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(locator))
    
    def setup(self):
        # Cria pasta temporária para salvar o arquivo de download
        self.downloads = path.join(str(pathlib.Path().resolve()),'tmp')
        if path.isdir(self.downloads):
            # removedirs(self.downloads)
            rmtree(self.downloads)
        mkdir(self.downloads)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        # options.add_experimental_option('detach',True)
        options.add_experimental_option('prefs',{
            'download.default_directory' : self.downloads
        })
        self.browser = webdriver.Chrome(options=options)
        self.browser.get(SirosParser.url)

    def parse(self,begin,end):
        self.setup()
        self.waitFor((By.ID, 'MainContent_txtAerodromoOrigem'))
        # BUG: Nem sempre funciona clicar não processa o formulário para carregar a opção de local
        # Descobri que o problema vem da inicialziação do ASP.NET que está possívelmente relacionado a:
        # Sys.WebForms.PageRequestManager._initialize('ctl00$ctl08', 'ctl01', [], [], [], 90, 'ctl00');
        # Por hora para sobrepor o obstaculo um sleep de 5 segundos depois que a página abre para sobrepor
        time.sleep(5)
        self.browser.find_element(By.ID,'MainContent_txtAerodromoOrigem').send_keys(self.aerodromo)
        self.browser.find_element(By.ID,'MainContent_btnAerodromoOrigem').click()
        self.waitFor((By.XPATH, '//*[@id="MainContent_cboAerodromoOrigem"]/option[@value=162]'))
        self.browser.find_element(By.ID,'MainContent_txtAerodromoDestino').send_keys(self.aerodromo)
        self.browser.find_element(By.ID,'MainContent_btnAerodromoDestino').click()
        self.waitFor((By.XPATH, '//*[@id="MainContent_cboAerodromoOrigem"]/option[@value=162]'))
        self.browser.find_element(By.ID,'MainContent_txtDtIni').send_keys(begin)
        self.browser.find_element(By.ID,'MainContent_txtDtFim').send_keys(end)
        # self.browser.find_element(By.ID,'MainContent_rdHorario_1').click() # Define horário em UTC
        self.browser.find_element(By.ID,'MainContent_btnExportar').click()
        self.waitFor((By.ID,'MainContent_btnBaixar'))
        self.browser.find_element(By.ID,'MainContent_btnBaixar').click()
        # Abre uma aba e rastreia o download
        # driver.execute_script('window.open()')
        self.browser.get('chrome://downloads')
        time.sleep(5)
        # Aguarda completar download no chrome quando navegador visivel
        # BUG: Incompatível com headless mode do chrome
        porcentagem = 0
        while porcentagem != 100:
            porcentagem = self.browser.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
        #Nome do arquivo baixado
        arquivo = self.browser.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content #file-link').text")
        return self.parseCSV(arquivo)
        
    def parseCSV(self, arquivo):
        #Processamento do CSV
        voos = []
        # Varre o arquivo processando os voos e coloca na lista
        with open(path.join(str(pathlib.Path().resolve()),arquivo)) as csvfile:
            primeiralinha = csvfile.readline()
            if md5(primeiralinha.encode()).hexdigest() != self.checksum:
                raise 'Aparentemente houve uma mudança na versão e modelo do arquivo gerado pela ANAC'
            reader = csv.reader(csvfile, delimiter = ';')
            for row in reader:
                voos.append(Voo(row,self.aerodromo))
        # Remove arquivo CSV se self.maintain = False
        if not self.maintain:
            remove(path.join(str(pathlib.Path().resolve()),arquivo))
        return voos
