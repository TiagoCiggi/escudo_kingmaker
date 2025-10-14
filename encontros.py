from jogadas import rolar_d20, d20, ResultadoTeste
from random import randint
import json

with open('json/zona_encontros.json', 'r', encoding='utf-8') as arquivo:
    zonas = json.load(arquivo)

nomes_zonas = [zona["nome"] for zona in zonas]

def jogada_encontros(cd):
    return rolar_d20(0, cd).resultado

def buscar_tabela(tabela, rolar_func=None):
    rolar = rolar_func if rolar_func else d20
    rolagem = rolar()
    for entrada in tabela:
        intervalo = entrada["rolagem"]
        if len(intervalo) == 2:
            inicio, fim = intervalo
        else:
            inicio = fim = intervalo[0]
        if inicio <= rolagem <= fim:
            encontro = entrada["encontro"]
            quantidade = entrada["quantidade"]
            if isinstance(encontro, int):
                if quantidade == -1:
                    return busca_encontro(encontro, rolar_func=lambda: randint(1, 12) + 8)
                else:
                    return busca_encontro(encontro)

            else:
                return quantidade, encontro

def busca_encontro(zn, rolar_func=None):
    for zona in zonas:
        if (isinstance(zn, int) and zona.get("key") == zn) or \
           (isinstance(zn, str) and zona["nome"].lower() == zn.lower()):
            return buscar_tabela(zona["tabela"], rolar_func)


def busca_cd_encontro(zn):
    for zona in zonas:
        if zona["nome"] == zn:
            return zona["CD_do_encontro"]

def encontro(zn):
    encontro = busca_encontro(zn)
    return encontro

def teste(zn):
    cd = busca_cd_encontro(zn)
    if jogada_encontros(cd) in {ResultadoTeste.SUCESSO, ResultadoTeste.SUCESSO_DECISIVO}:
        quantidade, criatura = busca_encontro(zn)
        return f"Encontro: {quantidade} {criatura}"
    else:
        return "Sem encontros hoje!"