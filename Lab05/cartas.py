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
  for aux in os.listdir('.'):      #Itera sobre as imagens do diretório especificado
    if not(aux.endswith(".jpg")):      #Se não for imagem.jpg pula pra próxima iteração
      continue
    img = cv2.imread(aux, 0)
    _, bin_img = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    bin_img = cv2.medianBlur(bin_img,5)
    kernel = np.array([[0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [1, 1, 1, 1, 1],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0]], dtype=np.uint8)
    h_dilate = cv2.dilate(bin_img,kernel,iterations = 10)
    kernel = np.array([[0, 0, 1, 0, 0],
                       [0, 0, 1, 0, 0],
                       [0, 0, 1, 0, 0],
                       [0, 0, 1, 0, 0],
                       [0, 0, 1, 0, 0]], dtype=np.uint8)
    v_dilate = cv2.dilate(bin_img,kernel,iterations = 10)

    bin_img = cv2.bitwise_and(h_dilate,v_dilate)
    bin_img = cv2.medianBlur(bin_img,9)

    kernel = np.array([[0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [1, 1, 1, 1, 1],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0]], dtype=np.uint8)

    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel)
    bin_img = cv2.dilate(bin_img,kernel,iterations = 20)

    cnt,_ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(len(cnt))

    plt.imshow(bin_img, 'gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.show()
