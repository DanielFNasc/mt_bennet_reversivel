from fita import Fita

class MaquinaTuringMultifita:
    def __init__(self, transicoes, estado_inicial, estado_final, branco="_"):
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
        self.branco = branco
        
        #cria as 3 fitas
        self.fita_trabalho = Fita("", branco)  
        self.fita_historico = Fita("", branco) 
        self.fita_saida = Fita("", branco)     

    def executar(self, entrada):
        #fita 1 recebe a entrada, as outras começam vazias
        self.fita_trabalho = Fita(entrada, self.branco)
        estado_atual = self.estado_inicial

        print(f"\nINÍCIO | Estado: {estado_atual}")
        print(f"F1 (Trabalho):  {self.fita_trabalho}")
        print(f"F2 (Histórico): {self.fita_historico}")
        print(f"F3 (Saída):     {self.fita_saida}\n")

        #loop principal
        while estado_atual != self.estado_final:
            #le o simbolo onde os 3 cabeçotes tao parados
            simbolos_lidos = (
                self.fita_trabalho.ler(), 
                self.fita_historico.ler(), 
                self.fita_saida.ler()
            )
            
            chave_busca = (estado_atual, simbolos_lidos)

            if chave_busca not in self.transicoes:
                print(f"PARADA: Nenhuma transição para {chave_busca}")
                break

            #pega a quadrupla correspondente
            quad = self.transicoes[chave_busca]

            #escreve novo simbolos nas fitas
            self.fita_trabalho.escrever(quad.simbolos[0])
            self.fita_historico.escrever(quad.simbolos[1])
            self.fita_saida.escrever(quad.simbolos[2])

            #move os cabeçotes
            self.fita_trabalho.mover(quad.movimentos[0])
            self.fita_historico.mover(quad.movimentos[1])
            self.fita_saida.mover(quad.movimentos[2])

            #atualiza o estado
            estado_atual = quad.proximo_estado

            print(f"PASSO | Estado: {estado_atual}")
            print(f"F1: {self.fita_trabalho} | F2: {self.fita_historico} | F3: {self.fita_saida}")

        if estado_atual == self.estado_final:
            print("\nSUCESSO: Máquina parou no estado final.")