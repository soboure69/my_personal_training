# Jour 5 — Power BI, DAX & dictionnaire de KPI : exercices

**Outil :** Power BI Desktop (gratuit, Windows).
**Livrables :** `rapport_production.pbix`, `dictionnaire_kpi.md`, captures, `fiche.md`.

> Cadre provisoire, à détailler après le J4.

## Exercices

1. **Modèle.** Importe les tables Gold du J3 (ou les CSV du kit nettoyés). Relations 1 → * à sens unique, table de dates marquée comme telle, aucune relation bidirectionnelle.
2. **Mesures.** Crée au minimum : quantité produite (t), quantité rebutée, **taux de rebut** (avec `DIVIDE` sur des sommes), nombre de lots, **taux de non-conformité**, quantité M-1, évolution M-1 %, cumul annuel (`TOTALYTD`), CA, CA N-1 (`SAMEPERIODLASTYEAR`).
3. **Réconciliation.** Pour 2025, retrouve **exactement** la même quantité totale et le même taux de rebut dans Power BI et dans ta requête SQL du J2. S'il y a un écart, explique-le.
4. **Rapport en 3 pages :**
   - *Vue d'ensemble* : 4 cartes KPI, tendance mensuelle, segments date / site / famille ;
   - *Qualité* : taux de non-conformité par machine et par mois. La dérive trouvée au J2 doit **sauter aux yeux** ;
   - *Ventes* : CA mensuel, cumul, top clients.
5. **Dictionnaire de KPI.** Pour au moins 6 KPI : définition métier, formule, table source, grain, fréquence, propriétaire, et un **piège d'interprétation** (par exemple : un taux de non-conformité calculé sur peu de lots).
6. **Sécurité.** Crée un rôle RLS « Responsable Nesle » qui ne voit que le site de Nesle, et teste-le avec *Afficher comme*.

## Critères de réussite

- [ ] Je sais expliquer contexte de ligne et contexte de filtre, et ce que fait `CALCULATE`.
- [ ] Mes chiffres sont réconciliés avec le SQL.
- [ ] Un responsable qualité comprend la page « Qualité » sans explication.
