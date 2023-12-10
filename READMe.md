# Projet 9 DA-Python OC (Fouchal Sami)

***Livrable du Projet 9 du parcours D-A Python d'OpenClassrooms : MVP de LITReview, site communautaire de partage de critiques de livres ou d'article.***

_Testé sous Windows 10 - Python 3.11.4 - Django 4.2.7_

## Initialisation du projet

### Windows :
Dans Windows Powershell, naviguer vers le dossier souhaité.
###### • Récupération du projet

```
git clone https://github.com/Gaiden92/P9OC.git
```

###### • Activer l'environnement virtuel

```
cd P9OC 
python -m venv env 
env\Scripts\activate
```

###### • Installer les paquets requis

```
pip install -r requirements.txt
```


### MacOS et Linux :
Dans le terminal, naviguer vers le dossier souhaité.
###### • Récupération du projet
```
git clone https://github.com/Gaiden92/P9OC.git
```

###### • Activer l'environnement virtuel
```
cd P9OC 
python3 -m venv env 
source env/bin/activate
```

###### • Installer les paquets requis
```
pip install -r requirements.txt
```

## Utilisation

1. Effectuer les migrations

```
python manage.py makemigrations

```
python manage.py migrate

```

2. Lancer le serveur Django:

```
python manage.py runserver

```

3. Dans le navigateur de votre choix, se rendre à l'adresse http://127.0.0.1:8000/


## Infos

### Django administration

Identifiant : **Admin** | Mot de passe : **samifouchal92**

&rarr; http://127.0.0.1:8000/admin/

### Liste des utilisateurs existants

| *Identifiant* | *Mot de passe* |
|---------------|----------------|
| toto          | password123    |
| tata          | password123    |
| titi          | password123    |
| tutu          | password123    |
| momo          | password123    |
| mimi          | password123    |
| mumu          | password123    |


### Fonctionnalités

- S'inscrire et se connecter;
- Consulter un flux contenant les tickets et critiques des utilisateurs auxquels on est abonné ;
- Créer des tickets de demande de critique ;
- Créer des critiques, en réponse ou non à des tickets ;
- Voir ses propres posts, les modifier ou les supprimer ;
- Suivre d'autres utilisateurs, ou se désabonner.