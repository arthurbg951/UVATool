import numpy as np
import math as m

"""

VARIÁVEIS

"""

# Matriz de Equilibrio
ang = []
l_e = []
# Matriz de rigidez
inrc = []
area = []
mdes = []
p_el = []
# Verificações
vrfy = False
"""

USER INPUT

"""
while vrfy != 'ok':
    # Informações gerais da estrutura
    nodes = int(input('Informe o número de nós: '))
    n_elm = int(input('Informe o número de elementos: '))
    n_gdl = nodes * 3
    print(f'\nDados do sistema: '
          f'\nNúmero de nós: {nodes}'
          f'\nGraus de liberdade: {n_gdl}'
          f'\nNúmero de elementos: {n_elm}\n')
    vrfy = str(input("""Digite "ok" para confirmar as informações: \n"""))

# Para montar a matriz de equilibrio

for i in range(n_elm):
    ang_e = float(input(f'[ELEMENTO {i+1}] Qual o ângulo em graus do elemento {i + 1} em relação ao eixo x? \n'))
    l_eit = float(input(f'[ELEMENTO {i+1}] Qual o comprimento do vão do elemento {i + 1} em metros? \n'))
    ang.append(ang_e)
    l_e.append(l_eit)

"""
# Para montar a matriz de rigidez
for i in range(n_elm):
    sec = float(input(f'Qual o tipo de seção do elemento {i + 1} ? '))
    if sec == 'retangular':
        h_i = float(input('informe a altura (h) em metros : '))
        b_i = float(input('informe a base (b) em metros : '))
    mod_elast_e
    pm_e
    pj_e
"""
print(ang)
print(l_e)
"""

CALCULATIONS

"""