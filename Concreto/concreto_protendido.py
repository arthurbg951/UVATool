import math as m

print("""
-------------------------------------------------------------------------
    
                   ESTRUTURAS DE CONCRETO PROTENDIDO
    
               Dimensionamento de viga faixa protendida:
                    Projeto proposto na disciplina
    
                    Autor: Victtor Rodrigues Feijão
    
-------------------------------------------------------------------------
""")


l_x = 21.60  # comprimento externo da  no eixo x
l_y = 6.00  # comprimento externo da edificação no eixo y

percas = 25  # %

# Dimensão da viga protendida V1 e V2

hx_pilar = 0.60  # Largura do pilar em x (hx)

l_vcp = l_x - hx_pilar  # Vão da viga protendida (L)


b_vcp = 1.20  # Largura da viga protendida (b)
h_vcp = 0.85  # Altura da viga protendida  (h)


d_vcp = h_vcp - 0.07  # Altura útil da viga protendida (d)
f_cb = 0.5 * h_vcp - 0.07  # Flecha da cablagem (f1)

hy_pilar = b_vcp  # Largura do pilar em y (hy)

# Dimensão da laje nervurada

h_laje = 0.25  # Altura da laje nervurada

b_v3_v4 = 0.20  # largura das vigas de concreto armado

vao_laje_x = l_x - b_v3_v4  # vão da laje em x
vao_laje_y = l_y - b_vcp  # vão da laje em y
area_laje1 = vao_laje_x * vao_laje_y  # área da laje
pd = 4.5  # pé direito

print(f'\n-> CARACTERISTICAS DA VIGA PROTENDIDA \n'
      f'\n - Viga protendida biapoiada com vão de {l_vcp:.2f}m\n'
      f' - Seção: {b_vcp * 100:.0f}cm x {h_vcp * 100:.0f}cm\n'
      f' - Ac: {(b_vcp * h_vcp):.2f}m²\n'
      f' - Percas de protensão: {percas}%\n'
      f' - Altura útil (d): {d_vcp*100:.1f}cm\n'
      f' - Pé direito: {pd:.2f}m\n'
      f' - Pilar: {hx_pilar*100:.0f} x {hy_pilar*100:.0f} cm')


"""------------------------------------------------------------------------------------------------------------------"""
"""
CARREGAMENTO DA LAJE 1

->  Laje nervurada com formas 80x80 e h=25cm com peso próprio de 303,9kg/m²

-->   CARREGAMENTO PERMANENTE (g)

"""
# > Peso próprio: -------------------------------------------------------------------------------------------------------

pp_impacto = 1.95  # kN/m² Laje nervurada com caixotes 61x61 unidirecional com 25cm de altura total. Fonte: Impacto


# > Alvenaria sobre a laje: --------------------------------------------------------------------------------------------
l_alvenaria = 0  # Comprimento de alvenaria decidido pelo usuário
b_alvenaria = 0.15  # Largura da alvernaria


alvenaria = 13 * (l_alvenaria * b_alvenaria * (pd - h_laje)) / area_laje1  # kN/m²

# > Revestimento: ------------------------------------------------------------------------------------------------------

revestimento = 1.00  # kN/m²

# > Pavimentação:-------------------------------------------------------------------------------------------------------

pavimentacao = 1.00  # kN/m²

# Somatório das cargas permanentes

g_laje = pp_impacto + alvenaria + revestimento + pavimentacao


"""
-->   CARREGAMENTO VARIÁVEL (q)
"""

# Sobrecarga: sala comercial -------------------------------------------------------------------------------------------

sobre_carga = 6.00  # kN/m²

# Somatório das cargas permanentes

q_laje = sobre_carga  # kN/m²

# > Aréa de influência -------------------------------------------------------------------------------------------------

b_maior_influencia = vao_laje_x
h_ai = vao_laje_y / 2
b_menor_influencia = vao_laje_x - 2 * h_ai

# Calculo da área de influência
aa_influencia_l1 = (b_maior_influencia + b_menor_influencia) * h_ai / 2  # m²


# > Reação da laje 1

rl1 = (g_laje + q_laje) * aa_influencia_l1 / l_vcp  # kN/m²

