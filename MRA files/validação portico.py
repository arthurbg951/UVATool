import math as m
import numpy as np

'''
VALIDAÇÃO DOS RESULTADOS PELO UVATOOL E FTOOL
'''

# ---------------------------------------------------------------------------------------------------------------------

'''
Passo 1: Criando as matrizes e vetores
'''

# Matriz de equilibrio - [ L ]

af12 = 90 * (m.pi/180.)  # rad
af23 = 0 * (m.pi/180.)  # rad
af34 = 0 * (m.pi/180.)  # rad
af45 = 0 * (m.pi/180.)  # rad
af56 = -90 * (m.pi/180.)  # rad
l12, l23, l34, l45, l56 = 3, 2, 2, 2, 3   # m

c1 = np.cos(af12)
c2 = np.cos(af23)
c3 = np.cos(af34)
c4 = np.cos(af45)
c5 = np.cos(af56)

s1 = np.sin(af12)
s2 = np.sin(af23)
s3 = np.sin(af34)
s4 = np.sin(af45)
s5 = np.sin(af56)

lo_eq = np.array([
    [-c1,  s1/l12,  -s1/l12,   0,       0,        0,   0,       0,        0,   0,       0,        0,   0,       0,       0],
    [-s1, -c1/l12,   c1/l12,   0,       0,        0,   0,       0,        0,   0,       0,        0,   0,       0,       0],
    [  0,       1,        0,   0,       0,        0,   0,       0,        0,   0,       0,        0,   0,       0,       0],
    [ c1, -s1/l12,   s1/l12, -c2,  s2/l23,  -s2/l23,   0,       0,        0,   0,       0,        0,   0,       0,       0],
    [ s1,  c1/l12,  -c1/l12, -s2, -c2/l23,   c2/l23,   0,       0,        0,   0,       0,        0,   0,       0,       0],
    [  0,       0,       -1,   0,       1,        0,   0,       0,        0,   0,       0,        0,   0,       0,       0],
    [  0,       0,        0,  c2, -s2/l23,   s2/l23, -c3,  s3/l34,  -s3/l34,   0,       0,        0,   0,       0,       0],
    [  0,       0,        0,  s2,  c2/l23,  -c2/l23, -s3, -c3/l34,   c3/l34,   0,       0,        0,   0,       0,       0],
    [  0,       0,        0,   0,       0,       -1,   0,       1,        0,   0,       0,        0,   0,       0,       0],
    [  0,       0,        0,   0,       0,        0,  c3, -s3/l34,   s3/l34, -c4,  s4/l45,  -s4/l45,   0,       0,       0],
    [  0,       0,        0,   0,       0,        0,  s3,  c3/l34,  -c3/l34, -s4, -c4/l45,   c4/l45,   0,       0,       0],
    [  0,       0,        0,   0,       0,        0,   0,       0,       -1,   0,       1,        0,   0,       0,       0],
    [  0,       0,        0,   0,       0,        0,   0,       0,        0,  c4, -s4/l45,   s4/l45, -c5,  s5/l56, -s5/l56],
    [  0,       0,        0,   0,       0,        0,   0,       0,        0,  s4,  c4/l45,  -c4/l45, -s5, -c5/l56,  c5/l56],
    [  0,       0,        0,   0,       0,        0,   0,       0,        0,   0,       0,       -1,   0,       1,       0],
    [  0,       0,        0,   0,       0,        0,   0,       0,        0,   0,       0,        0,  c5, -s5/l56,  s5/l56],
    [  0,       0,        0,   0,       0,        0,   0,       0,        0,   0,       0,        0,  s5,  c5/l56, -c5/l56],
    [  0,       0,        0,   0,       0,        0,   0,       0,        0,   0,       0,        0,   0,       0,      -1]
])

print(lo_eq)

# Colocando as restrições de apoio em [ L ]
leq = np.delete(lo_eq, [0, 1, 2, 15, 16, 17], 0)
# print(leq.shape)
# print(leq)


# Matriz de equilibrio Transposta - [ L.T ]
leqt = lo_eq.transpose()
# Colocando as restrições de apoio em [ L.T ]
leqt = np.delete(leqt, [0, 1, 2, 15, 16, 17], 1)
# print(leqt.shape)
# print(leqt)

"""
 0 -> linha 
 1 -> coluna
"""

# Matriz de rigidez do elemento - [ k ]

p11, p12, p21, p22, p31, p32, p41, p42, p51, p52 = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
e12, e23, e34, e45, e56 = 27e9, 27e9, 27e9, 27e9, 27e9  # Pa
in12, in23, in34, in45, in56 = 1333300000000e-12, 27000000000000e-12, 27000000000000e-12, 27000000000000e-12, 1333300000000e-12  # m4
aa12, aa23, aa34, aa45, aa56 = 400000000e-6, 900000000e-6, 900000000e-6, 900000000-6,  400000000e-6   # m²

ft1_1 = (3 * p11 / (4 - p11 * p12)) * (4 * e12 * in12 / l12)
ft2_1 = (3 * p11 * p12 / (4 - p11 * p12)) * (-2 * e12 * in12 / l12)
ft3_1 = (3 * p12 / (4 - p11 * p12)) * (4 * e12 * in12 / l12)
ft4_1 = e12 * aa12 / l12

ft1_2 = (3 * p21 / (4 - p21 * p22)) * (4 * e23 * in23 / l23)
ft2_2 = (3 * p21 * p22 / (4 - p21 * p22)) * (-2 * e23 * in23 / l23)
ft3_2 = (3 * p22 / (4 - p21 * p22)) * (4 * e23 * in23 / l23)
ft4_2 = e23 * aa23 / l23

