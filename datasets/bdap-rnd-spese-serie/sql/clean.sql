-- clean.sql — bdap_rnd_spese_serie
-- Rendiconto Pubblicato — Spese per Amministrazione/Missione/Programma/Macroaggregato
-- CSV con header: skip 1, colonne via indice (column00..column11)
-- ATTENZIONE: "Previsioni Definitive" = bilancio definitivo, non consuntivo di cassa.

SELECT
    cast_int("column00")          AS anno,
    1                             AS annualita,
    normalize_string("column01")  AS stato_previsione,
    normalize_string("column02")  AS amministrazione,
    normalize_string("column03")  AS missione,
    normalize_string("column04")  AS programma,
    normalize_string("column09")  AS macroaggregato,
    cast_double("column10")       AS cp,
    cast_double("column11")       AS cs
FROM raw_input
WHERE cast_int("column00") IS NOT NULL
