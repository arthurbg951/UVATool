import numpy


class Export:
    # NÃO ESTÁ FUNCIONANDO CORRETAMENTE
    @staticmethod
    def matrixToCsv(file_name: str, matrix: numpy.array):
        # criar função para criar matrizes no exel
        file = open("{0}.csv".format(file_name), "w")
        linhas = matrix.shape[0]
        colunas = matrix.shape[1]
        print(linhas, colunas)
        linha = list()
        for i in range(linhas):
            for j in range(colunas):
                linha.append("{0},".format(matrix[i, j]))
            linha.append("\n")
        file.writelines(linha)
