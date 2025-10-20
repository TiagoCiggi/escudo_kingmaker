import json

with open('json/lista_monstros.json', 'r', encoding='utf-8') as arquivo:
    monstros = json.load(arquivo)

def escolhe_monstro(criatura):
    for monstro in monstros:
        if criatura == monstro["nome"]:
            return monstro

def formatar_monstro(monstro):
    linhas = []
    for chave, valor in monstro.items():
        if isinstance(valor, (str, int, float)):
            linhas.append(f"{chave}: {valor}")
        elif isinstance(valor, list):
            linhas.append(f"{chave}: {', '.join(str(v) for v in valor)}")
        elif isinstance(valor, dict):
            linhas.append(f"{chave}: {', '.join(f'{k}={v}' for k, v in valor.items())}")
        else:
            linhas.append(f"{chave}: {valor}")
    return "\n".join(linhas)

