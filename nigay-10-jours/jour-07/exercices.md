# Jour 7 — Power Automate : workflows et approbations : exercices

**Livrables :** captures du flux et d'une exécution réussie et échouée, `reponses.md`, `fiche.md`.

> Cadre provisoire. Ton tuteur t'a dit que Power Automate « ne correspond pas vraiment » aux besoins en pratique : profites-en pour comprendre **pourquoi**, c'est une vraie compétence d'arbitrage.

## Exercices

1. **Flux « Anomalie critique »** (cf. guide) : déclencheur sur création d'une anomalie → condition gravité Critique → approbation du responsable lu **dans la table Atelier** (pas codé en dur) → notification Teams → mise à jour du statut selon la réponse.
2. **Robustesse.** Ajoute : un délai d'expiration de l'approbation (48 h) avec relance, une branche « en cas d'échec » qui prévient un administrateur, et un filtre sur le déclencheur pour éviter la boucle infinie. Provoque volontairement un échec et capture l'historique d'exécution.
3. **Approbation séquentielle.** Variante : responsable d'atelier, puis directeur qualité.
4. **Analyse critique** dans `reponses.md`, à partir de ta propre expérience du jour :
   - limites rencontrées (débogage, versionnement, tests, volumétrie, licences, connecteurs premium) ;
   - dans quels cas Power Automate reste le bon outil (workflow métier humain, notifications M365) ;
   - dans quels cas un orchestrateur de données (Airflow, pipeline Fabric) est plus adapté ;
   - trois questions à poser à ton tuteur pour comprendre ce qui n'a pas fonctionné chez Nigay.

## Critères de réussite

- [ ] Mon flux gère l'expiration, l'échec et le rejet.
- [ ] Je sais distinguer un workflow **métier** d'un pipeline de **données**.
