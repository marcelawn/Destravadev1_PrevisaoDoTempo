'''
1. Navegação Automática:
○ Abrir um navegador e acessar um site de previsão do tempo(você pode escolher
o site)
2. Coleta de Dados Meteorológicos:
○ Extrair a temperatura atual.
○ Extrair a condição do tempo atual (ex. ensolarado, nublado, etc.).
○ Extrair a previsão para os próximos 3 dias (temperatura e condição do tempo).
3. Tratamento e Formatação de Dados:
○ Organizar os dados extraídos em um formato legível.
PASSOS REALIZADOS ACIMA!!!

4. Envio de E-mail:
○ Configurar o envio de e-mails.
○ Criar o conteúdo do e-mail com os dados meteorológicos coletados.
○ Enviar o e-mail para um destinatário específico.(pode enviar para você mesmo
como teste)
5. Automatização do Envio Diário:
○ Agendar a execução do script para rodar diariamente em um horário específico.
'''

import scrapy
import webbrowser
import smtplib
from email.message import EmailMessage
import imghdr
from time import sleep
import schedule






class TimePrevision(scrapy.Spider):
    name = 'destravadevbot'
    def start_requests(self):
        urls = ['https://www.accuweather.com/pt/br/fortaleza/43346/daily-weather-forecast/43346']
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self,response):
        for indice in range(1,4):
            for linha in response.xpath(f"//div[@class='page-content content-module']//div[@class='daily-wrapper'][{indice}]"):
                
                yield {
                    'Data' : linha.xpath("./a/div/h2[@class='date']/span[@class='module-header sub date']/text()").get(),
                    'Temperatura': linha.xpath("./a/div[@class='info']/div[@class='temp']/span[@class='high']/text()").get(),
                    'Condição': linha.xpath("./div[@class='half-day-card-content ']/div[@class='phrase']/text()").get()
                }

# Envio de Email


# Configurações de login
def email():
    EMAIL_ADDRESS = 'email_address'
    EMAIL_PASSWORD = 'password'


    # Criar e enviar um email
    mail = EmailMessage()
    mail['Subject'] = 'Previsão do Tempo'
    mensagem = '''
    Segue abaixo a previsão do tempo para os próximos 3 dias em Fortaleza - Ce!
    '''
    mail['From'] = EMAIL_ADDRESS
    mail['To'] = 'destinatario'
    mail.add_header('Content-Type','text/html')
    mail.set_payload(mensagem.encode('utf-8'))



    arquivos = ['teste.csv']
    for arquivo in arquivos:
        with open(arquivo,'rb') as arquivo:
            dados = arquivo.read()
            nome_arquivo = arquivo.name
            mail.add_attachment(dados,maintype='application',subtype='octet-stream',filename=nome_arquivo)
    # Enviar email
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as email:
        email.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        email.send_message(mail)


schedule.every().day.at('10:00').do(TimePrevision)
schedule.every().day.at('10:10').do(email)