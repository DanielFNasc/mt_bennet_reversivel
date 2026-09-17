from dataclasses import dataclass

#Para o campo de valor, para a chave usar simbolos e estado
@dataclass
class Quadrupla:
    proximo_estado: str
    simbolos: tuple
    movimentos: tuple