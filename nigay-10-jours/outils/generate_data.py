"""
Génère un jeu de données FICTIF inspiré d'un fabricant industriel de caramels.

- Aucune donnée réelle de Nigay : produits, clients, machines, mesures et
  volumes sont inventés. Seuls les noms de sites (Feurs, Nesle) sont publics.
- Reproductible : même graine => mêmes fichiers.
- Python standard uniquement (aucune installation nécessaire).

Usage :  python outils/generate_data.py
Sortie : data/*.csv  (séparateur « ; », décimales « . », encodage UTF-8)

⚠️  Conseil pédagogique : ne lis pas ce script avant d'avoir terminé le Jour 2.
    Il révèle les anomalies que tu dois trouver toi-même.
"""

from __future__ import annotations

import csv
import math
import random
from datetime import date, datetime, timedelta
from pathlib import Path

SEED = 42
DEBUT = date(2024, 1, 2)
FIN = date(2026, 9, 30)
OUT = Path(__file__).resolve().parent.parent / "data"

rng = random.Random(SEED)


# ---------------------------------------------------------------------------
# Référentiels
# ---------------------------------------------------------------------------

ATELIERS = [
    # code, libellé, site
    ("ATL-FEU-CUI", "Cuisson liquides", "Feurs"),
    ("ATL-FEU-SEC", "Poudres et éclats", "Feurs"),
    ("ATL-NES-CUI", "Cuisson Nesle", "Nesle"),
]

MACHINES = [
    # code, libellé, type, atelier, date mise en service
    ("CUI-01", "Cuiseur 1", "Cuiseur", "ATL-FEU-CUI", "2015-03-01"),
    ("CUI-02", "Cuiseur 2", "Cuiseur", "ATL-FEU-CUI", "2017-09-15"),
    ("CUI-03", "Cuiseur 3", "Cuiseur", "ATL-FEU-CUI", "2021-06-01"),
    ("ATO-01", "Atomiseur 1", "Atomiseur", "ATL-FEU-SEC", "2019-01-10"),
    ("BRO-01", "Broyeur éclats 1", "Broyeur", "ATL-FEU-SEC", "2018-05-20"),
    ("CUI-N1", "Cuiseur Nesle 1", "Cuiseur", "ATL-NES-CUI", "2023-04-01"),
    ("CUI-N2", "Cuiseur Nesle 2", "Cuiseur", "ATL-NES-CUI", "2023-04-01"),
]

# famille -> (formes possibles, couleur EBC cible, MS % cible, viscosité mPa.s
#             cible, pH cible, T° cuisson cible, durée cible min, prix €/kg)
FAMILLES = {
    "Aromatique": (["Liquide", "Pâte"], (3000, 9000), (74, 80), (2000, 9000), (3.8, 4.6), 165, 85, (3.2, 4.8)),
    "Colorant": (["Liquide", "Poudre"], (25000, 55000), (66, 72), (800, 3000), (2.8, 3.6), 185, 120, (1.6, 2.6)),
    "Spécialité": (["Liquide", "Pâte", "Éclats"], (1500, 6000), (76, 84), (5000, 25000), (4.2, 5.4), 155, 70, (5.5, 9.0)),
    "Burnt sugar": (["Liquide", "Poudre"], (12000, 22000), (70, 76), (1500, 5000), (3.0, 3.8), 195, 105, (2.4, 3.6)),
}
NB_PAR_FAMILLE = {"Aromatique": 8, "Colorant": 6, "Spécialité": 6, "Burnt sugar": 4}
NOMS = {
    "Aromatique": ["Blond doux", "Ambré", "Beurre salé", "Vanillé", "Brun intense", "Doré", "Crème", "Fleur de sel"],
    "Colorant": ["E150a clair", "E150a foncé", "E150c", "E150d standard", "E150d double force", "E150d poudre"],
    "Spécialité": ["Nappage dessert", "Fourrage", "Éclats croquants", "Pâte à tartiner", "Inclusion glace", "Praliné"],
    "Burnt sugar": ["Sucre brûlé clair", "Sucre brûlé foncé", "Sucre brûlé poudre", "Sucre brûlé aromatique"],
}
ABREV = {"Aromatique": "AROM", "Colorant": "COLO", "Spécialité": "SPEC", "Burnt sugar": "BURN"}


