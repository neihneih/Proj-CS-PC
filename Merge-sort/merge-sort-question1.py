import math, random, time
from array import array

def merge(left, right):
    tableau = array('i', [])  # tableau vide qui re�oit les r�sultats
    while len(left) > 0 and len(right) > 0:
        if left[0] < right[0]: tableau.append(left.pop(0))
        else: tableau.append(right.pop(0))

    tableau += left + right
    return tableau

def merge_sort(Tableau, nombre_tranches):
    Tableau_final = []
    length_Tableau = len(Tableau)
    if length_Tableau <= 1: return Tableau
    '''
    mid = length_Tableau // 2
    tab_left = Tableau[0:mid]
    tab_right = Tableau[mid:]
    tab_left = merge_sort(tab_left)
    tab_right = merge_sort(tab_right)
    '''
    length_tranche = length_Tableau//nombre_tranches
    for numero_tranche in range(nombre_tranches):
        left = numero_tranche * length_tranche
        right = length_tranche * (numero_tranche + 1) - 1
        tranche = Tableau[left : right]
        demi_tranche_left = Tableau[left : len(tranche)//2]
        demi_tranche_right = Tableau[len(tranche)//2 : right]
        print('tranche ', numero_tranche, 'va de ', left, ' à ', right)
        T1 = merge(demi_tranche_left, demi_tranche_right)
    return T1

def version_de_base(N):
    Tab = array('i', [random.randint(0, 2 * N) for _ in range(N)]) 
    print("Avant : ", Tab)
    start=time.time()
    Tab = merge_sort(Tab, nombre_tranches = 2)
    end=time.time()
    print("Apr�s : ", Tab)
    print("Le temps avec 1 seul Process = %f pour un tableau de %d eles " % ((end-start)*1000, N))
    
    print("V�rifions que le tri est correct --> ", end='')
    try :
        assert(all([(Tab[i] <= Tab[i+1]) for i in range(N-1)]))
        print("Le tri est OK !")
    except : print(" Le tri n'a pas march� !")

N = 16
version_de_base(N)