-- clean.sql — bdap_rnd_spese_capitolo
-- Rendiconto Pubblicato Elaborabile — Spese per capitolo (2011-2025)
-- Lettura per nome colonna: lo schema cambia dal 2024 (senza macroaggregato, con azione).
-- Importi: previsioni iniziali/variazioni/definitive, pagato, rimasto da pagare, totale, economie.

SELECT
    cast_int("Esercizio Finanziario")     AS anno,
    normalize_string("Stato di Previsione") AS stato_previsione,
    normalize_string("Amministrazione")   AS amministrazione,
    normalize_string("Numero Capitolo di Spesa") AS capitolo,
    normalize_string("Capitolo di Spesa") AS denominazione_capitolo,
    normalize_string("Codice Titolo")     AS codice_titolo,
    normalize_string("Titolo")            AS titolo,
    normalize_string("Codice Categoria")  AS codice_categoria,
    normalize_string("Categoria")         AS categoria,
    normalize_string("Codice Missione")   AS codice_missione,
    normalize_string("Missione")          AS missione,
    normalize_string("Codice Programma")  AS codice_programma,
    normalize_string("Programma")         AS programma,
    cast_double("Previsioni Iniziali CP") AS prev_iniziali_cp,
    cast_double("Variazioni CP")          AS variazioni_cp,
    cast_double("Previsioni Definitive CP") AS prev_def_cp,
    cast_double("Pagato CP")              AS pagato_cp,
    cast_double("Rimasto da Pagare CP")   AS rimasto_cp,
    cast_double("Totale CP")              AS totale_cp,
    cast_double("Economie-Maggiori Spese CP") AS economie_cp,
    cast_double("Previsioni Definitive CS") AS prev_def_cs,
    cast_double("Pagato CS")              AS pagato_cs,
    cast_double("Previsioni Definitive RS") AS prev_def_rs,
    cast_double("Pagato RS")              AS pagato_rs,
    cast_double("Rimasto da Pagare RS")   AS rimasto_rs,
    cast_double("Totale RS")              AS totale_rs
FROM raw_input
WHERE cast_int("Esercizio Finanziario") IS NOT NULL
