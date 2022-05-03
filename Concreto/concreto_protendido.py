import math as m
import numpy as np

print("""
----------------------------------------------------------------
               ESTRUTURAS DE CONCRETO PROTENDIDO

          Dimensionamento de viga faixa protendida:
                projeto proposto na disciplina

                Autor: Victtor Rodrigues Feijão

----------------------------------------------------------------
""")


"""
CARREGAMENTO DA LAJE 1
"""
l_x = 14.50  # comprimento externo da  no eixo x
l_y = 6.20  # comprimento externo da edificação no eixo y 
hx_pilar = 0.30


# Dimensão da viga protendida V1 e V2


l_vcp = l_x - hx_pilar
h_vcp = 0.60
b_vcp = 1.10
d_vcp = h_vcp - 7e-2

hy_pilar = b_vcp

# Dimensão da laje nervurada
h_laje = 0.25
b_v3_v4 = 0.15

vao_laje_x = l_x - b_v3_v4
vao_laje_y = l_y - b_vcp
area_laje1 = vao_laje_x * vao_laje_y
pd = 3.00

# Carregamento da Laje 1
# Laje nervurada com formas 80x80 e h=25cm com peso própio de 303,9kg/m²

#    CARREGAMENTO PERMANENTE (g)

# > Peso própio:
pp_impacto = 3.039  # kN/m²

# > Alvenaria sobre a laje
l_alvenaria = 18.00
b_alvenaria = 0.15
alvenaria = 13 * (l_alvenaria * b_alvenaria * (pd - h_laje)) / (area_laje1)  # # kN/m²

# > Revestimento:
revestimento = 1.00 # kN/m²

# > Pavimentação
pavimentacao = 1.00 # kN/m²

g_laje = pp_impacto + alvenaria + revestimento + pavimentacao

#    CARREGAMENTO VARIÁVEL (q)

# sobrecarga: sala comercial
sobre_carga = 2.00 # kN/m²

q_laje = sobre_carga

# > Aréa de influência

b_maior_influencia = vao_laje_x
h_ai = vao_laje_y / 2
b_menor_influencia = vao_laje_x - 2 * h_ai

aa_influencia_l1 = (b_maior_influencia + b_menor_influencia) * h_ai / 2
# print(f'{aa_influencia_l1:.2f}')

# > Reação da laje 1
rl1 = (g_laje + q_laje) * aa_influencia_l1 / l_vcp
# print(rl1)

"""  CARREGAMENTO DA VIGA PROTENDIDA 1  """

# Dados 
alvenaria_viga = 13 * (b_alvenaria * (pd - h_vcp))  # kN/m
peso_propio_vp = 25 * (b_vcp * h_vcp)  # kN/m
carregamento = rl1 + alvenaria_viga + peso_propio_vp  # kN/m
# -----------------------------------------------


"""  Cálculo do momento fletor Md  """
md = 1.4 * (carregamento * l_vcp ** 2 / 8)
# -----------------------------------------------


"""  DIMENSIONAMENTO  """

# Dados 
e_s = 10  # ‰
e_c = 3.5  # ‰
lmbd = 0.8  # Lambda
class_concreto = 40 * 1e6  # C40
s_cd = 0.85 * class_concreto / 1.4  # Sigma,cd
aa_cordoalha = 0.98  # cm²
percas = 21 / 100  # %
protension_force = 140e3  # 140 kN 
young_ap = 200e9  # 200GPa
# -----------------------------------------------

"""  Cálculos  """

# > Kmd
kmd = (md * 1e3) / (b_vcp * (d_vcp ** 2) * s_cd)

# > Kx
kx = (1 - m.sqrt(1 - 2 * kmd)) / lmbd

# > Definição dos domínios:

# > Domínio 2
if kx <= 0.259:
  print("Domínio 2")
  e_c = kx / (1 - kx) * e_s 
  if e_c < 2.00:
      s_cd = s_cd * (1 - (1 - kx / 2) ** 2)
      print(f'Verificação da Tensão de compressão no Concreto: {s_cd:.2f}MPa')
      kmd = (md * 1e3) / (b_vcp * (d_vcp ** 2) * s_cd)
      print(f'Novo Kmd = {kx:.3f}')
      kx = (1 - m.sqrt(1 - 2 * kmd)) / lmbd
      print(f'Novo Kx = {kx:.3f}')

# > Domínio 3
if kx > 0.259 and kx <= 0.324:
    print("Domínio 3")
    e_s = (1 - kx) / kx * e_c

# > Domínio 4 com ductilidade
if kx > 0.324  and kx <= 0.450:
    print("Domínio 4 com ductilidade")
    e_s = (1 - kx) / kx * e_c

# > Domínio 4 sem ductilidade e domínio 5 
if kx > 0.450:
    print("Domínio 4 sem ductilidade, ou domínio 5. Redimensione a seção!!!!")
    raise
  
# Deformações específicas do Aço de Protensão
e_fp = (1 - percas) * protension_force / (aa_cordoalha * 1e-4 * young_ap) * 1000
# print(f'{e_p:.2f}‰')

x_ep = e_s + e_fp
# print(x_ep)

cp190_def = [5.25, 6.794, 7.438, 8.167,  9.00, 9.962, 10.00, 12.50, 15.00, 17.50,
            20.00, 22.50, 25.00, 27.50, 30.00, 32.50, 35.00, 37.50, 40.00,]

cp190_ssd = [1025, 1314, 1411, 1459, 1482, 1486, 1486, 1496, 1507, 1517,
             1527, 1538, 1548, 1559, 1569, 1579, 1590, 1600, 1611]


for i in range(len(cp190_def)):
    if cp190_def[i] < x_ep:
      j = i + 1
      x1 = cp190_def[i]
      x2 = cp190_def[j]
      y1 = cp190_ssd[i]
      y2 = cp190_ssd[j]
    else:
        pass


s_pd = ((x_ep - x1) / (x2 - x1) * (y2 - y1) + y1) * 1e6
# print(f'Função de interpolação: {s_pd:.3f}')

# > Kz
kz = 1 - 0.5 * lmbd * kx

# > Área de aço ativa
as_ativa = md * 1e3 / (kz * d_vcp * s_pd)

as_ativa *= 1e4

# > Quantidade de cordoalhas
qtd_cordoalhas = int(as_ativa / aa_cordoalha) + 1


# > Área de aço passiva
as_min = 0.179 / 100 * ((b_vcp * 100) * (h_vcp * 100))
as_passiva = as_min

# > Número de bitolas
aa_bitola = 0.25 * m.pi * 1.25 ** 2 
qtd_bitolas = int(as_passiva / aa_bitola) + 1


# > Armadura sobre apoio
as_sobreapoio = as_passiva / 3
qtd_sobreapoio = int(as_sobreapoio / aa_bitola) + 1

if qtd_sobreapoio < 4:
    qtd_sobreapoio == 4

# > 5% do vão da viga
l5_100 = 0.05 * l_vcp * 1e2

print(f'\nN° de cordoalhas de armadura ativa:......  {qtd_cordoalhas} ∅ 12.7mm \n'
      f'N° de bitolas da armadura passiva:.......  {qtd_bitolas} ∅ 12.5mm \n'
      f'N° de bitolas da armadura sobre-apoio:...   {qtd_sobreapoio} ∅ 12.5mm \n'
      f''
      f''
      f''
      f''
      f''
      f''
)