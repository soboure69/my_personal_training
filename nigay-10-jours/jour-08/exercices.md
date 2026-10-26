# Jour 8 — IA générative, RAG & Copilot Studio : exercices

**Livrables :** `fiche_technique_agent.md`, `jeu_de_test.md`, captures ou code, `fiche.md`.

> Cadre provisoire, à détailler avant le J8. Règle d'or : **aucun document interne Nigay** dans un outil d'IA tant que les règles d'usage ne sont pas validées par ton entreprise.

## Exercices

1. **Corpus fictif.** Je te fournirai 6 à 8 procédures qualité fictives (HACCP, gestion des non-conformités, libération de lot, nettoyage d'un cuiseur…), avec des versions et des dates, dont une **obsolète** volontairement.
2. **Jeu de test d'abord.** Avant de construire quoi que ce soit, écris 15 questions avec la réponse attendue et le document source attendu. Inclus 3 questions **sans réponse dans le corpus** (l'agent doit s'abstenir) et 2 tentatives d'**injection de prompt**.
3. **Construire l'agent.**
   - Option A : Copilot Studio, avec les procédures comme source de connaissances, instructions système de la fiche du guide, canal Teams.
   - Option B, en local : mini-RAG en Python (découpage en passages, embeddings, recherche des plus proches, réponse avec citation), avec un LLM local (Ollama) ou par API.
4. **Évaluer.** Passe les 15 questions : bonne source retrouvée ? réponse juste ? abstention quand il le faut ? injection bloquée ? Calcule un score simple et liste les erreurs.
5. **Fiche technique.** Complète la fiche du guide (mission, utilisateurs, sources, instructions, hors périmètre, indicateurs) et ajoute : gestion des versions des documents, droits d'accès, journalisation, coût, et ce qui reste sous contrôle humain.

## Critères de réussite

- [ ] Je sais expliquer le RAG en 4 étapes à un non-technicien.
- [ ] Mon agent cite ses sources et sait dire « je ne sais pas ».
- [ ] J'ai mesuré la qualité avec un jeu de test, pas seulement « essayé quelques questions ».
