# Jour 3 — Microsoft Fabric & architecture Medallion : exercices

**Prérequis :** J2 terminé (tu sais ce qu'il faut nettoyer et pourquoi).
**Livrables :** captures du workspace et des tables, notebook exporté, `reponses.md`, `fiche.md`.

> Je détaillerai ces exercices après la correction du J2, en tenant compte de ce que tu auras vu chez Nigay le 27. Voici déjà le cadre.

## Accès

- **Option A — Fabric (recommandée si l'accès marche) :** essai gratuit de 60 jours sur app.fabric.microsoft.com, avec un compte professionnel ou scolaire (essaie ton compte Epitech).
- **Option B — en local, si Fabric est inaccessible :** même architecture avec DuckDB et des fichiers Parquet, dans `jour-03/lakehouse/bronze|silver|gold/`. C'est aussi plus proche d'une architecture sur site (Airflow + dbt) si c'est la direction que confirme Nigay.

## Exercices

1. **Bronze.** Charge `production_brute.csv` **sans aucune transformation**, avec deux colonnes techniques en plus : `_date_ingestion` et `_fichier_source`. Pourquoi ces deux colonnes sont-elles indispensables pour la traçabilité ?
2. **Silver.** Reprends ta logique du J2 (dédoublonnage, typage, dates aux deux formats, colonne `anomalie`) et écris-la en **PySpark** (option A) ou en SQL DuckDB vers Parquet (option B). Résultat : une table `silver_production`.
3. **Gold.** Construis le modèle en étoile conçu au J1 : `gold_fait_production`, `gold_dim_produit`, `gold_dim_machine` (aplatie avec atelier et site), `gold_dim_date`. Seules les lignes sans anomalie entrent dans le fait.
4. **Contrôles.** Écris trois vérifications automatiques entre couches :
   - nombre de lots distincts en Bronze = lignes Silver ;
   - lignes Silver saines = lignes du fait Gold ;
   - somme des quantités saines identique en Silver et en Gold.
5. **Delta.** (Option A) Exécute `DESCRIBE HISTORY` sur une table, modifie une ligne, puis relis l'ancienne version (*time travel*). À quoi cela sert-il lors d'un audit qualité ?
6. **Questions.** Écris tes réponses argumentées :
   - Un seul Lakehouse avec des préfixes, ou trois Lakehouses ? Avantages et inconvénients.
   - Que se passe-t-il si quelqu'un nettoie directement en Bronze ?
   - Fabric coûte cher pour une PME : quelles options d'architecture pourrais-tu présenter à ton tuteur, et avec quels critères de comparaison ?

## Critères de réussite

- [ ] Je sais expliquer le rôle de chaque couche en une phrase.
- [ ] Mes trois contrôles entre couches passent.
- [ ] Je sais ce qu'est une table Delta (Parquet + journal de transactions).
