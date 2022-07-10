import cv2
import sys
import numpy as np

#Confere se o programa foi executado com o número certo de argumentos
if len(sys.argv) != 3:
  print("ERRO DE SINTAXE: python3 floresta.py <IMG ENTRADA> <IMG SAIDA>")
  exit(0)

img = cv2.imread(sys.argv[1])
img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)       #Converte de imagem BGR para HSV

h, s, v = cv2.split(img_hsv)                        #Separa os 3 canais e transforma em array
h, s, v = h.flatten(), s.flatten(), v.flatten()

h_med = int(sum(h) / len(h))                        #Calcula média do canal hue, para definir a cor dominante

#Canal hue limitado entre +30 e -30 e demais pelo max e mínimo
limitador1 = (h_med-30, int(min(s)), int(min(v)))
limitador2 = (h_med+30, int(max(s)), int(max(v)))

mask = cv2.inRange(img_hsv, limitador1, limitador2)
result = cv2.bitwise_and(img, img, mask = mask)     #And bit a bit aplicando a máscara

#Escreve o resultado no arquivo especificado na entrada
cv2.imwrite(sys.argv[2], result)

