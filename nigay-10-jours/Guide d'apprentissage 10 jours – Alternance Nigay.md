# Guide d'apprentissage intensif — 10 jours pour l'alternance Nigay
### Data & BI · Digitalisation des processus · IA générative

> Légende : 🇫🇷 = vidéo en français · 🇬🇧 = vidéo en anglais (à défaut de bonne ressource FR).
> Rythme conseillé par jour : 1 h 30 de vidéos, 3 à 4 h de pratique, 30 min pour remplir la fiche.
> Les liens ont été vérifiés sur YouTube le 24/10/2026.

---

## Mode d'emploi

Chaque jour suit la même séquence :
1. **Regarder** les vidéos « Essentielles » (l'ordre est pensé pour progresser).
2. **Pratiquer** l'exercice du jour sur un cas Nigay (production, qualité, anomalies, ventes).
3. **Remplir la fiche** (modèle en fin de guide). Une version pré-remplie est donnée pour chaque jour : complétez-la avec vos propres mots.
4. Les vidéos « Pour aller plus loin » sont optionnelles.

Environnements gratuits utiles :
- Microsoft Fabric : essai gratuit 60 jours (app.fabric.microsoft.com)
- Power Apps / Power Automate / Copilot Studio : Developer Plan gratuit (Power Apps Developer Plan)
- Power BI Desktop : gratuit (Windows)
- SQL : SQLite Online, ou PostgreSQL local ; Python 3.11+ pour FastAPI, dbt, Airflow

---

# BLOC 1 — Fondations Data & Ingénierie des données (Jours 1 à 4)

## Jour 1 — Chaîne Data & modélisation en étoile

**Objectif** : comprendre le parcours d'une donnée, de la source (SAP, fichiers) au tableau de bord.

### Vidéos essentielles
| # | Vidéo | Langue | Pourquoi |
|---|---|---|---|
| 1 | [Comprendre le Star Schema, schéma en étoile, table de fait et dimensions](https://www.youtube.com/watch?v=naXjcM8DnEw) | 🇫🇷 | Base du jour |
| 2 | [Modèle en étoile vs flocon vs constellation](https://www.youtube.com/watch?v=SfNwpVa49N8) | 🇫🇷 | Variantes de modèles |
| 3 | [DAX (Power BI) – Module 0, Vidéo 2 : Le schéma en étoile et comment Power BI pense ses requêtes](https://www.youtube.com/watch?v=AfBTPZPIigU) | 🇫🇷 | Lien étoile ↔ Power BI |
| 4 | [Data Engineer Basics : OLTP, OLAP & Data Warehouse](https://www.youtube.com/watch?v=bDRIZD-5H2Y) | 🇬🇧 | OLTP vs OLAP |

### Pour aller plus loin
- 🇫🇷 [Mini-atelier : créer le schéma en étoile dédié aux ventes](https://www.youtube.com/watch?v=1HAy2RCUQ0s)
- 🇬🇧 [Difference Between OLTP and OLAP (with examples)](https://www.youtube.com/watch?v=qciTd_aXOYY)

### Notions à maîtriser
- **OLTP** (transactionnel : SAP, saisie, beaucoup d'écritures, normalisé) vs **OLAP** (analytique : lecture, agrégats, dénormalisé).
- **Grain** : « une ligne = un événement unitaire » (ex. une ligne = un lot produit sur une ligne de fabrication un jour donné). C'est la première décision à prendre.
- **Faits** : mesures numériques additives (quantité, durée d'arrêt, nombre de rebuts).
- **Dimensions** : axes d'analyse (Date, Produit, Client, Atelier, Machine, Type d'anomalie).
- **Clés** : clé de substitution (surrogate key, entier) dans la dimension, clé étrangère dans le fait ; la clé métier (code article SAP) est conservée en attribut.

### Pratique
Dessinez (draw.io, Excalidraw ou papier) :
`Source SAP / CSV → Pipeline Fabric → Lakehouse (Bronze/Silver/Gold) → Modèle sémantique → Rapport Power BI`
puis le schéma en étoile `Fait_Production` avec `Dim_Date`, `Dim_Produit`, `Dim_Atelier`, `Dim_Machine`.

### Fiche pré-remplie
- **Problème métier** : les données de production sont dispersées (SAP, Excel), on ne peut pas analyser vite ni de façon fiable.
- **Outils** : SAP (source), Fabric, Power BI, outil de schéma.
- **Entrées / Sorties** : extractions de tables SAP, CSV → modèle en étoile documenté.
- **Étapes** : identifier le processus → fixer le grain → lister les dimensions → lister les mesures → définir les clés.
- **Pièges** : mélanger deux grains dans un même fait ; relations plusieurs-à-plusieurs ; garder des données SAP trop normalisées (modèle en flocon).
- **Je sais refaire seule / À valider** : dessiner une étoile / quelles tables SAP sont réellement disponibles (modules PP, QM, SD ?).

---

## Jour 2 — SQL analytique & contrôle qualité

**Objectif** : interroger, nettoyer, transformer et contrôler la qualité des données en SQL.

### Vidéos essentielles
| # | Vidéo | Langue |
|---|---|---|
| 1 | [SQL Server : CTE, CTE récursives et fonctions de fenêtrage](https://www.youtube.com/watch?v=v4TZ_M6g1BQ) | 🇫🇷 |
| 2 | [Apprendre et maîtriser SQL : fonctions de fenêtrage](https://www.youtube.com/watch?v=qeqpmge-qZA) | 🇫🇷 |
| 3 | [[SQL #10] LAG() et LEAD() expliqués simplement](https://www.youtube.com/watch?v=flJ6m-ili4U) | 🇫🇷 |
| 4 | [SQL CTEs Explained — WITH clause for beginners](https://www.youtube.com/watch?v=Koka7IGgPM4) | 🇬🇧 |

### Pour aller plus loin
- 🇬🇧 [SQL Window Functions Explained: The Complete Guide](https://www.youtube.com/watch?v=gFV6QA7bWPQ)
- 🇬🇧 [SQL Window Functions You MUST Know to Crack Interviews](https://www.youtube.com/watch?v=3wI6_Dv-eI8)

### Notions à maîtriser
- Ordre logique d'exécution : `FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY`.
- `WHERE` filtre les lignes, `HAVING` filtre les groupes.
- `LEFT JOIN` conserve toutes les lignes de gauche → idéal pour détecter des orphelins (`WHERE d.id IS NULL`).
- CTE : `WITH etape1 AS (...), etape2 AS (...) SELECT ...`.
- Fenêtrage : `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)`, `RANK`, `LAG`, `LEAD`.

### Pratique (à exécuter)
```sql
-- 1. CA mensuel + comparaison avec le mois précédent
WITH ca_mensuel AS (
  SELECT DATE_TRUNC('month', date_vente) AS mois,
         SUM(montant)                   AS ca
  FROM ventes
  GROUP BY 1
)
SELECT mois, ca,
       LAG(ca) OVER (ORDER BY mois)                          AS ca_mois_prec,
       ROUND(100.0 * (ca - LAG(ca) OVER (ORDER BY mois))
             / NULLIF(LAG(ca) OVER (ORDER BY mois), 0), 1)  AS evolution_pct
FROM ca_mensuel
ORDER BY mois;

-- 2. Dédoublonnage : garder la dernière version de chaque lot
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY num_lot ORDER BY date_maj DESC) AS rn
  FROM production_brute
)
SELECT * FROM ranked WHERE rn = 1;

-- 3. Contrôles qualité
SELECT COUNT(*) FILTER (WHERE quantite < 0)      AS qte_negatives,
       COUNT(*) FILTER (WHERE code_article IS NULL) AS articles_vides
FROM production_brute;

SELECT p.* FROM production p
LEFT JOIN dim_produit d ON p.code_article = d.code_article
WHERE d.code_article IS NULL;   -- orphelins
```

### Fiche pré-remplie
- **Problème métier** : doublons, valeurs aberrantes et références manquantes faussent les KPI.
- **Pièges** : division par zéro (`NULLIF`) ; `COUNT(col)` ignore les NULL ; un JOIN qui multiplie les lignes (vérifier le nombre de lignes avant et après).

---

## Jour 3 — Microsoft Fabric & architecture Medallion

**Objectif** : comprendre l'écosystème Fabric et organiser les données en Bronze / Silver / Gold.

### Vidéos essentielles
| # | Vidéo | Langue |
|---|---|---|
| 1 | [Microsoft Fabric pour débutants : par où commencer quand on vient de Power BI ?](https://www.youtube.com/watch?v=imLlUm7PiZM) | 🇫🇷 |
| 2 | [Microsoft Fabric Lakehouse : apprends à ingérer tes données en 15 minutes](https://www.youtube.com/watch?v=J1QZtsxcnP0) | 🇫🇷 |
| 3 | [Les avantages d'une architecture en médaillon pour vos projets Fabric](https://www.youtube.com/watch?v=wVYYV-rI9Z0) | 🇫🇷 |
| 4 | [Create a medallion architecture in a Microsoft Fabric lakehouse](https://www.youtube.com/watch?v=hITkBPHxs7k) | 🇬🇧 (pratique) |

### Pour aller plus loin
- 🇬🇧 [Microsoft Fabric Explained : OneLake, Lakehouse & all workloads](https://www.youtube.com/watch?v=BNCur4HFZsU)
- 🇬🇧 [Organize your Fabric lakehouse using a medallion architecture (Lab)](https://www.youtube.com/watch?v=f-LFDCoo0bQ)
- 🇬🇧 [Microsoft Fabric End-to-End Project : from SQL to Power BI](https://www.youtube.com/watch?v=3ESSrFpMbQI)

### Notions à maîtriser
- **Workspace** : conteneur de projet (droits, capacité).
- **OneLake** : un seul lac de données pour toute l'organisation (le « OneDrive des données »).
- **Lakehouse** : zone `Files` (fichiers bruts) + zone `Tables` (tables Delta) + point de terminaison SQL en lecture.
- **Delta** = fichiers Parquet + journal de transactions `_delta_log` (ACID, historique, time travel).
- **Bronze** : brut, horodaté, traçable. **Silver** : typé, nettoyé, dédoublonné. **Gold** : agrégé, en étoile, prêt pour Power BI.

### Pratique
1. Créer un workspace `Nigay_Formation` (essai Fabric).
2. Créer 3 Lakehouses : `LH_Bronze`, `LH_Silver`, `LH_Gold` (ou un seul avec des préfixes de tables).
3. Charger un CSV de production dans `Files`, puis « Charger dans une table ».
4. Dans un notebook, écrire la transformation Bronze → Silver :
```python
df = spark.read.table("bronze_production")
from pyspark.sql import functions as F
silver = (df.dropDuplicates(["num_lot"])
            .withColumn("date_prod", F.to_date("date_prod", "dd/MM/yyyy"))
            .filter(F.col("quantite") >= 0))
silver.write.mode("overwrite").format("delta").saveAsTable("silver_production")
```

### Fiche pré-remplie
- **Pièges** : nettoyer directement en Bronze (on perd la traçabilité) ; formats de dates FR mal interprétés ; oublier de nommer et documenter les couches.

---

## Jour 4 — Data Factory, API (FastAPI) & planification

**Objectif** : automatiser l'ingestion depuis plusieurs sources (API, SharePoint, SQL) et planifier les exécutions.

### Vidéos essentielles
| # | Vidéo | Langue |
|---|---|---|
| 1 | [Ingestion et transformation de données avec Data Factory dans Microsoft Fabric](https://www.youtube.com/watch?v=-JnXIwmujOM) | 🇫🇷 |
| 2 | [Ingérer des données avec des flux de données Gen2 dans Microsoft Fabric](https://www.youtube.com/watch?v=XUSQKcBf0Qc) | 🇫🇷 |
| 3 | [Créer une API en Python avec FastAPI](https://www.youtube.com/watch?v=pxhBixh6f7Y) | 🇫🇷 |
| 4 | [Microsoft Fabric Pipeline in 10 Minutes](https://www.youtube.com/watch?v=dsVuhoKTJrk) | 🇬🇧 |

### Pour aller plus loin
- 🇫🇷 [Playlist Python et FastAPI : 1. Introduction à FastAPI](https://www.youtube.com/watch?v=MRgEsgjcI30&list=PLo53cbpzes8Z1lVzjKGeL_DJ7Hij3vmRt)
- 🇫🇷 [FastAPI en Python : c'est quoi et pourquoi l'utiliser ? (Pydantic, Uvicorn…)](https://www.youtube.com/watch?v=PJQEyghYmzg)
- 🇬🇧 [Data Cleaning with PySpark Notebook in Microsoft Fabric](https://www.youtube.com/watch?v=5K07LSYalK8)
- 🇬🇧 [Dataflow Gen2 – Low-Code ETL in Fabric](https://www.youtube.com/watch?v=MikCyAEmsis)

### Notions à maîtriser
- **Pipeline** = orchestrateur (activités : Copie de données, Notebook, Dataflow, conditions, boucles ForEach).
- **Dataflow Gen2** = Power Query en ligne (transformations sans code).
- **Notebook** = Python/PySpark pour les transformations complexes.
- **Planification** : onglet Schedule du pipeline (ex. tous les jours à 6 h).
- **API REST** : endpoints GET/POST, JSON, codes HTTP (200, 404, 500), documentation auto `/docs`.

### Pratique
1. Mini-API locale qui simule un capteur machine :
```python
# main.py  —  pip install fastapi uvicorn  —  uvicorn main:app --reload
from fastapi import FastAPI
from datetime import datetime
import random
app = FastAPI()

@app.get("/mesures/{machine_id}")
def mesures(machine_id: str):
    return {"machine": machine_id, "horodatage": datetime.now().isoformat(),
            "temperature": round(random.uniform(60, 90), 1),
            "pieces_produites": random.randint(80, 120)}
```
2. Dans Fabric : pipeline `PL_Ingestion_Production` = Copie (CSV/SharePoint → Bronze) → Notebook (Bronze → Silver) → Notebook (Silver → Gold) → planification quotidienne.

### Fiche pré-remplie
- **Pièges** : identifiants en dur dans le code (utiliser les connexions sécurisées) ; pas de gestion d'échec (ajouter une alerte « en cas d'échec ») ; recharger tout au lieu d'un chargement incrémental.

---

# BLOC 2 — Business Intelligence & restitution (Jour 5)

## Jour 5 — Power BI, modélisation, DAX & dictionnaire de KPI

**Objectif** : concevoir des tableaux de bord professionnels, performants et réutilisables.

### Vidéos essentielles
| # | Vidéo | Langue |
|---|---|---|
| 1 | [Power BI #10 : réaliser des calculs avec le langage DAX](https://www.youtube.com/watch?v=y2mFEmEH0KY) | 🇫🇷 |
| 2 | [Comprendre le contexte de filtre avec CALCULATE](https://www.youtube.com/watch?v=L50TZY-OZ1o) | 🇫🇷 |
| 3 | [Créer une table de dates dans Power BI (Power Query & DAX)](https://www.youtube.com/watch?v=x55xMwaeBOc) | 🇫🇷 |
| 4 | [Exercice Power BI : modélisation, DAX et KPI dynamiques](https://www.youtube.com/watch?v=1Kokkl5PybM) | 🇫🇷 |

### Pour aller plus loin
- 🇫🇷 [DAX Module 1, Vidéo 8 : tables calculées (table de dates)](https://www.youtube.com/watch?v=CyNZE40aias)
- 🇫🇷 [Power BI : DAX et modélisation des données](https://www.youtube.com/watch?v=Cjbp_x8lVA0)
- 🇬🇧 [CALCULATE, CALCULATETABLE – DAX Guide (SQLBI)](https://www.youtube.com/watch?v=5eikzMqUck0)

### Notions à maîtriser
- Relations **1 → *** de la dimension vers le fait, filtrage à sens unique.
- **Mesures** (calculées à la volée) plutôt que colonnes calculées (stockées, alourdissent le modèle).
- Table de dates marquée « table de dates » : indispensable pour `TOTALYTD`, `SAMEPERIODLASTYEAR`, `DATEADD`.
- Contexte de ligne vs contexte de filtre ; `CALCULATE` modifie le contexte de filtre.

### Pratique — mesures de base
```dax
Quantité produite = SUM(Fait_Production[Quantite])
Quantité rebutée  = SUM(Fait_Production[Rebuts])
Taux de rebut %   = DIVIDE([Quantité rebutée], [Quantité produite])
Nb lots           = DISTINCTCOUNT(Fait_Production[NumLot])
Qté Atelier A     = CALCULATE([Quantité produite], Dim_Atelier[Atelier] = "A")
Qté M-1           = CALCULATE([Quantité produite], DATEADD(Dim_Date[Date], -1, MONTH))
Évolution M-1 %   = DIVIDE([Quantité produite] - [Qté M-1], [Qté M-1])

Dim_Date = ADDCOLUMNS(CALENDAR(DATE(2024,1,1), DATE(2026,12,31)),
   "Année", YEAR([Date]), "Mois", FORMAT([Date],"MMM"), "NumMois", MONTH([Date]))
```
Rapport : 4 cartes KPI, courbe de tendance mensuelle, histogramme par atelier, segments (date, atelier, produit).

### Modèle de dictionnaire de KPI
| KPI | Définition métier | Formule DAX | Source / table | Grain | Fréquence | Propriétaire |
|---|---|---|---|---|---|---|
| Taux de rebut | Part des pièces non conformes | `DIVIDE([Rebuts],[Qté produite])` | Gold.Fait_Production | Lot / jour | Quotidien | Resp. Qualité |
| TRS | Disponibilité × Performance × Qualité | à définir | Gold.Fait_Machine | Machine / poste | Quotidien | Resp. Production |

### Fiche pré-remplie
- **Pièges** : relations bidirectionnelles partout ; utiliser `/` au lieu de `DIVIDE` ; même KPI calculé différemment selon les services (d'où le dictionnaire).

---

# BLOC 3 — Digitalisation des processus & low-code (Jours 6 et 7)

## Jour 6 — Dataverse & Power Apps

**Objectif** : dématérialiser les processus papier avec une base relationnelle et une application de saisie.

### Vidéos essentielles
| # | Vidéo | Langue |
|---|---|---|
| 1 | [Dataverse expliqué simplement : tables, colonnes, relations](https://www.youtube.com/watch?v=dB7AejY_FYA) | 🇫🇷 |
| 2 | [Créer un formulaire Power Apps : tutoriel complet](https://www.youtube.com/watch?v=kTtje5YAkew) | 🇫🇷 |
| 3 | [Easy Power Apps : les formulaires](https://www.youtube.com/watch?v=R1DfFw5UYw0) | 🇫🇷 |
| 4 | [Les rôles de sécurité Power Apps](https://www.youtube.com/watch?v=2pLnLOLUUi0) | 🇫🇷 |

### Pour aller plus loin
- 🇬🇧 [Power Apps Dataverse Tutorial for Beginners : tables, lookups & relationships (real project)](https://www.youtube.com/watch?v=461MMfVe6gs)
- 🇬🇧 [Dataverse Table Types with a Real-World Example](https://www.youtube.com/watch?v=hX4UStkuZXg)
- 🇬🇧 [Managing Dataverse Security Roles with Power Apps](https://www.youtube.com/watch?v=BZAoQBAUcPU)

### Notions à maîtriser
- Types de colonnes : texte, choix (liste fermée), date, nombre, devise, fichier/image, **recherche (Lookup)**.
- Relations 1-à-plusieurs (un atelier → plusieurs anomalies) ; plusieurs-à-plusieurs à éviter si possible.
- **Canvas app** (interface libre, mobile) vs **model-driven app** (générée depuis Dataverse, formulaires et vues).
- Sécurité : rôles (création / lecture / écriture), niveaux (utilisateur, unité, organisation).

### Pratique — application « Déclaration d'anomalies »
- Tables : `Anomalie` (n°, date, description, gravité [choix : Mineure/Majeure/Critique], photo, statut [Ouverte/En validation/Validée/Clôturée]), `Atelier`, `Machine` ; Lookups `Anomalie → Atelier`, `Anomalie → Machine`.
- Application canvas mobile : écran liste (galerie filtrée « mes anomalies »), écran formulaire (`SubmitForm`), écran détail.
- Rôles : Opérateur (créer/lire ses lignes), Responsable (lire/modifier tout son atelier).

### Fiche pré-remplie
- **Pièges** : texte libre au lieu de colonnes Choix (statistiques impossibles) ; délégation dans les filtres de galerie (limite de 500/2000 lignes) ; oublier les rôles avant la mise en production.

---

## Jour 7 — Power Automate : workflows, approbations, notifications

**Objectif** : automatiser les tâches répétitives, les notifications et les circuits de validation.

### Vidéos essentielles
| # | Vidéo | Langue |
|---|---|---|
| 1 | [Flux d'approbation et notifications avec Power Automate](https://www.youtube.com/watch?v=hbwBx8j1dhM) | 🇫🇷 |
| 2 | [Power Automate #08 : demande d'approbation via Forms vers Teams](https://www.youtube.com/watch?v=wVNo57OivLk) | 🇫🇷 |
| 3 | [Formation Power Apps Model Driven, partie 3 : règles d'entreprise, workflows & Power Automate](https://www.youtube.com/watch?v=9FI-kbjhmUA) | 🇫🇷 |
| 4 | [Power Automate & Dataverse Connector Explained](https://www.youtube.com/watch?v=p66Vtd80Iuc) | 🇬🇧 |

### Pour aller plus loin
- 🇬🇧 [Power Automate Masterclass : Dataverse triggers, business process flows](https://www.youtube.com/watch?v=ieAISWDjlP4)
- 🇬🇧 [How to connect Microsoft Dataverse to Microsoft Teams](https://www.youtube.com/watch?v=NJnq8ZekwdQ)

### Notions à maîtriser
- Flux = **déclencheur** → **conditions** → **actions**.
- Types : automatisé (événement), instantané (bouton), planifié (récurrence).
- Approbations : « premier à répondre », « tout le monde doit approuver », séquentielle (N1 puis N2).
- Contenu dynamique, expressions (`formatDateTime`, `concat`), gestion d'erreurs (« Configurer l'exécution après »).

### Pratique — flux « Anomalie critique »
1. Déclencheur Dataverse : *Lorsqu'une ligne est ajoutée* (table Anomalie).
2. Condition : Gravité = Critique.
3. Oui → Mettre à jour le statut « En validation » → *Démarrer et attendre une approbation* (responsable d'atelier) → message Teams au canal Qualité.
4. Si approuvé → statut « Validée » + e-mail Outlook à l'émetteur ; si rejeté → statut « Ouverte » + commentaire du responsable.
5. Variante séquentielle : 2ᵉ approbation par le directeur qualité.

### Fiche pré-remplie
- **Pièges** : boucles infinies (un flux qui modifie la ligne qui le déclenche → filtrer le déclencheur sur colonnes) ; approbateur codé en dur (le lire depuis la table Atelier) ; pas de délai d'expiration.

---

# BLOC 4 — IA générative & industrialisation (Jours 8 à 10)

## Jour 8 — IA générative, RAG & Copilot Studio

**Objectif** : créer des agents IA d'entreprise sécurisés pour assister les collaborateurs.

### Vidéos essentielles
| # | Vidéo | Langue |
|---|---|---|
| 1 | [Comprendre le RAG : adapter l'IA à ses documents](https://www.youtube.com/watch?v=qUHEUXwr_J8) | 🇫🇷 |
| 2 | [Créer votre agent IA avec Microsoft Copilot Studio](https://www.youtube.com/watch?v=arJeN_Swyn4) | 🇫🇷 |
| 3 | [Copilot Studio tuto n°01 : on plonge dedans direct](https://www.youtube.com/watch?v=XKYeiHDGa7A) | 🇫🇷 |
| 4 | [Formation au prompt engineering (français)](https://www.youtube.com/watch?v=H89bSRvuY14) | 🇫🇷 |
| 5 | [Copilot Studio : add SharePoint knowledge sources](https://www.youtube.com/watch?v=PQHVIcZvFG8) | 🇬🇧 |

### Pour aller plus loin
- 🇫🇷 [RAG, bases de données vectorielles et IA Gen](https://www.youtube.com/watch?v=q23RgZl3oFk)
- 🇫🇷 [Les bases du RAG – Tuto GenAI FR](https://www.youtube.com/watch?v=zgDBXGi9zQU)
- 🇬🇧 [Copilot Studio Course – Day 03 : knowledge sources and grounded answers](https://www.youtube.com/watch?v=vuBfkQC0UWE)
- 🇬🇧 [SharePoint Lists as Knowledge in Copilot Studio](https://www.youtube.com/watch?v=WISe73gZsrQ)

### Notions à maîtriser
- **Agent déclaratif** (Copilot Studio « light », dans Microsoft 365 Copilot : instructions + sources de connaissances) vs **agent complet** (Copilot Studio : sujets, actions, flux Power Automate, canaux, déclencheurs autonomes).
- **RAG** : question → recherche des passages pertinents (index/embeddings) → injection dans le prompt → réponse avec citations. Réduit les hallucinations et respecte les droits SharePoint de l'utilisateur.
- **Prompt système** : rôle, périmètre, ton, format, refus hors périmètre, obligation de citer la source.
- Sécurité : authentification Entra ID, pas de données sensibles hors périmètre, gouvernance DLP.

### Pratique — fiche technique de l'agent « Assistant Qualité Nigay »
| Rubrique | Contenu |
|---|---|
| Mission | Répondre aux questions sur les procédures qualité, HACCP, fiches de non-conformité |
| Utilisateurs | Opérateurs, chefs d'équipe, service qualité |
| Sources | Site SharePoint « Qualité » (procédures PDF, modes opératoires) |
| Instructions | « Tu es l'assistant qualité de Nigay. Réponds uniquement à partir des documents fournis, cite le document et la section. Si l'information est absente, dis-le et oriente vers le service qualité. Réponds en français, de façon concise. » |
| Hors périmètre | RH, salaires, données clients, avis personnels |
| Actions | (option) Créer une anomalie Dataverse via un flux Power Automate |
| Canal | Microsoft Teams |
| Indicateurs | Taux de réponses utiles, questions sans réponse, temps gagné |

### Fiche pré-remplie
- **Pièges** : documents obsolètes dans les sources ; droits SharePoint trop larges ; prompts vagues ; ne pas tester avec de vraies questions métiers.

---

## Jour 9 — dbt & Airflow vs écosystème Microsoft

**Objectif** : connaître les outils spécialisés de data engineering et savoir arbitrer.

### Vidéos essentielles
| # | Vidéo | Langue |
|---|---|---|
| 1 | [C'est quoi dbt ?](https://www.youtube.com/watch?v=nRbd65H657g) | 🇫🇷 |
| 2 | [Tutoriel dbt : créer son premier projet](https://www.youtube.com/watch?v=KknqyXOTq_o) | 🇫🇷 |
| 3 | [Tout savoir sur dbt : dbt Core vs dbt Cloud (tutoriel & REX)](https://www.youtube.com/watch?v=dP1DBHVOkII) | 🇫🇷 |
| 4 | [Introduction à Airflow](https://www.youtube.com/watch?v=r5kesvgvOCI) | 🇫🇷 |

### Pour aller plus loin
- 🇫🇷 [dbt : transformez vos données dans votre data warehouse](https://www.youtube.com/watch?v=ptbYKvXpgsw)
- 🇫🇷 [Apache Airflow #06 : exécution et planification d'un DAG](https://www.youtube.com/watch?v=V7ff6rlxOUY&list=PLQGJaVbkt_sqLCLFpE6O-KdbViwZpAIBO&index=6)
- 🇬🇧 [dbt Crash Course for Beginners (dbt Core)](https://www.youtube.com/watch?v=toSAAgLUHuk)
- 🇬🇧 [Airflow tutorial 1 : introduction to Apache Airflow](https://www.youtube.com/watch?v=AHMm1wfGuHE)

### Notions à maîtriser
- **dbt** : modèles SQL versionnés (Git), `ref()` pour les dépendances, tests (`unique`, `not_null`, `relationships`), documentation et lignage auto.
- **Airflow** : DAG Python, tâches, opérateurs, dépendances `t1 >> t2`, planification cron, reprises.

### Pratique — matrice d'arbitrage
| Besoin | Solution Microsoft | Alternative | Quand préférer l'alternative |
|---|---|---|---|
| Ingestion SAP / SharePoint | Data Factory (pipelines) | Airflow + scripts | Sources très hétérogènes, besoin multi-cloud |
| Transformations SQL | Notebooks / Warehouse Fabric | dbt Core | Beaucoup de modèles SQL, besoin de tests et de versionnage |
| Orchestration | Pipelines Fabric | Airflow | Dépendances complexes, équipe Python expérimentée |
| Workflows métier | Power Automate | — | Rarement : Power Automate reste le standard M365 |
| Coût | Inclus dans la capacité Fabric / licences M365 | Open source mais hébergement et maintenance | Équipe data capable d'opérer l'infrastructure |
| Gouvernance | Purview, Entra ID natifs | À construire | — |

Recommandation type pour une PME industrielle déjà Microsoft : rester sur Fabric + Power Platform, introduire dbt (compatible avec Fabric Warehouse) seulement si le volume de transformations SQL le justifie.

---

## Jour 10 — Projet intégrateur & communication métier

**Objectif** : assembler toutes les briques et préparer la prise de poste.

### Vidéos essentielles
| # | Vidéo | Langue |
|---|---|---|
| 1 | [Microsoft Fabric End-to-End Project : from SQL to Power BI](https://www.youtube.com/watch?v=3ESSrFpMbQI) | 🇬🇧 (révision globale) |
| 2 | [Elevator pitch : se présenter en entretien – Objectif premier job](https://www.youtube.com/watch?v=z7L-ekqnvpo) | 🇫🇷 |
| 3 | [Comment construire un pitch pertinent ?](https://www.youtube.com/watch?v=I4Bi9fGR7IY) | 🇫🇷 |
| 4 | [Quinzaine de l'alternance : préparer son entretien](https://www.youtube.com/watch?v=agNXMQNk6Do) | 🇫🇷 |

### Architecture cible
```
SAP / API FastAPI / SharePoint
        │  Pipeline Data Factory (planifié 6 h)
        ▼
Lakehouse : Bronze ──► Silver ──► Gold (étoile)
        │
        ▼
Modèle sémantique Power BI (mesures DAX + dictionnaire KPI) ──► Rapports
        ▲
Power Apps + Dataverse (saisie anomalies) ──► Power Automate (approbation, Teams)
        │
Copilot Studio (agent RAG sur SharePoint Qualité, dans Teams)
```

### Pitch de 5 minutes (trame)
1. **Contexte (30 s)** : données dispersées, processus papier, besoin de fiabilité.
2. **Solution (2 min)** : parcours de la donnée, de la source au rapport, puis l'appli et l'agent.
3. **Démo ou captures (1 min 30)** : un KPI, une anomalie déclarée puis approuvée, une question à l'agent.
4. **Valeur (30 s)** : temps gagné, KPI uniques, traçabilité.
5. **Suite (30 s)** : ce que je veux construire chez Nigay.

### Questions à poser au tuteur la première semaine
- Quelles sources sont prioritaires (modules SAP, fichiers Excel, MES) ? Comment y accède-t-on ?
- Une capacité Fabric est-elle en place ? Quels workspaces et quelles conventions de nommage ?
- Existe-t-il déjà un dictionnaire de KPI ? Qui valide les définitions ?
- Quels processus papier sont prioritaires à digitaliser ?
- Quelles licences Power Platform / Copilot sont disponibles ? Quelles règles DLP ?
- Où documenter le travail (SharePoint, wiki, Git) ? Comment se passent les mises en production ?
- Quels sont mes premiers livrables attendus à 1 mois et à 3 mois ?

---

# Modèle de fiche quotidienne (à copier chaque jour)

```markdown
## Fiche — Jour X : [titre]
**Date :**            **Vidéos vues :** (liens)

### 1. Problème métier résolu
### 2. Outils utilisés
### 3. Entrées & sorties de données
- Entrées :
- Sorties :
### 4. Étapes du flux
1.
2.
3.
### 5. Vocabulaire & pièges évités
| Terme | Définition en une phrase |
|---|---|
Pièges :
### 6. Bilan
- Ce que je sais refaire seule :
- Ce que je dois valider avec mon tuteur :
```

---

# Récapitulatif du planning

| Jour | Thème | Livrable de fin de journée |
|---|---|---|
| 1 | Chaîne data & étoile | Schéma du flux + schéma en étoile |
| 2 | SQL analytique | Fichier `.sql` de requêtes et contrôles qualité |
| 3 | Fabric & Medallion | Lakehouse avec tables Bronze et Silver |
| 4 | Data Factory & FastAPI | Pipeline planifié + mini-API |
| 5 | Power BI & DAX | Rapport de production + dictionnaire de KPI |
| 6 | Dataverse & Power Apps | Application de déclaration d'anomalies |
| 7 | Power Automate | Flux d'approbation des anomalies critiques |
| 8 | RAG & Copilot Studio | Fiche technique + agent qualité |
| 9 | dbt & Airflow | Matrice d'arbitrage |
| 10 | Projet intégrateur | Schéma global, pitch, questions au tuteur |