def construire_produits() -> list[dict]:
    produits = []
    for fam, (formes, coul, ms, visc, ph, t, d, prix) in FAMILLES.items():
        for i in range(NB_PAR_FAMILLE[fam]):
            forme = formes[i % len(formes)]
            if "poudre" in NOMS[fam][i].lower():
                forme = "Poudre"
            if "éclats" in NOMS[fam][i].lower():
                forme = "Éclats"
            c = round(rng.uniform(*coul), -2)
            m = round(rng.uniform(*ms), 1)
            v = round(rng.uniform(*visc), -2)
            p = round(rng.uniform(*ph), 2)
            produits.append({
                "code_article": f"CAR-{ABREV[fam]}-{i + 1:03d}",
                "libelle": f"Caramel {NOMS[fam][i]}",
                "famille": fam,
                "forme": forme,
                "couleur_cible_ebc": int(c),
                "couleur_tol_pct": 8,
                "ms_cible_pct": m,
                "ms_tol_pts": 2.0,
                "viscosite_min_mpas": int(v * 0.6),
                "viscosite_max_mpas": int(v * 1.4),
                "ph_min": round(p - 0.4, 2),
                "ph_max": round(p + 0.4, 2),
                "prix_kg_eur": round(rng.uniform(*prix), 2),
                "_t": t, "_d": d, "_v": v, "_ph": p,
            })
    return produits


PREFIXES_CLIENTS = [
    ("Boulangerie industrielle", "Boulangeries"), ("Boissons", "Boissons"),
    ("Brasserie", "Brasseries"), ("Produits laitiers", "Laiterie"),
    ("Biscuiterie", "Biscuiterie"), ("Confiserie", "Confiserie"),
    ("Glaces", "Glacier"), ("Plats cuisinés", "Cuisine"),
]
SUFFIXES = ["Alpha", "Horizon", "des Monts", "Atlantique", "du Val", "Boréal", "Méridien",
            "Lumière", "Rivage", "Sommet", "Orée", "Prisme", "Tilleul", "Cobalt", "Azur",
            "Granit", "Sirocco", "Vallon", "Aurore", "Nordique"]
PAYS = ["France"] * 12 + ["Allemagne"] * 3 + ["Belgique"] * 2 + ["Espagne"] * 2 + \
       ["Italie"] * 2 + ["Royaume-Uni", "Pologne", "Pays-Bas", "Japon", "Brésil"]


def construire_clients(n: int = 40) -> list[dict]:
    clients, vus = [], set()
    while len(clients) < n:
        secteur, prefixe = rng.choice(PREFIXES_CLIENTS)
        nom = f"{prefixe} {rng.choice(SUFFIXES)}"
        if nom in vus:
            continue
        vus.add(nom)
        clients.append({
            "code_client": f"CLI-{len(clients) + 1:04d}",
            "nom_client": nom,
            "secteur": secteur,
            "pays": rng.choice(PAYS),
            "remise_pct": rng.choice([0, 0, 2, 3, 5, 8]),
        })
    return clients


# ---------------------------------------------------------------------------
# Production
# ---------------------------------------------------------------------------

def jours_ouvres(d0: date, d1: date):
    d = d0
    while d <= d1:
        if d.weekday() < 5:
            yield d
        d += timedelta(days=1)


def machine_pour(produit: dict, d: date) -> str:
    if produit["forme"] == "Poudre":
        return "ATO-01"
    if produit["forme"] == "Éclats":
        return "BRO-01"
    choix = ["CUI-01", "CUI-02", "CUI-03"]
    if d >= date(2024, 3, 1):          # montée en charge du site de Nesle
        choix += ["CUI-N1", "CUI-N2"]
    return rng.choice(choix)


def simuler_lot(produit: dict, machine: str, d: date) -> dict:
    t_cible, d_cible = produit["_t"], produit["_d"]
    temperature = rng.gauss(t_cible, 3.0)
    duree = rng.gauss(d_cible, d_cible * 0.08)

    # Dérive volontaire : sonde du Cuiseur 2 déréglée de juillet à octobre 2025
    if machine == "CUI-02" and date(2025, 7, 1) <= d <= date(2025, 10, 31):
        temperature += 6.5

    # Les cuiseurs de Nesle sont un peu plus réguliers
    if machine.startswith("CUI-N"):
        temperature = t_cible + (temperature - t_cible) * 0.7

    effet = 1 + 0.012 * (temperature - t_cible) + 0.004 * (duree - d_cible)
    couleur = produit["couleur_cible_ebc"] * effet * rng.gauss(1, 0.025)
    ms = rng.gauss(produit["ms_cible_pct"], 0.7) + 0.05 * (duree - d_cible) / 10
    visc = produit["_v"] * math.exp(0.22 * (ms - produit["ms_cible_pct"])) * rng.gauss(1, 0.08)
    ph = rng.gauss(produit["_ph"], 0.12) - 0.012 * (temperature - t_cible)

    if produit["forme"] in ("Poudre", "Éclats"):
        qte = rng.uniform(400, 1500)
    else:
        qte = rng.uniform(1800, 8000)

    tol = produit["couleur_tol_pct"] / 100
    conforme = (
        abs(couleur / produit["couleur_cible_ebc"] - 1) <= tol
        and abs(ms - produit["ms_cible_pct"]) <= produit["ms_tol_pts"]
        and produit["viscosite_min_mpas"] <= visc <= produit["viscosite_max_mpas"]
        and produit["ph_min"] <= ph <= produit["ph_max"]
    )
    rebuts = qte * (rng.uniform(0, 0.02) if conforme else rng.uniform(0.05, 0.30))

    return {
        "temperature_max_c": round(temperature, 1),
        "duree_cuisson_min": int(round(duree)),
        "ph": round(ph, 2),
        "matiere_seche_pct": round(ms, 1),
        "viscosite_mpas": int(round(visc, -1)),
        "couleur_ebc": int(round(couleur, -1)),
        "quantite_kg": round(qte, 1),
        "rebuts_kg": round(rebuts, 1),
        "conforme": "O" if conforme else "N",
    }


