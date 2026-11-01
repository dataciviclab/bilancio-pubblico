-- mart_anno.sql — totali annui del consuntivo entrate
SELECT
    anno,
    round(sum(prev_def_cp) / 1e9, 3)           AS prev_def_cp_mld,
    round(sum(totale_cp) / 1e9, 3)             AS totale_cp_mld,
    round(sum(versato_cp) / 1e9, 3)            AS versato_cp_mld,
    round(sum(rimasto_versare_cp) / 1e9, 3)    AS rimasto_versare_cp_mld,
    round(sum(rimasto_riscuotere_cp) / 1e9, 3) AS rimasto_riscuotere_cp_mld,
    round(sum(prev_def_cs) / 1e9, 3)           AS prev_def_cs_mld,
    round(sum(versato_cs) / 1e9, 3)            AS versato_cs_mld
FROM clean_input
GROUP BY 1
ORDER BY 1
