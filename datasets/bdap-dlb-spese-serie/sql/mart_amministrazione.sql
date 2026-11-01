-- mart_dlb_spese_amministrazione.sql — spese per amministrazione e macroaggregato
SELECT
    anno,
    annualita,
    amministrazione,
    macroaggregato,
    round(sum(cp) / 1e9, 3) AS cp_mld,
    round(sum(cs) / 1e9, 3) AS cs_mld
FROM clean_input
GROUP BY 1, 2, 3, 4
ORDER BY 1, 2, 3, 4
