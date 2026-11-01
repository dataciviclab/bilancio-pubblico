-- mart_articolo.sql — dettaglio per capitolo e articolo di entrata
SELECT
    anno,
    amministrazione,
    capitolo,
    articolo,
    max(titolo)      AS titolo,
    max(natura)      AS natura,
    max(tipologia)   AS tipologia,
    max(provento)    AS provento,
    max(categoria)   AS categoria,
    round(sum(prev_def_cp) / 1e6, 3)           AS prev_def_cp_mln,
    round(sum(versato_cp) / 1e6, 3)            AS versato_cp_mln,
    round(sum(rimasto_versare_cp) / 1e6, 3)    AS rimasto_versare_cp_mln,
    round(sum(rimasto_riscuotere_cp) / 1e6, 3) AS rimasto_riscuotere_cp_mln,
    round(sum(totale_cp) / 1e6, 3)             AS totale_cp_mln,
    round(sum(prev_def_cs) / 1e6, 3)           AS prev_def_cs_mln,
    round(sum(versato_cs) / 1e6, 3)            AS versato_cs_mln
FROM clean_input
GROUP BY 1, 2, 3, 4
ORDER BY 1, 2, 3, 4
