import numpy as np
import cv2
import sys
import os
from os import listdir
from matplotlib import pyplot as plt

#Programa principal
if len(sys.argv) != 2:
    print("ERRO DE SINTAXE: python3 cartas.py <ARGUMENTO>")
    exit(0)

if sys.argv[1] == '-l':
  for aux in os.listdir('./tr/'):       #Itera sobre as imagens do diretório especificado
    if not(aux.endswith(".jpg")):      #Se não for imagem.jpg pula pra próxima iteração
      continue
    img = cv2.imread('./tr/'+aux, 0)
    _, bin_img = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
  
    bin_media = cv2.GaussianBlur(bin_img, (21,21), 0)
    kernel = np.ones((5,5),np.uint8)
    bin_img = cv2.dilate(bin_img,kernel,iterations = 3)
    #bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel)

    plt.imshow(bin_img, 'gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.show()



