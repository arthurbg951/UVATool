import math as m
import numpy as np

'''
Resolvendo o Exemplo do material pelo método da Rigidez Analítica com Python


Passo 1: Criando as matrizes e vetores
'''

# ----------------------------------------------------------------------------------------------------------------------------

# Matriz de equilibrio - [ L ]

af12 = 0 * (m.pi/180.)
af23 = 0 * (m.pi/180.)
l12, l23 = 5., 5.

c1 = np.cos(af12)
c2 = np.cos(af23)

s1 = np.sin(af12)
s2 = np.sin(af23)

lo_eq = np.array([
    [-c1,  s1/l12,  -s1/l12,    0,        0,       0],
    [-s1, -c1/l12,   c1/l12,    0,        0,       0],
    [0,         1,        0,    0,        0,       0],
    [c1,  -s1/l12,   s1/l12,  -c2,   s2/l23, -s2/l23],
    [s1,   c1/l12,  -c1/l12,  -s2,  -c2/l23,  c2/l23],
    [0,         0,       -1,    0,        1,       0],
    [0,         0,        0,   c2,  -s2/l23,  s2/l23],
    [0,         0,        0,   s2,   c2/l23, -c2/l23],
    [0,         0,        0,    0,        0,      -1]
])

print(lo_eq)
A
# Colocando as restrições de apoio em [ L ]
leq = np.delete(lo_eq, [0, 1, 6, 7], 0)
# print(leq.shape)
# print(leq)

# Matriz de equilibrio Transposta - [ L.T ]
leqt = lo_eq.transpose()
# Colocando as restrições de apoio em [ L.T ]
leqt = np.delete(leqt, [0, 1, 6, 7], 1)
# print(leqt.shape)
# print(leqt)

"""
 0 -> linha 
 1 -> coluna
"""

# Matriz de rigidez do elemento - [ k ]

p11, p12, p22, p23 = 0.1e-27, 1., 1., 0.1e-27
e12, e23 = 1, 1
in12, in23 = 1, 1
aa12, aa23 = 1, 1

ft1_1 = (3 * p11 / (4 - p11 * p12)) * (4 * e12 * in12 / l12)
ft2_1 = (3 * p11 * p12 / (4 - p11 * p12)) * (-2 * e12 * in12 / l12)
ft3_1 = (3 * p12 / (4 - p11 * p12)) * (4 * e12 * in12 / l12)
ft4_1 = e12 * aa12 / l12

ft1_2 = (3 * p22 / (4 - p22 * p23)) * (4 * e23 * in23 / l23)
ft2_2 = (3 * p22 * p22 / (4 - p22 * p23)) * (-2 * e23 * in23 / l23)
ft3_2 = (3 * p23 / (4 - p22 * p23)) * (4 * e23 * in23 / l23)
ft4_2 = e23 * aa23 / l23


k_el = np.array([
    [ft4_1,     0,     0,     0,     0,     0],
    [    0, ft1_1, ft2_1,     0,     0,     0],
    [    0, ft2_1, ft3_1,     0,     0,     0],
    [    0,     0,     0, ft4_2,     0,     0],
    [    0,     0,     0,     0, ft1_2, ft2_2],
    [    0,     0,     0,     0, ft2_2, ft3_2]
])

# print(k_el.shape)
print(f'MATRIZ DE RIGIDEZ DO ELEMENTO - k :  \n\n{k_el}\n')


# ----------------------------------------------------------------------------------------------------------------------------

'''
Passo 2: Através da triangularização de Gauss Jordan, encontrar os valores dos Deslocamentos Nodais δ:

        {λ} = [L k LT] * {δ}


Matriz de Rigidez Global - k_global

        ([L * k * L.T])
'''
k_global = leq @ k_el @ leqt
# Também pode ser escrito -> k_global = leq.dot(k_el).dot(leqt)
print(f'MATRIZ DE RIGIDEZ GLOBAL - L k LT: \n\n{k_global}\n')
# print(k_global.shape)


# Vetor das Cargas Nodais (Cargas Pontuais e Cargas de Momento) - { λ }
f1x, f2y, f3m, f4x, f5y, f6m, f7x, f8y, f9m = None, None, 0, 0, -10000, 0, None, None, 0
force = np.array([f1x, f2y, f3m, f4x, f5y, f6m, f7x, f8y, f9m])
fn = np.transpose(force)  # Transformando em vetor

# Colocando as restrições de apoio em { λ }
fn = np.delete(fn, [0, 1, 6, 7], 0)
print(f'Vetor das Cargas Nodais - λ: \n\n{fn}\n')


# ----------------------------------------------------------------------------------------------------------------------------



# Vetor dos Deslocamentos Nodais (Deslocamentos Lineares e Rotacionais) - { δ }
dt1x, dt2y, dr3m, dt4x, dt5y, dr6m, dt7x, dt8y, dr9m = None, None, 41666.666667, 0, -104166.666667,-20833.333333, None, None, 62500.000000
dt = np.array([dt1x, dt2y, dr3m, dt4x, dt5y, dr6m, dt7x, dt8y, dr9m])
dlt = np.transpose(dt)  # Transformando em vetor
# Colocando as restrições de apoio em ( δ )
dlt = np.delete(dlt, [0, 1, 6, 7], 0)
print(f'Vetor dos Deslocamentos Nodais - δ :  \n\n{dlt}\n')

# ----------------------------------------------------------------------------------------------------------------------------

'''
Passo 3: Encontrar os valores das Deformações Correspondentes:

        {θ} = [L.T] * {δ}
'''

tta = leqt @ dlt
print(f'Vetor das Deformações Correspondentes - θ: \n\n{tta}\n')

# ----------------------------------------------------------------------------------------------------------------------------

'''
Passo 4: Encontrar os valores dos Esforços Seccionais Internos:

        {m} = [k] * {θ}
'''

esf_in = k_el @ tta
print(f'Vetor dos esforçso internos - m: \n\n{esf_in}\n')






