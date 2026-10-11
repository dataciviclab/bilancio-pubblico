-- mart_per_missione_italia.sql
-- Solo livello ITALIA, misura "Valori Assoluti (mln)".
-- Confrontabile (con cautela) con bdap_spese_stato per missione.

SELECT
    anno,
    codice_missione,
    ANY_VALUE(missione) AS missione,
    ROUND(SUM(importo), 2) AS importo_mln,
    STRING_AGG(DISTINCT titolo, ' | ' ORDER BY titolo) AS titoli,
    COUNT(DISTINCT categoria) AS n_categorie
FROM clean_input
WHERE livello_territoriale = 'Italia'
  AND misura = 'Spesa Complessiva - Valori Assoluti (mln)'
  AND codice_missione IS NOT NULL
GROUP BY anno, codice_missione
ORDER BY anno, importo_mln DESC
