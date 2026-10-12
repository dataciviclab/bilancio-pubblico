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
--
-- Macro toolkit: normalize_string, cast_int, cast_double.

SELECT
    cast_int("Anno di Interesse") AS anno,
    normalize_string("Territorio") AS territorio,
    CASE
        WHEN normalize_string("Territorio") = 'ITALIA' THEN 'Italia'
        WHEN normalize_string("Territorio") IN (
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
    cast_double("Importo") AS importo
FROM raw_input
WHERE cast_int("Anno di Interesse") IS NOT NULL
  AND normalize_string("Territorio") IS NOT NULL
  AND normalize_string("Missione") IS NOT NULL
