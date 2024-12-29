class Analise:
    viaRigidezAnalitica = 0  # elastica
    viaMinimaNormaEuclidiana = 1  # rígido plastica


# CLASSE SUPPORT EM PORTUGUES
class Apoio:
    primeiro_genero = 0
    segundo_genero = 1
    terceiro_genero = 2
    rotula = 3
    semi_rigido = 4
    sem_suporte = 5

    # SUGESTÃO PARA SOLUCIONAR APOIO SEMI RIGIDO - NOT IMPLEMENTED
    sem_suporte_semi_rigido = 6


class Support:
    roller = 0  # PRIMEIRO GENERO
    pinned = 1  # SEGUNDO GENERO
    fixed = 2  # TERCEIRO GENERO
    middle_hinge = 3  # RÓTULA
    semi_fixed = 4  # SEMI RÍGIDO
    no_support = 5  # SEM SUPORTE
