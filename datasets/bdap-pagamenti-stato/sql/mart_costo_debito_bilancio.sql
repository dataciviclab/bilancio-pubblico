-- mart_costo_debito_bilancio.sql — Spesa della missione Debito pubblico e sue componenti
--
-- ATTENZIONE ALLA DEFINIZIONE: la missione 034 non è il solo costo per interessi.
-- Contiene:
--   - INTERESSI PASSIVI E ALTRI ONERI FINANZIARI  -> interessi_pagati
--   - RIMBORSO PASSIVITA' FINANZIARIE             -> rimborsi_pagati
--   - ACQUISIZIONI DI ATTIVITA' FINANZIARIE + CONSUMI INTERMEDI -> altri_oneri_debito
--
-- Per il confronto con le stime OCPI (costo del debito) usare `interessi_pagati`.
-- `spesa_missione_debito` è il totale della missione e include la restituzione del capitale.

WITH per_anno AS (
    SELECT
        esercizio_finanziario AS anno,
        SUM(totale_pagato) AS spesa_missione_debito,
        SUM(
            CASE
                WHEN categoria = 'INTERESSI PASSIVI E ALTRI ONERI FINANZIARI' THEN totale_pagato
                ELSE 0
            END
        ) AS interessi_pagati,
        SUM(
            CASE
                WHEN categoria = 'RIMBORSO PASSIVITA'' FINANZIARIE' THEN totale_pagato
                ELSE 0
            END
        ) AS rimborsi_pagati,
        SUM(
            CASE
                WHEN categoria NOT IN (
                    'INTERESSI PASSIVI E ALTRI ONERI FINANZIARI',
                    'RIMBORSO PASSIVITA'' FINANZIARIE'
                ) THEN totale_pagato
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