print(f'\n-> CARREGAMENTO DA LAJE 1 NERVURADA \n'
      f'\nLaje nervurada com caixotes 61x61 unidirecional com 25cm de altura total\n'
      f'apoiada nos 4 cantos. Peso próprio de {pp_impacto*100:.2f}kg/m² (calculado).\n'
      f'68 caixotes duplos  ...................... 61 x 122 cm\n'
      f'34 caixotes  ............................. 61 x 61 cm\n'
      f'34 meio caixotes  ........................ 61 x 30,5 cm\n'
      f'1 meio caixote  .......................... 30,5 x 61 cm\n'
      f'2 meio caitote duplo  .................... 30,5 x 122 cm\n'
      f'1 meio meio caixote  ..................... 30,5 x 30,5 cm\n'
      f'Fonte: Impacto Protensão\n'
      f'\n'
      f'Vão da laje em x: {vao_laje_x:.2f}m e Vão da laje em y: {vao_laje_y:.2f}m'
      f'\n'
      f'\n - Carregamento permanente (g)\n'
      f'Peso próprio:  ...............................  {pp_impacto:.3f}kN/m²\n'
      f'Revestimento:  ...............................  {revestimento:.2f}kN/m²\n'
      f'Pavimentação:  ...............................  {pavimentacao:.2f}kN/m²\n'
      f'Alvenaria: {l_alvenaria:.2f}m .............................  {alvenaria:.2f}kN/m²\n'
      f'                                        Total:  {g_laje:.2f}kN/m²\n'
      f'\n - Carregamento variável (q)\n'
      f'Sobrecarga: Biblioteca  ......................  {sobre_carga:.2f}kN/m²\n'
      f'                                        Total:  {q_laje:.2f}kN/m²\n\n'
      f' - Carregamento total (g + q)  ...............  {g_laje + q_laje:.2f}kN/m²\n'
      f'\n'
      f' - Área de influência da laje 1:  ............  {aa_influencia_l1:.2f}m²\n')
"""------------------------------------------------------------------------------------------------------------------"""


"""  CARREGAMENTO DA VIGA PROTENDIDA 1  """

# Dados 
alvenaria_viga = 13 * (b_alvenaria * (pd - h_vcp))  # kN/m
peso_propio_vp = 25 * (b_vcp * h_vcp)  # kN/m
carregamento = rl1 + alvenaria_viga + peso_propio_vp  # kN/m

print(f'\n-> CARREGAMENTO DA VIGA 1 PROTENDIDA \n'
      f'\nReação da Laje 1  ............................  {rl1:.2f}kN/m\n'
      f'Peso próprio:  ...............................  {peso_propio_vp:.2f}kN/m\n'
      f'Alvenaria sob viga:  .........................   {alvenaria_viga:.2f}kN/m\n'
      f'                                        Total:  {carregamento:.2f}kN/m\n')

"""------------------------------------------------------------------------------------------------------------------"""

"""  CÁLCULO DO MOMENTO FLETOR NO ESTADO LIMITE ÚLTIMO (ELU) DE VIGA BIAPOIADA  """

mk = (carregamento * l_vcp ** 2 / 8)
md = 1.4 * mk

print(f'\n-> CÁLCULO DO MOMENTO FLETOR NO ESTADO LIMITE ÚLTIMO (ELU) DE VIGA BIAPOIADA \n'
      f'\nMk = {mk:.2f}kNm\n'
      f'Md = 1.4 * Mk\n'
      f'Md = {md:.2f}kNm\n')

"""------------------------------------------------------------------------------------------------------------------"""


"""  DIMENSIONAMENTO  """

# Dados 
e_s = 10  # ‰
e_c = 3.5  # ‰
lmbd = 0.8  # Fator de retangularização - Lambda
class_concreto = 40 * 1_000_000  # C40
class_aco = 500 * 1e6  # CA-50
s_cd = 0.85 * class_concreto / 1.4  # Sigma,cd
aa_cordoalha = 0.98  # cm²
efc_prot = (100 - percas) / 100
protension_force = 140e3  # 140 kN 
young_ap = 200e9  # 200GPa

"""------------------------------------------------------------------------------------------------------------------"""

print("""\n-> VERIFICAÇÃO DO DOMÍNIO DA SEÇÃO ADOTADA \n""")

# > Kmd
kmd = (md * 1e3) / (b_vcp * (d_vcp ** 2) * s_cd)

# > Kx
kx = (1 - m.sqrt(1 - 2 * kmd)) / lmbd

# > Definição dos domínios:

# > Domínio 2
if kx <= 0.259:
    print("Domínio 2\n")
    e_c = (kx / (1 - kx)) * e_s 
    print(f'Verificações:\n'
          f'Deformação específica na zona comprimida de concreto'
          f'\nεc: {e_c:.2f}‰  -> OK!\n')
    
    if e_c < 2.00:
        raise ValueError("Domínio 2 com baixa tensão no concreto, redefinir a seção!!!!\n\n")
        # s_cd = (0.85 * class_concreto / 1.4) * (1 - (1 - (kx / 2)) ** 2)
        # print(s_cd)
        # print(f'Ec menor que 2‰ > {e_c:.2f}‰\n')
        # print(f'Verificação da Tensão de compressão no Concreto: {s_cd*1e-6:.2f}MPa\n')
        # kmd_corr = (md * 1e3) / (b_vcp * (d_vcp ** 2) * s_cd)
        # print(f'Kmd, corrigido = {kmd_corr:.3f}\n')
        # kx_corr = (1 - m.sqrt(1 - 2 * kmd_corr)) / lmbd
        # print(f'Kx, corrigido = {kx_corr:.3f}\n')
        # kmd = kmd_corr
        # kx = kx_corr

# > Domínio 3
if (kx > 0.259) and (kx <= 0.324):
    print("Domínio 3\n")
    e_s = (1 - kx) / kx * e_c
    print(f'Verificações:\n'
          f'Deformação específica do aço protendido'
          f'\nεs: {e_s:.2f}‰\n')

