import numpy as np
import cv2
import sys
import os
import scipy.ndimage as inter
from matplotlib import pyplot as plt

#Algoritmo de correção de rotação de https://python.tutorialink.com/python-opencv-skew-correction-for-ocr/
def correct_skew(bin_img, delta=1, limit=5):
  def determine_score(arr, angle):
      data = inter.rotate(arr, angle, reshape=False, order=0)
      histogram = np.sum(data, axis=1)
      score = np.sum((histogram[1:] - histogram[:-1]) ** 2)
      return histogram, score
  
  scores = []
  angles = np.arange(-limit, limit + delta, delta)
  
  for angle in angles:
      histogram, score = determine_score(bin_img, angle)
      scores.append(score)
  best_angle = angles[scores.index(max(scores))]
  
  (h, w) = bin_img.shape[:2]
  center = (w // 2, h // 2)
  M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
  rotated = cv2.warpAffine(bin_img, M, (w, h), flags=cv2.INTER_CUBIC, 
            borderMode=cv2.BORDER_REPLICATE)
  
  return best_angle, rotated

#Programa principal
if len(sys.argv) != 2:
    print("ERRO DE SINTAXE: python3 cartas.py <ARGUMENTO>")
    exit(0)


def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)

acertos = 0
for aux in os.listdir('.'):      #Itera sobre as imagens do diretório especificado
  if not(aux.endswith(".jpg")):      #Se não for imagem.jpg pula pra próxima iteração
    continue
  #Lê imagem
  img = cv2.imread(aux)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  #Gera imagem binária usando métrica de Otsu
  _, bin_img = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
  
  #======================================================
  #Conta Número de palavras na imagem
  if sys.argv[1] == '-w':
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    b_rect = cv2.morphologyEx(bin_img, cv2.MORPH_GRADIENT, kernel)
    b_rect = cv2.dilate(b_rect,kernel,iterations = 3)

    cont = 0
    cnt, _ = cv2.findContours(b_rect, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cnt:
        perim = cv2.arcLength(c, True)
        if perim > 200:
          cont += 1
          x,y,w,h = cv2.boundingRect(c)
          cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)

    plt.imshow(img)
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.show()

    if 'c10' in aux:
      print(aux[0:3], cont)
    else: 
      print(aux[0:2], cont)

  #======================================================
  #Conta número de linhas escritas
  elif sys.argv[1] == '-l':
    #Remove ruidos
    bin_img = cv2.medianBlur(bin_img,5)
    
    #Corrige angulo de rotação do texto
    angle, rotated = correct_skew(bin_img)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    rotated = cv2.morphologyEx(rotated, cv2.MORPH_GRADIENT, kernel)
    rotated = cv2.dilate(rotated,kernel,iterations = 2)

    #Conta o número de linhas
    cont = 0
    i = 0 
    cnt, hierarchy = cv2.findContours(rotated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    hier = hierarchy[0]

    while hier[i][0] != -1: #Next existe na hierarquia
      cont += 1 #Nova Linha
      _,y1,_,h1 = cv2.boundingRect(cnt[i])
      i = hier[i][0] # i recebe o next na hierarquia
      while hier[i][0] != -1:
        _,y2,_,h2 = cv2.boundingRect(cnt[i])
        #Se a distancia das linhas dos dois for grande o suficiente, conta nova linha
        if abs(y2 - y1) > 100:
          break
        else:
          i = hier[i][0]

    #Imprime os resultados
    if 'c10' in aux:
      print(aux[0:3],aux[6:8],cont)
      if cont == int(aux[6:8]):
        acertos = acertos + 1
    else: 
      print(aux[0:2],aux[5:7],cont)
      if cont == int(aux[5:7]):
        acertos = acertos + 1

if sys.argv[1] == '-l':
  print('Cartas corretas:',acertos,'de 20')

else:
  print('Programa encerrado, utilize o argumento -l ou -w')
