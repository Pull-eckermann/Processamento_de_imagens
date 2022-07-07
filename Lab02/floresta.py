import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt

#Confere se o programa foi executado com o número certo de argumentos
if len(sys.argv) != 3:
  print("ERRO DE SINTAXE: python3 floresta.py <IMG ENTRADA> <IMG SAIDA>")
  exit()
img = cv2.imread(sys.argv[1])
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

limitador1 = (60, 200, 200)
limitador2 = (80, 255, 100)
mask = cv2.inRange(img_hsv, limitador1, limitador2)
result = cv2.bitwise_and(img, img, mask = mask)

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors


r, g, b = cv2.split(img)
fig = plt.figure()
axis = fig.add_subplot(1, 1, 1, projection="3d")
pixel_colors = img.reshape((np.shape(img)[0]*np.shape(img)[1], 3))
norm = colors.Normalize(vmin=-1.,vmax=1.)
norm.autoscale(pixel_colors)
pixel_colors = norm(pixel_colors).tolist()
axis.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=pixel_colors, marker=".")
axis.set_xlabel("Red")
axis.set_ylabel("Green")
axis.set_zlabel("Blue")
plt.show()


h, s, v = cv2.split(img_hsv)
fig = plt.figure()
axis = fig.add_subplot(1, 1, 1, projection="3d")

axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker=".")
axis.set_xlabel("Hue")
axis.set_ylabel("Saturation")
axis.set_zlabel("Value")
plt.show()

"""
plt.subplot(1, 2, 1)
plt.imshow(mask, cmap="gray")
plt.subplot(1, 2, 2)
plt.imshow(result)
plt.show()
"""
