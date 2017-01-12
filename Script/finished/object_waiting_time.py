# -*- coding: utf-8 -*-
# Version 1: Calculer la probabilite d'apparition d'un 
#objet dans l'heure, le jour, la semaine et le mois qui suit sous R 
# Objectif: Calculer la probabilite d'apparition d'un
# objet dans l'heure, le jour, la semaine et le mois qui suit sous Python
##---------------------------------------------------
# Projet WASTY DataBase
# Groupe 8
# Objectif: Calculer la probabilite d'apparition d'un
# objet dans l'heure, le jour, la semaine et le mois qui suit
##---------------------------------------------------

import pandas as pd
import json
from datetime import datetime
import math

# Import des donnees au format json
with open('../../../Wasty-G7/Annonce.json') as data_file:
    data = json.load(data_file)

# Transformation des donnees en dataframe
df = pd.read_json(data)



# Prédiction du temps dattente avant qu'un objet soit disponible 
# Entrees : id sous categorie et etat de l'objet
# Objectif : Calculer la probabilite d'apparition
# d'un objet dans l'heure, le jour, la semaine et 
# le mois qui suit.
# Sorties : Probabilites d'appartition dans l'heure, 
# le jour, la semaine et le mois qui suit


def object_waiting_time(pid_sub_category, padvert_state):

    # Donnees ciblees sur la categorie et l'etat souhaite
    df_u = df[(df['id_sub_category'] == pid_sub_category) & (
        df['object_state'] == padvert_state)]

    # Date du jour
    now = datetime.now()

    # Date du dernier depot
    max_date_u = max(df_u.date)
    max_date_u = max_date_u.strftime("%Y-%m-%d %H:%M:%S")
    max_date_u = datetime.strptime(max_date_u, "%Y-%m-%d %H:%M:%S")

    # Date du premier depot
    min_date_u = min(df_u.date)
    min_date_u = min_date_u.strftime("%Y-%m-%d %H:%M:%S")
    min_date_u = datetime.strptime(min_date_u, "%Y-%m-%d %H:%M:%S")

    # Calcul du nombre de jour passe depuis le dernier post
    last = abs((now - max_date_u).days)

    # Nombre de jours entre le premier et le dernier depot
    time_slot = abs((max_date_u - min_date_u).days)

    # Calcul de la frequence en nombre de jour (Exemple : Une chaise
    # apparait tous les 20 jours)
    freq = time_slot/len(df_u)

    # Prochaine apparition en heure par rapport a la frequence et le
    # dernier depot
    # Interpretation : Dans la prochaine heure, il va apparaitre 0.4
    # objet
    next_hour = 1/(freq*24/int(last))

    # Prochaine apparition en jour par rapport a la frequence et le
    # dernier depot
    # Interpretation : Dans le prochain jour, il va apparaitre 9.6
    # objets
    next_day = 1/(freq/int(last))

    # Prochaine apparition en semaine par rapport a la frequence et le
    # dernier depot
    # Interpretation : Dans la prochaine semaine, il va apparaitre 67.2
    # objets
    next_week = 1/(freq/(7+int(last)))

    # Prochaine apparition en mois par rapport a la frequence et le
    # dernier depot
    # Interpretation : Dans le prochain mois, il va apparaitre 268.8 objets
    next_month = 1/(freq/(28+int(last)))

    # Calcul des probabilites d'apparitions des objets dans les 7jours
    # et dans les 28jours

    # Utilisation de la loi exponentielle

    prob_hour = round((1-math.exp(-next_hour))*100, 2)
    prob_day = round((1-math.exp(-next_day))*100, 2)
    prob_week = round((1-math.exp(-next_week))*100, 2)
    prob_month = round((1-math.exp(-next_month))*100, 2)

    print("La probabilite d'avoir l'objet demande est de",
          prob_hour, "% dans l'heure, de",
          prob_day, "% dans les 24 prochaines heures, de",
          prob_week, "% dans les 7 jours et de",
          prob_month, "% dans les 28 jours")

    return [prob_hour, prob_day, prob_week, prob_month]