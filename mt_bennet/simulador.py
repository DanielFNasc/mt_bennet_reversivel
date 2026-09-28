from fita import Fita

NAO_LIDO = "/"


class Simulador:
    def __init__(self, quadruplas, branco="_"):
        self.quadruplas = quadruplas
        self.branco = branco

        # indexa as quadruplas por estado, pois o "/" na leitura e um
        # coringa ("fita nao lida") que combina com qualquer simbolo -
        # nao da pra usar (estado, leitura_exata) como chave de busca.
        self._por_estado = {}
        for (estado, leitura), valor in quadruplas.items():
            self._por_estado.setdefault(estado, []).append((leitura, valor))

    def _combina(self, padrao, leitura_real):
        return all(p == NAO_LIDO or p == r for p, r in zip(padrao, leitura_real))

    def passo(self, estado, fitas):
        """Executa um unico passo a partir do estado atual. Retorna o
        novo estado, ou None se nao houver transicao definida (parada)."""
        leitura_atual = tuple(f.ler() for f in fitas)

        candidatas = self._por_estado.get(estado, [])
        encontrados = [v for (padrao, v) in candidatas if self._combina(padrao, leitura_atual)]

        if not encontrados:
            return None
        if len(encontrados) > 1:
            raise RuntimeError(
                f"Determinismo violado: mais de uma quadrupla combina com "
                f"estado='{estado}', leitura={leitura_atual}"
            )

        proximo_estado, escrita, movimento = encontrados[0]

        for k, fita_k in enumerate(fitas):
            if escrita[k] != NAO_LIDO:
                fita_k.escrever(escrita[k])
            if movimento[k] != "S":
                fita_k.mover(movimento[k])

        return proximo_estado

    def executar(self, estado_inicial, estado_final, fitas, max_passos=100000, verboso=False):
        #Executa ate atingir estado_final (ou estourar max_passos)
        estado = estado_inicial
        passos = 0

        while estado != estado_final:
            if verboso:
                print(f"  estado={estado:<12} " + " | ".join(str(f) for f in fitas))

            novo_estado = self.passo(estado, fitas)
            if novo_estado is None:
                raise RuntimeError(
                    f"Nenhuma transicao definida para o estado '{estado}' "
                    f"com leitura {tuple(f.ler() for f in fitas)}"
                )
            estado = novo_estado
            passos += 1

            if passos > max_passos:
                raise RuntimeError("Numero maximo de passos excedido (possivel loop infinito)")

        if verboso:
            print(f"  estado={estado:<12} " + " | ".join(str(f) for f in fitas))

        return estado, passos


def copiar_fita(fita_origem, fita_destino):
    
    #Fase 2 (Copy output) simplificada: copia o conteudo nao-branco da fita de trabalho para a fita de saida, celula a celula.
    # ISSO AINDA TEM QUE SER FEITO
    #     
    if not fita_origem.celulas:
        return

    posicoes_com_dado = [
        p for p, s in fita_origem.celulas.items() if s != fita_origem.branco
    ]
    if not posicoes_com_dado:
        return

    inicio = min(posicoes_com_dado)
    fim = max(posicoes_com_dado)

    deslocamento = 1 - inicio  # a primeira posicao com dado vira a posicao 1
    for posicao in range(inicio, fim + 1):
        simbolo = fita_origem.celulas.get(posicao, fita_origem.branco)
        if simbolo != fita_origem.branco:
            fita_destino.celulas[posicao + deslocamento] = simbolo