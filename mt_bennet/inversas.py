#Fase 3 (Retrace) da maquina reversivel de Bennett.

#inverter_quadrupla
#gerar_estagio3: aplica a inversao a TODAS as quadruplas da fase 1 e renomeia os estados por Cs pra referir a fase 3

NAO_LIDO = "/"


def inverte_movimento(mov):
    #R <-> L ; S (parado) continua S
    if mov == "R":
        return "L"
    if mov == "L":
        return "R"
    if mov == "S":
        return "S"
    raise ValueError(f"Movimento invalido: {mov!r}")


def inverter_quadrupla(estado_atual, leitura, proximo_estado, escrita, movimento):
    
    # recebe uma quadrupla no formato (estado_atual, leitura) -> (proximo_estado, escrita, movimento) e devolve a inversa
    # troca-se o estado inicial pelo final
    # em cada fita que foi lida ou escrita: passa-se a ler o que antes era escrito, e a escrever o que antes era lido (ela continua parada, movimento "S")
    # em cada fita que so foi deslocada (leitura "/"): ela continua "nao lida" e so deslocada, mas na direcao oposta

    #retorna (nova_chave, novo_valor)
    
    n = len(leitura)
    nova_leitura = [None] * n
    nova_escrita = [None] * n
    novo_movimento = [None] * n

    for k in range(n):
        lido_k = leitura[k]
        escrito_k = escrita[k]
        mov_k = movimento[k]

        if lido_k == NAO_LIDO:
            # fita k so foi deslocada -> continua so deslocada, direcao oposta
            nova_leitura[k] = NAO_LIDO
            nova_escrita[k] = NAO_LIDO
            novo_movimento[k] = inverte_movimento(mov_k)
        else:
            # fita k foi lida e escrita -> troca leitura <-> escrita
            nova_leitura[k] = escrito_k
            nova_escrita[k] = lido_k
            novo_movimento[k] = "S"

    nova_chave = (proximo_estado, tuple(nova_leitura))
    novo_valor = (estado_atual, tuple(nova_escrita), tuple(novo_movimento))
    return nova_chave, novo_valor


def renomear_estado(estado, prefixo="C_"):
    """A_i -> C_i (aqui os estados da fase 1 nao tem o prefixo 'A_'
    explicito, entao so acrescentamos o prefixo 'C_' a cada um)."""
    return f"{prefixo}{estado}"


def gerar_estagio3(quadruplas_estagio1, prefixo="C_"):
    
    # gera a fase Retrace inteira a partir do dicionario de quadruplas da fase Compute: inverte cada uma e renomeia os estados pra C no iniicio
    estagio3 = {}

    for chave, valor in quadruplas_estagio1.items():
        estado_atual, leitura = chave
        proximo_estado, escrita, movimento = valor

        chave_inv, valor_inv = inverter_quadrupla(
            estado_atual, leitura, proximo_estado, escrita, movimento
        )

        estado_de, leitura_inv = chave_inv
        estado_para, escrita_inv, movimento_inv = valor_inv

        chave_c = (renomear_estado(estado_de, prefixo), leitura_inv)
        valor_c = (
            renomear_estado(estado_para, prefixo),
            escrita_inv,
            movimento_inv,
        )

        estagio3[chave_c] = valor_c

    return estagio3