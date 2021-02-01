##=================##
# Tracé - Animation #
##=================##

import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

#lecture du fichier
file = open('points_tries.txt', 'r')
listeLignes = file.readlines()
file.close()
n = len(listeLignes)
Lx = np.ones(n)
Ly = np.ones(n)
for i,ligne in enumerate(listeLignes):
    x, y = ligne.split('\t')
    Lx[i] = int(x)
    Ly[i] = int(y)

#verif
tau = 2*np.pi
Lt = np.linspace(0,tau,len(Lx))
plt.plot(Lx, Ly, 'o')
#plt.show()


### I / Coefficients de l'analyse de Fourier complexe ###

#nbr de coeffs à calculer pour chaque sens de rotation
k = 100

#initialisation liste des coefficients
ListeA = np.ones(k+1,dtype=complex)

#intégration sur les listes
def integrationTrapeze(L):
    """
    fonction qui renvoie la somme obtenue par la méthode des trapèzes
    """
    pas = 1
    somme = L[0]/2
    for k in range(1,len(L)-1):
        somme = somme + L[0+k*pas]
    somme = somme + L[-1]/2
    return somme*pas

#le coefficient devant exp(i0) n'est pas intéressant, il positionne
#l'origine de la figure. On prendra par défaut l'origine (0,0) comme
#centre du premier cercle.


#rotation trigo
for i in range(k+1):
    #liste de la partie réelle
    Lr = Lx*np.cos(i*Lt)+Ly*np.sin(i*Lt)
    #intégration partie réelle
    Ar = integrationTrapeze(Lr)/tau
    #liste de la partie imaginaire
    Li = Ly*np.cos(i*Lt)-Lx*np.sin(i*Lt)
    #intégration partie imaginaire
    Ai = integrationTrapeze(Li)/tau
    #coefficient complexe et ajout
    A = Ar + 1j*Ai
    ListeA[i] = A

#listes des modules et arguments
LrayonsT = abs(ListeA)/100
LphasesT = np.angle(ListeA)


#rotation horaire
for i in range(k+1):
    #liste de la partie réelle
    Lr = Lx*np.cos(-i*Lt)+Ly*np.sin(-i*Lt)
    #intégration partie réelle
    Ar = integrationTrapeze(Lr)/tau
    #liste de la partie imaginaire
    Li = Ly*np.cos(-i*Lt)-Lx*np.sin(-i*Lt)
    #intégration partie imaginaire
    Ai = integrationTrapeze(Li)/tau
    #coefiicient complexe et ajout
    A = Ar + 1j*Ai
    ListeA[i] = A

#listes des modules et arguments
LrayonsH = abs(ListeA)/100
LphasesH = np.angle(ListeA)

#création d'une liste qui regroupe toutes les données
ListeDonnees = np.zeros((2*k,4))

#sens trigo
for i in range(k):
    #on ne prend pas le premier
    rayon = LrayonsT[i+1]
    phase = LphasesT[i+1]
    #0 pour sens trigo, i+1 = vitesse de rotation
    ListeDonnees[i,:] = rayon, phase, 0, i+1

#sens horaire
for i in range(k):
    rayon = LrayonsH[i+1]
    phase = LphasesH[i+1]
    #1 pour sens horaire
    ListeDonnees[k+i,:] = rayon, phase, 1, i+1

#tri selon rayon, modif du tri rapide pour ListeDonnees
def triRapide(L):
    long = len(L)
    L_inf = []
    L_sup = []
    if long <= 1:
        return L
    else:
        pivot = L[0][0]
        tPivot = L[0]
        for i in range(1, long):
            if L[i][0] >= pivot:
                L_sup.append(L[i])
            else:
                L_inf.append(L[i])
        return triRapide(L_sup)+[tPivot]+triRapide(L_inf)

#tri
ListeDonnees = triRapide(ListeDonnees)

### II / Initialisation des positions des cercles

#fonctions utiles
def cercle(r, nbrPoints = 200):
    """
    renvoie les listes d'un cercle de centre O et de rayon r
    """
    angles = np.linspace(0,2*np.pi,nbrPoints)
    X = r*np.cos(angles)
    Y = r*np.sin(angles)
    return X,Y

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

def indicePhase(angle, nbrPoints = 200):
    """
    renvoie l'indice du point du cercle
    d'argument l'angle donné
    """
    angles = np.linspace(0,2*np.pi,nbrPoints)
    #on prend l'indice du minimum des écarts
    ecarts = abs(angle*np.ones(nbrPoints)-angles)%(2*np.pi)
    return indice_min(ecarts)

#initialisation de la figure d'animation
plt.rcParams['animation.ffmpeg_path'] = 'FFmpeg/ffmpeg.exe' #création d'un mp4
fig = plt.figure(dpi = 150, figsize = (16,9))
#bornes
ax = plt.axes(xlim=(-150, 150), ylim=(-100, 100))
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_aspect('equal')


