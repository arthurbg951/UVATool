 ## Instruções para utilização do UVATool pelo código fonte

Para utilização do UVATool é necessário: 1 - python 3.8 ; 2 - biblioteca "pyqt5-tools"

OBS: para instalar o passo 2, basta executar o comando: pip install pyqt5-tools

No github, procure o botão code e baixe o zip do código, ou clone, caso conheça o sistema do git.

Após instalar o python e a biblioteca, para executar, siga os comandos para o seu sistema operacional:

Windows: Basta executar o arquivo setup.bat dentro da pasta src/UVATool_UI

MacOS: Entre na pasta src/UVATool_UI pelo terminal e digite: python3.8 form_uvatool.py

Linux: Entre na pasta src/UVATool_UI pelo terminal e digite: python3.8 form_uvatool.py


<!-- Para iniciar os trabalhos é necessário a instalação do git no computador do usuário. Cada pasta conterá informações
sobre a utilização do sistema em cada área de desenvolvimento.

## O que é o git?

O git é um sistema de versionamento que utilizamos no UVATools para manter as alterações
feitas pelo sistema a medida que é desenvolvido. Segue algumas orientações para utilização do git
para novos usuários.  -->

## Anotações git

### Adiciona todos os arquivos no git

git add .

### Para adicionar somente um arquivo o comando fica o seguinte

git add ARQUIVO

obs:o arquivo deve conter a extenção exemplo - arquivo.txt


### Adiciona um commit no branch master

git commit -m "COMENTÁRIO"


### Sincroniza os arquivos no github

git push


### Atualiza os arquivos locais

git pull


### Verifica commits pelo terminal

git log --oneline

