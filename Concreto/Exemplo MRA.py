import math as m
import numpy as np

'''
Resolvendo o Exemplo do material pelo método da Rigidez Analítica com Python


Passo 1: Criando as matrizes e vetores
'''
# Matriz de equilibrio - [ L ]

af12 = 0 * (m.pi/180.)
af23 = 0 * (m.pi/180.)
af34 = 0 * (m.pi/180.)
l12, l23, l34 = 1.5, 1.5, 1.5

c1 = np.cos(af12)
c2 = np.cos(af23)
c3 = np.cos(af34)

s1 = np.sin(af12)
s2 = np.sin(af23)
s3 = np.sin(af34)

lo_eq = np.array([
    [-c1,  s1/l12,  -s1/l12,    0,        0,       0,    0,       0,       0],
    [-s1, -c1/l12,   c1/l12,    0,        0,       0,    0,       0,       0],
    [0,         1,        0,    0,        0,       0,    0,       0,       0],
    [c1,  -s1/l12,   s1/l12,  -c2,   s2/l23, -s2/l23,    0,       0,       0],
    [s1,   c1/l12,  -c1/l12,  -s2,  -c2/l23,  c2/l23,    0,       0,       0],
    [0,         0,       -1,    0,        1,       0,    0,       0,       0],
    [0,         0,        0,   c2,  -s2/l23,  s2/l23,  -c3,  s3/l34, -s3/l34],
    [0,         0,        0,   s2,   c2/l23, -c2/l23,  -s3, -c3/l34,  c3/l34],
    [0,         0,        0,    0,        0,      -1,    0,       1,       0],
    [0,         0,        0,    0,        0,       0,   c3, -s3/l34,  s3/l34],
    [0,         0,        0,    0,        0,       0,   s3,  c3/l34, -c3/l34],
    [0,         0,        0,    0,        0,       0,    0,       0,      -1]
])
# Colocando as restrições de apoio em [ L ]
leq = np.delete(lo_eq, [0, 1, 10], 0)
# print(lo_eq.shape)

# Matriz de equilibrio Transposta - [ L.T ]
leqt = lo_eq.transpose()
# Colocando as restrições de apoio em [ L.T ]
#leqt = np.delete(leqt, [0, 1, 10], 1)
# print(leqt.shape)

"""
 0 -> linha 
 1 -> coluna
"""

# Matriz de rigidez do elemento - [ k ]

p11, p12, p22, p23, p33, p34 = 0, 1, 1, 1, 1, 0
e12, e23, e34 = 205e6, 205e6, 205e6
in12, in23, in34 = 1.7067e-2, 1.7067e-2, 1.7067e-2
aa12, aa23, aa34 = 0.32, 0.32, 0.32

ft1_1 = (3 * p11 / (4 - p11 * p12)) * (4 * e12 * in12 / l12)
ft2_1 = (3 * p11 * p12 / (4 - p11 * p12)) * (-2 * e12 * in12 / l12)
ft3_1 = (3 * p12 / (4 - p11 * p12)) * (4 * e12 * in12 / l12)
ft4_1 = e12 * aa12 / l12

ft1_2 = (3 * p22 / (4 - p22 * p23)) * (4 * e23 * in23 / l23)
ft2_2 = (3 * p22 * p22 / (4 - p22 * p23)) * (-2 * e23 * in23 / l23)
ft3_2 = (3 * p23 / (4 - p22 * p23)) * (4 * e23 * in23 / l23)
ft4_2 = e23 * aa23 / l23

ft1_3 = (3 * p33 / (4 - p33 * p34)) * (4 * e34 * in34 / l34)
ft2_3 = (3 * p33 * p34 / (4 - p33 * p34)) * (-2 * e34 * in34 / l34)
ft3_3 = (3 * p34 / (4 - p33 * p34)) * (4 * e34 * in34 / l34)
ft4_3 = e34 * aa34 / l34

k_el = np.array([
    [ft1_1, ft2_1,     0,     0,     0,     0,     0,     0,     0],
    [ft2_1, ft3_1,     0,     0,     0,     0,     0,     0,     0],
    [0,         0, ft4_1,     0,     0,     0,     0,     0,     0],
    [0,         0,     0, ft1_2, ft2_2,     0,     0,     0,     0],
    [0,         0,     0, ft2_2, ft3_2,     0,     0,     0,     0],
    [0,         0,     0,     0,     0, ft4_2,     0,     0,     0],
    [0,         0,     0,     0,     0,     0, ft1_3, ft2_3,     0],
    [0,         0,     0,     0,     0,     0, ft2_3, ft3_3,     0],
    [0,         0,     0,     0,     0,     0,     0,     0, ft4_3]
])
# print(k_el.shape)
'''
Matriz de Rigidez Global - k_global

        ([L * k * L.T])
'''
# k_global = lo_eq @ k_el @ leqt

aux = lo_eq.dot(k_el)
k_global = aux.dot(leqt)

# Também pode ser escrito -> k_global = leq.dot(k_el).dot(leqt)
print(k_global)
print(k_global.shape)
k_global = np.delete(k_global, [0, 1, 10], 0)
k_global = np.delete(k_global, [0, 1, 10], 1)
print(f'\n\n {k_global}')
print(k_global.shape)



