class Fita:
    
    def __init__(self, entrada="", branco="_"):
        self.celulas = {i: char for i, char in enumerate(entrada)}
        self.posicao = 0
        self.branco = branco

    def ler(self):
        return self.celulas.get(self.posicao, self.branco)

    def escrever(self, simbolo):
        self.celulas[self.posicao] = simbolo

    def mover(self, direcao):
        if direcao in ["L", "-"]:
            self.posicao -= 1
        elif direcao in ["R", "+"]:
            self.posicao += 1
        elif direcao in ["S", "0"]:
            pass

    def __str__(self):
        if not self.celulas:
            return f"[{self.branco}]"
        
        min_pos = min(self.celulas.keys())
        max_pos = max(self.celulas.keys())
        
        saida = []
        for i in range(min_pos, max_pos + 1):
            simbolo = self.celulas.get(i, self.branco)
            if i == self.posicao:
                saida.append(f"[{simbolo}]")
            else:
                saida.append(f" {simbolo} ")
        return "".join(saida)