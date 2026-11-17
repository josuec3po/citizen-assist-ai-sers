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
    print("\n--- Calcular economia de energia no banho ---")
    premissas = carregar_premissas(caminho)
    if premissas is None:
        print("Não consegui ler as premissas de energia (data/energia_premissas.json).")
        return
    faltando = [nome for nome in OBRIGATORIAS if valor(premissas, nome) is None]
    if faltando:
        print("Ainda faltam valores nas premissas: " + ", ".join(faltando))
        return

    tarifa_padrao = valor(premissas, "tarifa_kwh")
    minutos_padrao = valor(premissas, "banho_minutos_pessoa_dia")

    pessoas = int(pedir_numero("Quantas pessoas tomam banho na casa? (1 a 10): ", 1, 10))
    minutos = pedir_numero(f"Minutos de banho por pessoa por dia (Enter = {fmt(minutos_padrao, 0)}): ",
                           1, 60, minutos_padrao)
    tarifa = pedir_numero(f"Valor do kWh na sua conta, em R$ (Enter = {fmt(tarifa_padrao)}): ",
                          0.01, 10, tarifa_padrao)

    fator = valor(premissas, "fator_emissao_kg_co2_kwh")
    invest = valor(premissas, "investimento_solar_rs")
    atual = energia.consumo_kwh_mes(valor(premissas, "chuveiro_potencia_w"),
                                    minutos * pessoas, valor(premissas, "dias_mes"))
    consciente = energia.consumo_com_reducao(atual, valor(premissas, "reducao_banho_pct"))
    solar = energia.consumo_com_solar(atual, valor(premissas, "fracao_solar_pct"))

    opcoes = [
        ("Chuveiro elétrico (situação atual)", energia.comparar(atual, atual, tarifa, fator)),
        ("Uso consciente (banho mais curto)", energia.comparar(atual, consciente, tarifa, fator)),
        ("Aquecimento solar (com apoio elétrico)", energia.comparar(atual, solar, tarifa, fator, invest)),
    ]

    print("\nEstimativa por mês:")
    for nome, r in opcoes:
        print(f"\n{nome}")
        print(f"  Consumo: {fmt(r['consumo_kwh_mes'])} kWh | Custo: R$ {fmt(r['custo_mes'])} "
              f"| CO2: {fmt(r['emissao_kg_mes'])} kg")
        if r["economia_kwh_mes"] > 0:
            print(f"  Economia: R$ {fmt(r['economia_reais_mes'])} por mês "
                  f"e {fmt(r['emissao_evitada_kg_mes'])} kg de CO2 evitados")
        if r["payback_meses"] is not None:
            print(f"  Investimento: R$ {fmt(invest, 0)} | retorno em cerca de "
                  f"{fmt(r['payback_meses'] / 12, 1)} anos")

    print("\nCondições e limitações:")
    for texto in premissas.get("limitacoes", []):
        print(f"  - {texto}")
    print("  - São estimativas, não garantem a economia real na sua conta.")
    print("\nFontes das premissas:")
    for nome in OBRIGATORIAS:
        item = premissas[nome]
        print(f"  - {nome} ({item.get('tipo', '?')}): {item.get('fonte', '')}")
    print("Aviso: este assistente NÃO é um canal oficial.")