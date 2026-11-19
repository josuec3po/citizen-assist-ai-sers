# Elderly Assist (Citizen Assist AI)

Assistente de terminal em Python que orienta **pessoas idosas** sobre saúde, transporte, direitos, prevenção de golpes e economia de energia, usando uma base de conhecimento verificada em fontes oficiais e uma calculadora de consumo residencial.

## Integrantes
- Josué Franco Braga — RM 569174
- Manoel da Silva Ferreira — RM 572045
- Fernando Lobato Rodrigues — RM 569377

## Público e problema
- **Público:** pessoas idosas (60 anos ou mais) e familiares que auxiliam nas tarefas e contas da casa.
- **Problema:** informações sobre Cartão SUS, vacinas, benefícios do INSS, transporte e prevenção de golpes estão espalhadas em linguagem técnica ou misturadas com páginas falsas. Na parte energética, o chuveiro elétrico pesa no orçamento de quem vive de aposentadoria ou BPC, e faltam comparativos simples sobre quando vale a pena mudar hábitos ou investir em aquecimento solar.

## ODS relacionados
- **ODS 3, Saúde e Bem-Estar (meta 3.8):** orienta sobre Cartão SUS, vacinas e remédios gratuitos pelo Farmácia Popular.
- **ODS 7, Energia Limpa e Acessível (metas 7.1 e 7.3):** ajuda famílias a cortar o desperdício elétrico no banho e avalia a viabilidade do aquecimento solar térmico.
- **ODS 10, Redução das Desigualdades (meta 10.2):** reúne em linguagem direta direitos e benefícios (aposentadoria, BPC, transporte gratuito, atendimento prioritário).
- **ODS 16, Paz, Justiça e Instituições Eficazes (metas 16.10 e 16.1):** entrega informação com fonte oficial e data de verificação, além de canais de denúncia contra golpes e violência.

## Como executar
Requisitos: Python 3 (somente biblioteca padrão, sem instalar pacotes externos).

```bash
cd citizen-assist-ai-sers
python main.py


Execute sempre dentro da pasta raiz do projeto, pois os caminhos de `data/` são relativos.

Para rodar os testes automatizados da parte de energia:

```bash
python -m unittest testes.test_energia -v

```

## Estrutura do projeto

```text
citizen-assist-ai-sers/
├── README.md
├── main.py                  # menu principal (opções 0 a 12)
├── orientacao.py            # classe Orientacao
├── base_conhecimento.py     # classe BaseConhecimento + normalizar()
├── assistente.py            # classe Assistente (busca, sugestões e métricas)
├── gerir.py                 # CRUD e consultas administrativas
├── lista_encadeada.py       # estrutura de dados própria
├── no.py                    # nó da lista encadeada
├── ordenacao.py             # algoritmos Insertion Sort e Merge Sort
├── energia_calculos.py      # fórmulas de consumo, custo, CO2 e payback
├── tela_da_energia.py       # interface da opção 12 (calculadora de banho)
├── data/
│   ├── base_conhecimento.json   # 14 orientações em 5 categorias
│   ├── energia_premissas.json   # parâmetros reais e estimados com fontes
│   ├── historico.json           # atendimentos registrados
│   └── atendimentos.csv         # exportação dos atendimentos
├── docs/
│   ├── calculos_comparacao.md   # memória de cálculo e comparação (A, B e C)
│   ├── referencias.md           # fontes técnicas e links verificados
│   └── testes_usuarios.md       # registros dos testes de usabilidade (energia)
└── testes/

