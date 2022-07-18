from multiprocessing.connection import wait
from statistics import median
import numpy as np
import random
import cv2
import sys

#Função que adiciona ruído aleatório à imagem
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

#FIltragem pela média
def filtro_media(img, mask):
    noise_img = sp_noise(img,float(sys.argv[2]))        #Gera imagem ruidosa
    media = cv2.GaussianBlur(noise_img,(mask,mask),0)   #Aplica filtro por média
    return media

#FIltragem pela mediana
def filtro_mediana(img, mask):
    noise_img = sp_noise(img,float(sys.argv[2]))        #Gera imagem ruidosa
    mediana = cv2.medianBlur(noise_img,mask)            #Aplica filtro mediana
    return mediana

#Filtro de empilhamento de imagens
def filtro_empilhamento(img, nivel, n):
    img_emp = sp_noise(img, nivel)
    img_emp = cv2.divide(img_emp, n)
    #Gera n imagens e soma pixel a pixel, guardando em img_emp  
    for i in range(0,n-1):
        noise_img = sp_noise(img, nivel)
        noise_img = cv2.divide(noise_img, n)            #Divide pelo número de imagens e soma
        img_emp = cv2.add(noise_img,img_emp)            #a fim de evitar overflow

    return img_emp

#Programa principal
if len(sys.argv) != 5:
    print("ERRO DE SINTAXE: python3 filtro.py <IMG ORIGINAL> <NIVEL RUIDO> <FILTRO> <IMG SAIDA>")
    exit(0)

mask_media = 13                 #Tamanho da máscara definida para media
mask_mediana = 5                    #Mascara para mediana
n_empilhamento = 20                #Número de imagens a empilhar
img = cv2.imread(sys.argv[1],0)

if sys.argv[3] == '0':
    filter_img = filtro_media(img, mask_media)

if sys.argv[3] == '1':
    filter_img = filtro_mediana(img, mask_mediana)

if sys.argv[3] == '2':
    filter_img = filtro_empilhamento(img, float(sys.argv[2]), n_empilhamento)

print("PSNR comparation:", cv2.PSNR(img, filter_img))   #Taxa de semelhança entre imagem original e filtrada
cv2.imwrite(sys.argv[4], filter_img)

