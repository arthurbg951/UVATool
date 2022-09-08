import numpy as np

'''
# -------------------------------------------------------------------------------------- #
  INPUT DATA 
# -------------------------------------------------------------------------------------- #
'''
# MATRIZ DE RIGIDEZ NODAL -------> Certo: do elemento
k = np.array(
    [
        [1/2,  0,  0],  # Matriz de rigidez escrita de forma errada
        [  0,  2, -1],
        [  0, -1,  2]
    ]
)
print('[k] = \n', k)

# MATRIZ DE EQUILÍBRIO
L = np.array(
    [
        [-1, 0, 0],
        [0, -1/2, 1/2],  # Se o resultado não bater, revisar os valores obtidos nestas matrizes
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

# COLOCAÇÃO DAS RESTRIÇÕES DE APOIO ------> corrigido

# MATRIZEZ DE EQUILÍBRIO
L_eq = np.delete(L, [0, 1, 2], 0)
L_eqt = np.delete(L_T, [0, 1, 2], 1)
# VETOR CARGAS NODAIS
q = np.delete(q, [0, 1, 2], 0)
print('[λ] = \n', q)

# MATRIZ DE EQUILÍBRIO GLOBAL  ------> Só deve ser calculada após a colocações dos apoios
k_global = L_eq @ k @ L_eqt  # ------> alteração na multiplicação de matriz
print('[L][k][LT] = \n', k_global)

'''
# -------------------------------------------------------------------------------------- #
  ANSWER
# -------------------------------------------------------------------------------------- #
'''

# DESLOCAMENTO NODAL
d_nodal = (np.linalg.inv(k_global)) @ q  # Função correta pela inversão da matriz de rigidez global
print('[δ] = \n', d_nodal)

'''
# -------------------------------------------------------------------------------------- #
Continuando o código....
# -------------------------------------------------------------------------------------- #
'''

# DEFORMAÇÕES CORRESPONDENTES
tta = L_eqt @ d_nodal
print('[θ] = \n', tta)

# ESFORÇOS SECCIONAIS INTERNOS
esf_in = k @ tta
print('[θ] = \n', esf_in)