```

## Contribuição: Soluções em Energias Renováveis e Sustentáveis

Esta disciplina foi integrada ao assistente para resolver o alto gasto com água quente no banho residencial:

* **Calculadora de economia no banho (Opção 12 do menu):** implementada em `energia_calculos.py` e `tela_da_energia.py`. Lê as premissas de `data/energia_premissas.json`, pergunta quantas pessoas moram na casa (além de permitir ajustar minutos de banho e tarifa local) e compara três cenários para o mesmo período (1 mês e 12 meses):
1. **Chuveiro elétrico atual** (5.500 W na posição inverno);
2. **Uso consciente** (redução de 30% por banho mais curto ou chave em morno);
3. **Aquecimento solar com apoio elétrico** (fonte renovável que atende 70% da demanda térmica).


* **Base de conhecimento (Opções 1 e 2 do menu):** adicionada a categoria `"Energia e Economia"` em `data/base_conhecimento.json` (IDs 13 e 14) com o resumo dos cálculos para uma casa de referência (2 pessoas), condições de instalação e limitações.
* **Documentação técnica:**
* Premissas e origens dos dados: `data/energia_premissas.json`
* Memória de cálculo, comparação e análise de viabilidade/impacto ambiental: `docs/calculos_comparacao.md`
* Referências bibliográficas e links: `docs/referencias.md`
* Testes com usuários na parte de energia: `docs/testes_usuarios.md`



## Regra de pontuação (Busca textual)

Pergunta, títulos e palavras-chave são normalizados (minúsculas, sem acento e sem pontuação):

* Palavra-chave da orientação presente na pergunta: **+3 pontos**
* Palavra da pergunta (4+ letras) presente no título: **+1 ponto**
* **6 pontos ou mais:** confiança **ALTA**
* **3 a 5 pontos:** confiança **MÉDIA**
* **Menos de 3 pontos:** retorna "não encontrei" e aciona `sugerir()` (busca flexível por palavras soltas: categoria +2, título +1, palavra-chave +1).

## Privacidade e transparência

* O sistema nunca pede nome, CPF, telefone ou e-mail.
* Entradas com 8 ou mais dígitos consecutivos ou com `@` são bloqueadas e não vão para o histórico.
* Todas as respostas exibem fonte, data de verificação, limitações das estimativas e o aviso de que o assistente não é canal oficial.

## Fontes consultadas

* **Saúde, Direitos e Segurança:** Ministério da Saúde (Meu SUS Digital, Vacinação, Farmácia Popular), Estatuto da Pessoa Idosa (Lei 10.741/2003), INSS e Ministério dos Direitos Humanos (Disque 100).
* **Energia e Sustentabilidade:** ANEEL / Enel SP (tarifas), Inmetro / Procel (potência de chuveiros), Sabesp, LabEEE / UFSC (fração solar), Energia Solar Explicada (cotação de mercado) e MCTI (fator de emissão de CO2 do SIN).

## Testes com usuários

### 1. Base geral (Saúde, Transporte, Direitos e Golpes)

Testado com 4 pessoas de fora da equipe, somando 11 atendimentos entre 12 e 13 de novembro de 2026 (códigos anônimos P05 a P08):

* **Indicadores (opção 10):** 82% de resposta encontrada, 82% de taxa de acerto, tempo médio de 10,2 s, 1,0 tentativa por atendimento e nota de facilidade 4,2/5.
* **Dúvidas sem solução:** `"transporte"` e `"meios de transporte gratis"`.
* **Ajuste realizado:** a orientação 5 usava apenas `"gratuito"` nas palavras-chave. Adicionamos `"transporte"` e `"transporte gratis"`, elevando a pontuação para 4 pontos (confiança MÉDIA).

### 2. Funcionalidade de Energia (Opção 1 e Opção 12)

Os registros detalhados dos testes da calculadora de energia e das perguntas sobre economia na conta de luz estão documentados em `docs/testes_usuarios.md`.

## Limitações

* Responde apenas às 14 orientações cadastradas na base e depende das palavras-chave registradas para reconhecer variações de escrita.
* Os cálculos de energia são **estimativas** baseadas em premissas médias; a economia real muda conforme a tarifa da distribuidora, bandeira tarifária, potência do aparelho, clima e hábitos dos moradores.
* Regras municipais (como gratuidade de ônibus local) variam por cidade.

## Vídeo técnico

* Link do vídeo (YouTube não listado): [INSERIR LINK AQUI ANTES DE SUBIR NO GITHUB]

```

```