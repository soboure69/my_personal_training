# Jour 9 — dbt & Airflow face à l'écosystème Microsoft : exercices

**Installation :** `pip install dbt-duckdb` (dbt sur la base DuckDB du kit). Airflow est facultatif (Docker).
**Livrables :** projet `dbt_nigay/`, `matrice_arbitrage.md`, `fiche.md`.

> Ce jour est peut-être **le plus directement utile** chez Nigay : ton tuteur a évoqué un passage vers Airflow + dbt sur site pour des raisons de coût. Cadre provisoire, à détailler avant le J9.

## Exercices

1. **Projet dbt.** Initialise `dbt_nigay` sur `nigay.duckdb` et réécris ta chaîne du J2/J3 en modèles :
   - `staging/stg_production.sql` (typage, dates aux deux formats) ;
   - `intermediate/int_production_dedup.sql` ;
   - `marts/fct_production.sql`, `marts/dim_produit.sql`, `marts/dim_machine.sql`.
   Les dépendances passent **uniquement** par `ref()` et `source()`.
2. **Tests.** Au minimum : `unique` et `not_null` sur les clés, `relationships` entre le fait et les dimensions, `accepted_values` sur `conforme`, plus un test personnalisé « rebuts ≤ quantité ». Lance `dbt build` : les anomalies connues doivent être détectées en staging et absentes des marts.
3. **Documentation.** `dbt docs generate` puis `dbt docs serve` : capture le graphe de lignage.
4. **Orchestration.** Écris un DAG Airflow : ingestion (J4) → `dbt build` → contrôle de fraîcheur → notification. Si Docker n'est pas disponible, écris-le sans l'exécuter et explique chaque paramètre (`schedule`, `retries`, `catchup`).
5. **Matrice d'arbitrage.** Reprends celle du guide et complète-la **pour le contexte d'une PME industrielle** : coût de licence ou de capacité, coût humain d'exploitation, compétences nécessaires, sécurité et gouvernance, dépendance à un éditeur, intégration avec l'ERP et sa future migration. Termine par une recommandation argumentée **et ses conditions** (ce qu'il faudrait vérifier avant de décider).

## Critères de réussite

- [ ] Je sais expliquer ce que dbt apporte par rapport à des scripts SQL isolés.
- [ ] Mes tests dbt détectent les défauts que j'avais trouvés à la main au J2.
- [ ] Ma recommandation présente des options, des coûts et des risques, et laisse la décision au métier.
