# Notes Frontend
## Arborescence generee du frontend
### 📂 À la racine (Le "Garage" & La "Paperasse")

* **`package.json`**
    * **Rôle :** Liste les ingrédients (librairies) et les commandes de lancement.
    * **Analogie :** La **Carte d'identité** + Le **Livre de recettes** du projet.
* **`package-lock.json`**
    * **Rôle :** Verrouille les versions exactes des dépendances pour que tout le monde ait le même code.
    * **Analogie :** La **Photo figée** de votre garde-manger à l'instant T.
* **`next.config.mjs`**
    * **Rôle :** Configuration avancée du serveur Next.js (rarement touché au début).
    * **Analogie :** Le **Capot moteur** (on l'ouvre pour des réglages pointus).
* **`tsconfig.json`**
    * **Rôle :** Définit la rigueur du TypeScript.
    * **Analogie :** Le **Bescherelle** (les règles de grammaire que le code doit respecter).
* **`tailwind.config.ts`**
    * **Rôle :** Personnalise les couleurs, polices et espacements de Tailwind.
    * **Analogie :** La **Palette du peintre** (quelles couleurs sont disponibles).
* **`postcss.config.js`**
    * **Rôle :** Outil technique qui transforme le CSS Tailwind en CSS standard.
    * **Analogie :** Le **Traducteur** (rend le style compréhensible par le navigateur).
* **`.eslintrc.json`**
    * **Rôle :** Détecte les mauvaises pratiques de code.
    * **Analogie :** Le **Professeur sévère** qui surveille votre syntaxe.
* **`.gitignore`**
    * **Rôle :** Liste les fichiers à ne jamais envoyer sur GitHub (clés, gros dossiers temporaires).
    * **Analogie :** La **Liste noire** des objets à laisser à la maison.

---

### 📂 Dossier `app/` (La "Maison" habitable)

* **`layout.tsx`**
    * **Rôle :** Structure globale (`<html>`, `<body>`) qui enveloppe toutes les pages.
    * **Analogie :** Les **Murs porteurs et le Toit** de la maison (toujours là, même si on change de pièce).
* **`page.tsx`**
    * **Rôle :** Le contenu spécifique de la page d'accueil (votre `/`).
    * **Analogie :** Les **Meubles** dans le salon (ce qu'on voit et utilise).
* **`globals.css`**
    * **Rôle :** Styles CSS appliqués à toute l'application.
    * **Analogie :** La **Peinture des murs** (l'ambiance générale).

---

### 📂 Dossier `public/` (Le "Débarras" public)

* **`next.svg` / `vercel.svg`** (et autres images)
    * **Rôle :** Fichiers statiques accessibles directement via URL (ex: `/next.svg`).
    * **Analogie :** Le **Présentoir à flyers** sur le trottoir (tout le monde peut se servir).

---

### 📂 Dossier `node_modules/` (L' "Usine")
*(Généré automatiquement, n'apparaît pas toujours dans l'éditeur mais présent sur le disque)*
* **Rôle :** Stocke les milliers de fichiers des librairies téléchargées.
* **Analogie :** La **Salle des machines** (immense, bruyante, on n'y touche jamais, mais sans elle, rien ne tourne).