#Simulador da maquina reversivel de Bennett com tres fitas.
#manter as tres fitas
#executar quadruplas
#executar os tres estagios de Bennett quando recebe as transicoes

from fita import Fita

NAO_LIDO = "/"


class Simulador:
    #Executa uma maquina de Turing reversivel de 3 fitas

    def __init__(self, branco="_", max_passos=100000):
        self.branco = branco
        self.max_passos = max_passos

    @staticmethod
    def criar_fitas(entrada, branco="_"):
        #Cria as fitas iniciais: trabalho, historico e saida
        return [
            Fita(entrada, branco),
            Fita("", branco),
            Fita("", branco),
        ]

    @staticmethod
    def _indexar(quadruplas):
        #Indexa transicoes por estado, pois '/' funciona como coringa
        por_estado = {}
        for (estado, leitura), valor in quadruplas.items():
            por_estado.setdefault(estado, []).append((leitura, valor))
        return por_estado

    @staticmethod
    def _combina(padrao, leitura_real):
        return all(
            esperado == NAO_LIDO or esperado == real
            for esperado, real in zip(padrao, leitura_real)
        )

    def passo(self, estado, fitas, quadruplas):
        #Executa uma quadrupla a partir do estado informado
        if len(fitas) != 3:
            raise ValueError("A maquina reversivel de Bennett usa exatamente 3 fitas.")

        por_estado = self._indexar(quadruplas)
        leitura_real = tuple(fita.ler() for fita in fitas)

        encontrados = [
            valor
            for padrao, valor in por_estado.get(estado, [])
            if self._combina(padrao, leitura_real)
        ]

        if not encontrados:
            return None

        if len(encontrados) > 1:
            raise RuntimeError(
                "Determinismo violado: mais de uma quadrupla combina com "
                f"estado={estado!r}, leitura={leitura_real!r}"
            )

        proximo_estado, escrita, movimentos = encontrados[0]

        for fita, simbolo, movimento in zip(fitas, escrita, movimentos):
            if simbolo != NAO_LIDO:
                fita.escrever(simbolo)
            if movimento != "S":
                fita.mover(movimento)

        return proximo_estado

    def executar(
        self,
        quadruplas,
        estado_inicial,
        estado_final,
        fitas,
        verboso=False,
    ):
        #Executa transicoes ate chegar ao estado_final
        estado = estado_inicial
        passos = 0
        por_estado = self._indexar(quadruplas)

        while estado != estado_final:
            leitura_real = tuple(fita.ler() for fita in fitas)

            encontrados = [
                valor
                for padrao, valor in por_estado.get(estado, [])
                if self._combina(padrao, leitura_real)
            ]

            if not encontrados:
                raise RuntimeError(
                    f"Nenhuma transicao definida para o estado {estado!r} "
                    f"com leitura {leitura_real!r}."
                )

            if len(encontrados) > 1:
                raise RuntimeError(
                    "Determinismo violado: mais de uma quadrupla combina com "
                    f"estado={estado!r}, leitura={leitura_real!r}"
                )

            proximo_estado, escrita, movimentos = encontrados[0]

            if verboso:
                self.mostrar_configuracao(estado, fitas, passos)

            for fita, simbolo, movimento in zip(fitas, escrita, movimentos):
                if simbolo != NAO_LIDO:
                    fita.escrever(simbolo)
                if movimento != "S":
                    fita.mover(movimento)

            estado = proximo_estado
            passos += 1

            if passos > self.max_passos:
                raise RuntimeError(
                    "Numero maximo de passos excedido (possivel loop infinito)."
                )

        if verboso:
            self.mostrar_configuracao(estado, fitas, passos)

        return estado, passos

    def executar_estagio1(
        self,
        quadruplas_estagio1,
        estado_inicial,
        estado_aceitacao,
        fitas,
        verboso=False,
    ):
        #Executa o Compute (Fase 1)
        return self.executar(
            quadruplas_estagio1,
            estado_inicial,
            estado_aceitacao,
            fitas,
            verboso,
        )

    def executar_estagio2(
        self,
        quadruplas_estagio2,
        estado_aceitacao,
        fitas,
        verboso=False,
    ):
        #Executa o Copy Output (Fase 2)
        estado_inicial = estado_aceitacao
        estado_final = f"C_{estado_aceitacao}"
        return self.executar(
            quadruplas_estagio2,
            estado_inicial,
            estado_final,
            fitas,
            verboso,
        )

    def executar_estagio3(
        self,
        quadruplas_estagio3,
        estado_inicial,
        estado_aceitacao,
        fitas,
        verboso=False,
    ):
        #Executa o Retrace (Fase 3)
        estado_inicial_retrace = f"C_{estado_aceitacao}"
        estado_final_retrace = f"C_{estado_inicial}"
        return self.executar(
            quadruplas_estagio3,
            estado_inicial_retrace,
            estado_final_retrace,
            fitas,
            verboso,
        )

    def executar_bennett(
        self,
        quadruplas_estagio1,
        quadruplas_estagio2,
        quadruplas_estagio3,
        entrada,
        estado_inicial,
        estado_aceitacao,
        verboso=False,
    ):
        """Executa Compute -> Copy Output -> Retrace."""
        fitas = self.criar_fitas(entrada, self.branco)

        resultado_1 = self.executar_estagio1(
            quadruplas_estagio1,
            estado_inicial,
            estado_aceitacao,
            fitas,
            verboso,
        )

        resultado_2 = self.executar_estagio2(
            quadruplas_estagio2,
            estado_aceitacao,
            fitas,
            verboso,
        )

        resultado_3 = self.executar_estagio3(
            quadruplas_estagio3,
            estado_inicial,
            estado_aceitacao,
            fitas,
            verboso,
        )

        return {
            "fitas": fitas,
            "estagio1": resultado_1,
            "estagio2": resultado_2,
            "estagio3": resultado_3,
        }

    @staticmethod
    def mostrar_configuracao(estado, fitas, passo):
        fitas_texto = " | ".join(str(fita) for fita in fitas)
        print(f"passo={passo:<5} estado={estado:<18} {fitas_texto}")


# Compatibilidade caso algum outro arquivo ainda importe o nome antigo.
SimuladorQuadruplas = Simulador