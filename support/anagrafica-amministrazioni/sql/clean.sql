-- clean.sql — bdap_ni_amministrazioni (support)
-- Anagrafica STP → denominazione delle amministrazioni centrali.
-- Fonte: sezione "Amministrazioni" delle Note Integrative (openbdap),
-- tre file per anno (DLB, LB, Rendiconto) uniti con inject_column.

SELECT
    cast_int(r."Anno")                                 AS anno,
    normalize_string(r.fase_codice)                    AS fase,
    LPAD(normalize_string(r."STP"), 2, '0')            AS stp,
    normalize_string(r."Descrizione Amministrazione")  AS amministrazione,
    normalize_string(r."Descrizione Amministraz. breve") AS amministrazione_breve
FROM raw_input r
WHERE cast_int(r."Anno") IS NOT NULL
  AND normalize_string(r."STP") IS NOT NULL
  AND normalize_string(r."Descrizione Amministrazione") IS NOT NULL
