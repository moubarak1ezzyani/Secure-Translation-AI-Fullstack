# Notes Docker
### 📌 Rôle des instructions Docker

- **EXPOSE**  
  - Sert à **documenter** le port sur lequel l’application écoute à l’intérieur du conteneur.  
  - Exemple : `EXPOSE 8000` indique que l’app utilise le port 8000.  
  - ⚠️ Cela **n’ouvre pas** le port automatiquement, mais informe Docker et les autres développeurs. Pour rendre le port accessible, il faut utiliser `-p` ou `--publish` lors du `docker run`.  

- **ENTRYPOINT**  
  - Définit la **commande principale** qui sera toujours exécutée quand le conteneur démarre.  
  - Exemple :  
    ```dockerfile
    ENTRYPOINT ["uvicorn", "main:app"]
    ```  
    → Le conteneur lancera toujours Uvicorn.  
  - Différence avec `CMD` : `ENTRYPOINT` fixe la commande, tandis que `CMD` fournit des arguments par défaut (mais peut être remplacé).  

---

👉 Bref :  
- **EXPOSE** = annonce le port utilisé.  
- **ENTRYPOINT** = commande de démarrage obligatoire du conteneur.  

Veux-tu que je te montre un **exemple combiné ENTRYPOINT + CMD** pour voir comment ils interagissent ensemble ?
