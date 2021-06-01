import multiprocessing as mp
import random, time


        #VARIABLES
#Ecran
CLEARSCR="\x1B[2J\x1B[;H"          #Efface l'ecran

#Curseur
CURSON   = "\x1B[?25h"             #Affiche le curseur
CURSOFF  = "\x1B[?25l"             #Cache le curseur


#Couleurs
CL_WHITE="\033[01;37m"                  #Blanc
CL_BLACK="\033[22;30m"                  #Noir



        #FONCTIONS



#Fonctions affichage
def effacer_ecran() : print(CLEARSCR,end='')
def efface_ligne_curseur() : print("\033[1K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(ligne, colonne) : print("\033[" + str(ligne) + ";" + str(colonne) + "f",end='')
def couleur_txt(Coul) : print(Coul,end='')




def indice_to_coord(X,nbCol):
    colonne = X % nbCol
    ligne = X // nbCol
    return [ligne, colonne]

def afficherTableau(tableau):
    return [tableau[i] for i in range(len(tableau))]

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
    heureDepart = 21
    minuteDepart = 00
    heure = "21"
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

def processClient(resto_ouvert,liste, mutexCommande):
    time.sleep(2)
    while True:

        while resto_ouvert.value == 1:

            mutexCommande.acquire()
            listeFull = listePleine(liste)
            #TEST
            # print(afficherTableau(tableauCommande))
            # print(listeFull)
            if not listeFull:
                liste = changer(liste, random.randint(1000000,9000000), random.randint(0,25))
            mutexCommande.release()
            time.sleep(random.randint(2,10)*0.1)

def processServ(resto_ouvert,idServ, mutexServeurs,mutexCommande, tableauServeurs,tableauCommandeServie,mutexServie):
    while True:
        idxServ = idServ - 1
        while resto_ouvert.value == 1:

            mutexServie.acquire()
            tableauCommandeServie[3*idxServ+1] = -1
            tableauCommandeServie[3*idxServ+2] = -1
            mutexServie.release()

            mutexCommande.acquire()
            [idx, menu] = prendre(tableauCommande)
            if idx != -1:
                mutexServeurs.acquire()
                tableauServeurs[3*idxServ+1] = idx
                tableauServeurs[3*idxServ+2] = menu
                mutexServeurs.release()
            else:
                mutexServeurs.acquire()
                tableauServeurs[3*idxServ+1] = -1
                tableauServeurs[3*idxServ+2] = -1
                mutexServeurs.release()

            mutexCommande.release()
            time.sleep(random.randint(1,idServ+3))

            if idx != -1:
                mutexServie.acquire()
                tableauCommandeServie[3*idxServ+1] = idx
                tableauCommandeServie[3*idxServ+2] = menu
                mutexServie.release()

            time.sleep(1)



    
def Major_dHomme(resto_ouvert,tableauCommande, mutexCommande, tableauServeurs, mutexServeurs, nbCommandeMax, nbServeurs,tableauCommandeServie,mutexServie):
    while True:
#Interface
        for i in range(len(tableauCommande)//(2*nbCommandeMax//5)):
            move_to(i+2*nbServeurs, 100)
            efface_ligne_curseur()

        for i in range(len(tableauServeurs)//3):
            move_to(i+2, 100)
            efface_ligne_curseur()
            move_to(i+2, 1)
            idServ = tableauServeurs[3*i]
            print("Le serveur "+str(idServ)+" prepare la commande :")

        for i in range(len(tableauCommandeServie)//3):
            move_to(i+2+20, 100)
            efface_ligne_curseur()
            move_to(i+20+2, 1)
            idServ = tableauServeurs[3*i]
            print("Le serveur "+str(idServ)+" a donné la commande :")
        time.sleep(1)
        while resto_ouvert.value == 1:
            mutexCommande.acquire()
            mutexServeurs.acquire()
            mutexServie.acquire()
    #COMMANDES
        #Efface le tableau des commande en attente
            for i in range(len(tableauCommande)//(2*nbCommandeMax//5)):
                move_to(i+2*nbServeurs, 100)
                efface_ligne_curseur()

        #Ecrit le nouveau tableau des commandes en attente
            for i in range(len(tableauCommande)//2):
                if tableauCommande[2*i] != -1:
                    [ligne, colonne] = indice_to_coord(i, 5)
                    move_to(ligne + 2*nbServeurs, 15*colonne)
                    idClient = tableauCommande[2*i]
                    menu = tableauCommande[2*i+1]
                    print("("+str(idClient)+","+chr(ord('A')+int(menu))+")")

    #SERVEURS
            for i in range(len(tableauServeurs)//3):
                move_to(i+2, 100)
                efface_ligne_curseur()
                move_to(i+2, 1)
                idServ = tableauServeurs[3*i]
                print("Le serveur "+str(idServ)+" prepare la commande :")

            for i in range(len(tableauServeurs)//3):
                if tableauServeurs[3*i+1] != -1:
                    ligne = i+2
                    idServ = tableauServeurs[3*i]
                    idClient = tableauServeurs[3*i+1]
                    menu = tableauServeurs[3*i+2]
                    text = "Le serveur "+str(idServ)+" prepare la commande : ("+str(idClient)+","+chr(ord('A')+int(menu))+")"
                    move_to(ligne, 1)
                    print(text)

    #COMMANDES SERVIES
            for i in range(len(tableauCommandeServie)//3):
                move_to(i+2+20, 100)
                efface_ligne_curseur()
                move_to(i+20+2, 1)
                idServ = tableauServeurs[3*i]
                print("Le serveur "+str(idServ)+" a donné la commande :")

            for i in range(len(tableauCommandeServie)//3):
                if tableauCommandeServie[3*i+1] != -1:
                    ligne = i+2+20
                    idServ = tableauCommandeServie[3*i]
                    idClient = tableauCommandeServie[3*i+1]
                    menu = tableauCommandeServie[3*i+2]
                    text = "Le serveur "+str(idServ)+" a donné la commande : ("+str(idClient)+","+chr(ord('A')+int(menu))+")"
                    move_to(ligne, 1)
                    print(text)

            mutexServie.release()
            mutexCommande.release()
            mutexServeurs.release()
            time.sleep(0.5)




if __name__ == "__main__" :
    effacer_ecran()
    resto_ouvert = mp.Value('i', 0)
    nbCommandeMax = 50
    tableauCommande = mp.Array('i', [-1 for i in range(2*nbCommandeMax)])
    nbServeurs = 5
    tableauServeurs = mp.Array('i', [-1 for i in range(3*nbServeurs)])
    tableauCommandeServie = mp.Array('i', [-1 for i in range(3*nbServeurs)])
    for i in range(nbServeurs):
        tableauServeurs[3*i] = i+1
        tableauCommandeServie[3*i] = i+1
    liste_process = []

    mutexServeurs = mp.Lock()
    mutexCommande = mp.Lock()
    mutexServie = mp.Lock()
    mutexResto = mp.Lock()

    #Affichage UI

    move_to(nbServeurs + 3, 1)
    print("COMMANDES EN ATTENTE :")
    ligneinfo = (nbCommandeMax//5)+nbServeurs*2+8
    move_to((nbCommandeMax//5)+nbServeurs*2+8, 1)
    print(" ---------------------------------")
    print(" | Restaurant ouvert de 8h à 22h |")
    print(" ---------------------------------")
    time.sleep(1)
    ProcessHorloge = mp.Process(target = horloge, args=(0,resto_ouvert,mutexResto, ligneinfo))
    liste_process.append(ProcessHorloge)

    for i in range(nbServeurs):
        i += 1
        p = mp.Process(target=processServ, args=(resto_ouvert,i, mutexServeurs,mutexCommande, tableauServeurs,tableauCommandeServie,mutexServie))
        liste_process.append(p)

    p1 = mp.Process(target=processClient, args=(resto_ouvert,tableauCommande, mutexCommande))
    liste_process.append(p1)

    p2 = mp.Process(target=Major_dHomme, args=(resto_ouvert,tableauCommande, mutexCommande, tableauServeurs, mutexServeurs,nbCommandeMax, nbServeurs,tableauCommandeServie,mutexServie))
    liste_process.append(p2)


    for p in liste_process:    
        p.start()
    for p in liste_process:    
        p.join()