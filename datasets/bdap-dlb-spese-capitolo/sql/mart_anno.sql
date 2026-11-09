-- mart_anno.sql — totali annui del DLB per capitolo
SELECT
    anno,
    round(sum(plb_vigente_cp_a1) / 1e9, 3)   AS plb_vigente_cp_a1_mld,
    round(sum(rimodulazioni_cp_a1) / 1e9, 3) AS rimodulazioni_cp_a1_mld,
    round(sum(rif_def_rip_cp_a1) / 1e9, 3)   AS rif_def_rip_cp_a1_mld,
    round(sum(var_manovra_sez2_cp_a1) / 1e9, 3) AS var_manovra_sez2_cp_a1_mld,
    round(sum(effetti_dlb_sez1_cp_a1) / 1e9, 3) AS effetti_dlb_sez1_cp_a1_mld,
    round(sum(dlb_sez2_cp_a1) / 1e9, 3)      AS dlb_sez2_cp_a1_mld,
    round(sum(dlb_integrato_cp_a1) / 1e9, 3) AS dlb_integrato_cp_a1_mld,
    round(sum(dlb_integrato_cp_a2) / 1e9, 3) AS dlb_integrato_cp_a2_mld,
    round(sum(dlb_integrato_cp_a3) / 1e9, 3) AS dlb_integrato_cp_a3_mld,
    round(sum(dlb_integrato_cs_a1) / 1e9, 3) AS dlb_integrato_cs_a1_mld,
    round(sum(dlb_integrato_rs_a1) / 1e9, 3) AS dlb_integrato_rs_a1_mld,
    round(sum(quadratura_cp_a1) / 1e9, 3)    AS quadratura_cp_a1_mld,
    count(*)                                 AS n_capitoli
FROM clean_input
GROUP BY 1
ORDER BY 1