def construire_production(produits: list[dict]) -> tuple[list[dict], dict]:
    # Popularité inégale des produits (quelques best-sellers)
    poids = [rng.paretovariate(1.6) for _ in produits]
    lignes = []
    for d in jours_ouvres(DEBUT, FIN):
        nb = rng.choice([2, 3, 3, 3, 4])
        if d.month == 8 and 5 <= d.day <= 23:      # congés d'été
            nb = 1
        for seq in range(1, nb + 1):
            p = rng.choices(produits, weights=poids)[0]
            m = machine_pour(p, d)
            mesures = simuler_lot(p, m, d)
            maj = datetime.combine(d, datetime.min.time()) + timedelta(
                hours=rng.randint(14, 20), minutes=rng.randint(0, 59))
            lignes.append({
                "num_lot": f"L{d:%y}{d.timetuple().tm_yday:03d}-{seq:02d}",
                "date_prod": d.strftime("%d/%m/%Y"),
                "code_article": p["code_article"],
                "code_machine": m,
                **mesures,
                "date_maj": maj.strftime("%Y-%m-%d %H:%M:%S"),
            })
    return injecter_anomalies(lignes)


def injecter_anomalies(lignes: list[dict]) -> tuple[list[dict], dict]:
    """Injecte des défauts réalistes et renvoie le journal (corrigé privé)."""
    journal: dict[str, list[str]] = {}
    n = len(lignes)
    deja: set[int] = set()

    def tirer(k: int) -> list[int]:
        idx = []
        while len(idx) < k:
            i = rng.randrange(n)
            if i not in deja:
                deja.add(i)
                idx.append(i)
        return idx

    def enregistrer(nom, idx):
        journal[nom] = sorted(lignes[i]["num_lot"] for i in idx)

    idx = tirer(12)
    for i in idx:                                   # erreur de signe
        lignes[i]["quantite_kg"] = -lignes[i]["quantite_kg"]
    enregistrer("quantite_negative", idx)

    idx = tirer(6)
    for i in idx:                                   # saisie en tonnes
        lignes[i]["quantite_kg"] = round(lignes[i]["quantite_kg"] / 1000, 3)
        lignes[i]["rebuts_kg"] = round(lignes[i]["rebuts_kg"] / 1000, 3)
    enregistrer("quantite_en_tonnes", idx)

    idx = tirer(4)
    for i in idx:
        lignes[i]["rebuts_kg"] = round(lignes[i]["quantite_kg"] * rng.uniform(1.2, 3), 1)
    enregistrer("rebuts_superieurs_quantite", idx)

    idx = tirer(9)
    for i in idx:
        lignes[i]["code_article"] = ""
    enregistrer("code_article_vide", idx)

    idx = tirer(5)
    for k, i in enumerate(idx):
        lignes[i]["code_article"] = f"CAR-ESSAI-{k + 1:03d}"
    enregistrer("code_article_orphelin", idx)

    idx = tirer(3)
    for i in idx:
        lignes[i]["code_machine"] = "CUI-04"
    enregistrer("code_machine_orphelin", idx)

    idx = tirer(7)
    for i in idx:
        lignes[i]["ph"] = rng.choice([0.0, 99.9])
    enregistrer("ph_erreur_capteur", idx)

    idx = tirer(15)
    for i in idx:
        lignes[i]["conforme"] = ""
    enregistrer("conformite_en_attente", idx)

    idx = tirer(60)
    for i in idx:
        j, m, a = lignes[i]["date_prod"].split("/")
        lignes[i]["date_prod"] = f"{a}-{m}-{j}"
    enregistrer("date_format_iso", idx)

    # Doublons : un lot ressaisi/corrigé quelques jours plus tard
    idx = tirer(45)
    doublons = []
    for i in idx:
        copie = dict(lignes[i])
        maj = datetime.strptime(copie["date_maj"], "%Y-%m-%d %H:%M:%S")
        copie["date_maj"] = (maj + timedelta(days=rng.randint(1, 5),
                                             hours=rng.randint(0, 5))).strftime("%Y-%m-%d %H:%M:%S")
        if rng.random() < 0.6:
            copie["matiere_seche_pct"] = round(copie["matiere_seche_pct"] + rng.choice([-0.3, 0.2, 0.4]), 1)
        doublons.append((i, copie))
    for i, copie in sorted(doublons, key=lambda x: -x[0]):
        lignes.insert(i + rng.randint(1, 6), copie)
    journal["doublons_num_lot"] = sorted(c["num_lot"] for _, c in doublons)

    return lignes, journal


