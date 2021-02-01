### Tri des points
import numpy as np
import matplotlib.pyplot as plt

#lecture du fichier
file = open('points.txt', 'r')
listeLignes = file.readlines()
file.close()
n = len(listeLignes)
listeX = np.ones(n)
listeY = np.ones(n)
for i,ligne in enumerate(listeLignes):
    x, y = ligne.split('\t')
    listeX[i] = int(x)
    listeY[i] = int(y)

#verif
plt.plot(listeX, listeY, 'o')
#plt.show()



#on met dans l'ordre les points selon la distance qui les sépare


def distance(x1, y1, x2, y2):
    """
    renvoie la distance entre les points 1 et 2
    """
    return ((x2-x1)**2+(y2-y1)**2)**(1/2)

def indice_min(L):
    """
    renvoie l'indice du minimum d'une liste
    """
    Min = L[0]
    s = 0
    for i,elem in enumerate(L):
        if elem < Min:
            Min = elem
            s = i
    return s

#on ajoute le tuple des coord du point à une pile lorsqu'il est trié
#init listes triées
Lx_triee = np.ones(n, dtype = int)
Ly_triee = np.ones(n, dtype = int)
Pile_points_tries = []
Pile_points_pas_tries = []
Pile_inter = [] #pile de transition


#premier point
x, y = listeX[0], listeY[0]
Pile_points_tries.append((x,y))

#on remplit la pile avec les points
for k in range(1,n):
    Pile_points_pas_tries.append((listeX[k],listeY[k]))

#tri
for i in range(1,n):
    #init liste des distances
    listeDistances = np.zeros(n-i)
    k = 0 #compteur
    #on calcule toutes les distances
    while Pile_points_pas_tries != []:
        X, Y = Pile_points_pas_tries.pop()
        dist = distance(x,y,X,Y)
        #on ajoute la distance
        listeDistances[k] = dist
        #on ajoute le point à la pile de transition
        Pile_inter.append((X,Y))
        k = k+1
    #indice du minimum dans la liste des distances
    indMin = indice_min(listeDistances)

    ##ajout du point correspondant à la pile des points triés
    p = 0 #compteur
    while n-i-p-1 != indMin:#tant qu'on est pas au bon indice
        #on enleve le point qui n'est pas voulu
        point = Pile_inter.pop()
        #on le remet dans la pile des points non triés
        Pile_points_pas_tries.append(point)
        p = p+1
    #point recherché, on l'ajoute à la pile des points triés
    nouvPoint = Pile_inter.pop()
    x,y = nouvPoint#pour calculer les prochaines distances
    Pile_points_tries.append(nouvPoint)
    #on rajoute les points restants à la liste des points non triés
    while Pile_inter!=[]:
        point = Pile_inter.pop()
        Pile_points_pas_tries.append(point)

#points à enlever selon l'image
points_enleves = 1

#listes des coordonnées des points
Lx = np.ones(n-points_enleves, dtype = int)
Ly = np.ones(n-points_enleves, dtype = int)
Lt = np.linspace(0,2*np.pi,n-points_enleves)

for i,point in enumerate(Pile_points_tries[:-points_enleves]):
    x,y = point
    Lx[i] = x
    Ly[i] = y

plt.figure()
plt.plot(Lx, Ly)
plt.axis('equal')
plt.savefig('contour')
#plt.show()

plt.plot(Lt,Lx, label = 'x(t)')
plt.plot(Lt,Ly, label = 'y(t)')
plt.legend(loc='best')
#plt.savefig('fonctions_coord')
#plt.show()

##création d'un fichier
file = open('points_tries.txt', 'w')
for k in range(n-1-points_enleves):
    x,y = Lx[k], Ly[k]
    file.write(str(x)+'\t'+str(y)+'\n')
xLast = Lx[-1]
yLast = Ly[-1]
file.write(str(xLast)+'\t'+str(yLast))
file.close()
