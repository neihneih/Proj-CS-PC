import time, random, os
import multiprocessing as mp
import numpy as np
import SharedArray as sa
from array import array

def merge(left, right, jeton_array):
    tableau = array('i', [])  # tableau vide qui reçoit les résultats
    while len(left) > 0 and len(right) > 0:
        if left[0] < right[0]: tableau.append(left.pop(0))
        else: tableau.append(right.pop(0))
    tableau += left + right
    jeton_array.acquire()
    tableau_trie.append(tableau) #cette instruction n'est pas possible. il faut changer les éléments 1 a 1 avec tableau_trie[0]=0 par exemple
    


def merge_sort(Tableau_a_trier,borne_left, borne_right, jeton_value, jeton_array):
    length_Tableau_a_trier = len(Tableau_a_trier)
    if length_Tableau_a_trier <= 1:
        return Tableau_a_trier
    mid = borne_left + (borne_right - borne_left)//2
    left = Tableau_a_trier[borne_left:mid]
    right = Tableau_a_trier[mid:borne_right]

    jeton_value.acquire()
    n = nombre_processus_dispos.value
    if n > 0:
        #cas où il y a des processus disponibles
        nombre_processus_dispos.value -= 1

        #processus tableau de gauche
        left = mp.Process(target = merge_sort, args=(Tableau_a_trier, borne_left, (borne_left + borne_right)//2 , jeton_value, jeton_array))
        left.start()
        left.join()
        nombre_processus_dispos.value =+ 1
        jeton_value.release()

        #processus tableau de droite
        right = merge_sort(Tableau_a_trier, (borne_left + borne_right)//2 + 1, borne_right, jeton_value, jeton_array)
    else:
        #cas où il n'y a plus de processus disponibles 
        left = merge_sort(Tableau_a_trier, borne_left, (borne_left + borne_right)//2, jeton_value, jeton_array)
        right = merge_sort(Tableau_a_trier, (borne_left + borne_right)//2 + 1, borne_right, jeton_value, jeton_array)
    return merge(left, right, jeton_array)




def version_de_base(N, jeton_value):
    Tab = array('i', [random.randint(0, 2 * N) for _ in range(N)]) 
    print("Avant : ", Tab)
    start=time.time()
    Tab = merge_sort(Tab, 0, len(Tab), jeton_value, jeton_array)
    end=time.time()
    print("Après : ", Tab)
    print("Le temps avec 1 seul Process = %f pour un tableau de %d eles " % ((end-start)*1000, N))
    
    print("Vérifions que le tri est correct --> ", end='')
    try :
        assert(all([(Tab[i] <= Tab[i+1]) for i in range(N-1)]))
        print("Le tri est OK !")
    except : print(" Le tri n'a pas marché !")


if __name__ == "__main__" :
    N = 24
    nombre_processus = 4

    jeton_value = mp.Lock()
    nombre_processus_dispos = mp.Value('i', nombre_processus)
    
    jeton_array = mp.Lock()
    tableau_trie = mp.Array('i', [0 for i in range(nombre_processus)])

    version_de_base(N, jeton_value)
