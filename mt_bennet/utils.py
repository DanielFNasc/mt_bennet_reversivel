
#Mudar as quintuplas p quadruplas
#Essa implementacao nao usad cidciionarip 
def transformar_quintuple(dicionario_q):

    primeira = Quadruple(
        estado_atual=q.estado_atual,
        leitura=(q.simbolo_lido,),
        acao=(q.simbolo_escrito,),
        proximo_estado=estado_intermediario
    )

    segunda = Quadruple(
        estado_atual=estado_intermediario,
        leitura=("/",),
        acao=(q.movimento,),
        proximo_estado=q.proximo_estado
    )

    return primeira, segunda