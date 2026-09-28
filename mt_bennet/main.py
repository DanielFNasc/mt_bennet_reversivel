import sys
from parser import faz_o_parsing
from mt_ordinaria import MaquinaTuring
from utils import transformar_quintuplas
from inversas import gerar_estagio3
from simulador import Simulador
from fase2 import gerar_estagio2
from fita import Fita

BRANCO = "_"

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

estrutura = faz_o_parsing(sys.argv[1])

# isso é pq não tava padronizado B e _
for quintupla in estrutura.quintuplas:
    if quintupla.simbolo_lido == "B":
        quintupla.simbolo_lido = BRANCO

    if quintupla.simbolo_escrito == "B":
        quintupla.simbolo_escrito = BRANCO

mt_original = MaquinaTuring(
    quintuplas=estrutura.quintuplas,
    estado_inicial=estrutura.estado_inicial,
    estado_final=estrutura.estado_aceitacao,
    branco="BRANCO",
)

print("Transições originais:")
print(mt_original.transicoes)
print()

#mt_original.executar(estrutura.entrada)

# FASE 1
quadruplas_estagio1 = transformar_quintuplas(mt_original.transicoes)

# FASE 2
quadruplas_estagio2 = gerar_estagio2(
    estado_aceitacao=estrutura.estado_aceitacao,
    numero_quintuplas=estrutura.num_transicoes,
    alfabeto_trabalho=estrutura.alfabeto_fita,
    branco=BRANCO,
)

# FASE 3
quadruplas_estagio3 = gerar_estagio3(quadruplas_estagio1)

print("=== FASE 3: RETRACE ===") 
print(f"Quádruplas inversas geradas: {len(quadruplas_estagio3)}") 
print()

# Junta as transições das duas fases
quadruplas = {}
quadruplas.update(quadruplas_estagio1)
quadruplas.update(quadruplas_estagio3)

# Três fitas: 
# # fita 1 = trabalho 
# # fita 2 = histórico 
# # fita 3 = saída
fitas = [
Fita(estrutura.entrada, branco=BRANCO), 
Fita("", branco=BRANCO),
Fita("", branco=BRANCO),
]

simulador = Simulador(branco=BRANCO)

# FASE 1: COMPUTE 
print("Executando Fase 1...")
estado, passos = simulador.executar(
    quadruplas_estagio1,
    estado_inicial=estrutura.estado_inicial,
    estado_final=estrutura.estado_aceitacao,
    fitas=fitas, 
) 

print(f"Estado final da Fase 1: {estado}") 
print(f"Passos: {passos}") 
print(f"Fita 1: {fitas[0]}") 
print(f"Fita 2: {fitas[1]}") 
print() 

# FASE 2: COPY OUTPUT
print("=== FASE 2: COPY OUTPUT ===")

estado, passos = simulador.executar(
    quadruplas_estagio2,
    estado_inicial=estrutura.estado_aceitacao,
    estado_final=f"C_{estrutura.estado_aceitacao}",
    fitas=fitas,
)

print(f"Estado final da Fase 2: {estado}")
print(f"Passos: {passos}")
print(f"Fita 1: {fitas[0]}")
print(f"Fita 2: {fitas[1]}")
print(f"Fita 3: {fitas[2]}")
print()

# FASE 3: RETRACE 
print("=== FASE 3: RETRACE / INVERSAS ===") 
estado_inicial_retrace = f"C_{estrutura.estado_aceitacao}" 
estado_final_retrace = f"C_{estrutura.estado_inicial}" 
estado, passos = simulador.executar( 
    quadruplas_estagio3,
    estado_inicial=estado_inicial_retrace, 
    estado_final=estado_final_retrace, 
    fitas=fitas, 
    ) 
print(f"Estado final da Fase 3: {estado}") 
print(f"Passos: {passos}") 
print(f"Fita 1: {fitas[0]}") 
print(f"Fita 2: {fitas[1]}") 
print(f"Fita 3: {fitas[2]}")