import sys
from parser import faz_o_parsing
from mt_ordinaria import MaquinaTuring
from utils import transformar_quintuplas
from inversas import gerar_estagio3
from simulador import Simulador
from fita import Fita
from estagio_copia import gerar_regras_copia
from fase2 import gerar_estagio2

BRANCO = "_"

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

# FASE 1: transforma as quíntuplas da MT original em quádruplas
quadruplas_estagio1 = transformar_quintuplas(mt_original.transicoes)

# FASE 2: Gera regras de cópia baseadas em transições de estados
# quadruplas_estagio2 = gerar_regras_copia(
#     alfabeto=["0", "1", "_", "$", "X"], 
#     estado_inicio_copia=estrutura.estado_aceitacao,
#     estado_fim_copia=f"C_{estrutura.estado_aceitacao}",
#     branco=BRANCO
# )

quadruplas_estagio2 = gerar_estagio2(estrutura.estado_aceitacao,estrutura.num_transicoes,estrutura.alfabeto_fita,
                                    BRANCO)

# FASE 3: gera as inversas das quádruplas da Fase 1 
quadruplas_estagio3 = gerar_estagio3(quadruplas_estagio1)

print("=== FASE 3: RETRACE ===") 
print(f"Quádruplas inversas geradas: {len(quadruplas_estagio3)}") 
print()

# Junta as regras das três fases no dicionário de transições
quadruplas = {}
quadruplas.update(quadruplas_estagio1)
quadruplas.update(quadruplas_estagio2)
quadruplas.update(quadruplas_estagio3)
print(quadruplas)

# Três fitas: 
# fita 1 = trabalho 
# fita 2 = histórico 
# fita 3 = saída
fitas = [
    Fita(estrutura.entrada, branco=BRANCO), 
    Fita("", branco=BRANCO),
    Fita("", branco=BRANCO),
]

simulador = Simulador(branco=BRANCO)

# FASE 1: COMPUTE 
print("Executando TUDO...")
estado, passos = simulador.executar(
    quadruplas,
    estado_inicial=estrutura.estado_inicial,
    estado_final=f"C_{estrutura.estado_inicial}",
    fitas=fitas, 
) 

print(f"Passos: {passos}") 
print(f"Fita 1: {fitas[0]}") 
print(f"Fita 2: {fitas[1]}") 
print(f"Fita 3: {fitas[2]}")


# FASE 1: COMPUTE 
print("Executando fase 1...")
estado, passos = simulador.executar(
    quadruplas_estagio1,
    estado_inicial=estrutura.estado_inicial,
    estado_final=estrutura.estado_aceitacao,
    fitas=fitas,) 


# FASE 2: COPY OUTPUT
print("=== FASE 2: COPY OUTPUT ===")
estado, passos = simulador.executar(
    quadruplas_estagio2,
    estado_inicial=estrutura.estado_aceitacao,
    estado_final=f"C_{estrutura.estado_aceitacao}",
    fitas=fitas,
)

# FASE 3: RETRACE 
print("=== FASE 3: RETRACE ===")
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