# ---------------------------------------------------------------------------
# Ventes
# ---------------------------------------------------------------------------

SAISON = {  # coefficient mensuel par secteur
    "Boissons": [0.8, 0.8, 0.9, 1.0, 1.2, 1.4, 1.4, 1.2, 1.0, 0.9, 0.8, 0.8],
    "Brasserie": [0.8, 0.8, 0.9, 1.0, 1.2, 1.3, 1.3, 1.2, 1.0, 0.9, 0.9, 1.0],
    "Glaces": [0.5, 0.6, 0.9, 1.2, 1.5, 1.7, 1.6, 1.2, 0.9, 0.6, 0.5, 0.5],
    "Confiserie": [0.8, 0.9, 1.0, 1.0, 0.8, 0.7, 0.7, 0.8, 1.1, 1.3, 1.6, 1.3],
}


def construire_ventes(produits, clients) -> list[dict]:
    ventes, num = [], 1
    d = date(DEBUT.year, DEBUT.month, 1)
    portefeuille = {c["code_client"]: rng.sample(produits, rng.randint(2, 6)) for c in clients}
    taille = {c["code_client"]: rng.paretovariate(1.3) for c in clients}
    while d <= FIN:
        annee_idx = (d.year - 2024) + d.month / 12
        tendance = 1 + 0.06 * annee_idx              # croissance ~6 %/an
        for c in clients:
            coef = SAISON.get(c["secteur"], [1.0] * 12)[d.month - 1]
            nb_cmd = max(0, int(rng.gauss(2.2 * coef, 1.0)))
            for _ in range(nb_cmd):
                p = rng.choice(portefeuille[c["code_client"]])
                jour = rng.randint(1, 28)
                dv = date(d.year, d.month, jour)
                if dv > FIN:
                    continue
                qte = round(rng.uniform(200, 3000) * taille[c["code_client"]] ** 0.5 * tendance, 0)
                gratuit = rng.random() < 0.004       # échantillons
                montant = 0.0 if gratuit else qte * p["prix_kg_eur"] * (1 - c["remise_pct"] / 100)
                ventes.append({
                    "num_facture": f"FA{dv:%y}-{num:06d}",
                    "date_vente": dv.isoformat(),
                    "code_client": c["code_client"],
                    "code_article": p["code_article"],
                    "quantite_kg": qte,
                    "montant_eur": round(montant, 2),
                })
                num += 1
        d = date(d.year + (d.month == 12), d.month % 12 + 1, 1)
    ventes.sort(key=lambda v: (v["date_vente"], v["num_facture"]))
    return ventes


# ---------------------------------------------------------------------------

def ecrire(nom: str, lignes: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    champs = [k for k in lignes[0] if not k.startswith("_")]
    with open(OUT / nom, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=champs, delimiter=";", extrasaction="ignore")
        w.writeheader()
        w.writerows(lignes)
    print(f"  {nom:<24} {len(lignes):>6} lignes")


def main() -> None:
    produits = construire_produits()
    clients = construire_clients()
    production, journal = construire_production(produits)
    ventes = construire_ventes(produits, clients)

    print(f"Écriture dans {OUT}")
    ecrire("dim_atelier.csv", [dict(zip(["code_atelier", "libelle_atelier", "site"], a)) for a in ATELIERS])
    ecrire("dim_machine.csv", [dict(zip(["code_machine", "libelle_machine", "type_machine",
                                          "code_atelier", "date_mise_en_service"], m)) for m in MACHINES])
    ecrire("dim_produit.csv", produits)
    ecrire("dim_client.csv", clients)
    ecrire("production_brute.csv", production)
    ecrire("ventes.csv", ventes)

    # Corrigé privé : à ne pas ouvrir avant d'avoir fait le Jour 2
    import json
    corrige = Path(__file__).resolve().parent.parent / ".corrige_anomalies.json"
    corrige.write_text(json.dumps(journal, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
