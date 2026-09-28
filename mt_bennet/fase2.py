# Fase 2: percorre a saída da fita 1 da esquerda para a direita,
# copiando os símbolos para a fita 3, e depois retorna as cabeças
# para suas posições originais.

#As transicoes sao:
#Af [b,N,b]  -> [b,N,b] B1'
#B1' [/ ,/ ,/] -> [R,S,R] B1

#B1 [x,N,b]  -> [x,N,x] B1'    para todo x != b
#B1 [b,N,b]  -> [b,N,b] B2'
#B2' [/ ,/ ,/] -> [L,S,L] B2

#B2 [x,N,x]  -> [x,N,x] B2'   para todo x != b
#B2 [b,N,b]  -> [b,N,b] Cf

NAO_LIDO = "/"


def _normalizar_simbolos(alfabeto, branco):
    """Retorna os simbolos unicos do alfabeto, mantendo a ordem."""
    resultado = []
    for simbolo in alfabeto:
        simbolo = branco if simbolo == "B" and branco == "_" else simbolo
        if simbolo not in resultado:
            resultado.append(simbolo)
    return resultado


def gerar_estagio2(
    estado_aceitacao,
    numero_quintuplas,
    alfabeto_trabalho,
    branco="_",
    prefixo_b="B_",
    prefixo_c="C_",
):

    if not alfabeto_trabalho:
        raise ValueError("O alfabeto da fita de trabalho nao pode ser vazio.")

    simbolos = _normalizar_simbolos(alfabeto_trabalho, branco)
    if branco not in simbolos:
        simbolos.append(branco)

    simbolos_nao_brancos = [s for s in simbolos if s != branco]

    historico_final = str(numero_quintuplas)

    estado_b1 = f"{prefixo_b}1"
    estado_b1_linha = f"{prefixo_b}1_linha"
    estado_b2 = f"{prefixo_b}2"
    estado_b2_linha = f"{prefixo_b}2_linha"
    estado_c_final = f"{prefixo_c}{estado_aceitacao}"

    estagio2 = {}

    # Af [b,N,b] -> [b,N,b] P_esq
    # A Fase 1 termina com a cabeca da fita 1 a direita da saida

    estado_posiciona_esquerda = f"{prefixo_b}pos_esq"
    
    estagio2[(
        estado_aceitacao,
        (branco, historico_final, branco),
    )] = (
        estado_posiciona_esquerda,
        (branco, historico_final, branco),
        ("L", "S", "S"),
    )

    estado_posiciona_esquerda = f"{prefixo_b}pos_esq"
    estado_dentro_saida_esq = f"{prefixo_b}pos_esq_dentro"

    # Sai do branco à direita da saída e procura a saída.
    estagio2[(
        estado_aceitacao,
        (branco, historico_final, branco),
    )] = (
        estado_posiciona_esquerda,
        (branco, historico_final, branco),
        ("L", "S", "S"),
    )

    # Enquanto estiver nos brancos à direita da saída, continua para a esquerda.
    estagio2[(
        estado_posiciona_esquerda,
        (branco, historico_final, branco),
    )] = (
        estado_posiciona_esquerda,
        (branco, historico_final, branco),
        ("L", "S", "S"),
    )

    # Encontrou o primeiro símbolo da saída.
    for simbolo in simbolos_nao_brancos:
        estagio2[(
            estado_posiciona_esquerda,
            (simbolo, historico_final, branco),
        )] = (
            estado_dentro_saida_esq,
            (simbolo, historico_final, branco),
            ("L", "S", "S"),
        )

    # Continua atravessando a saída para a esquerda.
    for simbolo in simbolos_nao_brancos:
        estagio2[(
            estado_dentro_saida_esq,
            (simbolo, historico_final, branco),
        )] = (
            estado_dentro_saida_esq,
            (simbolo, historico_final, branco),
            ("L", "S", "S"),
        )

    # Encontrou o branco imediatamente à esquerda da saída.
    estagio2[(
        estado_dentro_saida_esq,
        (branco, historico_final, branco),
    )] = (
        estado_b1_linha,
        (branco, historico_final, branco),
        ("S", "S", "S"),
    )

    # B1' [///] -> [+ 0 +] B1
    estagio2[(
        estado_b1_linha,
        (NAO_LIDO, NAO_LIDO, NAO_LIDO),
    )] = (
        estado_b1,
        (NAO_LIDO, NAO_LIDO, NAO_LIDO),
        ("R", "S", "R"),
    )

    # B1 [x N b] -> [x N x] B1'
    for simbolo in simbolos_nao_brancos:
        estagio2[(
            estado_b1,
            (simbolo, historico_final, branco),
        )] = (
            estado_b1_linha,
            (simbolo, historico_final, simbolo),
            ("S", "S", "S"),
        )

    # B1 [b N b] -> [b N b] B2'
    estagio2[(
        estado_b1,
        (branco, historico_final, branco),
    )] = (
        estado_b2_linha,
        (branco, historico_final, branco),
        ("S", "S", "S"),
    )

    # B2' [///] -> [- 0 -] B2
    estagio2[(
        estado_b2_linha,
        (NAO_LIDO, NAO_LIDO, NAO_LIDO),
    )] = (
        estado_b2,
        (NAO_LIDO, NAO_LIDO, NAO_LIDO),
        ("L", "S", "L"),
    )

    # B2 [x N x] -> [x N x] B2'
    for simbolo in simbolos_nao_brancos:
        estagio2[(
            estado_b2,
            (simbolo, historico_final, simbolo),
        )] = (
            estado_b2_linha,
            (simbolo, historico_final, simbolo),
            ("S", "S", "S"),
        )

    # B2 [b,N,b] -> [b,N,b] P_dir
    # Terminou a copia no branco a esquerda da saida.
    estado_posiciona_direita = f"{prefixo_b}pos_dir"

    estagio2[(
        estado_b2,
        (branco, historico_final, branco),
    )] = (
        estado_posiciona_direita,
        (branco, historico_final, branco),
        ("R", "S", "S"),
    )

    # P_dir [x,N,b] -> [x,N,b] P_dir
    # Anda para a direita ate chegar ao branco onde a Fase 1 terminou.
    for simbolo in simbolos_nao_brancos:
        estagio2[(
            estado_posiciona_direita,
            (simbolo, historico_final, branco),
        )] = (
            estado_posiciona_direita,
            (simbolo, historico_final, branco),
            ("R", "S", "S"),
        )

    # P_dir [b,N,b] -> [b,N,b] C_f
    # Voltou a posicao original da cabeca da fita 1.
    estagio2[(
        estado_posiciona_direita,
        (branco, historico_final, branco),
    )] = (
        estado_c_final,
        (branco, historico_final, branco),
        ("R", "S", "S"),
    )

    return estagio2
