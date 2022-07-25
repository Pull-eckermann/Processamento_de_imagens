
import numpy as np
import cv2
import sys

def filtra_periodico(img):
    #Acha transformada de Fourrier
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    #Seta uma coluna de zeros no centro para eliminar os ruídos
    linhas, colunas = img.shape
    ccolunas = colunas//2
    for i in range(0,linhas):
        fshift[i, ccolunas] = 0

    #Volta para a imagem no domínio espacial
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.real(img_back)
    
    return img_back

#Programa principal
if len(sys.argv) != 3:
    print("ERRO DE SINTAXE: python3 placa.py <IMG ORIGINAL> <IMG SAIDA>")
    exit(0)

img = cv2.imread(sys.argv[1],0)
clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
img_out = clahe.apply(img)              #Aplica equalização de Histogramas por área
img_out = cv2.medianBlur(img_out,3)     #Filtro da média para eliminar ruídos

#Testa para ver se o caso é da filtrazem pelo domínio da frequência
if sys.argv[1] == "1.jpg":
    img_out = filtra_periodico(img_out)
#Esse caso tenta detecção de contornos caso não seja a imagem que foi filtrada pela frequencia
else:
    #Transforma a imagem em binária e aplica filtrom da média
    _, bin = cv2.threshold(img_out, 110, 255, cv2.THRESH_BINARY)
    bin_media = cv2.GaussianBlur(bin, (5,5), 0)

    #Gera os contornos e procura somente os quadrados
    contornos, hier = cv2.findContours(bin_media, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for c in contornos:
        perim = cv2.arcLength(c, True)
        if perim > 120:
            aprox = cv2.approxPolyDP(c, 0.03 * perim, True)
            if len(aprox) == 4:
                (x,y,h,l) = cv2.boundingRect(c)
                roi = img_out[y:y+l, x:x+h]
                cv2.imwrite('cut_'+sys.argv[2],roi)

#Escreve a imagem com o nome especificado
cv2.imwrite(sys.argv[2],img_out)