ft1_3 = (3 * p31 / (4 - p31 * p32)) * (4 * e34 * in34 / l34)
ft2_3 = (3 * p31 * p32 / (4 - p31 * p32)) * (-2 * e34 * in34 / l34)
ft3_3 = (3 * p32 / (4 - p31 * p32)) * (4 * e34 * in34 / l34)
ft4_3 = e34 * aa34 / l34

ft1_4 = (3 * p41 / (4 - p41 * p42)) * (4 * e45 * in45 / l45)
ft2_4 = (3 * p41 * p42 / (4 - p41 * p42)) * (-2 * e45 * in45 / l45)
ft3_4 = (3 * p42 / (4 - p41 * p42)) * (4 * e45 * in45 / l45)
ft4_4 = e45 * aa45 / l45

ft1_5 = (3 * p51 / (4 - p51 * p52)) * (4 * e56 * in56 / l56)
ft2_5 = (3 * p51 * p52 / (4 - p51 * p52)) * (-2 * e56 * in56 / l56)
ft3_5 = (3 * p52 / (4 - p51 * p52)) * (4 * e56 * in56 / l56)
ft4_5 = e56 * aa56 / l56


k_el = np.array([
    [ft4_1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0],
    [    0, ft1_1, ft2_1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0],
    [    0, ft2_1, ft3_1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0],
    [    0,     0,     0, ft4_2,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0],
    [    0,     0,     0,     0, ft1_2, ft2_2,     0,     0,     0,     0,     0,     0,     0,     0,     0],
    [    0,     0,     0,     0, ft2_2, ft3_2,     0,     0,     0,     0,     0,     0,     0,     0,     0],
    [    0,     0,     0,     0,     0,     0, ft4_3,     0,     0,     0,     0,     0,     0,     0,     0],
    [    0,     0,     0,     0,     0,     0,     0, ft1_3, ft2_3,     0,     0,     0,     0,     0,     0],
    [    0,     0,     0,     0,     0,     0,     0, ft2_3, ft3_3,     0,     0,     0,     0,     0,     0],
    [    0,     0,     0,     0,     0,     0,     0,     0,     0, ft4_4,     0,     0,     0,     0,     0],
    [    0,     0,     0,     0,     0,     0,     0,     0,     0,     0, ft1_4, ft2_4,     0,     0,     0],
    [    0,     0,     0,     0,     0,     0,     0,     0,     0,     0, ft2_4, ft3_4,     0,     0,     0],
    [    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0, ft4_5,     0,     0],
    [    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0, ft1_5, ft2_5],
    [    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0, ft2_5, ft3_5]
])

print(k_el.shape)
print(f'MATRIZ DE RIGIDEZ DO ELEMENTO - k :  \n\n{k_el}\n')

# k_el = np.identity(12)

print(f'MATRIZ DE RIGIDEZ DO ELEMENTO - k :\n\n'
      f'{k_el}\n'  
)

# ---------------------------------------------------------------------------------------------------------------------

'''
Passo 2: Através da triangularização de Gauss Jordan, encontrar os valores dos Deslocamentos Nodais δ:

        {λ} = [L k LT] * {δ}


Matriz de Rigidez Global - k_global

        ([L * k * L.T])
'''
k_global = leq @ k_el @ leqt
# Também pode ser escrito -> k_global = leq.dot(k_el).dot(leqt)
print(f'a) MATRIZ DE RIGIDEZ GLOBAL - L k LT: \n\n{k_global}\n')
# print(k_global.shape)


# Vetor das Cargas Nodais (Cargas Pontuais e Cargas de Momento) - { λ }
f1x, f2y, f3m, f4x, f5y, f6m, f7x, f8y, f9m, f10x, f11y, f12m, f13x, f14y, f15m, f16x, f17y, f18m = 0, 0, 0, 0, 0, 0, 0, -10e3, 0, 0, -10e3, 0, 0, 0, 0, 0, 0, 0
force = np.array([f1x, f2y, f3m, f4x, f5y, f6m, f7x, f8y, f9m, f10x, f11y, f12m, f13x, f14y, f15m, f16x, f17y, f18m])
fn = np.transpose(force)  # Transformando em vetor

# Colocando as restrições de apoio em { λ }
fn = np.delete(fn, [0, 1, 2, 15, 16, 17], 0)
print(f'b) Vetor das Cargas Nodais - λ: \n\n{fn}\n')


# ---------------------------------------------------------------------------------------------------------------------


# Utilizando a resolução de matriz inversa -> { δ } = [L k LT] ^ -1 * { λ }

dlt = (np.linalg.inv(k_global)) @ fn
print(f'c) Vetor dos Deslocamentos Nodais - δ :  \n\n{dlt}\n')

# ---------------------------------------------------------------------------------------------------------------------

'''
Passo 3: Encontrar os valores das Deformações Correspondentes:

        {θ} = [L.T] * {δ}
'''

tta = leqt @ dlt
print(f'd) Vetor das Deformações Correspondentes - θ: \n\n{tta}\n')

# ---------------------------------------------------------------------------------------------------------------------

'''
Passo 4: Encontrar os valores dos Esforços Seccionais Internos:

        {m} = [k] * {θ}
'''

esf_in = k_el @ tta
print(f'e) Vetor dos esforçso internos - m: \n\n{esf_in}\n')