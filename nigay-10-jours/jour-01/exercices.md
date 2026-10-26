# Jour 1 — Chaîne data & modèle en étoile : exercices

**Durée visée :** 3 h 30 de pratique après les vidéos essentielles du guide.
**Outils :** un éditeur ou Excel pour ouvrir les CSV, draw.io (app.diagrams.net) ou Excalidraw pour dessiner.
**Livrables, à déposer dans ce dossier :**
- `reponses.md` : tes réponses aux questions 1 à 7 ;
- `flux.png` (ou `.drawio`) : le schéma de la chaîne data ;
- `modele_etoile.png` (ou `.drawio`) : ton modèle dimensionnel ;
- `fiche.md` remplie.

> Aujourd'hui, **tu ne codes pas.** Tu apprends à regarder des données comme un architecte : à quoi correspond une ligne, quelles clés relient les tables, ce qui se mesure et ce qui sert à filtrer. Ce sont les décisions les plus coûteuses à corriger plus tard.

---

## Partie A — Lire les données (45 min)

Ouvre les six fichiers de `data/` (Excel : *Données → À partir d'un fichier texte/CSV*, séparateur point-virgule).

**Question 1 — Le grain.** Pour chaque fichier, complète le tableau :

| Fichier | Une ligne représente… | Clé (colonne(s) qui identifie(nt) une ligne de façon unique) | Fait, dimension ou autre ? |
|---|---|---|---|
| production_brute.csv | | | |
| ventes.csv | | | |
| dim_produit.csv | | | |
| dim_client.csv | | | |
| dim_machine.csv | | | |
| dim_atelier.csv | | | |

**Question 2 — Première intuition sur la qualité.** Fais défiler `production_brute.csv` quelques minutes, sans outil. Note **trois choses qui te semblent suspectes ou à vérifier**. (Tu les vérifieras pour de vrai au J2. Ne cherche pas l'exhaustivité.)

## Partie B — OLTP ou OLAP ? (20 min)

**Question 3.** Imagine que `production_brute.csv` est une extraction de l'ERP (SAP) ou du système de supervision de l'usine.

1. Pourquoi l'ERP stocke-t-il les données de façon **normalisée** (beaucoup de petites tables, peu de redondance) ?
2. Pourquoi est-ce une mauvaise idée de brancher Power BI directement sur les tables de l'ERP ? Donne au moins deux raisons : une technique et une liée au métier.
3. Dans `dim_produit.csv`, la famille (« Colorant »…) est répétée sur chaque produit. Est-ce un défaut dans un modèle analytique ? Justifie.

## Partie C — Concevoir le modèle (1 h 30)

**Question 4 — Mesures et attributs.** Classe chaque colonne de `production_brute.csv` dans l'une de ces catégories :

- **Clé** (relie à une dimension ou identifie l'événement) ;
- **Mesure additive** (on peut la sommer sur tous les axes : produit, date, machine…) ;
- **Mesure non additive** (une somme n'a pas de sens ; laquelle des agrégations a du sens : moyenne, min/max, moyenne pondérée ?) ;
- **Attribut descriptif / technique**.

Puis réponds : pourquoi ne faut-il **jamais** calculer le taux de rebut global comme la moyenne des taux de rebut de chaque lot ? Illustre avec deux lots inventés (un petit, un gros) dont la moyenne des taux est fausse.

**Question 5 — Deux faits, des dimensions partagées.** Dessine (fichier `modele_etoile`) :

- `Fait_Production`, au grain **un lot de fabrication** ;
- `Fait_Ventes`, au grain **une ligne de facture** ;
- les dimensions dont ils ont besoin.

Contraintes :
- `Dim_Date` et `Dim_Produit` doivent être **partagées** par les deux faits. Comment appelle-t-on ce type de modèle ?
- Pour chaque dimension, indique sa **clé de substitution** (`sk_…`, entier) et la **clé métier** conservée (`code_article`…).
- Indique le sens et la cardinalité de chaque relation (1 → *).

**Question 6 — Hiérarchies : étoile ou flocon ?** Il existe deux hiérarchies :
`Produit → Famille` et `Machine → Atelier → Site`.

1. Version flocon : à quoi ressemble le modèle si `Dim_Machine` pointe vers `Dim_Atelier` ?
2. Version étoile : que contient une `Dim_Machine` « aplatie » ?
3. Laquelle choisis-tu pour Power BI, et pourquoi ?

**Question 7 — Le cas qui fâche.** Une machine peut changer d'atelier (un cuiseur déménage de Feurs à Nesle en 2027).
1. Si tu écrases simplement l'atelier dans `Dim_Machine`, que deviennent les rapports de production 2025 par site ?
2. Comment s'appelle la technique qui conserve l'historique ? Quelles colonnes ajouterais-tu ? (Une intuition suffit, on l'approfondira plus tard.)

## Partie D — La chaîne de bout en bout (45 min)

Dessine `flux` : le chemin d'une donnée depuis l'atelier jusqu'au tableau de bord.

```text
Sources (ERP SAP, supervision, laboratoire, fichiers Excel)
  → Ingestion (pipeline planifié)
  → Bronze (brut) → Silver (nettoyé, typé) → Gold (modèle en étoile)
  → Modèle sémantique (mesures, relations, droits)
  → Rapport Power BI
```

Pour **chaque étape**, écris sur le schéma :
- ce qui entre et ce qui sort ;
- **une** transformation précise qui y a lieu, prise dans nos données (par exemple : « conversion de `date_prod` de JJ/MM/AAAA en date ») ;
- qui en est responsable (data, métier, IT ?).

Puis ajoute en bas du schéma les **trois questions** que tu poserais à ton tuteur pour savoir à quoi ressemble cette chaîne *réellement* chez Nigay.

---

## Critères de réussite

- [ ] Je sais dire ce qu'est le **grain** d'une table et pourquoi c'est la première décision.
- [ ] Je distingue mesure additive, mesure non additive et attribut.
- [ ] Je sais expliquer pourquoi un ratio se calcule à partir de **sommes**.
- [ ] Mon modèle a deux faits, des dimensions partagées et des clés de substitution.
- [ ] Je sais expliquer étoile contre flocon, et OLTP contre OLAP, en deux phrases chacun.

**Quand c'est fait, envoie-moi `reponses.md` et tes deux schémas (des captures suffisent).**
