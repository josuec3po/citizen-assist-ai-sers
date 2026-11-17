from no import No
from ordenacao import merge_sort


class ListaEncadeada:
    # Lista simplesmente encadeada com ponteiros para começo e final
    def __init__(self):
        self.comeco = None
        self.final = None
        self._tamanho = 0

    def __len__(self):
        return self._tamanho

    def esta_vazia(self):
        return self.comeco is None

    # ---------- inserção ----------
    def inserir_inicio(self, dado):
        # O(1)
        novo = No(dado)
        novo.proximo = self.comeco
        self.comeco = novo
        if self.final is None:  # lista estava vazia
            self.final = novo
        self._tamanho += 1

    def inserir_fim(self, dado):
        # O(1) por conta do ponteiro para o final.
        novo = No(dado)
        if self.final is None:
            self.comeco = novo
        else:
            self.final.proximo = novo
        self.final = novo
        self._tamanho += 1

    # ---------- percurso ----------
    def __iter__(self):
        # Percorre a lista do primeiro ao último nó -> O(n)
        atual = self.comeco
        while atual is not None:
            yield atual.dado
            atual = atual.proximo

    # ---------- busca ----------
    def buscar(self, atributo):
        # Busca linear: devolve o primeiro dado para qual a condição é verdadeira, ou None se não houver -> O(n)
        atual = self.comeco
        while atual is not None:
            if atributo(atual.dado):
                return atual.dado
            atual = atual.proximo
        return None

    def buscar_todos(self, atributo):
        # Devolve uma lista Python com todos os dados que satisfazem a condição
        return [dado for dado in self if atributo(dado)]

    # ---------- remoção ----------
    def remover(self, atributo):
        # Remove o primeiro nó que satisfaz a condição
        anterior = None
        atual = self.comeco
        while atual is not None:
            if atributo(atual.dado):
                if anterior is None:         
                    self.comeco = atual.proximo
                else:                        
                    anterior.proximo = atual.proximo
                if atual is self.final:      
                    self.final = anterior
                self._tamanho -= 1
                return True
            anterior = atual
            atual = atual.proximo
        return False

    def limpar(self):
        self.comeco = None
        self.final = None
        self._tamanho = 0

    # ---------- ordenação ----------
    def ordenar(self, chave, reverso=False):
        # Ordena lista com Merge Sort
        # O(n log n)
        self.comeco = merge_sort(self.comeco, chave, reverso)
        # a final pode ter mudado -> reencontra o ultimo nó
        atual = self.comeco
        self.final = atual
        while atual is not None:
            self.final = atual
            atual = atual.proximo
