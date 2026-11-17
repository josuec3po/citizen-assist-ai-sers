import json
import os

from lista_encadeada import ListaEncadeada
from ordenacao import insertion_sort
from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}

# Pesos da pontuação (explicados no README)
PONTOS_PALAVRA_CHAVE = 3
PONTOS_PALAVRA_TITULO = 1
TAMANHO_MINIMO_PALAVRA_TITULO = 4

# Palavras genéricas ignoradas na busca flexível (sugerir)
PALAVRAS_IGNORADAS = {"como", "para", "quero", "saber", "sobre", "preciso", "onde",
                      "fazer", "tenho", "minha", "qual", "quais", "pode", "posso",
                      "gostaria", "queria", "ajuda", "idoso", "idosa", "idosos",
                      "pessoa", "pessoas", "anos", "muito", "estou"}

# Campos que podem ser alterados em uma atualização (o id nunca muda)
CAMPOS_EDITAVEIS = {"categoria", "titulo", "palavras_chave", "resposta",
                    "documentos", "onde", "fonte", "verificado_em"}


def normalizar(texto):
    # Minúsculas, sem acentos e sem pontuação. Devolve com espaço nas pontas para que a busca encontre palavras inteiras (Por exemplo.: sus e não susto)
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    # Conjunto de todas as orientações, guardado em uma lista encadeada.
    # Le e grava o JSON, faz CRUD, busca, ordenação e análise.

    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = ListaEncadeada()  # lista encadeada de Orientacao

    def __len__(self):
        return len(self.orientacoes)

    # ---------- persistência ----------
    def carregar(self):
        # Le o JSON e insere cada Orientacao na lista encadeada.
        # Ignora (com aviso) registros inválidos ou com id repetido.
        self.orientacoes = ListaEncadeada()
        try:
            with open(self.caminho, encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print("Aviso: arquivo da base de conhecimento não encontrado.")
            return
        except (json.JSONDecodeError, OSError):
            print("Aviso: arquivo da base de conhecimento ausente ou corrompido.")
            return

        if not isinstance(dados, list):
            print("Aviso: o JSON da base deve ser uma lista de orientações.")
            return

        for registro in dados:
            try:
                orientacao = Orientacao(**registro)
            except TypeError:
                identificador = registro.get("id", "?") if isinstance(registro, dict) else "?"
                print(f"Aviso: registro (id {identificador}) com campos incorretos foi ignorado.")
                continue
            self.cadastrar(orientacao, avisar=True)

    def salvar(self):
        # Grava a lista no JSON usando um arquivo temporário, para não corromper
        # o arquivo se algo falhar no meio. Devolve True ou False.
        dados = [o.para_dict() for o in self.orientacoes]
        temporario = self.caminho + ".tmp"
        try:
            os.makedirs(os.path.dirname(self.caminho) or ".", exist_ok=True)
            with open(temporario, "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=2)
            os.replace(temporario, self.caminho)
            return True
        except OSError:
            return False

    # ---------- CRUD ----------
    def buscar_por_id(self, identificador):
        # Busca linear pelo id. Devolve a Orientacao ou None. O(n)
        return self.orientacoes.buscar(lambda o: o.id == identificador)

    def proximo_id(self):
        # Maior id existente + 1 (ou 1 se a lista estiver vazia). O(n)
        maior = 0
        for o in self.orientacoes:
            if o.id > maior:
                maior = o.id
        return maior + 1

    def cadastrar(self, orientacao, avisar=False):
        # Insere no final da lista. Recusa id repetido ou inválido.
        # Devolve True se cadastrou. O(n) por causa da checagem de id.
        if not isinstance(orientacao.id, int) or isinstance(orientacao.id, bool) \
                or orientacao.id <= 0:
            if avisar:
                print(f"Aviso: registro com id inválido ({orientacao.id!r}) foi ignorado.")
            return False
        if self.buscar_por_id(orientacao.id) is not None:
            if avisar:
                print(f"Aviso: id {orientacao.id} repetido; o segundo registro foi ignorado.")
            return False
        self.orientacoes.inserir_fim(orientacao)
        return True

    def atualizar(self, identificador, **campos):
        # Altera campos de uma orientação existente. Devolve True ou False.
        orientacao = self.buscar_por_id(identificador)
        if orientacao is None:
            return False
        for nome, valor in campos.items():
            if nome in CAMPOS_EDITAVEIS:
                setattr(orientacao, nome, valor)
        return True

    def excluir(self, identificador):
        # Remove o nó com esse id, mantendo o encadeamento. O(n)
        return self.orientacoes.remover(lambda o: o.id == identificador)

    # ---------- consultas ----------
    def categorias(self):
        # Lista de categorias, sem repetir, na ordem em que aparecem
        nomes = []
        for o in self.orientacoes:
            if o.categoria not in nomes:
                nomes.append(o.categoria)
        return nomes

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pesquisar_por_titulo(self, termo):
        # Busca linear: títulos que contêm o termo (sem acento nem maiúsculas).
        # Devolve lista vazia se nada for encontrado.
        termo_norm = normalizar(termo).strip()
        if not termo_norm:
            return []
        return self.orientacoes.buscar_todos(
            lambda o: termo_norm in normalizar(o.titulo))

    def pesquisar_por_categoria(self, termo):
        # Igual à busca por título, mas sobre a categoria
        termo_norm = normalizar(termo).strip()
        if not termo_norm:
            return []
        return self.orientacoes.buscar_todos(
            lambda o: termo_norm in normalizar(o.categoria))

    # ---------- ordenação ----------
    def ordenar(self, criterio, reverso=False):
        # Ordena a lista encadeada (Merge Sort) por 'id', 'titulo' ou 'categoria'.
        # Devolve False se o critério não existir.
        if criterio == "id":
            chave = lambda o: o.id
        elif criterio == "titulo":
            chave = lambda o: normalizar(o.titulo)
        elif criterio == "categoria":
            chave = lambda o: normalizar(o.categoria)
        else:
            return False
        self.orientacoes.ordenar(chave, reverso)
        return True

    # ---------- análise ----------
    def analise(self):
        # Resumo da base: total, quantidade por categoria (da maior para a menor),
        # média de palavras-chave e a verificação mais antiga.
        contagem = {}
        total_chaves = 0
        mais_antiga = None
        for o in self.orientacoes:
            contagem[o.categoria] = contagem.get(o.categoria, 0) + 1
            total_chaves += len(o.palavras_chave)
            if mais_antiga is None or o.verificado_em < mais_antiga:
                mais_antiga = o.verificado_em
        total = len(self.orientacoes)
        por_categoria = insertion_sort(list(contagem.items()),
                                       chave=lambda par: par[1], reverso=True)
        return {
            "total": total,
            "por_categoria": por_categoria,
            "media_palavras_chave": (total_chaves / total) if total else 0,
            "verificacao_mais_antiga": mais_antiga,
        }

    # ---------- busca por pontuação (assistente) ----------
    def pontuar(self, pergunta, orientacao):
        # +3 por palavra-chave que aparece na pergunta
        # +1 por palavra da pergunta (4+ letras) que aparece no titulo
        pergunta_norm = normalizar(pergunta)
        pontos = 0

        for palavra in orientacao.palavras_chave:
            if normalizar(palavra) in pergunta_norm:
                pontos += PONTOS_PALAVRA_CHAVE

        titulo_norm = normalizar(orientacao.titulo)
        for palavra in pergunta_norm.split():
            if (len(palavra) >= TAMANHO_MINIMO_PALAVRA_TITULO
                    and (" " + palavra + " ") in titulo_norm):
                pontos += PONTOS_PALAVRA_TITULO

        return pontos

    def buscar(self, pergunta):
        # Devolve lista de tuplas (pontos, orientacao), da maior para menor.
        # Ordena com o Insertion Sort próprio, sem sorted/sort.
        resultados = []
        for o in self.orientacoes:
            pontos = self.pontuar(pergunta, o)
            if pontos > 0:
                resultados.append((pontos, o))
        return insertion_sort(resultados, chave=lambda par: par[0], reverso=True)

    def sugerir(self, pergunta, maximo=3):
        # Busca flexivel -> palavras soltas da pergunta
        palavras = {p for p in normalizar(pergunta).split()
                    if len(p) >= 4 and p not in PALAVRAS_IGNORADAS}
        sugestoes = []
        for o in self.orientacoes:
            categoria = normalizar(o.categoria).split()
            titulo = normalizar(o.titulo).split()
            chaves = " ".join(normalizar(k) for k in o.palavras_chave).split()
            pontos = 0
            for p in palavras:
                if p in categoria:
                    pontos += 2
                if p in titulo:
                    pontos += 1
                if p in chaves:
                    pontos += 1
            if pontos > 0:
                sugestoes.append((pontos, o))
        sugestoes = insertion_sort(sugestoes, chave=lambda par: par[0], reverso=True)
        return sugestoes[:maximo]