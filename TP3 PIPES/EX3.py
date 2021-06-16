# CURRAL Maxime - NGUYEN Hien

import os,sys
import multiprocessing as mp
import random 

(NbPair_R,NbPair_W) = mp.Pipe()
(NbImpair_R,NbImpair_W) = mp.Pipe()
(SommePair_R,SommePair_W) = mp.Pipe()
(SommeImpair_R,SommeImpair_W) = mp.Pipe()


fork1 = os.fork()
N = 5

if fork1 != 0:
    fork2 = os.fork()

    if fork2 != 0:

        # On ferme ce qu'il n'est pas utile au processus
        NbPair_R.close()
        NbImpair_R.close()
        SommePair_W.close()
        SommeImpair_W.close()

        # 1er Processus
        for i in range (N):         
            R = random.randint(1,10) #On crée un entier aléatoire entre 1 et 9 inclus
            print (R)
            #On teste les conditions de parité et on déplace ces entiers
            if R%2 == 0:
                NbPair_W.send(R)
            else:
                NbImpair_W.send(R)

        # Une fois terminé on ajoute -1 = marque de fin        
        NbPair_W.send(-1)
        NbImpair_W.send(-1)

        # On ferme
        NbPair_W.close()
        NbImpair_W.close()


        # Affichage
        SommeP_Fin = SommePair_R.recv()
        SommePair_R.close()

        SommeI_Fin = SommeImpair_R.recv()
        SommeImpair_R.close()

        print("Somme paire",SommeP_Fin)
        print("Somme impaire",SommeI_Fin)
        print ("Somme totale",SommeP_Fin + SommeI_Fin)

    else:

        # On ferme ce qu'il n'est pas utile au processus
        SommeImpair_R.close()
        SommeImpair_W.close()
        NbImpair_R.close()
        NbImpair_W.close()
        NbPair_W.close()
        SommePair_R.close()

        # 2eme Processus
        Entier = NbPair_R.recv()
        SommeP = 0

        while Entier != -1: #On effectue la somme des entiers paires
            SommeP += Entier
            Entier = NbPair_R.recv()

        NbPair_R.close()

        SommePair_W.send(SommeP)
        SommePair_W.close()

else:

    # On ferme ce qu'il n'est pas utile au processus
    SommePair_R.close()
    SommePair_W.close()
    NbPair_R.close()
    NbPair_W.close()
    NbImpair_W.close()
    SommeImpair_R.close()

    ###3eme Processus
    Entier = NbImpair_R.recv()
    SommeI = 0

    while Entier != -1: #Onn effectue la sommes des entiers impaires
        SommeI += Entier
        Entier = NbImpair_R.recv()

    NbImpair_R.close()
    SommeImpair_W.send(SommeI)
    SommeImpair_W.close()