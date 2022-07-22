from cv2 import waitKey
import numpy as np
import random
import cv2
import sys
from matplotlib import pyplot as plt

#Programa principal
if len(sys.argv) != 3:
    print("ERRO DE SINTAXE: python3 placa.py <IMG ORIGINAL> <IMG SAIDA>")
    exit(0)

img = cv2.imread(sys.argv[1],0)
clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
img = clahe.apply(img)

#Aplica a transformada de Fourier
fourrier = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
fourrier_shift = np.fft.fftshift(fourrier)
magnitude_spectrum = 20*np.log(cv2.magnitude(fourrier_shift[:,:,0],fourrier_shift[:,:,1]))

i, j = img.shape
correct_i,correct_j = i/2 , j/2
# create a mask first, center square is 1, remaining all zeros
mask = np.zeros((i,j,2),np.uint8)
mask[int(correct_i)-50:int(correct_i)+50, int(correct_j)-50:int(correct_j)+50] = 1
# apply mask and inverse DFT
result = fourrier_shift*mask
invertion = np.fft.ifftshift(result)
img_back = cv2.idft(invertion)
img_back = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])

plt.subplot(131),plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(132),plt.imshow(magnitude_spectrum)
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.subplot(133),plt.imshow(img_back, cmap = 'gray')
plt.title('Result in JET'), plt.xticks([]), plt.yticks([])
plt.show()




#Aplica a equalização do histograma da imagem 
#img = cv2.imread(sys.argv[1],0)
#clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
#img_out = clahe.apply(img_in)

#Aplica filtro da mediana
#img_out = cv2.medianBlur(img_out,mask)

#result = np.hstack((img_in,img_out))    #Stack image side by side
#cv2.imshow('Placa',result)
#k = waitKey(0)
