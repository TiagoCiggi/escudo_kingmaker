from jogadas import rolar_d20, d20, ResultadoTeste

import json

with open('json/zona_encontros.json', 'r', encoding='utf-8') as arquivo:
    zonas = json.load(arquivo)

nomes_zonas = [zona["nome"] for zona in zonas]

def jogada_encontros(cd):
    return rolar_d20(0, cd).resultado

def busca_encontro(zn, rolagem):
    for zona in zonas:
        if zona["nome"].lower() == zn.lower():
            for tabela in zona["tabela"]:
                intervalo = tabela["rolagem"]
                if len(intervalo) == 2:
                    inicio, fim = intervalo
                else:
                    inicio = fim = intervalo[0]
                if inicio <= rolagem <= fim:
                    return tabela["quantidade"], tabela["encontro"]

def busca_cd_encontro(zn):
    for zona in zonas:
        if zona["nome"] == zn:
            return zona["CD_do_encontro"]

def encontro(zn):
    rolagem = d20()
    encontro = busca_encontro(zn, rolagem)
    return encontro

def teste(zn):
    cd = busca_cd_encontro(zn)
    if jogada_encontros(cd) in {ResultadoTeste.SUCESSO, ResultadoTeste.SUCESSO_DECISIVO}:
        rolagem = d20()
        quantidade, criatura = busca_encontro(zn, rolagem)
        return f"Encontro: {quantidade} {criatura}"
    else:
        return "Sem encontros hoje!"