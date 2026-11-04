-- clean.sql — bdap_ni_priorita
-- Note Integrative — sezione "Priorità Politiche".
-- Tre file per anno (DLB, LB, Rendiconto) uniti da toolkit con union_by_name.
--
-- La fonte cambia intestazioni nel tempo e il cambio non è uniforme per anno:
--   2018 DLB/LB e 2019 DLB   → "Descrizione Priorita' Politica"
--   2018 RND, 2019 LB/RND+   → "Contenuto Priorita' Politica"
-- Per questo il testo si legge con COALESCE su accesso JSON: un nome di
-- colonna assente farebbe fallire il bind, una chiave JSON assente vale NULL.
-- Il nome dell'amministrazione non è presente nei file dal 2020 in poi:
-- viene sempre preso dall'anagrafica STP (support), autorevole per anno.

WITH src AS (
    SELECT
        cast_int(r."Anno")                      AS anno,
        normalize_string(r.fase_codice)         AS fase,
        LPAD(normalize_string(r."STP"), 2, '0') AS stp,
        normalize_string(r."Codice Priorita' Politica") AS codice_priorita,
        normalize_string(r."Priorita' Politica")        AS priorita,
        normalize_string(
            COALESCE(
                to_json(r) ->> 'Contenuto Priorita'' Politica',
                to_json(r) ->> 'Descrizione Priorita'' Politica'
            )
        ) AS contenuto,
        normalize_string(r."Data Osservazione") AS data_osservazione
    FROM raw_input r
),
amm AS (
    -- Tutte le fasi, non solo LB: un ministero creato in corso d'anno può
    -- comparire nel rendiconto ma non nello stato di previsione iniziale.
    SELECT
        anno,
        stp,
        MAX(amministrazione) AS amministrazione
    FROM read_parquet('{support.bdap_ni_amministrazioni.clean}')
    WHERE amministrazione IS NOT NULL
    GROUP BY 1, 2
)

SELECT
    s.anno,
    s.fase,
    s.stp,
    a.amministrazione,
    s.codice_priorita,
    s.priorita,
    s.contenuto,
    s.data_osservazione
FROM src s
LEFT JOIN amm a
       ON a.anno = s.anno
      AND a.stp  = s.stp
WHERE s.anno IS NOT NULL
  AND s.stp IS NOT NULL
  AND s.codice_priorita IS NOT NULL
