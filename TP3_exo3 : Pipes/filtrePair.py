import os


#on initialise les variables
somme_pairs = 0
nb_recu = -1


#on somme les entiers reçus jusqu'à ce qu'on reçoive 0
while nb_recu != 0:
    fdnp = os.open("nombresPairs", os.O_RDONLY | os.O_CREAT)
    nb_recu = int.from_bytes(os.read(fdnp, 10), 'little')
    somme_pairs += nb_recu


#on renvoie la somme calculée dans le pipe
fdsp = os.open("sommePairs", os.O_WRONLY | os.O_CREAT)
os.write(fdsp, somme_pairs.to_bytes(10, 'little'))