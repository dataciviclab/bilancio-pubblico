-- mart_dlb_spese_missione.sql — spese per missione, con ripartizione per amministrazione
SELECT
    anno,
    annualita,
    missione,
    amministrazione,
    round(sum(cp) / 1e9, 3) AS cp_mld,
    round(sum(cs) / 1e9, 3) AS cs_mld
FROM clean_input
GROUP BY 1, 2, 3, 4
ORDER BY 1, 2, 3, 4
