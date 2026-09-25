#parser
from Quintupla import Quintupla, EstruturaMT

"""A primeira linha apresenta números, que indicam: número de estados, número de símbolos no 
alfabeto de entrada, número de símbolos no alfabeto da fita e número de transições, respectivamente. A seguir, temos os estados,
na próxima linha alfabeto de entrada e logo alfabeto da fita. Nas linhas sequentes temos a funcão de transição (como explicada 
no artigo). Depois da funcão de transição, segue uma entrada. Lembrando que o estado de aceitação é o último, no caso do exemplo, 
o 6."""


"""LEMBRETE: o seu programa deve ler de um arquivo como ele lê da entrada padrão. Por exemplo, a chamada deve funcionar para:

./simulador < entrada-quintupla.txt"""


def faz_o_parsing(nome_arquivo):
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        # remover os \n com strip
        linhas = [linha.strip() for linha in arquivo.readlines() if linha.strip() != ""]
        #separar a primeira linha e colocar numa lista com split 
        
        cabecalho = linhas[0].split()
        num_estados = int(cabecalho[0])
        num_simbolos_entrada = int(cabecalho[1])
        num_simbolos_fita = int(cabecalho[2])
        num_transicoes = int(cabecalho[3])
        
        # linha 2, 3, 4 
        estados = linhas[1].split()
        alfabeto_entrada = linhas[2].split()
        alfabeto_fita = linhas[3].split()

        #tranformar funções de transição em quintuplas
        quintuplas = []
        inicio_transicoes = 4
        for i in range(num_transicoes):
            linha = linhas[inicio_transicoes + i]

            # "(1,0)=(2,$,R)" -> lado_esq="(1,0)"  lado_dir="(2,$,R)"
            lado_esq, lado_dir = linha.split("=")

            estado_atual, simbolo_lido = lado_esq.strip("()").split(",")
            proximo_estado, simbolo_escrito, movimento = lado_dir.strip("()").split(",")

            quintuplas.append(
                Quintupla(
                    estado_atual=estado_atual,
                    simbolo_lido=simbolo_lido,
                    simbolo_escrito=simbolo_escrito,
                    movimento=movimento,
                    proximo_estado=proximo_estado,
                )
            )

        # última linha: entrada da máquina
        entrada = linhas[inicio_transicoes + num_transicoes]

        return EstruturaMT(
            num_estados=num_estados,
            num_simbolos_entrada=num_simbolos_entrada,
            num_simbolos_fita=num_simbolos_fita,
            num_transicoes=num_transicoes,
            estados=estados,
            alfabeto_entrada=alfabeto_entrada,
            alfabeto_fita=alfabeto_fita,
            quintuplas=quintuplas,
            entrada=entrada,
        )
    #pass