# Cálculos e comparação das alternativas

## 1. Necessidade e público
- **Público:** pessoas idosas (60 anos ou mais) e familiares que cuidam do orçamento da casa. Muitos vivem de aposentadoria ou BPC e passam mais tempo em casa.
- **Necessidade:** aquecimento de água para o banho diário. O chuveiro elétrico tem potência alta e pesa direto na conta de luz no fim do mês.
- **Papel do assistente:** responder dúvidas em português claro, sem jargão técnico, e rodar a calculadora da opção 12 para mostrar o gasto e o retorno financeiro conforme a realidade de cada casa.

## 2. Premissas
Dados copiados de `data/energia_premissas.json`. Itens marcados como **real** vêm de órgãos e tabelas técnicas; itens **estimados** são padrões definidos pela equipe.

| Parâmetro | Valor | Unidade | Tipo | Fonte | Acesso em |
|---|---|---|---|---|---|
| Tarifa de energia | 0,92 | R$/kWh | real | ANEEL / Enel SP — Tarifa Residencial B1 com impostos (PIS/COFINS/ICMS), bandeira verde | 2026-11 |
| Potência do chuveiro | 5500 | W | real | Procel / Inmetro — Tabela de Consumo de Chuveiros Elétricos (posição inverno) | 2026-11 |
| Duração do banho | 10 | min/pessoa/dia | estimado | Estimativa da equipe baseada em recomendações da Sabesp/Procel: 1 banho diário de 10 minutos por pessoa | 2026-11 |
| Dias de uso no mês | 30 | dias | estimado | Padrão comercial de faturamento mensal do setor elétrico | 2026-11 |
| Redução com banho mais curto | 30 | % | estimado | Procel Info — Dicas de Economia: corte estimado ao diminuir o banho (de 10 para ~7 min) ou mudar a chave para modo morno/verão | 2026-11 |
| Fração atendida pelo sol | 70 | % | real | EPE (Empresa de Pesquisa Energética) / Dasol-Abrava — Média anual para aquecedores solares no Sudeste/Brasil (30% de apoio elétrico) | 2026-11 |
| Investimento no aquecedor solar | 3200 | R$ | real | Cotação média de mercado — Aquecedor solar acoplado (boiler 200L + placas coletoras + instalação) para até 3 moradores | 2026-11 |
| Fator de emissão da rede elétrica | 0,0385 | kg CO2/kWh | real | MCTI — Fator Médio de Emissão do Sistema Interligado Nacional (SIN) | 2026-11 |

## 3. Fórmulas (iguais às de `energia_calculos.py`)
- **Consumo mensal (kWh):** `potência (W) / 1000 × minutos por dia / 60 × dias do mês`
- **Custo mensal (R$):** `consumo (kWh) × tarifa (R$/kWh)`
- **Emissão mensal (kg CO2):** `consumo (kWh) × fator de emissão`
- **Uso consciente:** `consumo × (1 − redução %)`
- **Aquecimento solar:** `consumo × (1 − fração solar %)`
- **Retorno do investimento (meses):** `investimento ÷ economia mensal em reais`

## 4. Alternativas comparadas
Todas atendem à mesma demanda (banho diário dos moradores) nos períodos de **1 mês** e **12 meses**:
- **A. Chuveiro elétrico (situação atual):** aparelho ligado na posição inverno, sem mudanças de rotina ou equipamento.
- **B. Uso consciente:** mesmo chuveiro elétrico, mas com banho mais curto ou chave na posição morno/verão.
- **C. Aquecimento solar (fonte renovável):** placas coletoras solares e reservatório térmico (boiler), usando resistência elétrica só em dias nublados ou muito frios (30% do consumo).

## 5. Resultados (casa de referência: 2 pessoas)
Com 2 moradores tomando 1 banho de 10 minutos por dia (20 minutos/dia), o gasto base é `5,5 kW × (20 / 60) h × 30 dias = 55,00 kWh/mês`:

| Alternativa | Consumo (kWh/mês) | Custo (R$/mês) | Custo (R$/ano) | CO2 (kg/ano) | Investimento (R$) | Retorno |
|---|---|---|---|---|---|---|
| **A. Chuveiro elétrico (atual)** | 55,00 | R$ 50,60 | R$ 607,20 | 25,41 | R$ 0,00 | - |
| **B. Uso consciente (-30%)** | 38,50 | R$ 35,42 | R$ 425,04 | 17,79 | R$ 0,00 | Imediato |
| **C. Aquecimento solar (-70%)** | 16,50 | R$ 15,18 | R$ 182,16 | 7,62 | R$ 3.200,00 | ~7,5 anos (90,3 meses) |

Se a casa tiver **4 moradores** (40 minutos/dia), o gasto atual dobra para R$ 101,20/mês. Nesse cenário, o aquecedor solar economiza R$ 70,84/mês e se paga em **~3,8 anos (45,2 meses)**.

## 6. Custos, viabilidade e impacto ambiental
- **Alternativa A (Chuveiro elétrico atual):**
  - *Custo e viabilidade:* gasto inicial zero, pois o aparelho já está na parede. O peso fica todo na conta mensal (R$ 607,20/ano para 2 pessoas).
  - *Manutenção:* troca simples e barata da resistência quando queima.
  - *Impacto ambiental:* gera 25,41 kg de CO2/ano no cenário base e sobrecarrega a rede elétrica no horário de pico (18h às 21h).
- **Alternativa B (Uso consciente):**
  - *Custo e viabilidade:* custo zero e aplicação imediata em qualquer imóvel (casa própria, alugada ou apartamento), sem quebra-quebra.
  - *Manutenção:* nenhuma alteração física; depende só do hábito dos moradores.
  - *Impacto ambiental:* corta 30% do gasto de eletricidade e água, evitando 7,62 kg de CO2 por ano.
- **Alternativa C (Aquecimento solar):**
  - *Custo e viabilidade:* exige R$ 3.200,00 na compra e instalação, além de telhado com sol, estrutura para aguentar o peso do boiler cheio e encanamento para água quente. Não serve para apartamentos ou imóveis alugados sem aval do proprietário.
  - *Vida útil e manutenção:* dura de 15 a 20 anos, pedindo apenas limpeza periódica dos vidros das placas e revisão eventual da resistência de apoio.
  - *Impacto ambiental:* usa energia solar térmica limpa, cortando 70% da eletricidade do banho e evitando 17,79 kg de CO2/ano (mais de 350 kg de CO2 evitados em 20 anos).

## 7. Recomendação e limitações
- **Quem deve escolher o quê:**
  - **Idosos em apartamento, imóvel alugado ou com orçamento apertado:** ficar com o **Uso Consciente (Alternativa B)**. Economiza ~R$ 182/ano na hora, sem gastar nada.
  - **Famílias com 3 ou mais pessoas em casa própria e com reserva financeira:** investir no **Aquecimento Solar (Alternativa C)**. O abatimento de 70% paga o equipamento em menos de 4 anos e reduz a emissão de carbono a longo prazo.
- **Limitações:**
  - Os números são **estimativas** e não garantem desconto exato na fatura.
  - O resultado muda conforme a tarifa da distribuidora local, bandeiras tarifárias, potência real do chuveiro, clima da cidade e tempo de banho de cada pessoa.