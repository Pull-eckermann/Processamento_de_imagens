ERICK ECKERMANN CARDOSO
GRR20186075

Primeiro trabalho de laboratório da disciplina de Processamento de imagens

Código escrito em Python3, utilizando as seguintes bibliotecas:
- Open-cv (cv2)
- OS com o import específico da listdir

O código está contido inteiramente no arquivo histograma.py

Antes de executar, certifique que o arquivo das 25 imagens estejam no mesmo diretório que histograma.py, pois o código lê as imagens à partir do diretório corrente.
Segue exemplo de como deve estar o diretório:

eckermann@firelink:~/Documentos/Processamento_de_imagens/Lab01$ ls
b1.bmp  b3.bmp  b5.bmp  h2.bmp  h4.bmp  histograma.py  l2.bmp  l4.bmp  m1.bmp  m3.bmp  m5.bmp   mg2.bmp  mg4.bmp
b2.bmp  b4.bmp  h1.bmp  h3.bmp  h5.bmp  l1.bmp         l3.bmp  l5.bmp  m2.bmp  m4.bmp  mg1.bmp  mg3.bmp  mg5.bmp

PS: Se houver outros arquivos no diretório, o programa irá ignorá-los e somente fará a leitura das imagens de formato .bpm

Para compilar e executar o programa, basta utilizar o comando python3 com o nome do arquivo, da seguinte maneira:

$ python3 histograma.py 

O programa nao deve receber nenhum parâmetro de execução nem compilação.

O resultado impresso no terminal será a taxa de acerto para os 4 métodos de comparação de histogramas do open-cv, numa escala de 0 a 1.
