-- clean.sql — bdap_rnd_entrate_articolo
-- Rendiconto Pubblicato Elaborabile — Entrate per articolo (2011-2025)
-- Lettura per nome colonna (lo schema cambia tra anni), tutto VARCHAR in raw.
-- Ciclo: previsione -> accertamento (totale) -> riscossione -> versamento.

SELECT
    cast_int("Esercizio Finanziario")        AS anno,
    normalize_string("Stato di Previsione")  AS stato_previsione,
    normalize_string("Amministrazione")      AS amministrazione,
    normalize_string("Numero Capitolo di Entrata") AS capitolo,
    normalize_string("Numero Articolo")      AS articolo,
    normalize_string("Codice Titolo")        AS codice_titolo,
    normalize_string("Titolo")               AS titolo,
    normalize_string("Natura")               AS natura,
    normalize_string("Tipologia")            AS tipologia,
    normalize_string("Attività/Provento")    AS provento,
    normalize_string("Categoria")            AS categoria,
    cast_double("Previsioni Iniziali CP")    AS prev_iniziali_cp,
    cast_double("Variazioni CP")             AS variazioni_cp,
    cast_double("Previsioni Definitive CP")  AS prev_def_cp,
    cast_double("Versato CP")                AS versato_cp,
    cast_double("Rimasto da Versare CP")     AS rimasto_versare_cp,
    cast_double("Rimasto da Riscuotere CP")  AS rimasto_riscuotere_cp,
    cast_double("Totale CP")                 AS totale_cp,
    cast_double("Previsioni Definitive CS")  AS prev_def_cs,
    cast_double("Versato CS")                AS versato_cs,
    cast_double("Riscosso RS")               AS riscosso_rs,
    cast_double("Totale RS")                 AS totale_rs
FROM raw_input
WHERE cast_int("Esercizio Finanziario") IS NOT NULL
