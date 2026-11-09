-- mart_manovra_capitolo.sql — cosa cambia la manovra, capitolo per capitolo.
-- Delta fra legislazione vigente (PLB) e DLB integrato: è la risposta a
-- "dove sono andati i soldi della legge di bilancio", riga per riga.
-- Un delta positivo = più soldi alla linea; negativo = taglio.
SELECT
    anno,
    stato_previsione,
    amministrazione,
    numero_capitolo,
    denominazione_capitolo,
    codice_missione,
    missione,
    codice_programma,
    programma,
    codice_azione,
    azione,
    codice_cdr,
    cdr,
    categoria,
    round(plb_vigente_cp_a1 / 1e6, 3) AS plb_vigente_cp_a1_mln,
    round(dlb_integrato_cp_a1 / 1e6, 3) AS dlb_integrato_cp_a1_mln,
    round((dlb_integrato_cp_a1 - plb_vigente_cp_a1) / 1e6, 3) AS delta_cp_a1_mln,
    round((dlb_integrato_cp_a2 - plb_vigente_cp_a2) / 1e6, 3) AS delta_cp_a2_mln,
    round((dlb_integrato_cp_a3 - plb_vigente_cp_a3) / 1e6, 3) AS delta_cp_a3_mln,
    round((dlb_integrato_cs_a1 - plb_vigente_cs_a1) / 1e6, 3) AS delta_cs_a1_mln,
    -- variazione relativa: null se la linea partiva da zero
    round(
        (dlb_integrato_cp_a1 - plb_vigente_cp_a1) / nullif(plb_vigente_cp_a1, 0),
        4
    ) AS quota_variazione_cp_a1
FROM clean_input
ORDER BY anno, abs(coalesce(dlb_integrato_cp_a1, 0) - coalesce(plb_vigente_cp_a1, 0)) DESC
