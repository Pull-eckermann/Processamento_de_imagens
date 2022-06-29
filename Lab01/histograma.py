from cgi import test
import cv2
from matplotlib import pyplot as plt
import os
from os import listdir

#Comparação usando HISTCMP_CORREL
aux = 0

for teste in os.listdir("."):
    if not(teste.endswith(".bmp")):                                 #Se não for imagem.bmp pula pra próxima iteração
        continue
    img1 = cv2.imread(teste)
    hist1 = cv2.calcHist([img1], [2], None, [256], [0,256])
    for comp in os.listdir("."):
        if (not(comp.endswith(".bmp")) or (comp == teste)):         #Se não for imagem.bmp ou se a imagem teste
            continue                                                #for a mesma da comparação, pula pra próxima iteração
        img2 = cv2.imread(comp)
        hist2 = cv2.calcHist([img2], [2], None, [256], [0,256])
        result = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        if result > aux:
            aux = result

"""
results_CORREL = list()
results_CHISQR = list()
results_INTERSECT = list()
results_BHATTACHARYYA = list()

img1 = cv2.imread('b2.bmp')
img2 = cv2.imread('b1.bmp')

hist1 = cv2.calcHist([img1], [1], None, [256], [0,256])
hist2 = cv2.calcHist([img2], [1], None, [256], [0,256])

sc = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
print(sc)

cv2.imshow("Display window", img1)
k = cv2.waitKey(0)

plt.plot (hist1, color = 'r')
plt.xlim ([0,256])
plt.show ()
"""
