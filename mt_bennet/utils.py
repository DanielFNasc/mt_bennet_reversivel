from Quintupla import Quintupla
#Mudar as quintuplas p quadruplas
#Essa implementacao nao usad cidciionarip 

def transformar_quintuplas(dicionario_q):

    dicionario_quadrupla = {}

    numero_quintupla = 1

    for chave, valor in dicionario_q.items():

        estado_atual, simbolo_lido = chave
        quintupla = valor
        proximo_estado, simbolo_escrito, movimento = (quintupla.proximo_estado,quintupla.simbolo_escrito,quintupla.movimento)

        # Estado intermediário exclusivo desta quíntupla
        estado_intermediario = f"q_inter_{numero_quintupla}"

        # =========================================================
        # PRIMEIRA QUÁDRUPLA
        # =========================================================
        #
        # Fita 1:
        #   lê o símbolo da máquina original
        #   escreve o novo símbolo
        #
        # Fita 2:
        #   desloca a cabeça para a próxima célula de histórico
        #
        # Fita 3:
        #   permanece parada
        #

        leitura = (
            simbolo_lido,
            "/",
            "_"
        )

        escrita = (
            simbolo_escrito,
            "/",
            "_"
        )

        movimento_1 = (
            "S",
            "R",
            "S"
        )

        dicionario_quadrupla[
            (estado_atual, leitura)
        ] = (
            estado_intermediario,
            escrita,
            movimento_1
        )

        # =========================================================
        # SEGUNDA QUÁDRUPLA
        # =========================================================
        #
        # Fita 1:
        #   realiza o movimento da máquina original
        #
        # Fita 2:
        #   escreve o índice da quíntupla executada
        #
        # Fita 3:
        #   permanece parada
        #

        leitura = (
            "/",
            "_",
            "/"
        )

        escrita = (
            "/",
            str(numero_quintupla),
            "/"
        )

        movimento_2 = (
            movimento,
            "S",
            "S"
        )

        dicionario_quadrupla[
            (estado_intermediario, leitura)
        ] = (
            proximo_estado,
            escrita,
            movimento_2
        )

        numero_quintupla += 1

    print(dicionario_quadrupla)
    return dicionario_quadrupla