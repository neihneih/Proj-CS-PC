import os


#on initialise les variables
somme_impairs = 0
nb_recu = -1


#on somme les entiers reçus jusqu'à ce qu'on reçoive 0
while nb_recu != 0:
    fdni = os.open("nombresImpairs", os.O_RDONLY | os.O_CREAT)
    nb_recu = int.from_bytes(os.read(fdni, 10), 'little')
    somme_impairs += nb_recu


#on renvoie la somme calculée dans le pipe
fdsi = os.open("sommeImpairs", os.O_WRONLY | os.O_CREAT)
os.write(fdsi, somme_impairs.to_bytes(10, 'little'))
