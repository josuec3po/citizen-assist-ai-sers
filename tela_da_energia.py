# Opção 12 do menu: calcula e compara alternativas de economia de energia no banho.
import json

import energia_calculos

CAMINHO_PREMISSAS = "data/energia_premissas.json"
OBRIGATORIAS = ["tarifa_kwh", "chuveiro_potencia_w", "banho_minutos_pessoa_dia", "dias_mes",
                "reducao_banho_pct", "fracao_solar_pct", "investimento_solar_rs",
                "fator_emissao_kg_co2_kwh"]

def carregar_premissas(caminho=CAMINHO_PREMISSAS):
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None
    return dados if isinstance(dados, dict) else None

def valor(premissas, nome):
    item = premissas.get(nome)
    return item.get("valor") if isinstance(item, dict) else None

def fmt(numero, casas=2):
     # número no padrão brasileiro (vírgula decimal)
    return f"{numero:.{casas}f}".replace(".", ",")

def pedir_numero(texto, minimo, maximo, padrao=None):
    # repete até a pessoa digitar um número válido; Enter usa o padrão (se houver)
    while True:
        bruto = input(texto).strip().replace(",", ".")
        if bruto == "" and padrao is not None:
            return padrao
        try:
            numero = float(bruto)
        except ValueError:
            print("Valor inválido. Digite um número (exemplo: 12,5).")
            continue
        if minimo <= numero <= maximo:
            return numero
        print(f"Valor fora do limite. Digite um número de {fmt(minimo, 0)} a {fmt(maximo, 0)}.")

def calcular_economia(caminho=CAMINHO_PREMISSAS):
    
    print("teste")