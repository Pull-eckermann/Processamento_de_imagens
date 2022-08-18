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
if sys.argv[1] == '-l':
  for aux in os.listdir('.'):      #Itera sobre as imagens do diretório especificado
    if not(aux.endswith(".jpg")):      #Se não for imagem.jpg pula pra próxima iteração
      continue
    img = cv2.imread(aux, 0)
    
    _, bin_img = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    bin_img = cv2.medianBlur(bin_img,5)

    #Tentativa de rotação automática https://pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
    coords = list()
    h, l = bin_img.shape
    for i in range(1,h):
      for x in range(1,l):
        if bin_img(h,l) == 255:
          coords.append((h,l))
          break
      break
    for i in range(h,1):
      for x in range(1,l):
        if bin_img[h,l] == 255:
          coords.append((h,l))
          break
      break
    for i in range(1,h):
      for x in range(l,1):
        if bin_img[h,l] == 255:
          coords.append((h,l))
          break
      break
    for i in range(h,l):
      for x in range(l,1):
        if bin_img[h,l] == 255:
          coords.append((h,l))
          break
      break
    
    
    #coords = np.column_stack(np.where(bin_img > 0))
    _, _ ,angle = cv2.minAreaRect(coords)
    
    if angle < 45:
      (h, w) = bin_img.shape[:2]
      center = (w // 2, h // 2)
      M = cv2.getRotationMatrix2D(center, angle, 1)
      bin_img = cv2.warpAffine(bin_img, M, (w, h))
    print(angle)

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
    bin_img = cv2.medianBlur(bin_img,5)
    
    kernel = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=np.uint8)
    bin_img = cv2.dilate(bin_img,kernel,iterations = 20)

    plt.imshow(bin_img, 'gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.show()

    cont = 0  
    cnt,_ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnt:
        perim = cv2.arcLength(c, True)
        if perim > 500:
          cont = cont + 1
    
    print(aux[0:2],aux[5:7],cont)
    if cont == int(aux[5:7]):
      acertos = acertos + 1

print('Cartas corretas:',acertos,'de 10')