# > Domínio 4 com ductilidade
if (kx > 0.324) and (kx <= 0.450):
    print("Domínio 4 com ductilidade\n")
    e_s = (1 - kx) / kx * e_c
    print(f'Verificações:\n'
          f'Deformação específica do aço protendido'
          f'\nεs: {e_s:.2f}‰\n')

# > Domínio 4 sem ductilidade e domínio 5 
if kx > 0.450:
    raise ValueError("Domínio 4 sem ductilidade, ou domínio 5. Redimensione a seção!!!!\n\n")
  
# Deformações específicas do Aço de Protensão
e_fp = efc_prot * protension_force / (aa_cordoalha * 1e-4 * young_ap) * 1000
# print(f'{e_p:.2f}‰')

x_ep = e_s + e_fp
# print(x_ep)

cp190_def = [5.25, 6.794, 7.438, 8.167,  9.00, 9.962, 10.00, 12.50, 15.00, 17.50,
             20.00, 22.50, 25.00, 27.50, 30.00, 32.50, 35.00, 37.50, 40.00]

cp190_ssd = [1025, 1314, 1411, 1459, 1482, 1486, 1486, 1496, 1507, 1517,
             1527, 1538, 1548, 1559, 1569, 1579, 1590, 1600, 1611]

x1, x2, y1, y2 = None, None, None, None

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

# > Area de aço se fosse passiva

aa_steel = as_ativa * s_pd * 1.15 / class_aco


# > Quantidade de cordoalhas
qtd_cordoalhas = int(as_ativa / aa_cordoalha) + 1


# > Área de aço passiva >>>>>>> IMPLEMENTAR RO MINIMO
as_min = 0.179 / 100 * ((b_vcp * 100) * (h_vcp * 100))
as_passiva = as_min

# > Número de bitolas
aa_bitola = 0.25 * m.pi * 2.0 ** 2
qtd_bitolas = int(as_passiva / aa_bitola) + 1


# > Armadura sobre apoio
aa_bitola_sa = 0.25 * m.pi * 1.6 ** 2
as_sobreapoio = as_passiva / 3
qtd_sobreapoio = int(as_sobreapoio / aa_bitola_sa) + 1

if qtd_sobreapoio < 4:
    qtd_sobreapoio = 4

# > Cordoalhas necessárias para anular o peso próprio da viga
qtd_cordoalhas_pp = int(((25 * b_vcp * h_vcp) * (l_vcp ** 2)) / (8 * protension_force * 1e-3 * efc_prot * f_cb))
qtd_cordoalhas_pp += 1

# > Verificação da anulação do peso próprio

alv_prot = None

if qtd_cordoalhas > qtd_cordoalhas_pp:
    rel_prot = qtd_cordoalhas/qtd_cordoalhas_pp
    carga_exced = peso_propio_vp + ((peso_propio_vp * rel_prot) - peso_propio_vp)
    alv_prot = (carga_exced - peso_propio_vp) / alvenaria_viga
    if alv_prot > 1:
        raise ValueError("Protensão de Carga Variável!!!!!\n\n")

# > 5% do vão da viga
l5_100 = 0.05 * l_vcp * 1e2

print(f'\n-> DIMENSIONAMENTO    \n\n'
      f'Kmd:  ........................................  {kmd:.3f}\n'
      f'Kx:  .........................................  {kx:.3f}\n'
      f'εc:  .........................................  {e_c:.2f}‰\n'
      f'εs:  .........................................  {e_s:.2f}‰\n'
      f'εp:  .........................................  {e_fp:.2f}‰\n'
      f'εtotal:  .....................................  {x_ep:.2f}‰\n'
      f'σ,pd: ........................................  {s_pd * 1e-6:.2f}Mpa CP 190 RB\n'
      f'Kz:  .........................................  {kz:.3f}\n'
      f'Ap:  .........................................  {as_ativa:.2f}cm²\n'
      f'As sem protensão:  ...........................  {aa_steel:.2f}cm²\n'
      f'As,min:  .....................................  {as_passiva:.2f}cm² - C40\n'
      f'As,sobreapoio:  ..............................  {as_sobreapoio:.2f}cm²\n'
      f'\nnº de cordoalhas peso próprio:  ..............  {qtd_cordoalhas_pp} ∅ 12.7mm CP 190 RB')

if qtd_cordoalhas > qtd_cordoalhas_pp:
    print(f'% de carga da alvenaria protendida:  .........  {alv_prot*100:.2f}%')

print(f'\n\n-> DETALHAMENTO\n\n'
      f'Armaduras:\n\n'
      f'n° de cordoalhas de armadura ativa:  .........  {qtd_cordoalhas} ∅ 12.7mm CP 190 RB\n'
      f'n° de bitolas da armadura passiva:  ..........   {qtd_bitolas} ∅ 20.0mm CA 50\n'
      f'n° de bitolas da armadura sobre-apoio:  ......   {qtd_sobreapoio} ∅ 16.0mm CA 50\n'
      f'\nCablagem:\n'
      f'\n5% de L: .....................................  {l5_100:.1f}cm'
      f'\nFlecha da cablagem  ..........................  {f_cb * 100:.0f}cm'
      f'\n')
