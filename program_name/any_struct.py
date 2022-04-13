# PASSO 1:
"""
-----------------------------------------------------------------------
# RECEBER DADOS DO USUARIO:

 - n de nós
 - n de elementos
 - ang dos elementos
 - l dos elementos
 - A, E e I dos elementos
 - P dos elementos 

# RECEBER DADOS DOS TIPOS DE APOIOS E EM QUAIS PONTOS:

 - Tipos de apoio:
   1 - 1º genero
   2 - 2º gênero
   3 - 3º gênero
   4 - 3º gênero + semirigidez
   5 - Rótula == 2º gênero

 - Armazenar os dados que irão ser descartados - cortados
-----------------------------------------------------------------------
"""
# PASSO 2:
"""
-----------------------------------------------------------------------
# MONTAR AS MATRIZES E VETOR

 - [L] : Matriz de equilibrio
 - [k] : Matriz de rigidez local dos elementos
 - {λ} : Vetor das cargas nodais

# APLICAR AS CONDIÇÕES DE CONTORNO

 - Cortes das linhas referentes aos tipos e ponot dos apoios
-----------------------------------------------------------------------
"""
# PASSO 3:
"""
-----------------------------------------------------------------------
# CÁLCULOS

 - Matriz de Rigidez Global - k_global
     ([L * k * L.T]) 

 - Vetor dos deslocamentos nodais
     {δ} = (L . k . L.T]^-1 . {λ}

 - Vetor das deformações correspondentes:
     {θ} = [L.T] . {δ}

 - Vetor dos esforços internos:
     {m} = [k] * {θ}
      - Remover os elementos adicionais em caso de semirigidez
 
 - Retornar os resultados ao usuário, de acordo com sua seleção
     - Opções
     1 - Deformações nodais
     2 - Rotações
     3 - Esforços internos

-----------------------------------------------------------------------
"""