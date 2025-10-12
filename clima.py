from jogadas import rolar_d20, d20, ResultadoTeste
from enum import Enum
import random
import json

class Mes(Enum):
    ABADIUS = "Abadius"
    CALISTRIL = "Calistril"
    PHARAST = "Pharast"
    GOZRAN = "Gozran"
    DESNUS = "Desnus"
    SERENITH = "Serenith"
    ERASTUS = "Erastus"
    ARODUS = "Arodus"
    ROVA = "Rova"
    LAMASHAN = "Lamashan"
    NETH = "Neth"
    KUTHONA = "Kuthona"

def temperatura(mes: Mes):
    inverno = {Mes.CALISTRIL, Mes.KUTHONA}
    alto_inverno = {Mes.ABADIUS}
    if mes in inverno:
        return rolar_d20(0,18), True #retorna o resultado e a condição true para saber se é inverno
    elif mes in alto_inverno:
        return rolar_d20(0,16), True
    else:
        return None, False

def precipitacao(mes: Mes):
    verao = {Mes.SERENITH, Mes.ERASTUS, Mes.ARODUS}
    inverno = {Mes.ABADIUS, Mes.CALISTRIL, Mes.KUTHONA}
    if mes in verao:
        return rolar_d20(0, 20)
    if mes in inverno:
        return rolar_d20(0,8)
    else:
        return rolar_d20(0,15)

class Evento:
    def __init__(self, dados: dict):
        self.key = dados.get("key", [])
        self.nome = dados.get("nome")
        self.perigo = dados.get("perigo")
        self.sobrevivencia = dados.get("sobrevivencia")
        self.requerimento = dados.get("requerimento")
        self.descricao = dados.get("descrição")
        self.preparacao = dados.get("preparação")
        self.rotina = dados.get("rotina")
        self.acao = dados.get("ação")
        self.agravamento = dados.get("agravamento")

    def mostrar(self):
        return (f"🌪️ Nome: {self.nome}"
                f"\nPerigo: {self.perigo}"
                f"\nTeste de Sobrevivencia {self.sobrevivencia}"
                f"\nRequerimento para ocorrer o evento: {self.requerimento}"
                f"\nDescrição: {self.descricao}"
                f"\nTeste necessário para se preparar: {self.preparacao}"
                f"\nRotina (+ teste simples CD11 para prolongar o evento: {self.rotina}"
                f"\nAção: {self.rotina}"
                f"\nAgravamento: {self.agravamento})")

def carregar_eventos_json(caminho="eventos_climaticos.json") -> list[Evento]:
    with open("eventos_climaticos.json", encoding="utf-8") as f:
        dados = json.load(f)
    return [Evento(e) for e in dados]

def sorteio_evento(): #rola na tabela pra achar qual evento
    eventos = carregar_eventos_json()
    valor = d20()
    return [evento for evento in eventos if valor in evento.key]

def qtd_evento(): #descobre se teve 1 ou 2 eventos
    qtd = rolar_d20(0,17)
    if qtd == ResultadoTeste.SUCESSO_DECISIVO:
        extra = rolar_d20(0,17)
        if extra.resultado in {ResultadoTeste.SUCESSO, ResultadoTeste.SUCESSO_DECISIVO}:
            return 2
    elif qtd == ResultadoTeste.SUCESSO:
        return 1
    else:
        return 0

def confirma_evento(nvl: int, perigo: int):
    return nvl+4 > perigo

def testa_evento(nvl: int):
    evento_1 = None
    evento_2 = None

    qtd = qtd_evento()

    if qtd >= 1:
        evento = sorteio_evento()
        if evento and confirma_evento(nvl, evento[0].perigo):
            evento_1 = evento[0]

    if qtd == 2:
        evento = sorteio_evento()
        if evento and confirma_evento(nvl, evento[0].perigo):
            evento_2 = evento[0]

    return evento_1, evento_2

def calcular_clima(mes: Mes, nivel: int) -> str:
    resultado_temp, inverno = temperatura(mes)
    resultado_prec = precipitacao(mes)
    evento1, evento2 = testa_evento(nivel)

    texto = f"📆 Mês: {mes.name} ({mes.value})\n\n"

    if resultado_temp:
        if resultado_temp.resultado == ResultadoTeste.SUCESSO_DECISIVO:
            texto += f"❄️ Frio extremo [-{random.randint(30, 59)}ºC]\n💤 Fadiga em 4h\n🧊 Dano (1d6) a cada 10min\n\n"
        elif resultado_temp.resultado == ResultadoTeste.SUCESSO:
            texto += f"🥶 Frio severo [-{random.randint(10, 29)}ºC]\n💤 Fadiga em 4h\n🧊 Dano (1d6) a cada hora\n\n"
        else:
            texto += f"🌬️ Frio leve [-{random.randint(0, 9)}ºC]\n💤 Fadiga em 4h\n\n"
    else:
        texto += f"🌤️ Clima ameno [+{random.randint(1, 35)}ºC]\n💤 Fadiga a cada 8h\n\n"

    if resultado_prec:
        if inverno:
            texto += "❄️ Neve\n👁️ -1 em Percepção\n💤 Fadiga em 4h\n\n"
        else:
            texto += "🌧️ Chuva\n👁️ -1 em Percepção\n💤 Fadiga em 4h\n\n"
    else:
        texto += "☀️ Sem precipitação\n\n"

    if evento1:
        texto += evento1.mostrar() + "\n\n"
    if evento2:
        texto += evento2.mostrar() + "\n\n"

    return texto
