import cv2
from matplotlib import pyplot as plt
import os
from os import listdir

#Inicializa as listas usadas para classificar as imagens
bart = list()
homer = list()
lisa = list()
margie = list()
megie = list()

#Função que calcula taxa de acerto de cada método de comparação
def calcula_acerto():
    acertos = 0
    for x in bart:
        if x[0] == "b":
            acertos += 1
    for x in homer:
        if x[0] == "h":
            acertos += 1
    for x in lisa:
        if x[0] == "l":
            acertos += 1
    for x in margie:
        if "m" == x[0] and x[1] != "g":
            acertos += 1
    for x in megie:
        if x[1] == "g":
            acertos += 1
    #retorna a quantidade de acertos em relação ao total de imagens
    return acertos/25

#Verifica pelo nome da imagem, a qual classe pertence teste
def verifica_classe(img_aux, teste):
    if "b" == img_aux[0]:                                           
        bart.append(teste)
    if "h" == img_aux[0]:
        homer.append(teste)
    if "l" == img_aux[0]:
        lisa.append(teste)
    if "m" == img_aux[0] and img_aux[1] != "g":
        margie.append(teste)
    if "g" in img_aux:
        megie.append(teste)

#Limpa as listas para utilização no próximo método
def limpa_listas():
    bart.clear()
    homer.clear()
    lisa.clear()
    margie.clear()
    megie.clear()

#Comparação usando HISTCMP_CORREL
for teste in os.listdir("."):                                       #Le todos os arquivos do diretório corrente
    aux = 0
    if not(teste.endswith(".bmp")):                                 #Se não for imagem.bmp pula pra próxima iteração
        continue
    img1 = cv2.imread(teste)
    hist1 = cv2.calcHist([img1], [2], None, [256], [0,256])
    cv2.normalize(hist1, hist1, 0, 255, cv2.NORM_MINMAX)

    for comp in os.listdir("."):
        if (not(comp.endswith(".bmp")) or (comp == teste)):         #Se não for imagem.bmp ou se a imagem teste
            continue                                                #for a mesma da comparação, pula pra próxima iteração
        img2 = cv2.imread(comp)
        hist2 = cv2.calcHist([img2], [2], None, [256], [0,256])
        cv2.normalize(hist2, hist2, 0, 255, cv2.NORM_MINMAX)
        result = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        if result > aux:                                            #Confere qual o maior resultado das comparações nas iterações
            aux = result
            img_aux = comp                                          #Guarda o nome da imagem com maior semelhança

    #Verifica pelo nome da imagem, a qual classe pertence teste
    verifica_classe(img_aux, teste)

correl_result = calcula_acerto()                                    
print("A taxa de acerto do método CORREL é:",correl_result)
limpa_listas()

#Comparação usando HISTCMP_CHISQR
for teste in os.listdir("."):                                       #Le todos os arquivos do diretório corrente
    aux = 100
    if not(teste.endswith(".bmp")):                                 #Se não for imagem.bmp pula pra próxima iteração
        continue
    img1 = cv2.imread(teste)
    hist1 = cv2.calcHist([img1], [2], None, [256], [0,256])
    cv2.normalize(hist1, hist1, 0, 255, cv2.NORM_MINMAX)

    for comp in os.listdir("."):
        if (not(comp.endswith(".bmp")) or (comp == teste)):         #Se não for imagem.bmp ou se a imagem teste
            continue                                                #for a mesma da comparação, pula pra próxima iteração
        img2 = cv2.imread(comp)
        hist2 = cv2.calcHist([img2], [2], None, [256], [0,256])
        cv2.normalize(hist2, hist2, 0, 255, cv2.NORM_MINMAX)
        result = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)
        if result < aux:                                            #Confere qual o maior resultado das comparações nas iterações
            aux = result
            img_aux = comp                                          #Guarda o nome da imagem com maior semelhança

    #Verifica pelo nome da imagem, a qual classe pertence teste
    verifica_classe(img_aux, teste)

chisqr_result = calcula_acerto()                                    
print("A taxa de acerto do método CHISQR é:",chisqr_result)
limpa_listas()

#Comparação usando HISTCMP_INTERSECT
for teste in os.listdir("."):                                       #Le todos os arquivos do diretório corrente
    aux = 0
    if not(teste.endswith(".bmp")):                                 #Se não for imagem.bmp pula pra próxima iteração
        continue
    img1 = cv2.imread(teste)
    hist1 = cv2.calcHist([img1], [2], None, [256], [0,256])
    cv2.normalize(hist1, hist1, 0, 255, cv2.NORM_MINMAX)

    for comp in os.listdir("."):
        if (not(comp.endswith(".bmp")) or (comp == teste)):         #Se não for imagem.bmp ou se a imagem teste
            continue                                                #for a mesma da comparação, pula pra próxima iteração
        img2 = cv2.imread(comp)
        hist2 = cv2.calcHist([img2], [2], None, [256], [0,256])
        cv2.normalize(hist2, hist2, 0, 255, cv2.NORM_MINMAX)
        result = cv2.compareHist(hist1, hist2, cv2.HISTCMP_INTERSECT)
        if result > aux:                                            #Confere qual o maior resultado das comparações nas iterações
            aux = result
            img_aux = comp                                          #Guarda o nome da imagem com maior semelhança

    #Verifica pelo nome da imagem, a qual classe pertence teste
    verifica_classe(img_aux, teste)

intersect_result = calcula_acerto()                                    
print("A taxa de acerto do método INTERSECT é:",intersect_result)
limpa_listas()

#Comparação usando HISTCMP_BHATTACHARYYA
for teste in os.listdir("."):                                       #Le todos os arquivos do diretório corrente
    aux = 100
    if not(teste.endswith(".bmp")):                                 #Se não for imagem.bmp pula pra próxima iteração
        continue
    img1 = cv2.imread(teste)
    hist1 = cv2.calcHist([img1], [2], None, [256], [0,256])
    cv2.normalize(hist1, hist1, 0, 255, cv2.NORM_MINMAX)

    for comp in os.listdir("."):
        if (not(comp.endswith(".bmp")) or (comp == teste)):         #Se não for imagem.bmp ou se a imagem teste
            continue                                                #for a mesma da comparação, pula pra próxima iteração
        img2 = cv2.imread(comp)
        hist2 = cv2.calcHist([img2], [2], None, [256], [0,256])
        cv2.normalize(hist2, hist2, 0, 255, cv2.NORM_MINMAX)
        result = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
        if result < aux:                                            #Confere qual o maior resultado das comparações nas iterações
            aux = result
            img_aux = comp                                          #Guarda o nome da imagem com maior semelhança

    #Verifica pelo nome da imagem, a qual classe pertence teste
    verifica_classe(img_aux, teste)

BHATTACHARYYA_result = calcula_acerto()                                    
print("A taxa de acerto do método BHATTACHARYYA é:",BHATTACHARYYA_result)
limpa_listas()
