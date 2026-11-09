-- mart_titolo.sql — entrate per titolo
SELECT
    anno,
    codice_titolo,
    max(titolo) AS titolo,
    round(sum(prev_bil_prec_cp) / 1e9, 3)    AS prev_bil_prec_cp_mld,
    round(sum(dlb_integrato_cp_a1) / 1e9, 3) AS dlb_integrato_cp_a1_mld,
    round(sum(dlb_integrato_cp_a2) / 1e9, 3) AS dlb_integrato_cp_a2_mld,
    count(*) AS n_articoli
FROM clean_input
GROUP BY 1, 2
ORDER BY 1, 2
