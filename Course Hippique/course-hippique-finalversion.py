# Mai 2021
# BINOME : CURRAL Maxime - NGUYEN Hien
# Exécuter sous Linux
# Cours hippique
# Version très basique, sans mutex sur l'écran, sans arbitre, sans annoncer le gagant, ... ...
# Sans mutex écran

CLEARSCR = "\x1B[2J\x1B[;H"        #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"
CRLF  = "\r\n"                     #  Retour à la ligne

# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# VT100 : Actions sur les caractères affichables
NORMAL = "\x1B[0m"                 #  Normal
BOLD = "\x1B[1m"                   #  Gras
UNDERLINE = "\x1B[4m"              #  Souligné


# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m"             #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"               #  Rouge
CL_GREEN="\033[22;32m"             #  Vert
CL_BROWN = "\033[22;33m"           #  Brun
CL_BLUE="\033[22;34m"              #  Bleu
CL_MAGENTA="\033[22;35m"           #  Magenta
CL_CYAN="\033[22;36m"              #  Cyan
CL_GRAY="\033[22;37m"              #  Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m"               #  Gris foncé
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"                  #  Blanc


#-------------------------------------------------------

import multiprocessing as mp 
import os, time,math, random, sys, ctypes
#from multiprocessing import Process, Value, Lock
#from array import array                             # Attention : différent des 'Array' des Process

LONGEUR_COURSE = 100 
keep_running = mp.Value(ctypes.c_bool, True)

lyst_colors = [CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY, CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN, \
             CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

def effacer_ecran() : 
    print(CLEARSCR,end='')
#    for n in range(0, 64, 1): print("\r\n",end='')

def erase_line_from_beg_to_course() : 
    print("\033[1K",end='')

def curseur_invisible() : 
    print(CURSOFF,end='')

def curseur_visible() : 
    print(CURSON,end='')

def move_to(lig, col) :         # No work print("\033[%i;%if"%(lig, col)) # print(GOTOYX%(x,y))
    print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : 
    print(Coul,end='')

def en_rouge() : 
    print(CL_RED,end='')


def un_cheval(mutex_position, tablCol, mutex, ma_ligne : int) : # ma_ligne commence � 0
    # move_to(20, 1); print("Le chaval ", chr(ord('A')+ma_ligne), " démarre ...")
    col = 1

    while col < LONGEUR_COURSE and keep_running.value :
        
        mutex.acquire()
        move_to(ma_ligne+1,col)         # pour effacer toute ma ligne
        erase_line_from_beg_to_course()
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        print('('+chr(ord('A')+ma_ligne)+'>')
        mutex.release()
        
        col += 1

        mutex_position.acquire()
        tablCol[ma_ligne] = col
        mutex_position.release()

        time.sleep(0.005 * random.randint(1,50))


def label_arbitre(cheval_en_tete, mutex_position, ligne, T): 
    
    for i in range(len(T)):
        T[i] = 0

    maxCol = 0

    # Cherche le premier
    while maxCol < LONGEUR_COURSE and keep_running.value:
        en_couleur(lyst_colors[0%len(lyst_colors)])
        move_to(ligne, 4)
        id_premier = []
        id_dernier = []

        mutex_position.acquire()
        maxCol = max(T)
        minCol = min(T)

        for val in range(len(T)):
            if T[val] == maxCol:
                id_premier.append(val)

            elif T[val] == minCol:
                id_dernier.append(val)
        mutex_position.release()

        affichage_premier = ''
        affichage_dernier = ''

        for i in id_premier:
            affichage_premier += chr(ord('0') + i) + ' '

        for i in id_dernier:
            affichage_dernier += chr(ord('0') + i) + ' '

        move_to(ligne, 50)
        erase_line_from_beg_to_course()

        move_to(ligne, 4)
        print('PREMIER : ' + affichage_premier)

        move_to(ligne+1, 50)
        erase_line_from_beg_to_course()

        move_to(ligne+1, 4)
        print('DERNIER : ' + affichage_dernier)


    while minCol < LONGEUR_COURSE-1 and keep_running.value:
        en_couleur(lyst_colors[0%len(lyst_colors)])
        move_to(ligne, 4)
        id_dernier = []

        mutex_position.acquire()
        minCol = min(T)

        for val in range(len(T)):
            if T[val] == minCol:
                id_dernier.append(val)
        mutex_position.release()

        affichage_dernier = ''
        for i in id_dernier:
            affichage_dernier += chr(ord('0')+i)+' '

        move_to(ligne+1, 50)
        erase_line_from_beg_to_course()
        move_to(ligne+1, 4)
        print('Dernier : '+affichage_dernier)

    for i in id_premier:
        cheval_en_tete[i] = i


def course_hippique() :
    resultat_final = False
    Nb_process = 10

    prediction = input('Sur quel cheval souhaitez-vous miser? Veuillez choisir entre 0 et ' + chr(ord('0') + Nb_process - 1) + ' inclus : ')


    mutex_affichage = mp.Lock()
    mutex_position = mp.Lock()

    tablCol = mp.Array('i', Nb_process)
    cheval_en_tete = mp.Array('i', [101 for i in range(Nb_process)])

    mes_process = [0 for i in range(Nb_process+1)]
    effacer_ecran()
    curseur_invisible()


    for i in range(Nb_process):  # Lancer     Nb_process  processus
        mes_process[i] = mp.Process(target = un_cheval, args = (mutex_position, tablCol,mutex_affichage, i)) #CHANGEMENT
        mes_process[i].start()

    process_arbitre = mp.Process(target = label_arbitre, args =(cheval_en_tete, mutex_position, Nb_process + 2, tablCol ))

    process_arbitre.start()
    mes_process[Nb_process] = process_arbitre

    en_couleur(lyst_colors[0%len(lyst_colors)])
    move_to(Nb_process + 4, 1)
    print("La course a commencé !")
    print('Vous avez misé sur le cheval '+str(prediction))

    for i in range(Nb_process + 1): mes_process[i].join()

    en_couleur(lyst_colors[0%len(lyst_colors)])
    move_to(Nb_process + 6, 1)
    curseur_visible()
    print("Fin de la course !")

    for i in cheval_en_tete:
        if i == int(prediction):
            print('BONNE PREDICTION')
            resultat_final = True

    if resultat_final == False:
        print('MAUVAISE PREDICTION')
    
# La partie principale :
if __name__ == "__main__" :
    course_hippique()
    