import numpy as np
import cv2
import sys
import os
from matplotlib import pyplot as plt

#Programa principal
if len(sys.argv) != 2:
    print("ERRO DE SINTAXE: python3 cartas.py <ARGUMENTO>")
    exit(0)

acertos = 0
for aux in os.listdir('.'):      #Itera sobre as imagens do diretório especificado
  if not(aux.endswith(".jpg")):      #Se não for imagem.jpg pula pra próxima iteração
    continue
  img = cv2.imread(aux, 0)
  
  _, bin_img = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
  bin_img = cv2.medianBlur(bin_img,5)

  kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
  b_rect = cv2.dilate(bin_img,kernel,iterations = 10)

  cont = 0
  cnt, _ = cv2.findContours(b_rect, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  for c in cnt:
      perim = cv2.arcLength(c, True)
      if perim > 100:
        cont += 1
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,0),2)
  print(cont)

  plt.imshow(img, 'gray')
  plt.title('Input Image'), plt.xticks([]), plt.yticks([])
  plt.show()
'''
  #Rotação automática https://pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
  coords = np.column_stack(np.where(bin_img > 0))
  _, _, angle = cv2.minAreaRect(coords)

  angle = angle *(-1)
  if angle < -45:
    angle = -(90 + angle)
  else:
    angle = -angle

  h, w = bin_img.shape
  center = (w // 2, h // 2)
  M = cv2.getRotationMatrix2D(center, angle, 1.0)
  bin_img = cv2.warpAffine(bin_img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

  print(angle)
  plt.imshow(bin_img, 'gray')
  plt.title('Input Image'), plt.xticks([]), plt.yticks([])
  plt.show()

  cont = 0  
  cnt,_ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  for c in cnt:
      perim = cv2.arcLength(c, True)
      if perim > 500:
        cont = cont + 1

  if 'c10' in aux:
    print(aux[0:3],aux[6:8],cont)
    if cont == int(aux[6:8]):
      acertos = acertos + 1
  else: 
    print(aux[0:2],aux[5:7],cont)
    if cont == int(aux[5:7]):
      acertos = acertos + 1

print('Cartas corretas:',acertos,'de 10')
'''


# kernel = np.array([[0, 0, 0, 0, 0],
#                   [0, 0, 0, 0, 0],
#                   [1, 1, 1, 1, 1],
#                   [0, 0, 0, 0, 0],
#                   [0, 0, 0, 0, 0]], dtype=np.uint8)
#h_dilate = cv2.dilate(bin_img,kernel,iterations = 20)
#kernel = np.array([[0, 0, 1, 0, 0],
#                   [0, 0, 1, 0, 0],
#                   [0, 0, 1, 0, 0],
#                   [0, 0, 1, 0, 0],
#                   [0, 0, 1, 0, 0]], dtype=np.uint8)
#v_dilate = cv2.dilate(bin_img,kernel,iterations = 10)
#bin_img = cv2.bitwise_and(h_dilate,v_dilate)
#kernel = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=np.uint8)
#bin_img = cv2.dilate(bin_img,kernel,iterations = 20)
    
#kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
#b_rect = cv2.dilate(bin_img,kernel,iterations = 5)
