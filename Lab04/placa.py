from cv2 import waitKey
import numpy as np
import random
import cv2
import sys

#Programa principal
if len(sys.argv) != 3:
    print("ERRO DE SINTAXE: python3 placa.py <IMG ORIGINAL> <IMG SAIDA>")
    exit(0)

mask = 3

img_in = cv2.imread(sys.argv[1],0)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
img_out = clahe.apply(img_in)

img_out = cv2.medianBlur(img_out,mask)

result = np.hstack((img_in,img_out))    #Stack image side by side
cv2.imshow('Placa',result)
k = waitKey(0)
