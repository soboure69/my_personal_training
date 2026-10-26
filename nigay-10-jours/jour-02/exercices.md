# Jour 2 — SQL analytique & contrôle qualité : exercices

**Durée visée :** 4 h de pratique après les vidéos essentielles du guide.
**Outil :** DuckDB (voir le README du kit). Écris tes requêtes dans `jour-02/requetes.sql`, puis exécute-les :

```bash
python outils/run_sql.py jour-02/requetes.sql
```

**Livrables :**
- `requetes.sql` : toutes tes requêtes, numérotées et commentées (`-- B3 : dédoublonnage…`) ;
- `rapport_anomalies.md` : le tableau de la partie E ;
- `fiche.md` remplie.

> ⚠️ `production_brute` est chargée **entièrement en texte**, comme une vraie couche Bronze. Pour calculer, tu devras convertir : `TRY_CAST(quantite_kg AS DOUBLE)` renvoie `NULL` au lieu de planter si la valeur est invalide. Pour les dates : `TRY_STRPTIME(date_prod, '%d/%m/%Y')`.
>
> N'ouvre pas `outils/generate_data.py` ni `.corrige_anomalies.json` : tout l'intérêt est de trouver les défauts toi-même.

---

## Partie A — Prise en main (20 min)

**A1.** Compte les lignes de chacune des six tables.

**A2.** Dans `production_brute`, compare le nombre de lignes au nombre de `num_lot` **distincts**. Qu'en conclus-tu ?

**A3.** Nombre de lots par `code_machine`, du plus grand au plus petit. Une valeur te surprend-elle ?

**A4.** Affiche `DESCRIBE production_brute;` puis `DESCRIBE ventes;`. Pourquoi les types sont-ils différents ?

## Partie B — Contrôles qualité (1 h 45)

Pour chaque contrôle : écris la requête, note **le nombre de lignes concernées**, et regarde quelques exemples.

**B1 — Doublons.** Liste les `num_lot` qui apparaissent plus d'une fois (`GROUP BY … HAVING …`). Combien y en a-t-il ?

**B2 — Comprendre un doublon.** Prends un `num_lot` en double et affiche ses lignes côte à côte. Qu'est-ce qui diffère ? À ton avis, que s'est-il passé dans le processus de saisie ? Quelle version faut-il garder ?

**B3 — Dédoublonner.** Avec `ROW_NUMBER() OVER (PARTITION BY … ORDER BY …)`, crée une vue `production_dedup` qui ne garde qu'une ligne par lot, la bonne.
Contrôle : le nombre de lignes de la vue doit être égal au nombre de lots distincts trouvé en A2.

**B4 — Valeurs manquantes.** Pour chaque colonne de `production_dedup`, compte les valeurs vides ou `NULL`.
Astuce : une chaîne vide `''` n'est pas `NULL`. Regarde comment ton CSV a été lu.
Parmi les colonnes incomplètes, laquelle est un **vrai problème** et laquelle peut être **normale** ? (Indice : qui remplit la colonne `conforme`, et quand ?)

**B5 — Quantités négatives.** Combien de lots ont une quantité négative ?

**B6 — Quantités aberrantes mais positives.** Certaines quantités sont **positives mais absurdes**.
1. Calcule, par `forme` de produit (jointure avec `dim_produit`), le minimum, la médiane (`MEDIAN`) et le maximum de `quantite_kg`.
2. Trouve les lots dont la quantité est inférieure à 1 % de la médiane de leur forme.
3. Formule une hypothèse sur l'origine de ces valeurs. Que proposerais-tu au métier : corriger automatiquement ou mettre en quarantaine ?

**B7 — Incohérence entre colonnes.** Combien de lots ont plus de rebuts que de quantité produite ?

**B8 — Mesures physiquement impossibles.** Le pH est compris entre 0 et 14. Cherche les valeurs impossibles **et** les valeurs suspectes (un pH de 0,00 pile est-il crédible pour un caramel ?).

**B9 — Orphelins.** Avec `LEFT JOIN … WHERE … IS NULL` :
1. Lots dont le `code_article` n'existe pas dans `dim_produit` (sépare bien « vide » et « inconnu ») ;
2. Lots dont la `code_machine` n'existe pas dans `dim_machine`.
Quelle hypothèse métier peut expliquer un code article commençant par `CAR-ESSAI` ?

