-- mart_costo_debito_bilancio.sql — Spesa della missione Debito pubblico e sue componenti
--
-- ATTENZIONE ALLA DEFINIZIONE: la missione 034 non è il solo costo per interessi.
-- Contiene:
--   - interessi (categoria "INTERESSI PASSIVI E REDDITI DA CAPITALE" fino al 2022,
--     "INTERESSI PASSIVI E ALTRI ONERI FINANZIARI" dal 2023) -> interessi_pagati
--   - RIMBORSO PASSIVITA' FINANZIARIE             -> rimborsi_pagati
--   - ACQUISIZIONI DI ATTIVITA' FINANZIARIE + CONSUMI INTERMEDI -> altri_oneri_debito
--
-- Il nome della categoria degli interessi cambia nel tempo: si usa il prefisso.
-- Per il confronto con le stime OCPI (costo del debito) usare `interessi_pagati`.
-- `spesa_missione_debito` è il totale della missione e include la restituzione del capitale.

WITH per_anno AS (
    SELECT
        esercizio_finanziario AS anno,
        SUM(totale_pagato) AS spesa_missione_debito,
        SUM(
            CASE
                WHEN categoria LIKE 'INTERESSI PASSIVI%' THEN totale_pagato
                ELSE 0
            END
        ) AS interessi_pagati,
        SUM(
            CASE
                WHEN categoria LIKE 'RIMBORSO PASSIVITA%' THEN totale_pagato
                ELSE 0
            END
        ) AS rimborsi_pagati,
        SUM(
            CASE
                WHEN categoria NOT LIKE 'INTERESSI PASSIVI%'
                 AND categoria NOT LIKE 'RIMBORSO PASSIVITA%' THEN totale_pagato
                ELSE 0
            END
        ) AS altri_oneri_debito,
        SUM(note_imputazione) AS note_imputazione
    FROM clean_input
    WHERE codice_missione = '034'
    GROUP BY 1
)
SELECT
    anno,
    ROUND(spesa_missione_debito, 0) AS spesa_missione_debito,
    ROUND(interessi_pagati, 0) AS interessi_pagati,
    ROUND(rimborsi_pagati, 0) AS rimborsi_pagati,
    ROUND(altri_oneri_debito, 0) AS altri_oneri_debito,
    ROUND(note_imputazione, 0) AS note_imputazione,
    ROUND(100.0 * (spesa_missione_debito - LAG(spesa_missione_debito) OVER (ORDER BY anno))
          / NULLIF(LAG(spesa_missione_debito) OVER (ORDER BY anno), 0), 2) AS var_pct_spesa,
    ROUND(100.0 * (interessi_pagati - LAG(interessi_pagati) OVER (ORDER BY anno))
          / NULLIF(LAG(interessi_pagati) OVER (ORDER BY anno), 0), 2) AS var_pct_interessi
FROM per_anno
ORDER BY anno
