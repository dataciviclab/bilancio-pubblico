-- mart_missione.sql — DLB integrato per missione
SELECT
    anno,
    codice_missione,
    max(missione) AS missione,
    round(sum(plb_vigente_cp_a1) / 1e9, 3)   AS plb_vigente_cp_a1_mld,
    round(sum(dlb_integrato_cp_a1) / 1e9, 3) AS dlb_integrato_cp_a1_mld,
    round(sum(dlb_integrato_cp_a2) / 1e9, 3) AS dlb_integrato_cp_a2_mld,
    round(sum(dlb_integrato_cp_a3) / 1e9, 3) AS dlb_integrato_cp_a3_mld,
    count(*) AS n_capitoli
FROM clean_input
GROUP BY 1, 2
ORDER BY 1, 2
