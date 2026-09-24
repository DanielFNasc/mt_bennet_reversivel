#parser

"""A primeira linha apresenta números, que indicam: número de estados, número de símbolos no 
alfabeto de entrada, número de símbolos no alfabeto da fita e número de transições, respectivamente. A seguir, temos os estados,
na próxima linha alfabeto de entrada e logo alfabeto da fita. Nas linhas sequentes temos a funcão de transição (como explicada 
no artigo). Depois da funcão de transição, segue uma entrada. Lembrando que o estado de aceitação é o último, no caso do exemplo, 
o 6."""


"""LEMBRETE: o seu programa deve ler de um arquivo como ele lê da entrada padrão. Por exemplo, a chamada deve funcionar para:

./simulador < entrada-quintupla.txt"""


def faz_o_parsing(nome_arquivo):
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
        print(conteudo)
        print("##########################")
        linhas = arquivo.readlines()
        for linha in linhas:
            print(linha)
        
    pass