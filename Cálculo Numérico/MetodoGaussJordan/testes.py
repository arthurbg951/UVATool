import numpy as np
matriz = np.array([
    [1,-0,0,-1,0,-0,0],
    [0,0.22222222,-0.22222222,-0,-0.66666667,0.66666667,-80],
    [0,0,-1,0,1,0,0],
    [0,0,0,1,-0,0,0],
    [0,0,0,0,0.66666667,-0.66666667,0],
    [0,0,0,0,0,-1,0]
])
#Transforma elementos da matriz em float
matriz = np.array(matriz, dtype=np.float64)
#Determina o numero de linhas e colunas
nLinhas = len(matriz)                 
nColunas = len(matriz[0])             
print("matriz com {0} linhas e {1} colunas".format(nLinhas, nColunas))
print("\n", matriz, "\n")

#[linhas, colunas]
#Altera linhas com pivor igual a zero
c = 0
for k in range(0, nLinhas-1):
  while matriz[k,k]==0:
    if matriz[k,k] == matriz[nLinhas-1,nLinhas-1]:
      aux = matriz[k,:].copy()
      matriz[k,:] = matriz[k-1,:].copy()
      matriz[k-1,:] = aux.copy() 
    if matriz[k+c,k] !=0:
      aux = matriz[k,:].copy()
      matriz[k,:] = matriz[k+c,:].copy()
      matriz[k+c,:] = aux.copy()
    else:
      c = c + 1
print("Matriz modificada:","\n", matriz, "\n")   

#Realiza o escalonamento por eliminação
for i in range(0, nLinhas): 
  for j in range(i+1, nLinhas):
    mult = matriz[j,i]/matriz[i,i]
    matriz[j,:] = matriz[j,:] - mult*matriz[i,:]
print("Escalonamento por eliminação\n", matriz)

#Realiza o metodo de Gauss Jordan
for i in range(nLinhas-1, -1,-1): 
  for j in range(nLinhas-1, -1,-1):
    if j<i:
      mult = matriz[j,i]/matriz[i,i]
      matriz[j,:] = matriz[j,:] - mult*matriz[i,:]
#Transforma a diagonal dos pivores em 1
for i in range(0, nLinhas): 
  for j in range(i, nLinhas):
    matriz[j,:] = matriz[j,:]/matriz[i,i]
print("Metodo de Gauss Jordan\n", matriz)