# Groupement de mes photos

> 41.2924°S / 174.7787° E

Voici ma serie d'algorithme afin de classer mes photos par lieux

## Contexte 

L'idée de faire cet algorithme me vient de mon voyage en Nouvelle Zélande ou je prends des milliers de photos. Sauf que je n'ai pas le temps de les trier au fur et à mesure. 
Donc je me retrouve à trier des gros blocs de photos et honnetement j'ai la flemme de le faire.

Au cours des années j'ai vite compris qu'un ordinateur est un bon outil pour automatiser des taches et il est bon d'utiliser les bons outils pour son travail. Si on ne plante pas des clous avec la main il y a une raison.

Concrétement voici mes besoins :
* 
* Stocker mes photos
* 


## Comment grouper mes photos ?

Eh oui ! Bonne question comment organiser des milliers de photos.

Pour ma part, j'ai decider de les grouper par contient / pays / lieux.
J'ai un dossier `PhotoVoyage` ou dedans j'ai `Oceanie` `Amerique` et `Europe`.
Dans chaqu'un de ces dossiers j'ai les pays que j'ai visiter. Dans `Europe` j'ai `France`, `Espagne`, ...
Puis dans `France`, je vais avoir `Nantes`, `Paris`, ...
Et dans chaqu'un de ses dossiers je peux avoir d'autre plus precis

