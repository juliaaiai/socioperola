import pandas as pd
from flask import Flask, request
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Conectando ao Google Sheets
def carregar_dados():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key("1A4H6zaccnZOodwbIaF6DYhJfSX0Yse0pz_f_kA7YHgc")

    # Pegando a aba correta: 2025
    aba = sheet.worksheet("2025")

    # Pega o cabeçalho da linha 17
    cabecalho = aba.row_values(17)

    # Dados a partir da linha 18
    dados = aba.get_all_values()[17:]

    # Montando o DataFrame
    df = pd.DataFrame(dados, columns=cabecalho)

    return df

# Dicionário com os significados das siglas
SIGNIFICADOS = {
    "OK": "PESSOA ESTÁ OK EM TODOS OS MESES",
    "SB": "(STAND BY) - FALTA PAGAR O MÊS",
    "DV": "(DEVEDOR) - PESSOA QUE DEVE O MÊS ANTERIOR E O MÊS ATIVO",
    "P": "(PARADÃO) - MÊS EM QUE TODOS AINDA ERAM APENAS PARADÃO ESTÃO PAGOS",
    "NJ": "NÃO JOGOU, ESTAVA FORA",
    "PTV": "PONTOS DE VANTAGENS (ACUMULATIVO)",
    "DP": "DIRETORIA DO PÉROLA",
    "ST": "SÓCIO TORCEDOR",
    "SM": "SÓCIO MASTER"
}

# Função para gerar a resposta com status e significado
def obter_status(socio, df):
    mes_atual = datetime.now().month
    meses = [
        "JAN", "FEV", "MAR", "ABR", "MAI", "JUN",
        "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"
    ]
    nome_mes = meses[mes_atual - 1]

    # Procurando o sócio pela coluna 'N°'
    linha = df[df['N°'] == socio]

    if linha.empty:
        return "Sócio não encontrado."

    status = linha.iloc[0].get(nome_mes, "Não disponível").strip().upper()
    significado = SIGNIFICADOS.get(status, "Sigla não reconhecida")

    return f"{status} - {significado}"

@app.route('/')
def index():
    numero_socio = request.args.get('n')
    if not numero_socio:
        return "Informe o número do sócio na URL. Ex: /?n=0001"

    try:
        df = carregar_dados()
        status_info = obter_status(numero_socio, df)
        return f"Pérola Futebol Clube\nSócio {numero_socio}:\n{status_info}"
    except Exception as e:
        return f"Erro ao processar os dados: {str(e)}"

if __name__ == "__main__":
    print("✅ Servidor iniciado com sucesso!")
    app.run(debug=True)
