-- mart_amministrazione.sql — consuntivo di competenza per amministrazione
SELECT
    anno,
    amministrazione,
    round(sum(prev_def_cp) / 1e9, 3) AS prev_def_cp_mld,
    round(sum(pagato_cp) / 1e9, 3)   AS pagato_cp_mld,
    round(sum(rimasto_cp) / 1e9, 3)  AS rimasto_cp_mld,
    round(sum(totale_cp) / 1e9, 3)   AS totale_cp_mld,
    round(sum(economie_cp) / 1e9, 3) AS economie_cp_mld,
    round(sum(pagato_cs) / 1e9, 3)   AS pagato_cs_mld
FROM clean_input
GROUP BY 1, 2
ORDER BY 1, 2
