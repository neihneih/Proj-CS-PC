import math, random, time, os
from array import array
import multiprocessing as mp

def merge(left, right):
    tableau = array('i', [])  # tableau vide qui reçoit les résultats
    while len(left) > 0 and len(right) > 0:
        if left[0] < right[0]: tableau.append(left.pop(0))
        else: tableau.append(right.pop(0))

    tableau += left + right
    return tableau

def merge_sort(Tableau):
    length_Tableau = len(Tableau)
    if length_Tableau <= 1: return Tableau
    mid = length_Tableau // 2
    tab_left = Tableau[0:mid]
    tab_right = Tableau[mid:]
    tab_left = merge_sort(tab_left)
    tab_right = merge_sort(tab_right)
    return merge(tab_left, tab_right)

def merge_sort_processus(Tableau, nombre_processus):
    liste_processus = []
    Tab = []
    length_Tableau = len(Tableau)
    taille_division = length_Tableau // nombre_processus
    if length_Tableau <= 1: return Tableau
    for numero_processus in range(nombre_processus):
        Tab == Tableau[numero_processus * taille_division : numero_processus * (taille_division + 1)]
        retour = os.fork()
        mid = len(Tab) // 2
        tab_left = Tab[0:mid]
        tab_right = Tab[mid:]
        if retour != 0:
            process = mp.Process(target=merge_sort_processus, args=(tab_right)) #le fils fait un merge_sort
        process = mp.Process(target=merge_sort_processus, args=(tab_left))
        liste_processus.append(process)
        process.start()
        for p in liste_processus:
            p.join()
        return merge(tab_left, tab_right)

def version_de_base(N):
    Tab = array('i', [random.randint(0, 2 * N) for _ in range(N)]) 
    #print("Avant : ", Tab)
    start=time.time()
    Tab = merge_sort(Tab)
    end=time.time()
    print("Après : ", Tab)
    print("Le temps avec 1 seul Process = %f pour un tableau de %d éléments " % ((end-start)*1000, N))
    
    print("Vérifions que le tri est correct --> ", end='')
    try :
        assert(all([(Tab[i] <= Tab[i+1]) for i in range(N-1)]))
        print("Le tri est OK !")
    except : print(" Le tri n'a pas marché !")

def version_processus(N, nombre_processus):
    Tab = array('i', [random.randint(0, 2 * N) for _ in range(N)]) 
    #print("Avant : ", Tab)
    start=time.time()
    Tab = merge_sort_processus(Tab, nombre_processus)
    end=time.time()
    print("Après : ", Tab)
    print("Le temps avec 1 seul Process = %f pour un tableau de %d éléments " % ((end-start)*1000, N))
    
    print("Vérifions que le tri est correct --> ", end='')
    try :
        assert(all([(Tab[i] <= Tab[i+1]) for i in range(N-1)]))
        print("Le tri est OK !")
    except : print(" Le tri n'a pas marché !")

N = 50
version_processus(N, 1)
