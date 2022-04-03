import numpy as np

'''
# -------------------------------------------------------------------------------------- #
  INPUT DATA 
# -------------------------------------------------------------------------------------- #
'''
# MATRIZ DE RIGIDEZ NODAL
k = np.array(
    [
        [2, -1, 0],
        [-1, 2, 0],
        [0, 0, 1/2]
    ]
)
print('[k] = \n', k)

# MATRIZ DE EQUILÍBRIO
L = np.array(
    [
        [-1, 0, 0],
        [0, -1/2, 1/2],
        [0, 1, 0],
        [1, 0, 0],
        [0, 1/2, -1/2],
        [0, 0, -1]
    ]
)
print('[L] = \n', L)

# VETOR CARGAS NODAIS
q = np.array([0, 0, 0, 0, -1, 0])
print('[λ] = \n', q)

'''
# -------------------------------------------------------------------------------------- #
  CALCULATIONS
# -------------------------------------------------------------------------------------- #
'''
# MATRIZ DE EQUILÍBRIO TRANSPOSTA
L_T = np.array(L).T
print('[LT] = \n', L_T)

# MATRIZ DE EQUILÍBRIO GLOBAL
k_global = np.dot(np.dot(L, k), L_T)
print('[L][k][LT] = \n', k_global)

# REMOVENDO REAÇÕES DAS MATRIZES
# VETOR CARGAS NODAIS
q = np.delete(q, [0, 1, 2], 0)
print('[λ] = \n', q)
# MATRIZ DE EQUILÍBRIO GLOBAL
k_global = np.delete(k_global, [0, 1, 2], 0)
k_global = np.delete(k_global, [0, 1, 2], 1)
print('[L][k][LT] = \n', k_global)

'''
# -------------------------------------------------------------------------------------- #
  ANSWER
# -------------------------------------------------------------------------------------- #
'''
# DESLOCAMENTO NODAL
d_nodal = np.linalg.solve(k_global, q)
print('[δ] = \n', d_nodal)
