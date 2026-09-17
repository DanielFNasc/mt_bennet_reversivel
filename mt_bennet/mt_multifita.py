from fita import Fita
class MaquinaTuringMultifita:

    def __init__(self, numero_fitas, branco="_"):
        self.fitas = [
            Fita(branco)
            for _ in range(numero_fitas)
        ]

        self.estado = None