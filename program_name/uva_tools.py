import numpy as np
import math as m
"""

VARIÁVEIS --------------------------------------------------------------------------------------------------------------

"""

# Matriz de Equilibrio
ang = []
l_e = []
# Matriz de rigidez
inrc = []
area = []
mdes = []
p_el = []
nelm = None

"""

USER INPUT's -----------------------------------------------------------------------------------------------------------

"""

vrfy = False
while vrfy != 'ok':
    # Informações gerais da estrutura

    nodes = int(input('Informe o número de nós: '))
    nelm = int(input('Informe o número de elementos: '))

    print('\n-------------------------------------------------------------------\n')

    ngdl = nodes * 3

    print(f'\nDados do sistema: \n'
          f'\nNúmero de nós: {nodes}'
          f'\nNúmero de elementos: {nelm}'
          f'\nGraus de liberdade da estrutura: {ngdl}\n')
    print('\n-------------------------------------------------------------------\n')

    vrfy = str(input("""Digite "ok" para confirmar as informações: \n"""))

print("\n" * 15)

# Para montar a matriz de equilibrio

vrfy = False
while vrfy != 'ok':

    ang.clear()
    l_e.clear()

    for i in range(nelm):
        ang_e = float(input(
            f'[ELEMENTO {i+1}] (α{i+1}) Qual o ângulo em graus do elemento {i + 1} em relação ao eixo x? \n'))
        l_eit = float(input(f'[ELEMENTO {i+1}] (L{i+1}) Qual o comprimento do vão do elemento {i + 1} em metros? \n'))
        print("\n" * 2)
        ang.append(ang_e)
        l_e.append(l_eit)

    for i in range(nelm):
        print(f'\nELEMENTO {i+1}: '
              f'\nComprimento do elemento: (L{i+1}) = {l_e[i]:.2f}m'
              f'\nÂngulo em relação ao eixo x: (α{i+1}) = {ang[i]:.2f}°')
    print('\n-------------------------------------------------------------------\n')
    vrfy = str(input("""\nDigite "ok" para confirmar as informações: \n"""))

print("\n" * 15)
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

"""

CALCULATIONS -----------------------------------------------------------------------------------------------------------

"""