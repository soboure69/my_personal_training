"""
Exécute un fichier .sql sur la base DuckDB locale du kit et affiche les résultats.

Installation (une seule fois) :   pip install duckdb
Usage (depuis le dossier nigay-10-jours) :
    python outils/run_sql.py jour-02/requetes.sql
    python outils/run_sql.py --init            # (re)charge les CSV dans la base

La base `nigay.duckdb` est créée au premier lancement à partir des CSV de data/.
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import duckdb
except ImportError:
    sys.exit("DuckDB n'est pas installé : lance d'abord  pip install duckdb")

RACINE = Path(__file__).resolve().parent.parent
BASE = RACINE / "nigay.duckdb"
INIT = RACINE / "outils" / "init_duckdb.sql"


def executer(con: "duckdb.DuckDBPyConnection", sql: str, afficher: bool = True) -> None:
    entete: list[str] = []                 # commentaires « -- … » placés avant la requête
    for stmt in con.extract_statements(sql):
        lignes = stmt.query.strip().splitlines()
        # DuckDB rattache les commentaires qui suivent un « ; » à la requête précédente :
        # on les déplace vers la requête suivante.
        suivants: list[str] = []
        while lignes and lignes[-1].strip().startswith("--"):
            suivants.insert(0, lignes.pop().strip())
        while lignes and lignes[0].strip().startswith("--"):
            entete.append(lignes.pop(0).strip())
        texte = "\n".join(lignes).strip().rstrip(";").strip()
        if texte:
            try:
                rel = con.sql(texte)
            except duckdb.Error as e:
                print(f"\n❌ Erreur ({' '.join(entete) or texte.splitlines()[0][:80]}) :\n   {e}\n")
            else:
                premier_mot = texte.split(None, 1)[0].upper()
                lecture = premier_mot in {"SELECT", "WITH", "FROM", "DESCRIBE", "SHOW",
                                          "SUMMARIZE", "EXPLAIN", "PIVOT", "UNPIVOT", "VALUES", "TABLE"}
                if rel is None or not lecture:   # CREATE, INSERT… : rien à afficher
                    if afficher:
                        print("\n" + (" ".join(entete) + " " if entete else "") + "✔ " + texte.splitlines()[0].split("(")[0][:70])
                elif afficher:
                    print("\n" + (" ".join(entete) if entete else texte.splitlines()[0][:100]))
                    try:
                        rel.show(max_rows=40, max_width=200)
                    except duckdb.Error as e:   # erreurs détectées à l'exécution
                        print(f"❌ {e}")
        entete = suivants


def main() -> None:
    import os
    fichiers = [Path(a).resolve() for a in sys.argv[1:] if not a.startswith("--")]
    os.chdir(RACINE)                       # les chemins data/... sont relatifs à la racine du kit
    premiere_fois = not BASE.exists()
    con = duckdb.connect(str(BASE))
    if premiere_fois or "--init" in sys.argv:
        executer(con, INIT.read_text(encoding="utf-8"), afficher=False)
        print("✅ Données chargées dans nigay.duckdb")
    for f in fichiers:
        executer(con, Path(f).read_text(encoding="utf-8"))
    con.close()


if __name__ == "__main__":
    main()
