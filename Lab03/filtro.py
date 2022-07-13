from statistics import median
import numpy as np
import random
import cv2
import sys

def sp_noise(image, prob):
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

def filtro_media(img, mask):
    noise_img = sp_noise(img,float(sys.argv[2]))
    media = cv2.GaussianBlur(noise_img,(mask),0)
    return media

def filtro_mediana(img, mask):
    noise_img = sp_noise(img,float(sys.argv[2]))
    mediana = cv2.medianBlur(noise_img,mask)
    return mediana

def filtro_empilhamento(img, nivel, n):
    noise_img = list()
    for i in range(0,n):
        noise_img[i] = sp_noise(img, nivel)

#Programa principal
if len(sys.argv) != 5:
    print("ERRO DE SINTAXE: python3 filtro.py <IMG ORIGINAL> <NIVEL RUIDO> <FILTRO> <IMG SAIDA")
    exit(0)

mask_media = 5
mask_mediana = 5
n_empilhamento = 6
img = cv2.imread(sys.argv[1],0)

if sys.argv[3] == '0':
    filter_img = filtro_media(img, mask_media)

if sys.argv[3] == '1':
    filter_img = filtro_mediana(img, mask_mediana)

if sys.argv[3] == '2':
    filter_img = filtro_empilhamento(img, float(sys.argv[2]), n_empilhamento)

