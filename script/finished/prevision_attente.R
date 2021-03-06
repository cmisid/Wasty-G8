### Auteurs : Giovanni Zanitti et Sofian Benjebria
### Derni�re modif : 04/01/17 17h

setwd("~/M2 CMI SID/WastyDB")

#Suppresion de la liste de travail

rm(list=ls())

#Packages

library("Imap")
library(sqldf)

#Import des donn�es

df <- read.csv2('data/Depot_Objet.csv', header = TRUE, sep = ";")

#Requ�te de l'utilisateur (categ,SS_categ,etat,Lon,Lat,rayon(en km),date,time) 

req <- c("Ameublement","Table","Bon","1.396912","43.57600","5","07/10/17","21:30:00")

#####################Fonction prevision_attente ##############################
##Entrees :  (categ,SS_categ,etat,Lon,Lat,rayon(en km),date,time)
##Objectif : Calculer la probabilit� d'apparition d'un objet, dans un rayon donn� dans les 7 jours et 28 jours
##Sorties : Proba sous 7 et 28 jours

prevision_attente <- function(pCateg,pSs_categ,pEtat,pLon,pLat,pRayon,pDate,pTime){
  
  #R�cup�ration de la date d'�mission de la requ�te en format utilisable par la suite
  t = paste(pDate,pTime)
  today <- strptime(t,"%d/%m/%y %H:%M:%S")
  
  #R�cup�ration des donn�es n�cessaire pour la requ�te
  
  ##Extraction des donn�es par rapport � la categorie, la sous-categorie et l'etat
  sql_req = paste("SELECT * FROM df WHERE Categ = '",pCateg,"' AND Ss_categ = '",pSs_categ,"' AND Etat= '",pEtat,"'", sep ='')
  df_req <- sqldf(sql_req)
  
  ##Limitation des donn�es dans l'espace gr�ce au rayon demand�
  
  ###Distance par rapport � l'utilisateur
  
  for(i in 1:nrow(df_req)){
    df_req$Distance[i] <- gdist(as.numeric(pLon),as.numeric(pLat),df_req$Longitude[i],df_req$Latitude[i],units = "km") 
  }
  
  ###Donn�es cibl�es par rapport au rayon souhait� (en km)
  
  df_req_dist <- sqldf(paste("Select * from df_req where Distance < ",pRayon))
  
  #Transformation de la date et de l'heure en un format utilisable dans une nouvelle variable (DTime)
  x <- paste(df_req_dist$Date, df_req_dist$Heure)
  df_req_dist$DTime<- strptime(x, "%d/%m/%y %H:%M:%S")
  
  #Calcul du nombre de jour pass� depuis le dernier post
  dernier <- today - max(df_req_dist$DTime)
  
  #Calcul des fr�quences
  
  ##Etendu de la plage horaire
  
  res <- max(df_req_dist$DTime) - min(df_req_dist$DTime)
  
  ##Calcul de la fr�quence en nombre de jour (Exemple : Une chaise apparait tous les 20 jours)
  
  freq <- (as.numeric(res)/nrow(df_req_dist)) 
  
  ##Calcul de la fr�quence dans l'heure en prenant en compte la date du dernier post (� expliquer � l'�crit)
  freq_heure <- 1/(freq*24/as.numeric(dernier))
  
  ##Calcul de la fr�quence en un jour
  freq_jour <- 1/(freq/as.numeric(dernier))
  
  ##Calcul de la fr�quence en 7 jours 
  freq_sem <- 1/(freq/(7+as.numeric(dernier)))
  
  ##Calcul de la fr�quence en un mois (4*7 jours)
  freq_mois <- 1/(freq/(28+as.numeric(dernier)))
  
  ##Calcul des probabilit�s d'apparitions des objets dans les 7jours et dans les 28jours
  
  ##Utilisation de la loi exponentielle
  
  prob_heure <- round(pexp(1,freq_heure)*100,2)
  prob_jour <- round(pexp(1,freq_jour)*100,2)
  prob_sem <- round(pexp(1,freq_sem)*100,2)
  prob_mois <- round(pexp(1,freq_mois)*100,2)
  
  ##Affichage des r�sultats
  print(
    paste("Dans un rayon de",pRayon,"km, la probabilit� d'avoir l'objet demand� est de",
          prob_heure,"% dans l'heure, de",
          prob_jour,"% dans les 24 prochaines heures, de",
          prob_sem,"% dans les 7 jours et de",
          prob_mois,"% dans les 28 jours")
  )
  return(c(prob_heure,prob_jour,prob_sem,prob_mois))
}

##################
resultats = prevision_attente("Ameublement","Table","Bon","1.396912","43.57600","5","07/10/17","21:30:00")