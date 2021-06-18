import os, sys
from random import randint



#on crée les pipes après avoir vérifié qu'ils n'existaient pas déjà
if os.path.exists("nombresPairs") :
    os.unlink("nombresPairs")
os.mkfifo("nombresPairs")

if os.path.exists("nombresImpairs") :
    os.unlink("nombresImpairs")
os.mkfifo("nombresImpairs")

if os.path.exists("sommePairs") :
    os.unlink("sommePairs")
os.mkfifo("sommePairs")

if os.path.exists("sommeImpairs") :
    os.unlink("sommeImpairs")
os.mkfifo("sommeImpairs")



#nombre d'entiers générés
N = 10

#on génère les entiers
for i in range(N):
    n = randint(1,5)
    print(n)
    if n%2 == 0:
        #cas où le nombre est pair
        fdnp = os.open("nombresPairs", os.O_WRONLY | os.O_CREAT)
        os.write(fdnp, n.to_bytes(10, 'little'))
        #os.close(fdnp)
    else:
        #cas où le nombre est impair
        fdni = os.open("nombresImpairs", os.O_WRONLY | os.O_CREAT)
        os.write(fdni, n.to_bytes(10, 'little'))
        #os.close(fdni)



#une fois tous les entiers envoyés, on envoie 0 pour indiquer la fin du comptage

#pair
nb_envoye = 0
fdnp = os.open("nombresPairs", os.O_WRONLY | os.O_CREAT)
os.write(fdnp, nb_envoye.to_bytes(10, 'little'))

#impair
fdni = os.open("nombresImpairs", os.O_WRONLY | os.O_CREAT)
os.write(fdni, nb_envoye.to_bytes(10, 'little'))



#on lit les résultats retournés par les filtres dans les pipes
fdsp = os.open("sommePairs", os.O_RDONLY | os.O_CREAT)
somme_pairs = int.from_bytes(os.read(fdsp, 10), 'little')

fdsi = os.open("sommeImpairs", os.O_RDONLY | os.O_CREAT)
somme_impairs = int.from_bytes(os.read(fdsi, 10), 'little')



#on ferme les pipes
os.close(fdnp)
os.close(fdni)
os.close(fdsp)
os.close(fdsi)



#on affiche les résultats
print("Somme des entiers pairs : ", somme_pairs)
print("Somme des entiers impairs : ", somme_impairs)
print("Somme totale : ", somme_pairs + somme_impairs)

sys.exit(0)