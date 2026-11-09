-- mart_variazione_articolo.sql — variazione rispetto al bilancio dell'anno precedente.
-- Sulle entrate non esiste la "legislazione vigente": il confronto naturale è
-- con "Prev. Bil. Esercizio prec.", cioè quanto era previsto l'anno prima.
-- Non è la manovra (che sulle spese è PLB -> DLB integrato): è anno-su-anno.
SELECT
    anno,
    stato_previsione,
    amministrazione,
    numero_capitolo,
    denominazione_capitolo,
    numero_articolo,
    articolo,
    codice_titolo,
    titolo,
    codice_categoria,
    categoria,
    round(prev_bil_prec_cp / 1e6, 3) AS prev_bil_prec_cp_mln,
    round(dlb_integrato_cp_a1 / 1e6, 3) AS dlb_integrato_cp_a1_mln,
    round((dlb_integrato_cp_a1 - prev_bil_prec_cp) / 1e6, 3) AS delta_vs_prec_cp_a1_mln,
    round(
        (dlb_integrato_cp_a1 - prev_bil_prec_cp) / nullif(prev_bil_prec_cp, 0),
        4
    ) AS quota_variazione_cp_a1
FROM clean_input
ORDER BY anno, abs(coalesce(dlb_integrato_cp_a1, 0) - coalesce(prev_bil_prec_cp, 0)) DESC
