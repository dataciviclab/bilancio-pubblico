-- clean.sql — bdap_ni_obiettivi
-- Note Integrative — sezione "Obiettivi" (strategici e strutturali).
-- Dal 2018 la struttura è stabile: missione → programma → CdR → obiettivo,
-- con collegamento a priorità politica e azione di bilancio.
-- L'anno 2016-2017 usa uno schema diverso (Cod. Missione, stanziamenti per
-- obiettivo) ed è escluso dal perimetro del dataset.

SELECT
    cast_int(r."Anno")                                  AS anno,
    normalize_string(r.fase_codice)                     AS fase,
    LPAD(normalize_string(r."STP"), 2, '0')             AS stp,
    normalize_string(r."Descrizione Amministrazione")   AS amministrazione,
    LPAD(normalize_string(r."Codice Missione"), 3, '0') AS missione_codice,
    normalize_string(r."Missione")                      AS missione,
    LPAD(normalize_string(r."Codice Programma"), 3, '0') AS programma_codice,
    normalize_string(r."Programma")                     AS programma,
    normalize_string(r."Codice CdR")                    AS cdr_codice,
    normalize_string(r."CdR")                           AS cdr,
    normalize_string(r."Codice Obiettivo")              AS obiettivo_codice,
    normalize_string(r."Obiettivo")                     AS obiettivo,
    normalize_string(r."Descrizione Obiettivo")         AS descrizione_obiettivo,
    normalize_string(r."Natura Obiettivo")              AS natura_obiettivo,
    normalize_string(r."Codice Priorita' Politica")     AS priorita_codice,
    normalize_string(r."Priorita' Politica")            AS priorita,
    normalize_string(r."Codice Azione")                 AS azione_codice,
    normalize_string(r."Azione")                        AS azione,
    normalize_string(r."Nota Illustrativa")             AS nota_illustrativa,
    normalize_string(r."Obiettivo trasversale")         AS obiettivo_trasversale,
    normalize_string(r."Data Osservazione")             AS data_osservazione
FROM raw_input r
WHERE cast_int(r."Anno") IS NOT NULL
  AND normalize_string(r."STP") IS NOT NULL
  AND normalize_string(r."Codice Obiettivo") IS NOT NULL
