# Jour 6 — Dataverse & Power Apps : exercices

**Accès :** Power Apps Developer Plan (compte professionnel ou scolaire).
**Livrables :** schéma des tables, captures de l'application, `reponses.md`, `fiche.md`.

> Cadre provisoire, à détailler avant le J6.

## Exercices

1. **Modèle de données.** Avant d'ouvrir Power Apps, dessine les tables `Anomalie`, `Atelier`, `Machine` avec leurs colonnes, leurs types (choix, recherche, date, image…) et leurs relations. Réutilise les codes machine et atelier du kit.
2. **Dataverse.** Crée les tables. La gravité et le statut doivent être des colonnes **Choix**, pas du texte libre. Pourquoi ?
3. **Application canevas mobile.** Trois écrans : liste « mes anomalies » (galerie filtrée), formulaire de déclaration (avec photo), détail. Ajoute une validation : la description fait au moins 20 caractères.
4. **Sécurité.** Deux rôles : Opérateur (crée et lit ses propres anomalies) et Responsable d'atelier (lit et modifie celles de son atelier). Teste avec deux comptes si possible, sinon décris le test.
5. **Délégation.** Explique le problème de délégation sur un filtre de galerie, et réécris un filtre non délégable pour qu'il le devienne.
6. **Option sans accès Power Apps :** maquette des écrans (papier ou Figma) + modèle de données + le même formulaire sous forme d'endpoint `POST /anomalies` (déjà fait au J4). Note ce qui change entre un outil low-code et une application codée.

## Critères de réussite

- [ ] Je sais quand choisir une application canevas plutôt qu'une application pilotée par modèle.
- [ ] Mes rôles empêchent un opérateur de modifier l'anomalie d'un autre.