![Image de l'organisation de mes photos](assets/OrganisationPhotos.png)

## Par date ?

Au début je me suis dit que j'allais les trier par instant ou j'ai pris la photo (sa date).
L'algorithme est assez simple.

1. On parcours toutes les photos
2. On extrait la date de la prise
3. On trie tout les photos par date
4. On parcours la liste de photos du plus ancien au plus récent
5. Si il y a plus de 2 heures entre deux photos alors elle ne sont pas dans le même groupe

2 heures c'est assez arbitraire mais je me suis dit que si je ne prends pas de photo pendant 2 heures j'ai surement changé de lieu. J'ai fais plusieurs essaies avant de trouve ce chiffre.

Easy !

Premièrement, il faut savoir comment recupèrer la date de la prise de la photo. 
Les photos contiennent tout un tas de metadata (temperature exterieur, coordonnée GPS, marque de l'appariel photo, horodatage, ...). Il y a differents format mais celui qui nous intéresse est `Exif`. Il contient au moins l'horodatage et les cordoonées GPS des photos.

Pour récuperer les données en Python, il existe une petite librairie qui permet de le faire. (https://exif.readthedocs.io/en/latest/index.html)

Le resultat est dans [classement_par_date.py](classement_par_date.py)

Rien de compliqué dans ce script, on respecte l'algorithme citée plus haut. Simple et efficace.

Voici le résultat : 

![Image l'organisation des photos par date](assets/PhotosParDate.png)

C'est bien mais il y a encore pas mal de travail manuel dérrière et si je retourne sur un même lieux une deuxieme fois ca me fera un autre dossiers.

## Par coordonnées GPS ?

Comme je disais plus haut, les données `Exif` stockent également les données GPS de la photo. Il faut bien entendu que l'appareil qui prends la photo soit capable de les fournir (Spoiler : ça sera un nouveau problème)

Je m'étais fait un petit script qui permettait d'extraire les coordonnées et les sortir au format `GPX`. Ca m'a donnée un idée de comment grouper mes photos

![Carte avec certaines photos](assets/CarteAvecPhoto.png).

Sur cette carte on voit bien deux regions distincts. La plage de Piha au nord et celle de Karekare au sud - Pour les cinéphile, c'est sur cette plage qu'a été tourné `La leçon de piano` -

Il me faut donc trouver un algo qui permet de les regrouper, j'ai fais plein d'essai et tester beaucoup de chose avant de me rendre à nouveau compte qu'il ne faut pas réinventer la roue. Il existe une librairie de clustering qui reponds exactement à mes besoins (https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html)

LA fonction que l'on utilisera est `DBScan`, cela va nous permettre de créer des clusters en fonction de la distance entre chaque photos.

Cette fonction à deux paramètre important, `eps` qui est la distance maximum entre deux données et `metric` qui la fonction choisi pour calculer la distance. Dans notre cas, ça sera la methode `haversine` (https://fr.wikipedia.org/wiki/Formule_de_haversine).

Voici le bout de code que j'utilise pour le clustering

```python
# Array numpy cast 
coordinates_list = [i.coord for i in data_images.values() if i.coord]
photo_paths = [i.path for i in data_images.values() if i.coord]

coords = np.array(coordinates_list)

eps_in_km = 4.0 
# Radians cast
eps_in_radians = eps_in_km / 6371

# Clustering by DBSCAN 
db = DBSCAN(eps=eps_in_radians, min_samples=3, metric='haversine').fit(np.radians(coords))
```
* La distance `eps` est en radians

Les deux premières lignes sont la pour séparer les données de ma liste de photos. Je veux deux listes distincts, une avec les coordonnées et l'autre avec les chemin.
On convertie ensuite le tableau de coordonnées au format de `numpy` - Librairie de calcul scientigique - pour la passer à `DBScan`. `DBScan` va créer une liste d'identifiant de cluster, la focntion de clustering va se baser sur la position dans le tableau pour pouvoir retrouver l'information initial.


DBScan decide que le cluster de la plage de Piha est `3`, mes photos de la plage sont en position 5, 12, 25, 32 alors le tableau sorti par `DBScan` aura en position 5, 12, 25 et 32 l'entier `3`.   

C'est pas forcement évidement, cela sera surement plus simple avec la fonction qui permet de rassembler toutes les informations :

```python
labels = db.labels_

# labelize photo paths
clusters = {}
for label, path, coord in zip(labels, photo_paths, coords):
  if label not in clusters:
    clusters[label] = []
  clusters[label].append(data_images[path])
  data_images[path].cluster = label
```

* `labels` : Liste des ids de mes clusters
* `photos_path` : Liste des chemins vers mes photos
* `coords` : Liste des coordonnées de mes photos


![Liste des dossiers après clustering](assets/PhotoDossierCluster.png).

Tadam ! On obtient un dossier pour chaque cluster ! Est-ce que j'ai resoulu mes problèmes du groupement avec le groupement par date ? Pas vraiment, c'est encore moins compréhensible qu'avant. C'est assez compliqué à voir comme ça mais les photos sont bien groupées par endroits.

J'ai extrait les coordonées GPS du centre de chaque cluster et j'ai mis un point sur chaque cluster.


![Carte avec le centre des clusters](assets/CarteCentreCluster.png).

Le resultat n'est pas si mal que ça. Je me retrouve avec 47 clusters differents. 
Le clusters sont assez bien regroupé et ça me convient bien (`EPS` est de 4km)

Les groupes fonctionnent bien quand on est dans la campagne les esapce sont assez grands un `EPS` de 4km est suffisants mais quand on est en ville, 4km c'est trop. Du coup, je me retrouve avec un cluster de 420 photos pour la ville de Wellington.


![Carte wellington](assets/CarteWellington.png).

C'est une evolution que j'envisage de faire. J'ai pensé à 2 solutions
* Detecter les points dans les villes et refaire une passe de DBScan. Efficace mais compliqué à mettre en place. Comment detecter si on est dans une ville ?
* Si un dossier contient un grand nombre de photo, alors on refait une passe de DBScan. Simple ! Mais j'ai certains dossiers qui contient beaucoup de photos d'une même zone. Pour Hobbiton j'ai plus de 130 photos ...

Bon, on va traiter un problème à la fois. 

### Trouver le nom des places

Une fois que j'ai fait mes clusters et que j'ai obtenu tout mes dossiers. J'enregistre dans un fichier `json` des metadata associées au cluster. J'ecris la coordonnées du centre de chaque cluster. 

Pour mon cluster 0, ça donne ça : 

```json
{"0": {"datetime": 1718253620.9124088, "centroid": [-37.85863017031631, 175.68077248580698]}}
```

Il existe des API qui permette de faire une recherche sur une geolocalitation inversée. c'est à dire on rentre des coordonnées et ça nous sort une adresse ou un lieux.

Je pense que l'API de Google Maps reponds parfaitement au besoin. Je l'ai déjà essayé pour un autre projet et c'est assez precis et assez rapide.
Malheuresement, ça coute 5$ toutes les 1000 requetes ...

Du coup j'ai choisi d'utiliser une API d'openstreetmap (https://nominatim.openstreetmap.org/reverse).

Je lui donne en paramètre les coordonnées du centre d'un de mes clusters et il me sort l'adresse ou l'endroit le plus proche. Et ça fonctionne plus ou moins ... Par exemple pour Hobbiton, voici les informations qu'il me sort 

```
"Hobbiton Movie Set, Lakeside, Matamata Piako District, Waikato, New Zealand / Aotearoa"
```

C'est pas mal mais il y a quand meme du traval manuel derrière car je veux que les noms des endroits soit clair et simple. Pour `Hobbiton`, je veux juste le nom `Hobbiton` et pas `Hobbiton Movie Set`.
Ce n'est peut être l'exemple le plus parlant.

En voici un autre.

``` 
"3637, Cape Palliser Road, Martinborough Community, South Wairarapa District, Wellington, New Zealand / Aotearoa"
```

C'est un endroit que l'on appelle "Cape Pallisier". Une magnifique randonnée le long de la côte de la region de Wellington. Mais elle se fait sur une route. La "Cape Palliser road" donc `nominatim` m'a trouvé ce lieu.

Si je reprends ma classification de mes photos de voyage. Voici comment je l'aurais fait à la main : `Océanie/Nouvelle_Zélande/Wellington/Cape_Palissier`

On voit bien que j'ai toutes les informations pour le faire (mis à part le contient, mais ce n'est pas un problème pour le moment), il faut juste le remettre en forme et garder les bonnes informations.

Je vais le faire à la main mais en me basant sur les informations que je posséde.

J'enregistre cette information dans mon fichier `json`

#### Affinage des noms des places

La première idée que j'ai eu pour affiner le nom des places était de renommer tout les dossiers des clusters par le noms trouver par l'API de recherche (`nominatim`), associé un cluster à un `UUID`, enregistré cette `UUID` dans un fichier dans le dossier du cluster, modifier le nom du dossier à la main.
Bref, une belle machine à gaz.

Finalement, en ecrivant le paragrahe ligne et si je me concentre sur mon besoin pour classer mon cluster, j'ai besoin d'avoir :
* Le nom du contient
* Le nom du pays
* Le nom de la region (Par forcement la region géographique)
* Le nom de l'endroit
* Un champs de données libre pour une descrption ou une autre informations.

J'ai pratiquement toutes les infos dont j'ai besoin. Il me manque le nom du contient mais encore une fois ce n'est pas vraiment un problème, l'information est très simple à trouver.

Je vais utiliser la bonne vielle méthode d'une entrée sur le termianl. Ca m'empèche d'avoir un traitement totalement automatisé. Mais j'ai conçut les algorithme pour être utilisé de manière indépedante. Donc cette partie là pourra être fait dans un seconds temps. Et puis si le nom sorti par `nominatim` n'est pas très bon, je peux aller consulter par moi même la photo.

Finalement, après un très court test avec mon terminal, je me suis rendu compte que ce n'est vraiment pas pratique. Je n'ai pas d'autocomplétion et je dois répété plusieurs fois la même information. j'ai opté pour un formulaire en JS/HTML qui enregistre les données dans mon fichier `JSON`.
J'épargne les details sur la conception de cette page, le developement web ce n'est pas vraimet ma spécialité (merci ChatGPT pour ton aide).

Voici un aperçu : 

![Formulaire de sasie en JS](assets/FormulaireJS.png)

J'ai dit que ce n'était pas mon truc ! Au moment au j'écris, je ne suis pas encore sur que ce soit la version definitive.

La page est accéssible dans [index.html](index.html)

## Et aprés ?

A partir de ce moment là, je galère à avancer, quelque chose de va pas dans ce que j'ai fait.
Toutes les solutions que j'envisage pour continuer le groupement de mes photos ne me convient pas.

Dans ma tête, tout ce qui existe, existe dans un ensemble cohérent. Si deux chose fonctionne l'un avec l'autre, elle le font de manière fluide.
Et la ma solution actuelle ne me permet pas d'avoir une suite coherente. Rien de ce que j'imagine ne fit avec ce que j'ai fait. Ca ne me convient pas.

J'arrive au bout de mon POC, mon projet manque de conception pour le moment.

# Part 2 !

## La révélation

Je developpe ces scripts pendant que je voyage, je ne peux pas m'y consacrer à 100% mais c'est une bonne chose.
Tout cela m'a rapellé que notre travail est un travail intellectuel.
Ce genre de travaux requit une certaines inspirations. Pour ma part, je ne l'a trouve pas assis sur une chaise en regardant un écran. 

C'est assez dur à expliqué mais mon esprit se nourri de ce que je vois, ce que je lis, des discussions avec des personnes. 

Dans ce projet, j'occupe tout les postes ! De l'architecte à l'admin et cette manière de le mener me plait.

Ca fait 2 semaines que je n'avais pas touché au projet. Mon esprit n'est pas consacré à 100% dessus.
Alors que je suis en train d'admirer un des plus paysages que je n'ai jamais vu : Les malbourrought sounds. Tout ce débloque ! 

Cela m'a refait penser à toute les heures de traval que je faisait enfermer dans un bureau a contempler un écran en esperant que la situation se débloque.
J'ai trouvé tellement de solution juste en marchant dehors. Pour moi un developpeur c'est un peu comme un artiste. Nous produisont des oeuvres de l'esprit tout comme eux. 
Un musicien peut être bloqué dans sa composition car il ne trouve pas le bon echainement de note. 
Notre travail nécisite de l'inspiration !

Bref our revenir à mon idée, il faut que je déduplique mes photos. La solution que j'ai trouvé est de rajouter dans les informations de mon cluster un dictionnaire avec comme clé le sha256 et en valeur le path de la photo.
Et j'arrete de copier mes photos dans un autre répertore. Cette solution n'était clairement pas la bonne, je le savais mais cela me faisait gagner beaucoup de temps. Cela me permettais d'avoir un resultat asse rapide

Maintenant que  

## Un peu de rangement

Mon code commence à grossir, j'en ai un peu partout. La première étape est de faire un peu de rangement. 
L'arhitecture de mon projet est assez simple. Ce sont plusieurs script qui effectue des taches "simple". Chaque script fait une et une seule tâche.

Je commence à identifier les objets de mon projet. Pas besoin d'avoir le nez dans le code pour ça. Je pense même que ce n'est pas une bonne chose.
Généralement pour ça, j'aime bien expliqué mon projet à des non-informaticien. Au moment de l'expliquer 
Et puis on n'a pas du tout la même vision. Pour moi, c'est logique, quand je vois mes programmes je vois des algorigrames, des conditions des instructions qu'un processeur va executé.
Pour eux, c'est abstrait, c'est juste un truc qui fonctionne sur un ordinateur. Ils n'ont pas la barrière technique que j'ai.
Mais bon la j'ai personne sous la main, ca me prends un peu plus de temps et bien afiner mes choix.

Tout est en bazar, je n'ai presque fait aucuune Il y a surtout besoin de factorisé le code. 

## Affiner les zones urbaines

On repart avec une petite tache simple. Definir si une zone est urbaine ou non. 
Simple ? On peut surement faire une machine à gaz et se basant sur des api qui contiennent le noms de toutes le villes du monde, estimait qu'une zone urbaine est une ville avec une population supérieur à un certains nombres de personnes. 

Il y a peut être d'autres solutions, plus simple ou compliqué mais je vais juste me baser sur le nombre de photo dans un clusteur. J'estime que si un clusteur à plus de 150 photos alors on est dans une ville.
Assez simple et rapide à mettre en place.

```python
import json
import sys
import copy

from group.load_images import load_images_from_paths_list
from group.clusterization import clusterize

clusters = {}

with sys.stdin as database:
  clusters = json.load(database)


def urbanize(clusters: dict):
  clusters_copy = copy.deepcopy(clusters)
  for cluster in clusters:
    cluster_data = clusters[cluster]
    cluster_len = len(cluster_data["photos"])
    if cluster_len > 150:
      paths_list = list(cluster_data["photos"].values())
      data_images = load_images_from_paths_list(paths_list)
      del clusters_copy[cluster]
      # Clusterization par coordonnées GPS (Point les proches proche à 200m)
      new_clusters = clusterize(data_images, 0.5)
      for id, new_cluster in new_clusters.items():
        if id != "ICanGroupThem":
          clusters_copy[int(cluster) * 100 + int(id)] = new_cluster

  return clusters_copy


print(json.dumps(urbanize(clusters)))
```

Grace au refacto, 32 lignes de code. 

Je ne voulais plus m'embeter avec des fichiers. Le script prend par defaut l'entrée standard et retourne le resultat sur la sortie standard.

Le scirpt prend en entrée le fichier JSON qu'il faut reclusterizer et retourne le liste des clusters refactorizé.
Pour le différencier, je prends l'id du cluster initial * 100 plus l'id du nouveau cluster. Cela me peremt de voir de quelle cluster, on part 



## TODO

J'ai rajouté l'information de l'eps en km avec lequelle à été calculé les clusters 

Chnager la sensibilité du DBScan dans les ville et noté l'information comme quoi c'est un cluster de ville

Une fois que les noms des dossiers son modifié, il faut modifier les metadatas avec le nouveaux noms des dossiers