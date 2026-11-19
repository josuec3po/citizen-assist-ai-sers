# Cálculos de energia Elderly Assist/Citizen Assist AI

def consumo_kwh_mes(potencia_w, minutos_por_dia, dias_mes=30):
    # kWh = potência (em kW) x horas de uso por dia x dias do mês
    return potencia_w / 1000 * (minutos_por_dia / 60) * dias_mes


def custo_mes(kwh, tarifa_kwh):
    return kwh * tarifa_kwh


def emissao_kg_mes(kwh, fator_kg_por_kwh):
    return kwh * fator_kg_por_kwh


def consumo_com_reducao(kwh, reducao_pct):
    # alternativa de uso consciente -> banho mais curto reduz o consumo
    return kwh * (1 - reducao_pct / 100)


def consumo_com_solar(kwh, fracao_solar_pct):
    # parte da água quente vem do sol -> restante usa energia elétrica
    return kwh * (1 - fracao_solar_pct / 100)


def payback_meses(investimento, economia_reais_mes):
    # em quantos meses a economia paga o investimento -> None se não há economia
    if economia_reais_mes <= 0:
        return None
    return investimento / economia_reais_mes


def comparar(kwh_atual, kwh_alternativa, tarifa_kwh, fator_emissao, investimento=0):
    # compara uma alternativa com a situação atual, por mês
    economia_kwh = kwh_atual - kwh_alternativa
    economia_reais = custo_mes(economia_kwh, tarifa_kwh)
    return {
        "consumo_kwh_mes": kwh_alternativa,
        "custo_mes": custo_mes(kwh_alternativa, tarifa_kwh),
        "emissao_kg_mes": emissao_kg_mes(kwh_alternativa, fator_emissao),
        "economia_kwh_mes": economia_kwh,
        "economia_reais_mes": economia_reais,
        "emissao_evitada_kg_mes": emissao_kg_mes(economia_kwh, fator_emissao),
        "payback_meses": payback_meses(investimento, economia_reais) if investimento > 0 else None,
    }
