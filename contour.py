### Silhouette par épicycloïdes

#import
from PIL import Image as im
import numpy as np
import matplotlib.pyplot as plt

#============================================#
# Lecture de l'image - Définition du contour #
#============================================#

#lecture de l'image
img = im.open("gamm.jpg")
pixImg = np.array(img)
nbrColonnes, nbrLignes = img.size

'''
Si il y existe un pixel blanc qui a un voisin non blanc alors il devient un point du contour
'''

#init img du contour
pixContour = np.zeros(pixImg.shape)#img noire
imgContour = im.fromarray(pixContour.astype('uint8'))

#seuil du blanc (au dessus de (seuil,seuil,seuil) c'est du blanc)
seuil = 200

def img_unie(r, v, b, taille = 500):
    """
    affiche une couleur unie selon le code RVB entré
    Entrée : coeffs RVB
    """
    #img sous forme de tableau (array)
    pixImg = np.zeros((taille,taille,3),dtype=int)

    #remplissage
    L = [r, v, b]
    for i,ligne in enumerate(pixImg):
        for j,pix in enumerate(pixImg[i]):
            pixImg[i, j,:] = np.array([r, v, b])
    img = im.fromarray(pixImg.astype('uint8'))
    img.show()


def pix_voisins(pixImg, i, j):
    """
    renvoie un array contenant les pixels voisins du pixels
    de coordonnées (i,j).
    """
    S = np.ones((4,3))
    for k in range(4):
        S[k,:]=255
    #pH coord = (i-1, j)
    if 0<i:
        p1 = pixImg[i-1, j,:]
        S[0,:] = p1
    #pD coord = (i, j+1)
    if j<nbrColonnes-1:
        p2 = pixImg[i, j+1,:]
        S[1,:] = p2
    #pB coord = (i+1, j)
    if i<nbrLignes-1:
        p3 = pixImg[i+1, j,:]
        S[2,:] = p3
    #pG coord = (i, j-1)
    if 0<j:
        p4 = pixImg[i, j-1,:]
        S[3,:] = p4
    return S

def test_blanc(pix, seuil):
    """
    renvoie un booléen selon si le pixel est blanc avec un seuil
    """
    r,v,b = pix
    return (r>=seuil and v>=seuil and b>=seuil)

##contour
k = 0 #compteur de points pris
listeX = []
listeY = []
for i,ligne in enumerate(pixImg):
    for j,pix in enumerate(ligne):
        if test_blanc(pixImg[i, j,:], seuil):
            #voisins
            v = pix_voisins(pixImg, i, j)
            t = 0 #compteur de test
            test = True
            while  t<4 and test:
                voisin = v[t] #on teste le voisin
                if not test_blanc(voisin,seuil):
                    pixContour[i,j,:] = 255
                    listeX.append(j)
                    listeY.append(-i+nbrLignes)#axe y inversé
                    test = False
                    k = k+1
                t = t+1

imgContour = im.fromarray(pixContour.astype('uint8'))
imgContour.show()

plt.plot(listeX, listeY, 'o')
#plt.show()
##création d'un fichier
file = open('points.txt', 'w')
for t in range(k-1):
    x = listeX[t]
    y = listeY[t]
    file.write(str(x)+'\t'+str(y)+'\n')
lastX, lastY = listeX[-1], listeY[-1]
file.write(str(lastX)+'\t'+str(lastY))
file.close()

