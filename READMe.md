
<p align="center">
    <img src="logo.png" alt="logo" />
</p>
<h1 align="center">Développez une application Web en utilisant Django</h1>
<p align="center">
    <a href="https://www.python.org">
        <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white" alt="python-badge">
    </a>
    <a href="https://docs.djangoproject.com/en/5.0/">
        <img src="https://img.shields.io/badge/Django-4.12+-d71b60?style=flat" alt="Django">
    </a>
</p>

***Livrable du Projet 9 du parcours D-A Python d'OpenClassrooms : MVP de LITReview, site communautaire de partage de critiques de livres ou d'article.***

_Testé sous Windows 10 - Python 3.12 - Django 4.2.7_

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
```
### MacOS et Linux :

```
source env/bin/activate
```
### Windows :

```
env\Scripts\activate
```

###### • Installer les paquets requis

```
pip install -r requirements.txt
```

###### • Créer un fichier .env qui contiendra la secret-key de votre application Django

```
SECRET_KEY="votre secret key"

```

## Utilisation

1. Effectuer les migrations

```
python manage.py makemigrations
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

| *Identifiant*   | *Mot de passe* |
|-----------------|----------------|
| claudy          | password123    |
| jeremy          | password123    |
| ouahid          | password123    |
| thomas          | password123    |
| edi             | password123    |



### Fonctionnalités

- S'inscrire et se connecter;
- Consulter un flux contenant les tickets et critiques des utilisateurs auxquels on est abonné ;
- Créer des tickets de demande de critique ;
- Créer des critiques, en réponse ou non à des tickets ;
- Voir ses propres posts, les modifier ou les supprimer ;
- Suivre d'autres utilisateurs, ou se désabonner.