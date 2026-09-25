from parser import faz_o_parsing
from mt_ordinaria import MaquinaTuring
#perguntar dos simbolos
"""transicoes_mt = {
    ("q0", "0"): ("q0", "1", "R"),
    ("q0", "1"): ("q0", "0", "R"),
    ("q0", "_"): ("qf", "_", "S")
    }

mt_original = MaquinaTuring(
    transicoes=transicoes_mt,
    estado_inicial="q0",
    estado_final="qf",
    branco="_"
)"""

#mt_original.executar("0110")

#estavmos discorrendo sobre futuras implementacoes
# ("q0", "0","8", "2")

# ou
# simbol = ("0","8","2")
# ("q0",simbol)

# movimentos = ("R","L","S")


estrutura = faz_o_parsing("entradaquintupla.txt")

mt_original = MaquinaTuring(
    quintuplas=estrutura.quintuplas,
    estado_inicial=estrutura.estado_inicial,
    estado_final=estrutura.estado_aceitacao,
    branco="B",
)

mt_original.executar(estrutura.entrada)