import numpy as np
import math as m

"""
------------------------------------------------------------------------------------------------------------------------
IDEAL STRUCT AND TIE MODEL - iSTM
------------------------------------------------------------------------------------------------------------------------
"""
print(f'--------------------------------------------------------------------------'
      f'\nIDEAL STRUCT AND TIE MODEL - iSTM\n\n'
      f'UNIVERSIDADE ESTADUAL VALE DO ACARAÚ - UVA\n'
      f'Bem-vindo, software em desenvolvimento por alunos de Engenharia civil\n'
      f'\nv.0.1\n'
      f'--------------------------------------------------------------------------')
"""
------------------------------------------------------------------------------------------------------------------------
USER INPUT's
------------------------------------------------------------------------------------------------------------------------
"""
print(f'\n1) - CARACTERISTICAS DA VIGA ENSAIADA'
      f'\n')
# ----------------------------------------------------------------------------------------------------------------------

l_viga = float(input('  a) Qual o vão (L) da viga em (cm):  '))
h_viga = float(input('  b) Qual a altura (h) da viga em (cm):  '))
b_viga = float(input('  c) Qual a largura (b) da viga em (cm):  '))
rec = float(input('  d) Qual o recobrimento em (cm):  '))

rup = str(input(f'  e) Qual o modo de ruptura desejado no ensaio? \n'
                f'  1 - Flexão\n'
                f'  2 - Cisalhamento\n\n'))

ensaio = str(input(f'  f) Qual o ponto de aplicação das cargas na viga? \n'
                   f'  1 - Carregamento linear\n'
                   f'  2 - Carga pontual no meio do vão\n'
                   f'  3 - Cargas aplicadas a 1/3 do vão (L/3)\n'
                   f'  4 - Cargas aplicadas a 1/4 do vão (L/4)'
                   f'\n\n'))

# ----------------------------------------------------------------------------------------------------------------------
lh = l_viga / h_viga
print(f'\nO L/h da viga é: {lh:.2f}\n')
# Zona morta para vigas parede com L/h < 1.00
if lh <= 1.00:
    lh = 1.00001

# Ângulo de formação da Biela

ang_biela = -15.2 * np.log(lh) + 66.281  # Mapeamento Ansys
print(f'o Ângulo entre as barras é: {ang_biela:.2f}°')

# Dimensões da treliça

ang_biela *= m.pi/180.
l_bzinf = l_viga
z = 0
if lh >= 2:
    z = 0.90 * (h_viga - (rec + 6.250))
if lh < 2:
    pdz = -0.1259 * (lh ** 2) + 0.6107 * lh + 0.1939  # Mapeamento Ansys correlacionando com a altura útil
    z = pdz * (h_viga - (rec + 6.250))

print(f'O valor do braço de alavanca (Z) é {z:.3f} cm')
l_biela = z / np    .sin(ang_biela)
l_bzsup = l_bzinf - 2 * (z / np .tan(ang_biela))

print(f'O comprimento das bielas comprimidas é: {l_biela:.3f} cm')
print(f'O comprimento do banzo superior é: {l_bzsup:.3f} cm')
print(f'O comprimento do banzo inferior é: {l_bzinf:.3f} cm')
