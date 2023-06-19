import csv
import re
from csv import writer
import time


def exibir_progresso(progresso, total):
    barra = '#' * int(progresso / total * 40)
    percentual = progresso / total * 100
    print(f'Progresso: [{barra.ljust(40)}] {percentual:.2f}%', end='\r')


REGEX_RUA = r'^(.*?)(?=,)'
REGEX_APENAS_NUMERO = r' (\d+),'
REGEX_NUMERO_BAIRRO = r'(\d+)\s*[ ]-[ ]\s*([^,]+),'
REGEX_CEP = r'\b\d{5}-\d{3}\b'
REGEX_CIDADE_ESTADO = r'(\b[a-zA-ZÃ§áàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\s]+\b)\s-\s(\b[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]+\b)'
REGEX_PAIS = r'(?<=,\s)[^,]+$'


class Endereco:
    def __init__(self, rua, bairro, numero, cep, cidade, estado, pais):
        self.rua = rua
        self.bairro = bairro
        self.numero = numero
        self.cep = cep
        self.cidade = cidade
        self.estado = estado
        self.pais = pais

    def __str__(self):
        return f"{self.rua},{self.bairro},{self.numero},{self.cep},{self.cidade},{self.estado},{self.pais}"

    def rowFormat(self):
        return [self.rua, self.bairro, self.numero, self.cep, self.cidade, self.estado, self.pais]


def getNumero(enderecoBruto):
    numero = re.search(REGEX_APENAS_NUMERO, enderecoBruto)
    numeroBairro = re.search(REGEX_NUMERO_BAIRRO, enderecoBruto)

    if (numero):
        return numero.group().replace(',', '')

    elif (numeroBairro):
        return numeroBairro.group(1)

    else:
        return "Sem Numero"


def getBairro(enderecoBruto):
    estado = re.search(REGEX_NUMERO_BAIRRO, enderecoBruto)

    if (estado):
        return estado.group(2)
    else:
        return "Nao possui Bairro"


def getCidade(enderecoBruto):
    estado = re.search(REGEX_CIDADE_ESTADO, enderecoBruto)

    if (estado):
        return estado.group(1)
    else:
        return "Nao possui Cidade"


def getEstado(enderecoBruto):
    estado = re.search(REGEX_CIDADE_ESTADO, enderecoBruto)

    if (estado):
        return estado.group(2)
    else:
        return "Nao possui Estado"


def extrairInformacoes(enderecoBruto):

    rua = re.search(REGEX_RUA, enderecoBruto).group()
    bairro = getBairro(enderecoBruto)
    numero = getNumero(enderecoBruto)
    cep = re.search(REGEX_CEP, enderecoBruto).group() if re.search(
        REGEX_CEP, enderecoBruto) else "Nao possui CEP"
    cidade = getCidade(enderecoBruto)
    estado = getEstado(enderecoBruto)
    pais = re.search(REGEX_PAIS, enderecoBruto).group()

    endereco = Endereco(
        rua, bairro, numero, cep, cidade, estado, pais)

    return endereco


def corrigirTexto(textoIncorreto):
    textoLatin1 = textoIncorreto.encode('latin-1').decode('utf-8')
    textoUTF8 = textoLatin1.encode('utf-8')
    return textoUTF8.decode('utf-8')


def processarArquivoCSV(nomeArquivo):
    enderecos = []

    with open(nomeArquivo, encoding='latin-1', newline='') as arquivoCsv:
        leitorCsv = csv.reader(arquivoCsv)
        cabecalho = next(leitorCsv)

        for linha in leitorCsv:
            enderecoBruto = corrigirTexto(linha[0])

            endereco = extrairInformacoes(enderecoBruto)
            if endereco:
                enderecos.append(endereco)

    return enderecos


def preencherArquivoCSV(enderecosProcessados, nomeArquivo):
    with open(nomeArquivo, 'w', encoding='latin-1', newline='') as f:
        thewriter = writer(f)
        totalLinhas = len(enderecosProcessados)-1
        thewriter.writerow(
            ['rua', 'bairro', 'numero', 'cep', 'cidade', 'estado', 'pais'])
        for i, endereco in enumerate(enderecosProcessados):
            data = endereco.rowFormat()
            thewriter.writerow(data)
            exibir_progresso(i, totalLinhas)
            time.sleep(0.002)  # Apenas para simular um preenchimento lento


nomeArquivo = 'dataset.csv'
enderecosProcessados = processarArquivoCSV(nomeArquivo)

nomeArquivoFinal = input(str('Digite o nome do arquivo final:')) + '.csv'

preencherArquivoCSV(enderecosProcessados, nomeArquivoFinal)
