-- clean.sql — bdap_spesa_statale_regionalizzata
-- SRS_SPE_BIL_SPESR_001 — spesa Stato per territorio destinatario
--
-- Fonte: OpenBDAP dump SpodCkanApi (cp1252, `;`)
-- Grano: anno × territorio × titolo × categoria × missione × misura
--
-- ATTNZIONE semantica (perché "non quadrava" con bdap_spese_stato):
--   1. Italia, ripartizioni e regioni sono livelli SOVRAPPOSTI — non sommarli.
--   2. Le 4 misure sono distinte (mln assoluti, % PIL, €/ab, €/kmq).
--   3. Schema e categorie variano tra annualità (drift dichiarato dalla fonte).
--   4. Non è grain programma/macroaggregato: è titolo/categoria/missione territorializzato.

SELECT
    CAST("Anno di Interesse" AS INTEGER) AS anno,
    normalize_string("Territorio") AS territorio,
    CASE
        WHEN UPPER(TRIM("Territorio")) = 'ITALIA' THEN 'Italia'
        WHEN UPPER(TRIM("Territorio")) IN (
            'CENTRO', 'ISOLE', 'NORD-EST', 'NORD-OVEST', 'SUD'
        ) THEN 'Ripartizione'
        ELSE 'Regione'
    END AS livello_territoriale,
    normalize_string("Titolo") AS titolo,
    normalize_string("Categoria") AS categoria,
    -- Missione nel formato "003-Relazioni finanziarie..."
    regexp_extract(normalize_string("Missione"), '^([0-9]{3})-', 1) AS codice_missione,
    regexp_replace(normalize_string("Missione"), '^[0-9]{3}-', '') AS missione,
    normalize_string("Tipo Misura") AS misura,
    CAST("Importo" AS DOUBLE) AS importo
FROM raw_input
WHERE CAST("Anno di Interesse" AS INTEGER) IS NOT NULL
  AND NULLIF(TRIM("Territorio"), '') IS NOT NULL
  AND NULLIF(TRIM("Missione"), '') IS NOT NULL