##Initialisation des listes de construction
#nombre de points par cercle
nbrP = 200

#tableau des points des cercles pour chaque cercle
Lcercles = np.ones((2*k,2,nbrP))
#liste des indices des centres des cercles
LindicePoints = np.ones(2*k, dtype = int)
#matrices des centres des cercles
Lpoints = np.ones((2*k,2))
#listes des line2D pour les cercles, les points et
#la trajectoire du dernier point
LinesCercles = [plt.plot([],[])[0] for t in range(2*k)]
LinesPoints = [plt.plot([],[])[0] for t in range(2*k)]
traj = plt.plot([],[])[0]

#Positionnement sur la figure

'''
On positionne les cercles dans l'ordre de la liste des donnees puisqu'il
faut placer les centres des cercles sur un autre cercle.
'''

#point de départ
x,y = 0,0


for i in range(2*k):
    rayon,phase,sens,n = ListeDonnees[i]
    #listes du cercle
    X,Y = cercle(rayon, nbrP)
    #ajout (pas besoin des les recalculer à chaque image)
    Lcercles[i,0,:] = X
    Lcercles[i,1,:] = Y
    #on le centre sur le point défini en dernier
    X = X+x*np.ones(len(X))
    Y = Y+y*np.ones(len(Y))
    #on détermine les coordonnées du nouveau point
    indice = indicePhase(phase,nbrP)
    #nouveau point
    x = X[indice]
    y = Y[indice]
    #ajout
    Lpoints[i] = x,y
    LindicePoints[i] = indice

#liste du dernier point (on les ajoute au fur et à mesure)
x,y = Lpoints[-1]
xDer = [x]
yDer = [y]


### III / Animation ###

#fonction d'initialisation
def init():

    for cercle in LinesCercles:
        cercle.set_data([],[])
    
    for point in LinesPoints:
        point.set_data([],[])
        
    traj.set_data([],[])

    
    return LinesCercles + LinesPoints + [traj]

#fonction de rafraichissement d'image
def animate(i):
    #suivi
    print("Image",i)

    ##Premier cercle
    #listes du cercle
    X,Y = Lcercles[0]
    #on adapte la line2D
    LinesCercles[0].set_data(X,Y)
    LinesCercles[0].set_color('k')

    #sens et vitesse de rotation
    r,p,sens,n = ListeDonnees[0]
    n = int(n)
    sens = int(sens)

    ##On détermine le nouveau premier point
    #nouvel indice
    if sens==0:
        #sens trigo
        nouvIndice = (LindicePoints[0]+n)%nbrP
    else:
        #sens horaire
        nouvIndice = (LindicePoints[0]-n)%nbrP
    #ajout
    LindicePoints[0] = nouvIndice
    #nouveau point
    x = X[nouvIndice]
    y = Y[nouvIndice]
    #ajout
    Lpoints[0] = x,y
    #on adapte la line2D du point
    LinesPoints[0].set_data(x,y)
    LinesPoints[0].set_marker('o')
    LinesPoints[0].set_color('b')
    LinesPoints[0].set_ms(4)
    
    #autres cercles et points
    for t in range(1,2*k):
        ##Cercle correspondant
        X,Y = Lcercles[t]
        #Positionnement du cercle
        #centre = point précédent
        x,y = Lpoints[t-1]
        #centrage sur ce point
        X = x*np.ones(nbrP)+X
        Y = y*np.ones(nbrP)+Y
        #on adapte la line2D
        LinesCercles[t].set_data(X,Y)
        LinesCercles[t].set_color('k')
        LinesCercles[t].set_lw(2)

        ##Point
        #sens et vitesse de rotation
        r,p,sens,n = ListeDonnees[t]
        sens = int(sens)
        n = int(n)
        #nouvel indice
        if sens==0:
            #sens trigo
            nouvIndice = (LindicePoints[t]+n)%nbrP
        else:
            #sens horaire
            nouvIndice = (LindicePoints[t]-n)%nbrP
        #ajout
        LindicePoints[t] = nouvIndice
        #nouveau point
        x = X[nouvIndice]
        y = Y[nouvIndice]
        #ajout
        Lpoints[t] = x,y
        #on adapte la line2D du point
        LinesPoints[t].set_data(x,y)
        LinesPoints[t].set_marker('o')
        LinesPoints[t].set_color('b')
        LinesPoints[t].set_ms(5)

    #listes du dernier point
    xDer.append(x)
    yDer.append(y)
    #on adapte la line2D de la trajectoire
    traj.set_data(xDer,yDer)
    traj.set_ls('-')
    traj.set_color('r')
    traj.set_lw(5)
    
    return LinesCercles + LinesPoints + [traj]


anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(X), interval=16,
                               blit=True, repeat = True)

writer = animation.FFMpegWriter(fps=60, bitrate=4000)
anim.save("dessin_croix_"+str(2*k)+"cercles.mp4", writer = writer)
