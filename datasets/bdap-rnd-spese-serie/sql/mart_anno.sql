-- mart_rnd_spese_anno.sql — totali per anno e annualità
SELECT
    anno,
    annualita,
    round(sum(cp) / 1e9, 3) AS cp_mld,
    round(sum(cs) / 1e9, 3) AS cs_mld
FROM clean_input
GROUP BY 1, 2
ORDER BY 1, 2
