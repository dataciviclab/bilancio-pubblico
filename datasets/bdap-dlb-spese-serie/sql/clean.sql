-- clean.sql — bdap_dlb_spese_serie
-- Disegno di Legge di Bilancio Presentato — spese per amministrazione/missione/programma/macroaggregato
-- Tre annualità nel raw (A1/A2/A3) -> tre righe per ciascuna riga raw.
-- La colonna RS A1 è presente nel raw ma non viene esposta: qui interessano CP/CS.

SELECT
    cast_int("column00")          AS anno,
    1                             AS annualita,
    normalize_string("column01")  AS stato_previsione,
    normalize_string("column02")  AS amministrazione,
    normalize_string("column03")  AS missione,
    normalize_string("column04")  AS programma,
    normalize_string("column07")  AS macroaggregato,
    cast_double("column08")       AS cp,
    cast_double("column11")       AS cs
FROM raw_input
WHERE cast_int("column00") IS NOT NULL

UNION ALL

SELECT
    cast_int("column00")          AS anno,
    2                             AS annualita,
    normalize_string("column01")  AS stato_previsione,
    normalize_string("column02")  AS amministrazione,
    normalize_string("column03")  AS missione,
    normalize_string("column04")  AS programma,
    normalize_string("column07")  AS macroaggregato,
    cast_double("column09")       AS cp,
    cast_double("column12")       AS cs
FROM raw_input
WHERE cast_int("column00") IS NOT NULL

UNION ALL

SELECT
    cast_int("column00")          AS anno,
    3                             AS annualita,
    normalize_string("column01")  AS stato_previsione,
    normalize_string("column02")  AS amministrazione,
    normalize_string("column03")  AS missione,
    normalize_string("column04")  AS programma,
    normalize_string("column07")  AS macroaggregato,
    cast_double("column10")       AS cp,
    cast_double("column13")       AS cs
FROM raw_input
WHERE cast_int("column00") IS NOT NULL
