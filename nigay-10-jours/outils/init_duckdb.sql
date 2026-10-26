-- Chargement des CSV du kit dans DuckDB.
-- Les données de production sont chargées TOUT EN TEXTE (all_varchar) :
-- c'est l'esprit d'une couche « Bronze » — on garde la donnée telle qu'elle
-- est arrivée, et c'est à toi de la typer et de la nettoyer ensuite.

CREATE OR REPLACE TABLE production_brute AS
SELECT * FROM read_csv('data/production_brute.csv', delim = ';', header = true, all_varchar = true);

CREATE OR REPLACE TABLE ventes AS
SELECT * FROM read_csv('data/ventes.csv', delim = ';', header = true);

CREATE OR REPLACE TABLE dim_produit AS
SELECT * FROM read_csv('data/dim_produit.csv', delim = ';', header = true);

CREATE OR REPLACE TABLE dim_client AS
SELECT * FROM read_csv('data/dim_client.csv', delim = ';', header = true);

CREATE OR REPLACE TABLE dim_machine AS
SELECT * FROM read_csv('data/dim_machine.csv', delim = ';', header = true);

CREATE OR REPLACE TABLE dim_atelier AS
SELECT * FROM read_csv('data/dim_atelier.csv', delim = ';', header = true);
