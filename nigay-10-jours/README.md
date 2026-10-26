# Kit de pratique — 10 jours de prise de poste Nigay

Ce dossier accompagne le **Guide d'apprentissage intensif — 10 jours** (Data & BI, digitalisation, IA générative).
Le guide donne les vidéos et les notions ; ce kit donne **des données sur lesquelles pratiquer** et **des exercices progressifs** pour chaque jour.

> **Toutes les données sont fictives.** Produits, clients, machines, mesures et volumes sont inventés.
> Seuls les noms des sites (Feurs, Nesle) sont publics. N'ajoute jamais de données internes Nigay dans ce dépôt.

---

## Contenu

```text
nigay-10-jours/
├── README.md                 ← ce fichier
├── data/                     ← jeu de données fictif (CSV, séparateur « ; »)
│   ├── production_brute.csv  2 138 lignes : lots de fabrication 2024 → sept. 2026 (avec défauts cachés)
│   ├── ventes.csv            2 322 lignes de facturation
│   ├── dim_produit.csv       24 caramels (famille, forme, spécifications qualité, prix)
│   ├── dim_client.csv        40 clients industriels
│   ├── dim_machine.csv       7 équipements
│   └── dim_atelier.csv       3 ateliers sur 2 sites
├── outils/
│   ├── generate_data.py      régénère les CSV (ne pas lire avant la fin du J2 !)
│   ├── init_duckdb.sql       charge les CSV dans une base DuckDB locale
│   └── run_sql.py            exécute un fichier .sql et affiche les résultats
├── jour-01/ … jour-10/       exercices.md + fiche.md pour chaque jour
```

## Installation (15 min)

1. **Python 3.10+** (tu l'as probablement déjà) puis :
   ```bash
   pip install duckdb
   ```
2. Se placer dans le dossier du kit et tester :
   ```bash
   cd nigay-10-jours
   python outils/run_sql.py --init
   ```
   Tu dois voir `✅ Données chargées dans nigay.duckdb`.
3. Facultatif mais confortable : l'interface web de DuckDB (notebook SQL dans le navigateur).
   Sous Windows : `winget install DuckDB.cli`, puis `duckdb nigay.duckdb -ui`.

Pourquoi **DuckDB** et pas SQLite Online comme suggéré dans le guide ? Les requêtes du J2 du guide utilisent la syntaxe PostgreSQL (`DATE_TRUNC`, `COUNT(*) FILTER (...)`). SQLite ne connaît pas `DATE_TRUNC` ; DuckDB exécute ces requêtes telles quelles, lit les CSV directement et tourne en local, sans serveur.

## Calendrier indicatif

Tu as choisi de suivre les 10 jours dans l'ordre, en parallèle de la prise de poste. Un « jour » du guide représente environ **5 à 6 h** : il peut être découpé en 2 ou 3 séances.

| Jour | Thème | Créneau proposé |
|---|---|---|
| J1 | Chaîne data & modèle en étoile | dimanche 25 oct. |
| J2 | SQL analytique & contrôle qualité | lundi 26 oct. |
| — | **Premier jour sur site** | **mardi 27 oct.** |
| J3 | Fabric & architecture Medallion | samedi 31 oct. |
| J4 | Ingestion, API FastAPI, planification | dimanche 1er nov. |
| J5 | Power BI, DAX, dictionnaire de KPI | soirs du 2 au 6 nov. |
| J6 | Dataverse & Power Apps | samedi 7 nov. |
| J7 | Power Automate | dimanche 8 nov. |
| J8 | RAG & Copilot Studio | soirs du 9 au 13 nov. |
| J9 | dbt & Airflow vs Microsoft | samedi 14 nov. |
| J10 | Projet intégrateur & pitch | dimanche 15 nov. |

⚠️ Ce rythme (≈ 14 h/semaine) dépasse la règle des 10 h/semaine du guide unifié. C'est acceptable **comme sprint de démarrage de trois semaines**, pas comme régime permanent. Si l'école ou l'entreprise demande plus, décale un jour plutôt que de rogner le sommeil.

**Après le 27 octobre, adapte les jours suivants à ce que tu observes sur place.** Si ton tuteur confirme par exemple qu'Airflow + dbt remplacent Fabric, le J9 devient plus important que le J3.

## Méthode de travail (coaching)

Pour chaque jour :

1. Regarder les vidéos **essentielles** du guide (1 h 30 max).
2. Faire `exercices.md` dans l'ordre — **sans chercher la solution toute faite**.
3. Remplir `fiche.md` avec tes propres mots.
4. M'envoyer tes réponses / ton fichier `.sql` / ta capture : je corrige, j'explique ce qui manque, puis on passe au jour suivant.

Règles :

- Une vidéo regardée n'est pas une compétence : seul compte ce que tu sais **refaire et expliquer**.
- Bloqué plus de 30 min sur une question ? Écris ce que tu as essayé et demande un **indice**, pas la solution.
- Note chaque erreur rencontrée dans la fiche : c'est ta meilleure source de révision.

## Corrections et précisions sur le guide

| Point du guide | Précision |
|---|---|
| « Liens vérifiés le 24/10/2026 » | Je n'ai pas revérifié chaque vidéo. Si un lien est mort, garde l'objectif du jour et prends une vidéo équivalente ou la documentation officielle. |
| SQL : SQLite Online | Remplacé par DuckDB (voir plus haut). |
| Essai Fabric, Power Apps Developer Plan, Copilot Studio | Ces essais exigent en général un **compte professionnel ou scolaire** Microsoft (pas un Gmail). Essaie ton compte Epitech. Chaque jour concerné propose une **alternative locale** si l'accès est impossible. |
| Contexte outils Nigay | D'après ce que ton tuteur t'a dit : SAP aujourd'hui et migration ERP prévue, coût de Fabric jugé élevé, intérêt pour Airflow + dbt sur site, retours mitigés sur Power Automate. **Rien de cela n'est confirmé par écrit** : apprends les principes, puis aligne-toi sur la stack réellement validée. |
| DAX `Dim_Date` jusqu'au 31/12/2026 | Couvre les données du kit (jusqu'à sept. 2026). En entreprise, génère la table de dates à partir des dates min/max réelles. |
| Fiche « Je sais refaire seule » | Corrigé en « seul » dans les fiches du kit. |

## Régénérer les données

```bash
python outils/generate_data.py
```

La graine est fixe : tu obtiens exactement les mêmes fichiers. Le script écrit aussi un fichier caché `.corrige_anomalies.json` : **ne l'ouvre qu'après avoir rendu ton J2.**
