class apoio(enumerate):
    primeiro = 1
    segundo = 2
    terceiro = 3
    no_reaction = 0

    def __str__(self):
        return (
            f'1º genero = {apoio.primeiro}'
            f'2º genero = {apoio.segundo}'
            f'3º genero = {apoio.terceiro}'
            f'sem reação = {apoio.no_reaction}'
        )

print(apoio.primeiro)

print(apoio)


