from no import No


def _dividir(comeco):
    # Divide a lista em duas metades usando dois ponteiros
    # Devolve (primeira_metade, segunda_metade). Exige pelo menos 2 nós
    lento = comeco
    rapido = comeco.proximo
    while rapido is not None and rapido.proximo is not None:
        lento = lento.proximo
        rapido = rapido.proximo.proximo
    segunda = lento.proximo
    lento.proximo = None  # corta a lista no meio
    return comeco, segunda


def _mesclar(a, b, chave, reverso):
    # Junta duas listas já ordenadas em uma só, religando os nós.
    ficticio = No(None)  # nó auxiliar para simplificar 
    ponta = ficticio
    while a is not None and b is not None:
        ka, kb = chave(a.dado), chave(b.dado)
        a_primeiro = (ka >= kb) if reverso else (ka <= kb)
        if a_primeiro:
            ponta.proximo = a
            a = a.proximo
        else:
            ponta.proximo = b
            b = b.proximo
        ponta = ponta.proximo
    ponta.proximo = a if a is not None else b
    return ficticio.proximo


def merge_sort(comeco, chave, reverso=False):
    # Merge Sort sobre nós encadeados
    if comeco is None or comeco.proximo is None:  # vazia ou com 1 nó
        return comeco
    esquerda, direita = _dividir(comeco)
    esquerda = merge_sort(esquerda, chave, reverso)
    direita = merge_sort(direita, chave, reverso)
    return _mesclar(esquerda, direita, chave, reverso)


def insertion_sort(itens, chave, reverso=False):
    # Insertion Sort, não altera lista -> devolve uma nova
    resultado = list(itens)
    for i in range(1, len(resultado)):
        atual = resultado[i]
        k = chave(atual)
        j = i - 1
        while j >= 0 and ((chave(resultado[j]) < k) if reverso
                          else (chave(resultado[j]) > k)):
            resultado[j + 1] = resultado[j]
            j -= 1
        resultado[j + 1] = atual
    return resultado
