from jogadas import rolar_d20, d20, ResultadoTeste
from random import randint
import json

with open('zona_encontros.json', 'r', encoding='utf-8') as arquivo:
    zonas = json.load(arquivo)

with open("lista_monstros.json", "r", encoding="utf-8") as arquivo:
    lista_monstros = json.load(arquivo)

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
            obs = entrada.get("obs", "")
            if isinstance(encontro, int): # se o encontro for int e não str ele confere
                if quantidade == -1: # se a quantidade for -1 ele rola buscar encontro usando o encontro como zn e a flag como função
                    return busca_encontro(encontro, rolar_func=lambda: randint(1, 12) + 8)
                else: # se for só um int ele rola buscar encontro com o encontro como zn
                    return busca_encontro(encontro)
            else:
                return quantidade, encontro, obs # se não ele retornar a quantidade e o encontro

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
def define_encontro(zn):
    encontro = busca_encontro(zn)
    return encontro

# função final
# recebe a zona
def teste(zn):
    cd = busca_cd_encontro(zn)
    if jogada_encontros(cd) in {ResultadoTeste.SUCESSO, ResultadoTeste.SUCESSO_DECISIVO}:
        encontro = define_encontro(zn)
        return encontro
    else:
        return "Sem encontros hoje!"

def definir_monstro(nome):
    for monstro in lista_monstros:
        if monstro["nome"].lower() == nome.lower():
            return monstro
    return None

def encontro_final(encontro):
    qtd, nomes, obs = encontro
    texto = f"📘 OBS: {obs}\n"

    if not isinstance(nomes, list):
        monstro = definir_monstro(nomes)
        texto += formatar_monstro(qtd, monstro)
    else:
        for i in range(len(nomes)):
            monstro = definir_monstro(nomes[i])
            texto += formatar_monstro(qtd[i], monstro)
            if i < len(nomes) - 1:
                texto += "\n" + "==##" * 40 + "\n"

    return texto

def formatar_monstro(qtd, monstro):
    texto = f"🧟 {qtd}X {monstro['nome']} (Nível {monstro['nivel']})\n"
    texto += f"📏 Tamanho: {monstro['traços']['tamanho']} | Tendência: {monstro['traços']['tendencia']}\n"
    texto += f"🎯 CA: {monstro['defesas']['CA']} | PV: {monstro['defesas']['PV']}\n"
    texto += f"⚡ Velocidade: {monstro['velocidade']['principal']}m\n"

    texto += "\n🧠 Atributos:\n"
    for atr, val in monstro["atributos"].items():
        texto += f"- {atr.upper()}: {val}\n"

    texto += "\n🎓 Perícias:\n"
    for pericia in monstro["pericias"]:
        texto += f"- {pericia['nome']}: +{pericia['modificador']}\n"

    texto += "\n🗡️ Ataques Corpo a Corpo:\n"
    for ataque in monstro["ataques"]["corpo_a_corpo"]:
        texto += f"- {ataque['nome']} (+{ataque['modificador']}): {ataque['dano']} {ataque['tipo_dano']}\n"

    if monstro["ataques"]["distancia"]:
        texto += "\n🏹 Ataques à Distância:\n"
        for ataque in monstro["ataques"]["distancia"]:
            texto += f"- {ataque['nome']} (+{ataque['modificador']}): {ataque['dano']} {ataque['tipo_dano']}\n"

    if monstro["habilidades_ofensivas"]:
        texto += "\n🔥 Habilidades Ofensivas:\n"
        for hab in monstro["habilidades_ofensivas"]:
            texto += f"- {hab['nome']}: {hab['descricao']}\n"

    if monstro["principais_caracteristicas"]:
        texto += "\n📘 Características:\n"
        for linha in monstro["principais_caracteristicas"]:
            texto += f"- {linha}\n"

    return texto

resultado = teste("Dunrelva")
if isinstance(resultado, tuple):
    encontro_final(resultado)
else:
    print(resultado)
