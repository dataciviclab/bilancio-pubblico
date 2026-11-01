-- mart_anno.sql — totali annui del rendiconto per capitolo
SELECT
    anno,
    round(sum(prev_def_cp) / 1e9, 3) AS prev_def_cp_mld,
    round(sum(pagato_cp) / 1e9, 3)   AS pagato_cp_mld,
    round(sum(rimasto_cp) / 1e9, 3)  AS rimasto_cp_mld,
    round(sum(totale_cp) / 1e9, 3)   AS totale_cp_mld,
    round(sum(economie_cp) / 1e9, 3) AS economie_cp_mld,
    round(sum(prev_def_cs) / 1e9, 3) AS prev_def_cs_mld,
    round(sum(pagato_cs) / 1e9, 3)   AS pagato_cs_mld,
    round(sum(prev_def_rs) / 1e9, 3) AS prev_def_rs_mld,
    round(sum(pagato_rs) / 1e9, 3)   AS pagato_rs_mld,
    round(sum(rimasto_rs) / 1e9, 3)  AS rimasto_rs_mld
FROM clean_input
GROUP BY 1
ORDER BY 1
