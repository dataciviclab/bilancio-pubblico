-- mart_capitolo.sql — dettaglio per capitolo di spesa
SELECT
    anno,
    stato_previsione,
    amministrazione,
    numero_capitolo,
    max(denominazione_capitolo) AS denominazione_capitolo,
    max(codice_missione)        AS codice_missione,
    max(missione)               AS missione,
    max(codice_programma)       AS codice_programma,
    max(programma)              AS programma,
    max(codice_azione)          AS codice_azione,
    max(azione)                 AS azione,
    max(codice_cdr)             AS codice_cdr,
    max(cdr)                    AS cdr,
    max(categoria)              AS categoria,
    round(sum(plb_vigente_cp_a1) / 1e6, 3)   AS plb_vigente_cp_a1_mln,
    round(sum(rimodulazioni_cp_a1) / 1e6, 3) AS rimodulazioni_cp_a1_mln,
    round(sum(dlb_sez2_cp_a1) / 1e6, 3)      AS dlb_sez2_cp_a1_mln,
    round(sum(effetti_dlb_sez1_cp_a1) / 1e6, 3) AS effetti_dlb_sez1_cp_a1_mln,
    round(sum(dlb_integrato_cp_a1) / 1e6, 3) AS dlb_integrato_cp_a1_mln,
    round(sum(dlb_integrato_cp_a2) / 1e6, 3) AS dlb_integrato_cp_a2_mln,
    round(sum(dlb_integrato_cp_a3) / 1e6, 3) AS dlb_integrato_cp_a3_mln,
    round(sum(dlb_integrato_cs_a1) / 1e6, 3) AS dlb_integrato_cs_a1_mln
FROM clean_input
GROUP BY 1, 2, 3, 4
ORDER BY 1, 2, 3, 4
