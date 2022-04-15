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
ngdl = None
nodes = None
"""

USER INPUT's -----------------------------------------------------------------------------------------------------------

"""

# CARACTERISTICAS DO PORTICO PLANO

vrfy = False
while vrfy != 'ok':

    # Informações gerais da estrutura

    nodes = int(input('Informe o número de nós: '))
    nelm = int(input('Informe o número de elementos: '))

    print('\n-------------------------------------------------------------------\n')

    ngdl = int(nodes * 3)

    print(f'\nDados do sistema: \n'
          f'\nNúmero de nós: {nodes}'
          f'\nNúmero de elementos: {nelm}'
          f'\nGraus de liberdade da estrutura: {ngdl}\n')
    print('\n-------------------------------------------------------------------\n')

    vrfy = str(input("""Digite "ok" para confirmar as informações: \n"""))

print("\n" * 5)

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

print("\n" * 5)


# INSERÇÃO DOS APOIOS


# PROPRIEDADES DOS MATERIAIS E SEÇÃO TRANSVERSAL

# Para montar a matriz de rigidez

"""
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

# Matriz de equilibrio - [ L ]  ----------- FUNCIONAL GRAÇAS A DEUS PAI RECEBA!!! -------------
lo_eq = None
if nelm < nodes:
    lo_eq = np.zeros((ngdl, ngdl-3))
if nelm == nodes:
    lo_eq = np.zeros((ngdl, ngdl))

for i in range(nelm):
    lo_eq[0 + (3 * i), 0 + (3 * i)] = -np.cos(ang[i] * (m.pi / 180.))
    lo_eq[0 + (3 * i), 1 + (3 * i)] = np.sin(ang[i] * (m.pi / 180.)) / l_e[i]
    lo_eq[0 + (3 * i), 2 + (3 * i)] = -np.sin(ang[i] * (m.pi / 180.)) / l_e[i]
    lo_eq[1 + (3 * i), 0 + (3 * i)] = -np.sin(ang[i] * (m.pi / 180.))
    lo_eq[1 + (3 * i), 1 + (3 * i)] = -np.cos(ang[i] * (m.pi / 180.)) / l_e[i]
    lo_eq[1 + (3 * i), 2 + (3 * i)] = np.cos(ang[i] * (m.pi / 180.)) / l_e[i]
    lo_eq[2 + (3 * i), 1 + (3 * i)] = 1
    lo_eq[3 + (3 * i), 0 + (3 * i)] = np.cos(ang[i] * (m.pi / 180.))
    lo_eq[3 + (3 * i), 1 + (3 * i)] = -np.sin(ang[i] * (m.pi / 180.)) / l_e[i]
    lo_eq[3 + (3 * i), 2 + (3 * i)] = np.sin(ang[i] * (m.pi / 180.)) / l_e[i]
    lo_eq[4 + (3 * i), 0 + (3 * i)] = np.sin(ang[i] * (m.pi / 180.))
    lo_eq[4 + (3 * i), 1 + (3 * i)] = np.cos(ang[i] * (m.pi / 180.)) / l_e[i]
    lo_eq[4 + (3 * i), 2 + (3 * i)] = -np.cos(ang[i] * (m.pi / 180.)) / l_e[i]
    lo_eq[5 + (3 * i), 2 + (3 * i)] = -1

print(lo_eq)

# Matriz de equilibrio transposta - [L.T]
leqt = lo_eq.copy()
leqt = leqt.transpose()

# Inserindo as restrições de apoio
leq = lo_eq.copy()


"""

RETURN -----------------------------------------------------------------------------------------------------------------

"""