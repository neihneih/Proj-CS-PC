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


def indice_to_coord(pI,nb_colonnes):
    colonne = pI % nb_colonnes
    ligne = pI // nb_colonnes
    return [ligne, colonne]


def changer(liste, pA, pB):
    for i in range(len(liste)//2):
        if liste[2*i] == -1:
            liste[2*i] = pA
            liste[2*i+1] = pB
            return liste
    return liste


def prendre(liste):
    for i in range(len(liste)//2):
        if liste[2*i] != -1:
            pX = liste[2*i]
            menu = liste[2*i + 1]
            liste[2*i] = -1
            liste[2*i + 1] = -1
            return [pX, menu]
    return [-1, -1]


def listePleine(liste):
    for i in range(len(liste)//2):
        if liste[2*i] == -1:
            return False
    return True


def horloge(a,ouverture,mutex_resto, label_info):
    heure_depart = 7
    minute_depart = 45
    heure = "07"
    minute = "45"

    while True:
        if heure_depart < 10:
            heure = "0" + str(heure_depart)

        else:
            heure = str(heure_depart)

        if minute_depart < 10:
            minute = "0" + str(minute_depart)

        else:
            minute = str(minute_depart)

        move_to(1, 10)
        print("Il est ", heure, "h", minute)

        minute_depart += 1

        if minute_depart == 60:
            minute_depart = 0
            heure_depart += 1

        if heure_depart == 24:
            heure_depart = 0

        time.sleep(0.1)

        mutex_resto.acquire()
        if int(heure) >= 8 and int(heure) < 22:
            ouverture.value = 1

            move_to(label_info + 1, 40)
            print("NOUS SOMMES OUVERTS")

        else:
            ouverture.value = 0

            move_to(label_info + 1, 40)
            print("NOUS SOMMES FERMES ")
        mutex_resto.release()


def processus_client(ouverture,liste, mutex_commandes):
    time.sleep(2)

    while True:
        while ouverture.value == 1:

            mutex_commandes.acquire()
            listeFull = listePleine(liste)

            if not listeFull:
                liste = changer(liste, random.randint(1000000,9000000), random.randint(0,25))
            mutex_commandes.release()

            time.sleep(random.randint(2,10)*0.2)


def processus_serveur(ouverture,id_serveur, mutex_serveurs,mutex_commandes, liste_serveurs,liste_commandesfinies,mutex_finies):
    while True:
        idxServ = id_serveur - 1

        while ouverture.value == 1:

            mutex_finies.acquire()
            liste_commandesfinies[3*idxServ+1] = -1
            liste_commandesfinies[3*idxServ+2] = -1
            mutex_finies.release()

            mutex_commandes.acquire()
            [pX, menu] = prendre(liste_commandes)

            if pX != -1:
                mutex_serveurs.acquire()
                liste_serveurs[3*idxServ+1] = pX
                liste_serveurs[3*idxServ+2] = menu
                mutex_serveurs.release()

            else:
                mutex_serveurs.acquire()
                liste_serveurs[3*idxServ+1] = -1
                liste_serveurs[3*idxServ+2] = -1
                mutex_serveurs.release()
            mutex_commandes.release()


            time.sleep(random.randint(1,id_serveur+3))

            if pX != -1:
                mutex_finies.acquire()
                liste_commandesfinies[3*idxServ+1] = pX
                liste_commandesfinies[3*idxServ+2] = menu
                mutex_finies.release()

            time.sleep(1)

    
def major_dHomme(ouverture,liste_commandes, mutex_commandes, liste_serveurs, mutex_serveurs, nbmax_commandes, nb_serveurs,liste_commandesfinies,mutex_finies):
    
    while True:
        for i in range(len(liste_commandes)//(2*nbmax_commandes//5)):
            move_to(i + 2*nb_serveurs, 100)
            efface_ligne_curseur()

        for i in range(len(liste_serveurs)//3):
            move_to(i + 2, 100)
            efface_ligne_curseur()

            move_to(i + 2, 1)
            id_serveur = liste_serveurs[3*i]
            print("Le serveur " + str(id_serveur) + " prepare la commande :")

        for i in range(len(liste_commandesfinies)//3):
            move_to(i + 2 + 20, 100)
            efface_ligne_curseur()

            move_to(i + 20 + 2, 1)
            id_serveur = liste_serveurs[3*i]
            print("Le serveur " + str(id_serveur) + " a servi la commande :")

        time.sleep(1)

        while ouverture.value == 1:
            mutex_commandes.acquire()
            mutex_serveurs.acquire()
            mutex_finies.acquire()


            # PARTIE AFFICHAGE DES COMMANDES
            # RESET tableau de commandes 
            for i in range(len(liste_commandes)//(2*nbmax_commandes//5)):
                move_to(i + 2*nb_serveurs, 100)
                efface_ligne_curseur()


            # Ecriture du tableau de commandes 
            for i in range(len(liste_commandes)//2):
                if liste_commandes[2*i] != -1:
                    [ligne, colonne] = indice_to_coord(i, 5)
                    
                    move_to(ligne + 2*nb_serveurs, 15*colonne)
                    idClient = liste_commandes[2*i]
                    menu = liste_commandes[2*i + 1]
                    print("(" + str(idClient) + "," + chr(ord('A') + int(menu)) + ")")


            # PARTIE AFFICHAGE DES SERVEURS
            for i in range(len(liste_serveurs)//3):

                move_to(i + 2, 100)
                efface_ligne_curseur()
                
                move_to(i + 2, 1)
                id_serveur = liste_serveurs[3*i]
                print("Le serveur " + str(id_serveur) + " prepare la commande :")

            for i in range(len(liste_serveurs)//3):
                if liste_serveurs[3*i + 1] != -1:
                    ligne = i + 2
                    id_serveur = liste_serveurs[3*i]
                    idClient = liste_serveurs[3*i + 1]
                    menu = liste_serveurs[3*i + 2]
                    text = "Le serveur " + str(id_serveur) + " prepare la commande : (" + str(idClient) + "," + chr(ord('A') + int(menu)) + ")"
                    
                    move_to(ligne, 1)
                    print(text)


            # PARTIE AFFICHAGE DES COMMANDES SERVIES
            for i in range(len(liste_commandesfinies)//3):
                move_to(i + 2 + 20, 100)
                efface_ligne_curseur()

                move_to(i + 20 + 2, 1)
                id_serveur = liste_serveurs[3*i]
                print("Le serveur " + str(id_serveur) + " a servi la commande :")

            for i in range(len(liste_commandesfinies)//3):
                if liste_commandesfinies[3*i + 1] != -1:
                    ligne = i + 2 + 20
                    id_serveur = liste_commandesfinies[3*i]
                    idClient = liste_commandesfinies[3*i + 1]
                    menu = liste_commandesfinies[3*i + 2]
                    text = "Le serveur " + str(id_serveur) + " a servi la commande : (" + str(idClient) + "," + chr(ord('A') + int(menu)) + ")"
                    move_to(ligne, 1)
                    print(text)

            mutex_finies.release()
            mutex_commandes.release()
            mutex_serveurs.release()
            time.sleep(0.5)


if __name__ == "__main__" :
    effacer_ecran()
    ouverture = mp.Value('i', 0)
    nbmax_commandes = 50
    liste_commandes = mp.Array('i', [-1 for i in range(2*nbmax_commandes)])
    nb_serveurs = 5
    liste_serveurs = mp.Array('i', [-1 for i in range(3*nb_serveurs)])
    liste_commandesfinies = mp.Array('i', [-1 for i in range(3*nb_serveurs)])

    for i in range(nb_serveurs):
        liste_serveurs[3*i] = i + 1
        liste_commandesfinies[3*i] = i + 1

    liste_process = []

    mutex_serveurs = mp.Lock()
    mutex_commandes = mp.Lock()
    mutex_finies = mp.Lock()
    mutex_resto = mp.Lock()

    #Affichage UI

    move_to(nb_serveurs + 3, 1)
    print("COMMANDES EN ATTENTE :")
    label_info = (nbmax_commandes//5) + nb_serveurs*2 + 8

    move_to((nbmax_commandes//5) + nb_serveurs*2 + 8, 1)
    print(" ====================== ")
    print(" | Service de 8h à 22h |")
    print(" ====================== ")

    time.sleep(1)

    ProcessHorloge = mp.Process(target = horloge, args = (0,ouverture,mutex_resto, label_info))
    liste_process.append(ProcessHorloge)

    for i in range(nb_serveurs):
        i += 1
        p_serv = mp.Process(target = processus_serveur, args = (ouverture,i, mutex_serveurs,mutex_commandes, liste_serveurs,liste_commandesfinies,mutex_finies))
        liste_process.append(p_serv)

    p_client = mp.Process(target = processus_client, args = (ouverture,liste_commandes, mutex_commandes))
    liste_process.append(p_client)

    p_affichage = mp.Process(target = major_dHomme, args = (ouverture,liste_commandes, mutex_commandes, liste_serveurs, mutex_serveurs,nbmax_commandes, nb_serveurs,liste_commandesfinies,mutex_finies))
    liste_process.append(p_affichage)


    for p_serv in liste_process:    
        p_serv.start()

    for p_serv in liste_process:    
        p_serv.join()