import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt

#Confere se o programa foi executado com o número certo de argumentos
if len(sys.argv) != 3:
  print("ERRO DE SINTAXE: python3 floresta.py <IMG ENTRADA> <IMG SAIDA>")
  exit(0)

img = cv2.imread(sys.argv[1])
img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

h, s, v = cv2.split(img_hsv)
h = h.flatten()

h_med = int(sum(h) / len(h))

limitador1 = (h_med-30,0,0)
limitador2 = (h_med+30,255,255)

mask = cv2.inRange(img_hsv, limitador1, limitador2)
result = cv2.bitwise_and(img, img, mask = mask)

plt.subplot(1, 2, 1)
plt.imshow(img_hsv)
plt.subplot(1, 2, 2)
plt.imshow(result)
plt.show()
