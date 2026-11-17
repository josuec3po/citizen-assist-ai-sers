from datetime import date

from assistente import pedir_opcao, pedir_sim_ou_nao
from orientacao import Orientacao

MSG_LISTA_VAZIA = "\nA base está vazia. Cadastre uma orientação primeiro."


# ---------- entradas validadas por categoria ----------
def pedir_texto(texto, obrigatorio=True):
    # Pede um texto; se obrigatório, repete até não ser vazio
    while True:
        valor = " ".join(input(texto).split())
        if valor or not obrigatorio:
            return valor
        print("Este campo não pode ficar vazio.")


def pedir_id(texto):
    # Aqui pede um id inteiro positivo. Devolve None se a pessoa digitar 0
    while True:
        valor = input(texto).strip()
        if valor == "0":
            return None
        if valor.isdecimal() and int(valor) > 0:
            return int(valor)
        print("ID inválido. Digite um número inteiro maior que zero (ou 0 para cancelar).")


def pedir_url(texto):
    while True:
        valor = pedir_texto(texto)
        if valor.startswith(("http://", "https://")):
            return valor
        print("A fonte deve ser um link que comece com http:// ou https://.")


def pedir_palavras_chave():
    while True:
        bruto = input("Palavras-chave separadas por vírgula: ")
        palavras = [p.strip() for p in bruto.split(",") if p.strip()]
        if palavras:
            return palavras
        print("Informe pelo menos uma palavra-chave.")


def pedir_documentos():
    documentos = []
    while True:
        item = pedir_texto(f"Documento {len(documentos) + 1} (Enter vazio para terminar): ",
                           obrigatorio=False)
        if not item:
            if documentos:
                return documentos
            print("Informe pelo menos um item (ex.: 'Nenhum documento é necessário').")
            continue
        documentos.append(item)


def pedir_categoria(base):
    categorias = base.categorias()
    print("Categorias existentes:")
    for i, nome in enumerate(categorias, start=1):
        print(f"  {i}. {nome}")
    print(f"  {len(categorias) + 1}. Criar nova categoria")
    escolha = pedir_opcao("Escolha a categoria: ", 1, len(categorias) + 1)
    if escolha <= len(categorias):
        return categorias[escolha - 1]
    return pedir_texto("Nome da nova categoria: ")


def hoje():
    # Funcao para data sempre atualizada
    return date.today().isoformat()


def salvar_ou_avisar(base):
    if not base.salvar():
        print("Aviso: a alteração vale nesta execução, mas não foi possível gravar o arquivo.")

# ---------- operações ----------
def cadastrar(base):
    print("\n--- Cadastrar orientação (ID 0 cancela) ---")
    sugestao = base.proximo_id()
    while True:
        novo_id = pedir_id(f"ID (sugestão: {sugestao}): ")
        if novo_id is None:
            print("Cadastro cancelado.")
            return
        if base.buscar_por_id(novo_id) is not None:
            print(f"Já existe uma orientação com o ID {novo_id}. Escolha outro.")
            continue
        break

    categoria = pedir_categoria(base)
    titulo = pedir_texto("Título: ")
    palavras = pedir_palavras_chave()
    resposta = pedir_texto("Resposta ao cidadão: ")
    documentos = pedir_documentos()
    onde = pedir_texto("Onde procurar: ")
    fonte = pedir_url("Fonte (link oficial): ")

    orientacao = Orientacao(novo_id, categoria, titulo, palavras, resposta,
                            documentos, onde, fonte, hoje())
    if base.cadastrar(orientacao):
        salvar_ou_avisar(base)
        print(f"\nOrientação {novo_id} cadastrada. Total na base: {len(base)}.")
    else:
        print("Não foi possível cadastrar (ID repetido ou inválido).")


def consultar_id(base):
    print("\n--- Consultar por ID ---")
    if len(base) == 0:
        print(MSG_LISTA_VAZIA)
        return
    identificador = pedir_id("ID da orientação (0 cancela): ")
    if identificador is None:
        return
    orientacao = base.buscar_por_id(identificador)
    if orientacao is None:
        print(f"Nenhuma orientação com o ID {identificador}.")
    else:
        orientacao.exibir()