# Vetor das Cargas Nodais (Cargas Pontuais e Cargas de Momento) - { λ }
f1x, f2y, f3m, f4x, f5y, f6m, f7x, f8y, f9m, f10x, f11y, f12m = 0, 0, 0, 0, -10, 0, 0, -10, 0, 0, 0, 0
force = np.array([f1x, f2y, f3m, f4x, f5y, f6m,
                 f7x, f8y, f9m, f10x, f11y, f12m])
fn = np.transpose(force)  # Transformando em vetor

# Colocando as restrições de apoio em { λ }
fn = np.delete(fn, [0, 1, 10], 0)

print(fn)

# esforcos, residuals, rank, s = np.linalg.lstsq(lo_eq, fn)
# print(esforcos)

def_nd = np.linalg.solve(k_global, fn)
print(def_nd)

'''
        ESTÁTICA
Relação de Equilíbrio -> {Cargas Nodais} = [Matriz de equilíbrio] * {Esforços Internos}

    {λ} = [L] * {m}
'''

esforcos = np.linalg.solve(leq, fn)
# print(esforcos)
'''
# Organizando o vetor resposta
convertido = []

# Elemento 1
convertido.append(f'm1 = {esforcos[1]:.2f}')
convertido.append(f'm2 = {esforcos[2]:.2f}')
convertido.append(f'n1 = {esforcos[0]:.2f}')
# Elemento 2
convertido.append(f'm3 = {esforcos[4]:.2f}')
convertido.append(f'm4 = {esforcos[5]:.2f}')
convertido.append(f'n2 = {esforcos[3]:.2f}')
# Elemento 3
convertido.append(f'm5 = {esforcos[7]:.2f}')
convertido.append(f'm6 = {esforcos[8]:.2f}')
convertido.append(f'n3 = {esforcos[6]:.2f}')

# Vetor dos esforços internos {m} organizado:
for i in range(len(convertido)):
        print(convertido[i])
'''
# Vetor dos Esforços Seccionais Internos (Momentos Fletores e Esforços Normais) - { m }
m1 = esforcos[1]
m2 = esforcos[2]
n1 = esforcos[0]
m3 = esforcos[4]
m4 = esforcos[5]
n2 = esforcos[3]
m5 = esforcos[7]
m6 = esforcos[8]
n3 = esforcos[6]
esf_in = np.array([m1, m2, n1, m3, m4, n2, m5, m6, n3])
esf_in = esf_in.transpose()
for i in range(len(esf_in)):
     print(esf_in[i])

# esf_in = np.linalg.solve(k_global, fn)
# x, residuals, rank, s = np.linalg.lstsq(k_global, fn)
# print(esf_in.shape)


'''
        ESTÁTICA X CINEMÁTICA
Relação Constitutiva do Material -> {Esforços Internos} = [Matriz de Rigidez] * {Deformações correspondentes}

          {m} = [k] * {θ}
'''

# x, residuals, rank, s = np.linalg.lstsq(k_el, esf_in)
# def_corresp = np.linalg.solve(k_el, esf_in)
# print(def_corresp)

"""
# Vetor dos Deslocamentos Nodais (Deslocamentos Lineares e Rotacionais) - { δ }
dt1x, dt2y, dr3m, dt4x, dt5y, dr6m, dt7x, dt8y, dr9m, dt10x, dt11y, dr12m = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
dt = np.array([dt1x, dt2y, dr3m, dt4x, dt5y, dr6m,
              dt7x, dt8y, dr9m, dt10x, dt11y, dr12m])
dlt = np.transpose(dt)  # Transformando em vetor
# Colocando as restrições de apoio em ( δ )
dlt = np.delete(dlt, [0, 1, 10], 0)
# print(dlt.shape)

# Vetor das Deformações Correspondentes (Deformações Lineares e Angulares) - { θ }
theta1, theta2, delta1, theta3, theta4, delta2, theta5, theta6, delta3 = 0, 0, 0, 0, 0, 0, 0, 0, 0
tta = np.array([theta1, theta2, delta1, theta3,
               theta4, delta2, theta5, theta6, delta3])
tta = np.transpose(tta)
# print(tta.shape)

# Vetor dos Esforços Seccionais Internos (Momentos Fletores e Esforços Normais) - { m }
# m1, m2, n1, m3, m4, n2, m5, m6, n3 = 0, 0, 0, 0, 0, 0, 0, 0, 0
# esf_in = np.array([m1, m2, n1, m3, m4, n2, m5, m6, n3])
# esf_in = np.linalg.solve(k_global, fn)
# x, residuals, rank, s = np.linalg.lstsq(k_global, fn)
# print(esf_in.shape)

# print(k_global)
# x = vetor solução
# print(x)
"""

'''
Passo 2: Através da triangularização de Gauss Jordan, encontrar os valores dos Deslocamentos Nodais δ:

        {λ} = [L k LT] * {δ}

'''


'''
Passo 3: Encontrar os valores das Deformações Correspondentes:

        {θ} = [L.T] * {δ}
'''


'''
Passo 4: Encontrar os valores das Esforços Seccionais Internos:

        {m} = [k] * {θ}
'''
