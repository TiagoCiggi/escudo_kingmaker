import random
from enum import Enum

class ResultadoTeste(Enum):
    SUCESSO_DECISIVO = "Sucesso decisivo"
    SUCESSO = "Sucesso"
    FALHA = "Falha"
    FALHA_CRITICA = "Falha crítica"

class ResultadoD20:
    def __init__(self, dado, modificador, cd):
        self.dado = dado
        self.modificador = modificador
        self.cd = cd
        self.total = dado + modificador
        self.natural = dado
        self.resultado = self.avaliar()

    def avaliar(self):
        # 1. Determina o resultado base
        if self.total >= self.cd:
            base = ResultadoTeste.SUCESSO
        else:
            base = ResultadoTeste.FALHA

        # 2. Aplica ajuste por natural 20 ou 1
        ordem = [
            ResultadoTeste.FALHA_CRITICA,
            ResultadoTeste.FALHA,
            ResultadoTeste.SUCESSO,
            ResultadoTeste.SUCESSO_DECISIVO
        ]
        indice = ordem.index(base)

        if self.natural == 20 and indice < len(ordem) - 1:
            indice += 1
        elif self.natural == 1 and indice > 0:
            indice -= 1

        return ordem[indice]

def d20():
    return random.randint(1, 20)

def rolar_d20(modificador, cd):
    return ResultadoD20(d20(), modificador, cd)
