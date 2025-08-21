import gspread
import csv
from google.oauth2.service_account import Credentials

def escreveCSV (dados, caminho):
    with open(caminho, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for linha in dados:
            spamwriter.writerow(linha)


# Escopos necessários para acessar o Sheets e Drive
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Caminho para o arquivo JSON baixado do Google Cloud
creds = Credentials.from_service_account_file("credenciais.json", scopes=scopes)

# Autenticar no Google Sheets
client = gspread.authorize(creds)

# Abrir a planilha pelo nome
spreadsheet = client.open("teste-FluxoCaixa")

# Ler todas as linhas
dadosPessoa = spreadsheet.worksheet("pessoa").get_all_values()
dadosEmpresa = spreadsheet.worksheet("empresa").get_all_values()
dadosArea_projeto = spreadsheet.worksheet("area_projeto") .get_all_values()
dadosServico =  spreadsheet.worksheet("servico").get_all_values()
dadosDespesa = spreadsheet.worksheet("despesa") .get_all_values()
dadosTributo = spreadsheet.worksheet("tributo").get_all_values()

commitSpreadSheet = [] # pair <table, directory>
commitSpreadSheet.append([dadosPessoa, 'data/dadosPessoa.csv'])
commitSpreadSheet.append([dadosEmpresa, 'data/dadosEmpresa.csv'])
commitSpreadSheet.append([dadosArea_projeto, 'data/dadosArea_projeto.csv'])
commitSpreadSheet.append([dadosServico, 'data/dadosServico.csv'])
commitSpreadSheet.append([dadosDespesa, 'data/dadosDespesa.csv'])
commitSpreadSheet.append([dadosTributo, 'data/dadosTributo.csv'])

for table, directory in commitSpreadSheet:  
    escreveCSV(table, directory)

'''
FUNÇOES
'''

