# Notes BackEnd
## 🚀 Pour l'installer proprement (venv):

Si vous avez fait beaucoup de tests, je vous conseille de "nettoyer" avant de réinstaller :

```Bash
pip freeze > uninstall.txt
pip uninstall -r uninstall.txt -y
pip install -r requirements.txt
```
(Ou supprimez simplement votre dossier venv et recréez-le).

---

## ✅ **Token**

➡️ C’est une **preuve d’authentification**.
➡️ Une petite chaîne de caractères envoyée par le serveur au client après un login réussi.
➡️ Le client l’envoie ensuite dans **Authorization: Bearer <token>** pour accéder aux routes protégées.

👉 **Il remplace le fait de renvoyer le mot de passe à chaque requête.**

---

## ✅ **JWT (JSON Web Token)**

➡️ C’est un **type particulier de token**.
➡️ Contient des informations encodées (ex : id utilisateur, expiration).
➡️ Est **signé** pour éviter la falsification.
➡️ Peut être vérifié **sans accéder à la base de données**.

Structure :
**header . payload . signature**

---

### 🧩 Résumé simple

* **Token** = billet d’accès.
* **JWT** = billet d’accès intelligent, signé, contenant des infos.

Voici **JWT brièvement** :

---

# ⚡ **JWT (JSON Web Token) — très bref**

Un **JWT** est un token d’authentification composé de trois parties :

```
header.payload.signature
```

### ✔️ **Header**

→ Indique le type de token et l’algorithme utilisé.

### ✔️ **Payload**

→ Contient les données (ex : id utilisateur, rôle).
→ Contient aussi une date d’expiration (`exp`).

### ✔️ **Signature**

→ Calculée avec une **clé secrète**.
→ Empêche de modifier le token frauduleusement.

### 🎯 **Utilité**

* S’authentifier sans renvoyer le mot de passe.
* Rapide : pas besoin d'interroger la base de données.
* Utilisé dans les APIs (Authorization: Bearer <token>).

---

Voici **4 exemples illustratifs**, simples et courts :

* **2 pour non-spécialistes (métaphores)**
* **2 techniques (abrégés)**

---

# 🧩 **A) Exemples pour non-spécialistes**

---

## ⭐ **1) CORS = le vigile d’un bâtiment**

Imagine une API comme un bâtiment.
Un site web (front-end) est un visiteur.

* Le **vigile (CORS)** vérifie :
  *“Ce visiteur vient-il d’un endroit autorisé ?”*

Si oui → il le laisse entrer.
Si non → **accès bloqué**, même si tout à l’intérieur fonctionne.

---

## ⭐ **2) Middleware = contrôle de sécurité à l’entrée**

Avant d’accéder aux bureaux (endpoints), un contrôle fouille ton sac.

* Le **middleware** inspecte chaque requête :
  ✔️ enlever les objets dangereux
  ✔️ noter des informations
  ✔️ ajouter des protections

Puis il laisse passer la requête vers le vrai bureau.

---

# 🛠 **B) Exemples techniques (abrégés)**

---

## ⚙️ **3) CORS technique :**

```
Frontend React (localhost:3000)
        ↓
API FastAPI (localhost:8000)
        ↓
Navigateur bloque la requête:  
"Origin non autorisée"
→ Ajouter CORS allow_origins pour autoriser ce domaine.
```

---

## ⚙️ **4) Middleware technique :**

Exemples réels FastAPI :

* **CORS middleware** → autorise domaines/headers/methods.
* **Authentication middleware** → vérifie un token JWT avant chaque requête.
* **Logging middleware** → écrit chaque requête dans un fichier log.
* **Compression middleware** → compresse les réponses (Gzip).

---

# 🎯 Résumé simple

* **CORS** : contrôle *d’où provient* la requête.
* **Middleware** : contrôle *comment* la requête est traitée avant d’arriver aux routes.


---

# 📩 **Headers (HTTP Headers)**

➡️ Ce sont des **informations supplémentaires** envoyées avec une requête ou réponse HTTP.
➡️ Ils décrivent **comment** la requête doit être traitée ou **ce que contient** la réponse.

---

# ✔️ À quoi servent les headers ?

### 1️⃣ **Envoyer des informations sur le client**

Ex : type de navigateur

```
User-Agent: Mozilla/5.0
```

### 2️⃣ **Envoyer des données d’authentification**

Ex : token JWT

```
Authorization: Bearer <token>
```

### 3️⃣ **Indiquer le format des données**

```
Content-Type: application/json
```

### 4️⃣ **Contrôler la sécurité, le cache, le CORS, etc.**

Ex :

```
Access-Control-Allow-Origin: *
```

---

# 🎯 Résumé ultra simple

**Les headers = des métadonnées.**
Ils indiquent *qui envoie*, *comment*, *sous quel format* et *avec quelle permission*.


---
Voici la logique la plus simple et directe pour relier Python à PostgreSQL, en utilisant la bibliothèque standard **SQLAlchemy** (c'est plus facile que d'écrire du SQL pur).

### 1\. Installation (Les outils)

Vous avez besoin du "traducteur" (driver) et de l'outil de gestion (ORM).
Dans le terminal :

```bash
pip install sqlalchemy psycopg2-binary
```

### 2\. Le Code (La logique en 4 étapes)

Voici le schéma minimal pour que ça marche :

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# ÉTAPE 1 : L'Adresse de connexion (Connection String)
# Format : postgresql://utilisateur:motdepasse@adresse_serveur:port/nom_bdd
DATABASE_URL = "postgresql://postgres:monpassword@localhost:5432/mabase"

# ÉTAPE 2 : Le Moteur (Créer la liaison)
engine = create_engine(DATABASE_URL)

# ÉTAPE 3 : La Session (L'outil pour envoyer/recevoir des données)
Session = sessionmaker(bind=engine)
session = Session()

# ÉTAPE 4 : Le Modèle (Définir à quoi ressemble votre table en Python)
Base = declarative_base()

class Utilisateur(Base):
    __tablename__ = 'utilisateurs' # Nom de la table dans Postgres
    id = Column(Integer, primary_key=True)
    nom = Column(String)

# --- Action ! ---

# Crée automatiquement la table dans Postgres si elle n'existe pas
Base.metadata.create_all(engine)

print("Connexion réussie et table prête !")
```

### Résumé de la logique :

1.  **URL :** On définit **où** est la base.
2.  **Engine :** On ouvre le **tuyau** vers la base.
3.  **Model :** On décrit la **forme** des données (colonnes) en code Python.
4.  **Create All :** Python envoie l'ordre à Postgres de **créer** les tables correspondantes.
5.  **Session :** On utilise cet objet pour **ajouter** ou **lire** des données par la suite.

---

## **httpx** vs **http**
* `httpx` = outil Python moderne pour envoyer des requêtes HTTP (synchro + async).
* `http` = le protocole ou le module bas niveau, pas comparable.