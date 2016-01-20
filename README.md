# Projet NoSQL
## Réflexion préliminaires
- Le choix de la base se fonde sur le type de requête à effectuer. 
Dans notre cas, il s'agit de sélectionner des dates contigües :
 **cassandra** / **hbase** sont bien adaptées au stockage séquentiel.

## Format de la base
1 fichier log / heure, sur trois mois.

|datetime | projectcode | pagnename | pageviews | bytes |
|---|---|---|---|---|
|xxx      | en          | Barack_Obama | 997 | 123091092|

## Schéma

Page Web ---Requête (date)---> base (150 Go)  
  ^                                |  
  |                                |  
  |                             30 jours  
  |                              ~ 13 Go  
  |                       Traitement (spark ?)  
  |                                |  
  |                                |  
  ----------------------------------  
                      
                                                     
