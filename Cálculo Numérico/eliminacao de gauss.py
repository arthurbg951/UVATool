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

# Exemplo de matriz a ser triangularizada

matriz = [[1, 1, 0, 3],
          [2, 1, -1, 1],
          [3, -1, -1, 2],
          [-1, 2, 3, -1]]

vector = [4, 1, -3, 4]

resposta = gauss(matriz, vector)

for i in resposta:
    print(i)
