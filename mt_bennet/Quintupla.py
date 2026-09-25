from dataclasses import dataclass, field


@dataclass
class Quintupla:
    """representa AT -> T' sigma A' """
    estado_atual: str
    simbolo_lido: str
    simbolo_escrito: str
    movimento: str        # L, R ou 0 (parado)
    proximo_estado: str
    

@dataclass
class EstruturaMT:
    """estrutura da MT ordinária extraída do arquivo de entrada."""
    num_estados: int
    num_simbolos_entrada: int
    num_simbolos_fita: int
    num_transicoes: int
    estados: list
    alfabeto_entrada: list
    alfabeto_fita: list
    quintuplas: list          #lista de quintuplas
    entrada: str
    estado_inicial: str = field(init=False)
    estado_aceitacao: str = field(init=False)

    def __post_init__(self):
        self.estado_inicial = self.estados[0]
        self.estado_aceitacao = self.estados[-1]