def pesquisar(base):
    print("\n--- Pesquisar ---")
    if len(base) == 0:
        print(MSG_LISTA_VAZIA)
        return
    print("1. Por título")
    print("2. Por categoria")
    print("0. Voltar")
    opcao = pedir_opcao("Escolha: ", 0, 2)
    if opcao == 0:
        return
    termo = pedir_texto("Termo de busca: ")
    if opcao == 1:
        achados = base.pesquisar_por_titulo(termo)
    else:
        achados = base.pesquisar_por_categoria(termo)
    if not achados:
        print(f"Nenhuma orientação encontrada para '{termo}'.")
        return
    print(f"\n{len(achados)} orientação(ões) encontrada(s):")
    for o in achados:
        print(f"  {o.id:>3} | {o.categoria} | {o.titulo}")


def atualizar(base):
    print("\n--- Atualizar orientação ---")
    if len(base) == 0:
        print(MSG_LISTA_VAZIA)
        return
    identificador = pedir_id("ID da orientação (0 cancela): ")
    if identificador is None:
        return
    orientacao = base.buscar_por_id(identificador)
    if orientacao is None:
        print(f"Nenhuma orientação com o ID {identificador}.")
        return

    orientacao.exibir()
    print("\nQual campo deseja alterar?")
    campos = ["categoria", "titulo", "palavras_chave", "resposta",
              "documentos", "onde", "fonte"]
    rotulos = ["Categoria", "Título", "Palavras-chave", "Resposta",
               "Documentos", "Onde procurar", "Fonte"]
    for i, rotulo in enumerate(rotulos, start=1):
        print(f"  {i}. {rotulo}")
    print("  0. Cancelar")
    escolha = pedir_opcao("Escolha: ", 0, len(campos))
    if escolha == 0:
        return

    campo = campos[escolha - 1]
    if campo == "categoria":
        valor = pedir_categoria(base)
    elif campo == "palavras_chave":
        valor = pedir_palavras_chave()
    elif campo == "documentos":
        valor = pedir_documentos()
    elif campo == "fonte":
        valor = pedir_url("Nova fonte (link oficial): ")
    else:
        valor = pedir_texto(f"Novo valor para {rotulos[escolha - 1]}: ")

    base.atualizar(identificador, **{campo: valor, "verificado_em": hoje()})
    salvar_ou_avisar(base)
    print(f"\nOrientação {identificador} atualizada.")


def excluir(base):
    print("\n--- Excluir orientação ---")
    if len(base) == 0:
        print(MSG_LISTA_VAZIA)
        return
    identificador = pedir_id("ID da orientação (0 cancela): ")
    if identificador is None:
        return
    orientacao = base.buscar_por_id(identificador)
    if orientacao is None:
        print(f"Nenhuma orientação com o ID {identificador}.")
        return
    print(f"Orientação encontrada: {orientacao.titulo} [{orientacao.categoria}]")
    if not pedir_sim_ou_nao("Tem certeza que deseja excluir? (s/n): "):
        print("Exclusão cancelada.")
        return
    base.excluir(identificador)
    salvar_ou_avisar(base)
    print(f"Orientação {identificador} excluída. Total na base: {len(base)}.")

def listar_ordenado(base):
    print("\n--- Listar orientações ordenadas ---")
    if len(base) == 0:
        print(MSG_LISTA_VAZIA)
        return
    print("Ordenar por:")
    print("  1. ID")
    print("  2. Título")
    print("  3. Categoria")
    print("  0. Voltar")
    criterio = pedir_opcao("Escolha: ", 0, 3)
    if criterio == 0:
        return
    print("  1. Crescente")
    print("  2. Decrescente")
    sentido = pedir_opcao("Sentido: ", 1, 2)

    base.ordenar(["id", "titulo", "categoria"][criterio - 1], reverso=(sentido == 2))
    print(f"\n{'ID':>3} | {'Categoria':<22} | Título")
    print("-" * 70)
    for o in base.orientacoes:  # percurso da lista encadeada
        print(f"{o.id:>3} | {o.categoria:<22} | {o.titulo}")

def analise(base):
    print("\n--- Análise da base ---")
    resumo = base.analise()
    if resumo["total"] == 0:
        print(MSG_LISTA_VAZIA)
        return
    print(f"Total de orientações: {resumo['total']}")
    print("Orientações por categoria:")
    for categoria, quantidade in resumo["por_categoria"]:
        porcentagem = quantidade / resumo["total"] * 100
        print(f"  {categoria:<24} {quantidade:>2}  ({porcentagem:.0f}%)")
    print(f"Média de palavras-chave por orientação: {resumo['media_palavras_chave']:.1f}")
    print(f"Verificação mais antiga: {resumo['verificacao_mais_antiga']}")
