# Jour 4 — Ingestion, API FastAPI & planification : exercices

**Livrables :** dossier `api/` (code + tests), script d'ingestion, captures du pipeline (si Fabric), `fiche.md`.

> Cadre provisoire, à détailler après le J3.

## Exercices

1. **Une API qui expose les données du kit.** Avec FastAPI, crée :
   - `GET /lots/{num_lot}` : renvoie un lot (404 s'il n'existe pas) ;
   - `GET /lots?date_debut=…&date_fin=…&page=1&taille=100` : lots d'une période, **paginés** ;
   - `POST /anomalies` : enregistre une déclaration d'anomalie validée par un modèle **Pydantic** (gravité limitée à `Mineure | Majeure | Critique`, description obligatoire, `num_lot` existant).
   Vérifie la documentation automatique sur `/docs`.
2. **Tests.** Avec `pytest` et `TestClient` : un cas 200, un cas 404, un cas 422 (gravité invalide).
3. **Un client d'ingestion robuste.** Script Python qui interroge `GET /lots` page par page et écrit le résultat en Bronze, avec :
   - un *timeout* et 3 tentatives maximum en cas d'erreur ;
   - un **chargement incrémental** : on ne récupère que les lots postérieurs à la dernière date déjà chargée ;
   - aucun identifiant en dur (variables d'environnement).
4. **Idempotence.** Lance ton ingestion deux fois de suite. Le nombre de lignes en Bronze doit rester identique. Si ce n'est pas le cas, corrige.
5. **Planification.** Option Fabric : pipeline `PL_Ingestion_Production` = Copie → Notebook Silver → Notebook Gold, planifié à 6 h, avec une alerte en cas d'échec. Option locale : décris le même enchaînement sous forme de DAG Airflow (sur papier ou en code, il sera exécuté au J9).

## Critères de réussite

- [ ] Je connais les codes HTTP 200, 201, 404, 422 et 500.
- [ ] Mon ingestion est incrémentale **et** idempotente, et je sais expliquer la différence.
- [ ] Aucun secret n'est présent dans le code.
