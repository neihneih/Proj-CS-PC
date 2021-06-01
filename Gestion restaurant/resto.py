# Mai 2021
# BINOME : CURRAL Maxime - NGUYEN Hien
# Exécuter sous Linux

import multiprocessing as mp
import random, time
#from multiprocessing import Process, Value, Lock
#from array import array                             # Attention : différent des 'Array' des Process

CLEARSCR = "\x1B[2J\x1B[;H"        #  Clear SCReen

# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible


#Couleurs
CL_WHITE = "\033[01;37m"                  #Blanc
CL_BLACK = "\033[22;30m"                  #Noir



#-------------------------------------------------------------

def effacer_ecran() : 
    print(CLEARSCR,end='')

def efface_ligne_curseur() :
    print("\033[1K",end='')

def curseur_invisible() :
    print(CURSOFF,end='')

def curseur_visible() : 
    print(CURSON,end='')

def move_to(ligne, colonne) : 
    print("\033[" + str(ligne) + ";" + str(colonne) + "f",end='')

def couleur_txt(Coul) : 
    print(Coul,end='')



def indice_to_coord(X,nbCol):
    colonne = X % nbCol
    ligne = X // nbCol
    return [ligne, colonne]


def changer(liste, elem1, elem2):
    for i in range(len(liste)//2):
        if liste[2*i] == -1:
            liste[2*i] = elem1
            liste[2*i+1] = elem2
            return liste
    return liste


def prendre(liste):
    for i in range(len(liste)//2):
        if liste[2*i] != -1:
            idx = liste[2*i]
            menu = liste[2*i+1]
            liste[2*i] = -1
            liste[2*i+1] = -1
            return [idx, menu]
    return [-1, -1]


def listePleine(liste):
    for i in range(len(liste)//2):
        if liste[2*i] == -1:
            return False
    return True


def horloge(a,resto_ouvert,mutexResto, ligneinfo):
    heureDepart = 9
    minuteDepart = 00
    heure = "09"
    minute = "00"

    while True:
        if heureDepart < 10:
            heure = "0"+str(heureDepart)

        else:
            heure = str(heureDepart)

        if minuteDepart < 10:
            minute = "0"+str(minuteDepart)

        else:
            minute = str(minuteDepart)

        move_to(1, 10)
        print(heure,":",minute)
        minuteDepart +=1

        if minuteDepart == 60:
            minuteDepart = 0
            heureDepart += 1

        if heureDepart == 24:
            heureDepart = 0

        time.sleep(0.1)
        mutexResto.acquire()

        if int(heure) >= 8 and int(heure)<22:
            resto_ouvert.value = 1
            move_to(ligneinfo+1, 40)
            print("O U V E R T")

        else:
            resto_ouvert.value = 0
            move_to(ligneinfo+1, 40)
            print("F E R M E  ")

        mutexResto.release()


def processus_client(resto_ouvert,liste, mutex_commandes):
    time.sleep(2)

    while True:
        while resto_ouvert.value == 1:
            mutex_commandes.acquire()
            listeFull = listePleine(liste)

            if not listeFull:
                liste = changer(liste, random.randint(1000000,9000000), random.randint(0,25))

            mutex_commandes.release()

            time.sleep(random.randint(2,10)*0.1)


def processus_serveur(resto_ouvert,id_serveur, mutex_serveurs,mutex_commandes, liste_serveurs,liste_commandesfinies,mutex_finies):
    while True:
        idxServ = id_serveur - 1

        while resto_ouvert.value == 1:

            mutex_finies.acquire()
            liste_commandesfinies[3*idxServ+1] = -1
            liste_commandesfinies[3*idxServ+2] = -1
            mutex_finies.release()

            mutex_commandes.acquire()
            [idx, menu] = prendre(liste_commandes)

            if idx != -1:
                mutex_serveurs.acquire()
                liste_serveurs[3*idxServ+1] = idx
                liste_serveurs[3*idxServ+2] = menu
                mutex_serveurs.release()

            else:
                mutex_serveurs.acquire()
                liste_serveurs[3*idxServ+1] = -1
                liste_serveurs[3*idxServ+2] = -1
                mutex_serveurs.release()

            mutex_commandes.release()

            time.sleep(random.randint(1,id_serveur+3))

            if idx != -1:
                mutex_finies.acquire()
                liste_commandesfinies[3*idxServ+1] = idx
                liste_commandesfinies[3*idxServ+2] = menu
                mutex_finies.release()

            time.sleep(1)

    
def employes(resto_ouvert,liste_commandes, mutex_commandes, liste_serveurs, mutex_serveurs, nbmax_commandes, nb_serveurs,liste_commandesfinies,mutex_finies):
    while True:
#Interface
        for i in range(len(liste_commandes)//(2*nbmax_commandes//5)):
            move_to(i+2*nb_serveurs, 100)
            efface_ligne_curseur()

        for i in range(len(liste_serveurs)//3):
            move_to(i+2, 100)
            efface_ligne_curseur()
            move_to(i+2, 1)
            id_serveur = liste_serveurs[3*i]
            print("Le serveur "+str(id_serveur)+" prepare la commande :")

        for i in range(len(liste_commandesfinies)//3):
            move_to(i+2+20, 100)
            efface_ligne_curseur()
            move_to(i+20+2, 1)
            id_serveur = liste_serveurs[3*i]
            print("Le serveur "+str(id_serveur)+" a donné la commande :")

        time.sleep(1)

        while resto_ouvert.value == 1:
            mutex_commandes.acquire()
            mutex_serveurs.acquire()
            mutex_finies.acquire()

    #COMMANDES
        #Efface le tableau des commande en attente
            for i in range(len(liste_commandes)//(2*nbmax_commandes//5)):
                move_to(i+2*nb_serveurs, 100)
                efface_ligne_curseur()

        #Ecrit le nouveau tableau des commandes en attente
            for i in range(len(liste_commandes)//2):
                if liste_commandes[2*i] != -1:
                    [ligne, colonne] = indice_to_coord(i, 5)
                    move_to(ligne + 2*nb_serveurs, 15*colonne)
                    idClient = liste_commandes[2*i]
                    menu = liste_commandes[2*i+1]
                    print("("+str(idClient)+","+chr(ord('A')+int(menu))+")")

    #SERVEURS
            for i in range(len(liste_serveurs)//3):
                move_to(i+2, 100)
                efface_ligne_curseur()
                move_to(i+2, 1)
                id_serveur = liste_serveurs[3*i]
                print("Le serveur "+str(id_serveur)+" prepare la commande :")

            for i in range(len(liste_serveurs)//3):
                if liste_serveurs[3*i+1] != -1:
                    ligne = i+2
                    id_serveur = liste_serveurs[3*i]
                    idClient = liste_serveurs[3*i+1]
                    menu = liste_serveurs[3*i+2]
                    text = "Le serveur "+str(id_serveur)+" prepare la commande : ("+str(idClient)+","+chr(ord('A')+int(menu))+")"
                    move_to(ligne, 1)
                    print(text)

    #COMMANDES SERVIES
            for i in range(len(liste_commandesfinies)//3):
                move_to(i+2+20, 100)
                efface_ligne_curseur()
                move_to(i+20+2, 1)
                id_serveur = liste_serveurs[3*i]
                print("Le serveur "+str(id_serveur)+" a donné la commande :")

            for i in range(len(liste_commandesfinies)//3):
                if liste_commandesfinies[3*i+1] != -1:
                    ligne = i+2+20
                    id_serveur = liste_commandesfinies[3*i]
                    idClient = liste_commandesfinies[3*i+1]
                    menu = liste_commandesfinies[3*i+2]
                    text = "Le serveur "+str(id_serveur)+" a donné la commande : ("+str(idClient)+","+chr(ord('A')+int(menu))+")"
                    move_to(ligne, 1)
                    print(text)

            mutex_finies.release()
            mutex_commandes.release()
            mutex_serveurs.release()
            time.sleep(0.5)


if __name__ == "__main__" :
    effacer_ecran()
    resto_ouvert = mp.Value('i', 0)
    nbmax_commandes = 50
    liste_commandes = mp.Array('i', [-1 for i in range(2*nbmax_commandes)])
    nb_serveurs = 5
    liste_serveurs = mp.Array('i', [-1 for i in range(3*nb_serveurs)])
    liste_commandesfinies = mp.Array('i', [-1 for i in range(3*nb_serveurs)])

    for i in range(nb_serveurs):
        liste_serveurs[3*i] = i+1
        liste_commandesfinies[3*i] = i+1

    liste_process = []

    mutex_serveurs = mp.Lock()
    mutex_commandes = mp.Lock()
    mutex_finies = mp.Lock()
    mutexResto = mp.Lock()

    #Affichage UI

    move_to(nb_serveurs + 3, 1)
    print("COMMANDES EN ATTENTE :")
    ligneinfo = (nbmax_commandes//5)+nb_serveurs*2+8
    move_to((nbmax_commandes//5)+nb_serveurs*2+8, 1)
    print(" ---------------------------------")
    print(" | Restaurant ouvert de 8h à 22h |")
    print(" ---------------------------------")
    time.sleep(1)
    ProcessHorloge = mp.Process(target = horloge, args=(0,resto_ouvert,mutexResto, ligneinfo))
    liste_process.append(ProcessHorloge)

    for i in range(nb_serveurs):
        i += 1
        p = mp.Process(target=processus_serveur, args=(resto_ouvert,i, mutex_serveurs,mutex_commandes, liste_serveurs,liste_commandesfinies,mutex_finies))
        liste_process.append(p)

    p1 = mp.Process(target=processus_client, args=(resto_ouvert,liste_commandes, mutex_commandes))
    liste_process.append(p1)

    p2 = mp.Process(target=employes, args=(resto_ouvert,liste_commandes, mutex_commandes, liste_serveurs, mutex_serveurs,nbmax_commandes, nb_serveurs,liste_commandesfinies,mutex_finies))
    liste_process.append(p2)


    for p in liste_process:    
        p.start()

    for p in liste_process:    
        p.join()