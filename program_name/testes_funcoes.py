import numpy as np
ngdl = 15
# Matriz de equilibrio - [ L ]
leq = np.zeros((ngdl, ngdl))
print(leq)
leq[1, 5] = 14764465465
print(f'{leq}:.2f')
