
def gerar_regras_copia(alfabeto, estado_inicio_copia, estado_fim_copia, branco="_"):
    
    """Gera as quádruplas para o Estágio 2: Copiar o resultado da Fita 1 para a Fita 3.
    A Fita 2 permanece intocada durante este processo."""
    
    regras = {}

    for simbolo in alfabeto:
        if simbolo != branco:
            chave = (estado_inicio_copia, (simbolo, branco, branco))
            # Retorna como tuplo (proximo_estado, simbolos, movimentos) para o simulador
            regras[chave] = (
                estado_inicio_copia, 
                (simbolo, branco, simbolo), 
                ("R", "S", "R")
            )
            
    chave_fim = (estado_inicio_copia, (branco, branco, branco))
    regras[chave_fim] = (
        estado_fim_copia, 
        (branco, branco, branco), 
        ("S", "S", "S")
    )

    return regras