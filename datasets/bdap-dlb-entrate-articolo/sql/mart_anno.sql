-- mart_anno.sql — totali annui delle entrate DLB
SELECT
    anno,
    round(sum(prev_bil_prec_cp) / 1e9, 3)     AS prev_bil_prec_cp_mld,
    round(sum(dlb_sez2_cp_a1) / 1e9, 3)       AS dlb_sez2_cp_a1_mld,
    round(sum(nuove_norme_cp_a1) / 1e9, 3)     AS nuove_norme_cp_a1_mld,
    round(sum(effetti_dlb_sez1_cp_a1) / 1e9, 3) AS effetti_cp_a1_mld,
    round(sum(dlb_integrato_cp_a1) / 1e9, 3)  AS dlb_integrato_cp_a1_mld,
    round(sum(dlb_integrato_cp_a2) / 1e9, 3)  AS dlb_integrato_cp_a2_mld,
    round(sum(dlb_integrato_cp_a3) / 1e9, 3)  AS dlb_integrato_cp_a3_mld,
    round(sum(dlb_integrato_cs_a1) / 1e9, 3)  AS dlb_integrato_cs_a1_mld,
    round(sum(quadratura_cp_a1) / 1e9, 3)     AS quadratura_cp_a1_mld,
    count(*)                                  AS n_articoli
FROM clean_input
GROUP BY 1
ORDER BY 1
