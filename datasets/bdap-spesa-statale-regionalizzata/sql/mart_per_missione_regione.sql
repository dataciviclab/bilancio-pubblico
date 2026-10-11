-- mart_per_missione_regione.sql
-- Regioni (livello Regione), misura valori assoluti — distribuzione territoriale.

SELECT
    anno,
    territorio,
    codice_missione,
    ANY_VALUE(missione) AS missione,
    ROUND(SUM(importo), 2) AS importo_mln,
    COUNT(DISTINCT categoria) AS n_categorie
FROM clean_input
WHERE livello_territoriale = 'Regione'
  AND misura = 'Spesa Complessiva - Valori Assoluti (mln)'
  AND codice_missione IS NOT NULL
GROUP BY anno, territorio, codice_missione
ORDER BY anno, importo_mln DESC
