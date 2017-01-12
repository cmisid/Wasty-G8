# -*- coding: utf-8 -*-
# Version 1 : Recommandation des annonces en 
# fonction du profil en R
# Version 2 : traduction en python

## --------------------------------------------------------
# Projet : WASTY
# Groupe 8 : Prédiction et recommandation
# Objectif : La prédiction du temps de disponibilité d'un
## --------------------------------------------------------

# Import des librairies
import pandas as pd
import numpy as np
from collections import Counter
import json

# Import des donnees
df = pd.read_csv("../../data/Historique/historique100u.csv", sep=";")

with open('../../data/Advert/Annonce.json') as data_file:
    data = json.load(data_file)

# Transformation des donnees en dataframe
annonce = pd.read_json(data)


# Calcul de la matrice des favoris

nb_user = len(set(df['id_user']))
nb_obj = len(set(df['id_advert']))

# Initialisation de matrice
tab = np.eye(nb_user+1, nb_obj+1)

# Pour chaque user
for i in range(1, nb_user+1):
    # Pour chaque objet
    for j in range(1, nb_obj+1):
        # Si l'user n'a pas vu l'objet
        if len(df[(df['id_user'] == i) & (df['id_advert'] == j)]) == 0:
            # Valeur dans tab = 0
            tab[i][j] = 0
        # Si il a vu l'annonce sans mettre en favoris
        elif df[(df['id_user'] == i) & (df['id_advert'] == j)][
            'favoris'
        ].item() == 0:
            # Valeur dans tab = 1
            tab[i][j] = 1
        # S'il a vu l'annonce et qu'il l'a mis en favoris
        elif df[(df['id_user'] == i) & (df['id_advert'] == j)][
            'favoris'
        ].item() == 1:
            # Valeur dans tab = 3
            tab[i][j] = 3

# Suppression de la premiere ligne et de la premiere colonne inutiles
tab = np.delete(tab, (0), axis=0)
tab = np.delete(tab, (0), axis=1)


# Calcul de la matrice des similarités

# Initialisation de matrice
sim = np.eye(nb_user, nb_user)

# Pour chaque utilisateur
for i in range(nb_user):
    # Pour chaque utilisateur
    for j in range(nb_user):
        # Calcul de leurs ressemblance
        sim[i][j] = sum(tab[i][:] * tab[:][j])


# Entree : id_user
# Objectif : Retourner les annonces a recommende a l'user choisi en
# fonction des vues des users qui on liker les memes annonces que lui
# Sortie : Liste des objets a recommende dans l'ordre
def recommendation_view(pid_user):

    # 5 plus proches voisins de l'user choisi
    top5_u = pd.DataFrame(sim[pid_user-1]).sort(0, ascending=0)[1:6]

    # Vecteur des favoris et vues de l'utilisateur
    vec_u = pd.DataFrame(tab[pid_user-1])
    vec_u.columns = ['val']
    # Favoris de l'utilisateur
    fav_u = vec_u[vec_u['val'] == 3]
    # Initialisation de liste
    recommend_list = list()
    # Pour i allant de 0 à 4
    for i in range(5):
        # On recupere l'id du i+1-ieme plus proche voisin (PPV)
        NN = top5_u.index.values[i]
        # On recupere ses vues, favoris et pages non vues
        vec_NN = pd.DataFrame(tab[NN])
        vec_NN.columns = ['val']
        # On recupere seulement ses favoris
        fav_NN = vec_NN[vec_NN['val'] == 3]
        # On regarde la difference entre les favoris du PPV
        # et l'utilisateur
        diff = list(
            set(list(fav_NN.index.values)) -
            set(list(fav_u.index.values))
        )
        # On les stocks dans une liste incrementer a chaque PPV
        recommend_list.extend(diff)

    # On compte le nombre de fois qu'un objet est recommende
    ct = Counter(recommend_list)
    # On ressort ceux qui sont le plus recommende dans cette liste
    mc = ct.most_common()
    # On reformate les donnees au format souhaite
    advert_to_recommend = [mc[i][0] for i in range(len(mc))]
    advert_to_recommend = pd.DataFrame({'id_advert': advert_to_recommend})
    # On va chercher l'information sur la disponibilite des objets
    advert_to_recommend = pd.concat([advert_to_recommend, annonce],
                                    axis=1, join='inner')
    # On ne garde que ceux en ligne
    advert_to_recommend_free = advert_to_recommend[
        advert_to_recommend['advert_state'] == 'en ligne'
    ]

    # On retourne la liste des 5 objets a recommender dans l'ordre
    return list(advert_to_recommend_free['id_advert'].iloc[:, 0])[0:5]