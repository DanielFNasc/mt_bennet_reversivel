from fita import Fita

class MaquinaTuring:
    
    def __init__(self, transicoes, estado_inicial, estado_final, branco="_"):
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
        self.branco = branco

    def executar(self, string_entrada):
        fita = Fita(string_entrada, self.branco)
        estado_atual = self.estado_inicial

        print(f"| Estado: {estado_atual} | Fita: {fita}")


        while estado_atual != self.estado_final:
            simbolo_lido = fita.ler()
            chave_busca = (estado_atual, simbolo_lido)

            prox_estado, simbolo_escrito, movimento = self.transicoes[chave_busca]

            fita.escrever(simbolo_escrito)
            fita.mover(movimento)
            estado_atual = prox_estado

            print(f"PASSO  | Estado: {estado_atual} | Fita: {fita}")

        if estado_atual == self.estado_final:
            print("\nmaquina parou no estado final.")
        
        return fita