**B10 — Dates.** Combien de `date_prod` ne respectent pas le format `JJ/MM/AAAA` ? Quel autre format apparaît ?
Écris une expression qui convertit **les deux formats** en une vraie date (indice : `COALESCE` de deux `TRY_STRPTIME`). Vérifie qu'il ne reste aucune date `NULL`.

## Partie C — Construire la couche Silver (45 min)

Crée une vue `silver_production` à partir de `production_dedup` :

- colonnes typées : `date_prod` en `DATE`, mesures en `DOUBLE` ou `INTEGER`, `conforme` en `BOOLEAN` (et `NULL` si en attente) ;
- une colonne `anomalie` qui vaut `NULL` si la ligne est saine, sinon un **motif** lisible (`'quantite_negative'`, `'article_inconnu'`, `'ph_impossible'`…) ;
- **on ne supprime aucune ligne** : on les étiquette.

Puis :
- **C1.** Combien de lignes saines, et combien par motif d'anomalie ?
- **C2.** Explique en trois phrases pourquoi on étiquette au lieu de supprimer (pense à la traçabilité, au propriétaire de la donnée et à l'audit qualité).

Conseil : si une ligne a plusieurs défauts, un `CASE WHEN` renvoie seulement le premier motif. C'est acceptable aujourd'hui, mais note-le comme limite.

## Partie D — SQL analytique (1 h)

Travaille sur les lignes **saines** de `silver_production`, et sur `ventes`.

**D1 — Production mensuelle.** Quantité produite par mois (en tonnes), avec la quantité du mois précédent (`LAG`) et l'évolution en %. Protège la division avec `NULLIF`.

**D2 — Taux de rebut correct.** Taux de rebut par famille de produit, calculé comme `SUM(rebuts) / SUM(quantite)`. Compare avec `AVG(rebuts / quantite)`. Les deux diffèrent-ils ? Lequel est juste, et pourquoi ? (C'est la question 4 du J1, en vrai.)

**D3 — Détecter une dérive.** Taux de non-conformité (part des lots avec `conforme = false`) **par machine et par mois**.
1. Une machine a connu un problème pendant quelques mois. Laquelle, et quand ?
2. Quelle mesure physique explique ce problème ? Compare la température moyenne de cette machine pendant et hors de la période suspecte.
3. Qui préviendrais-tu, et avec quelle preuve ?

**D4 — Classement.** Pour chaque année, les 3 produits les plus fabriqués en tonnes (`RANK()` ou `ROW_NUMBER()` partitionné par année). Quelle différence entre les deux fonctions en cas d'égalité ?

**D5 — Chiffre d'affaires.** Sur `ventes` : CA mensuel, évolution par rapport au mois précédent **et** CA cumulé depuis le début de l'année (`SUM(...) OVER (PARTITION BY année ORDER BY mois)`).

**D6 — Bonus.** Top 5 des clients par CA 2025, avec la part de chacun dans le CA total (`… / SUM(…) OVER ()`).

## Partie E — Rapport d'anomalies (30 min)

Dans `rapport_anomalies.md`, remplis ce tableau pour chaque défaut trouvé :

| Contrôle | Règle SQL (résumé) | Nb de lignes | Exemple de lot | Cause probable | Action proposée | Propriétaire à solliciter |
|---|---|---|---|---|---|---|
| Doublons de lot | `COUNT(*) > 1` par `num_lot` | | | | | |
| … | | | | | | |

Termine par **trois phrases** destinées à un responsable qualité **non technicien** : ce que tu as trouvé, ce que cela change pour les KPI, ce que tu proposes.

---

## Critères de réussite

- [ ] Je connais l'ordre logique d'exécution d'une requête SQL et la différence `WHERE` / `HAVING`.
- [ ] Je sais dédoublonner avec `ROW_NUMBER()` et **vérifier** le résultat par un comptage.
- [ ] Je sais trouver des orphelins avec un `LEFT JOIN`.
- [ ] Je sais utiliser `LAG`, `RANK` et une somme cumulée avec `OVER (PARTITION BY … ORDER BY …)`.
- [ ] Je calcule un ratio à partir de sommes, jamais comme une moyenne de ratios.
- [ ] Je sais expliquer un problème de qualité de données à un non-technicien.

**Quand c'est fait, envoie-moi `requetes.sql` et `rapport_anomalies.md`.** Je comparerai tes résultats au corrigé et on reviendra sur ce qui t'a échappé.
