-- mart_amministrazione.sql — consuntivo entrate per amministrazione
SELECT
    anno,
    amministrazione,
    round(sum(prev_def_cp) / 1e9, 3)           AS prev_def_cp_mld,
    round(sum(totale_cp) / 1e9, 3)             AS totale_cp_mld,
    round(sum(versato_cp) / 1e9, 3)            AS versato_cp_mld,
    round(sum(rimasto_riscuotere_cp) / 1e9, 3) AS rimasto_riscuotere_cp_mld
FROM clean_input
GROUP BY 1, 2
ORDER BY 1, 2
