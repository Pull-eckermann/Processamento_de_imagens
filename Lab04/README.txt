ERICK ECKERMANN CARDOSO
GRR20186075

Quarto trabalho de laboratório da disciplina de Processamento de imagens

Código escrito em Python3, utilizando as seguintes bibliotecas:
- Open-cv (cv2)
- sys
- numpy

O código está contido inteiramente no arquivo placa.py

Antes de executar, certifique que o arquivo das imagens estejam no mesmo diretório que placa.py, pois o código lê as imagens à partir do diretório corrente.

Para compilar e executar o programa, basta utilizar o comando python3 com o nome do arquivo, seguido pela imagem a ser filtrada e o nome da imagem de saída, da seguinte maneira:

$ python3 placa.py <IMG ENTRADA> <IMG SAIDA>

ex: python3 placa.py 2.jpg out.png

O programa criará uma imagem com o nome expecificado, sendo essa a imagem melhorada da melhor maneira possível para visualização da placa.
O programa irá gerar uma outra imagem contendo uma tentativa de identificação de bordas por contorno, a fim de trazer somente a imagem da placa a tona