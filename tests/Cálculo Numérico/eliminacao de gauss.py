import numpy as np

# Função que triangulariza e retorna o vetor resposta


def gauss(matriz, vector):
    n = len(matriz[0])
    mab = matriz

    # triangularização
    a = mab
    b = vector
    aux = 0
    for j in range(0, n):
        aux += 1
        for i in reversed(range(aux, n)):
            m = a[i][j]/a[j][j]

            for k in range(0, n):
                a[i][k] = a[i][k] - m*a[j][k]
            b[i] = b[i]-m*b[j]

    # Resolução do Sistema
    # Cálculo do vetor c
    x = []
    for i in range(n):
        x.append(0)

    n = n-1
    x[n] = b[n]/a[n][n]
    for i in reversed(range(0, n)):
        soma = 0
        for j in range(i, n):
            soma = soma+a[i][j+1]*x[j+1]
        x[i] = (b[i]-soma)/a[i][i]

    return x

# Exemplo vídeo CORRETO
# matriz = [[1, 1, 0, 3],
#           [2, 1, -1, 1],
#           [3, -1, -1, 2],
#           [-1, 2, 3, -1]]
# vector = [4, 1, -3, 4]


matriz = [
    [   2,     -0.5,     0],
    [-0.5,    0.625,  0.25],
    [   0,     0.25,   0.5]
]

vector = [0, -1, 0]


# Exemplo com ERRO
# matriz = [[6997470,0,4664980,0,0,0,0,0,0],
#          [0,9329960,-3109986.66666667,4664980,-9329960,3109986.66666667,0,0,0],
#          [4664980,-3109986.66666667,46130709.62962963,22935582.22222222,3109986.66666667,-23583685.92592593,-29155555.55555556,0,0],
#          [0,4664980,22935582.22222222,53063293.33333334,-4664980,6219973.33333333,0,0,0],
#          [0,-9329960,3109986.66666667,-4664980,16327430,-3109986.66666667,0,-6997470,0],
#          [0,3109986.66666667,-23583685.92592593,6219973.33333333,-3109986.66666667,43020722.96296296,29155555.55555556,0,-29155555.55555556],
#          [0,0,-29155555.55555556,0,0,29155555.55555556,43733333.33333334,0,0],
#          [0,0,0,0,-6997470,0,0,6997470,0],
#          [0,0,0,0,0,-29155555.55555556,0,0,43733333.33333334]]
# vector = [0,0,-10000,0,0,-10000,0,0,0]

# Exemplo com ERRO
# matriz = [
#     [0,3,0,0,0,0],
#     [0,0,0,-3,0,0],
#     [0,3,-1,0,0,1],
#     [0,0,-1,0,0,0],
#     [0,0,0,0,0,-1]
# ]
# vector = [0,0,-1,0,0,0]


resposta = gauss(matriz, vector)
print(resposta)

# resposta = np.linalg.solve(matriz, vector)
# print(resposta)
