import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt

#Confere se o programa foi executado com o número certo de argumentos
if len(sys.argv) != 3:
  print("ERRO DE SINTAXE: python3 floresta.py <IMG ENTRADA> <IMG SAIDA>")
  exit()

img = cv2.imread(sys.argv[1])
img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

r, g, b = cv2.split(img_rgb)
r, g, b = r.flatten(), g.flatten(), b.flatten()

r_med = int(sum(r) / len(r))
g_med = int(sum(g) / len(g))
b_med = int(sum(b) / len(b))

limitador1 = (r_med-40,g_med-40,b_med-40)
limitador2 = (r_med+40,g_med+40,b_med+40)

mask = cv2.inRange(img, limitador1, limitador2)
result = cv2.bitwise_and(img, img, mask = mask)

plt.subplot(1, 2, 1)
plt.imshow(img)
plt.subplot(1, 2, 2)
plt.imshow(result)
plt.show()

