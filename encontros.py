from jogadas import rolar_d20, d20, ResultadoTeste
from random import randint
import json

with open('json/zona_encontros.json', 'r', encoding='utf-8') as arquivo:
    zonas = json.load(arquivo)

with open("json/encontros.json", "r", encoding="utf-8") as arquivo:
    encontro = json.load(arquivo)

nomes_zonas = [zona["nome"] for zona in zonas]

# recebe a cd do encontro e retorna o resultado
def jogada_encontros(cd):
    return rolar_d20(0, cd).resultado

# recebe a tabela do encontro e se possui uma flag para a função interna de rolagem de d12
def buscar_tabela(tabela, rolar_func=None):
    rolar = rolar_func if rolar_func else d20 #rolar recebe d20 ou rolar_func se estiver com a flag
    rolagem = rolar() # rolagem recebe o resultado de rolar como função
    for entrada in tabela: # intera entrada dentro da tabela
        intervalo = entrada["rolagem"] # intervalo recebe a rolagem da tabela
        if len(intervalo) == 2: # se intervalo possuir 2 valores ele desmonta eles em inicio e fim
            inicio, fim = intervalo
        else:
            inicio = fim = intervalo[0] # se não inicio e fim recebem o intervalo
        if inicio <= rolagem <= fim: # compara o resultado de rolagem com inicio e fim
            encontro = entrada["encontro"] # encontro recebe o contudo de encontro da tabela escolhida
            quantidade = entrada["quantidade"] # quantidade recebe o conteudo de quantidade da tabela escolhida
            if isinstance(encontro, int): # se o encontro for int e não str ele confere
                if quantidade == -1: # se a quantidade for -1 ele rola buscar encontro usando o encontro como zn e a flag como função
                    return busca_encontro(encontro, rolar_func=lambda: randint(1, 12) + 8)
                else: # se for só um int ele rola buscar encontro com o encontro como zn
                    return busca_encontro(encontro)

            else:
                return quantidade, encontro # se não ele retornar a quantidade e o encontro

# recebe a zona e se possui flag para a função interna de rolagem de d12
def busca_encontro(zn, rolar_func=None):
    for zona in zonas: #intera dentro de zonas
        # se zn for um int E a key dentro da zona for a zn, ou se a zn of uma str E o nome dentro da zona for igual a zn
        if (isinstance(zn, int) and zona.get("key") == zn) or (isinstance(zn, str) and zona["nome"].lower() == zn.lower()):
            return buscar_tabela(zona["tabela"], rolar_func) # rola buscar_tabela com a tabela da zona

# recebe a zona e retorna qual a CD do encontro
def busca_cd_encontro(zn):
    for zona in zonas:
        if zona["nome"] == zn:
            return zona["CD_do_encontro"]

# recebe a zona e rola buscar encontro para retornar o encontro
def buscar_encontro(zn):
    encontro = busca_encontro(zn)
    return encontro

# função final
# recebe a zona
def teste(zn):
    cd = busca_cd_encontro(zn)
    if jogada_encontros(cd) in {ResultadoTeste.SUCESSO, ResultadoTeste.SUCESSO_DECISIVO}:
        quantidade, criatura, obs = buscar_encontro(zn)
        resultado = f"📍 Encontro em {zn}:\n"
        if obs:
            resultado += f"📘 {obs}\n"
        for qtd, nome in zip(quantidade, criatura):
            resultado += f"- {qtd}x {nome}\n"
        return resultado
    else:
        return "Sem encontros hoje!"
