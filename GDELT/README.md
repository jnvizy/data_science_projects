# Projet Bigdata
<a style="color: black" href="http://andreiarion.github.io/Projet2018-intro.html#/">Lien pour plus d'informations sur le projet</a>
## But
Analyser l’année 2018 via la base de données *GDELT* en utilisant le **tone**  des articles dans les medias des divers pays du monde

## Questions à répondre 

1. le nombre d’articles/evenements pour chaque (jour, pays de l’evenement, langue de l’article)
2. pour un acteur(pays/organisation ...) ⇒ afficher les evenements qui y font reference
3. les sujets (acteurs) qui ont eu le plus d’articles positifs/negatifs (mois, pays, langue de l’article).
4. acteurs/pays/organisations qui divisent le plus 

## Question supplémentaire
5. l'évolution de la relation entre deux pays au cours du temps



## Architecture proposée 
Pour ce projet , on a opté pour l'architecture suivante: 
* Utiliser Spark comme ETL avec son langage natif scala pour le traitement et les jointures intérmédiaires via spark SQL
* Déposer les fichier GDELT dans S3 sous format parquet pour accélerer le proccesus de lecture
* Mettre les fichiers traités en scala dans une instance Mongo sous AWS 
* Utiliser jupyter notebook et Flask pour requeter la base avec pymongo 

![Architcture](https://raw.githubusercontent.com/rreinette/INF728/master/Img/Screenshot%20from%202019-01-28%2009-42-38.png)


## Organistation du dossier : 

1. Le dossier Data contient des métadonnées sur les events et les pays et un exemple dejeux de donnée
2. Le dossier MongoDB contient les un notebook jupyter regroupant les résultats des requetes et la partie visualisation avec bokeh et matplotlib
3. Le dossier Vizualisation contient le code de l'application FLASK 
4. Le dossier config_aws regroupe tous les scripts de configurations utilisés dans le projet  ( il y a un fichier zip à utiliser directement ) 
5. Le dossier scala contient un zepplin notebook permettant le preprocessing des fichiers GDELT et un sous dossier "scripts" qui contient les codes scala pour chaque requetes 
6. Le dossier Presentation contient le support ppt de la présentation
