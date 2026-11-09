-- mart_articolo.sql — dettaglio per capitolo e articolo di entrata
SELECT
    anno,
    stato_previsione,
    amministrazione,
    centro_responsabilita,
    numero_capitolo,
    max(denominazione_capitolo) AS denominazione_capitolo,
    numero_articolo,
    max(articolo) AS articolo,
    max(codice_titolo) AS codice_titolo,
    max(titolo) AS titolo,
    max(codice_natura) AS codice_natura,
    max(natura) AS natura,
    max(codice_tipologia) AS codice_tipologia,
    max(tipologia) AS tipologia,
    max(codice_categoria) AS codice_categoria,
    max(categoria) AS categoria,
    round(sum(prev_bil_prec_cp) / 1e6, 3)    AS prev_bil_prec_cp_mln,
    round(sum(dlb_sez2_cp_a1) / 1e6, 3)      AS dlb_sez2_cp_a1_mln,
    round(sum(effetti_dlb_sez1_cp_a1) / 1e6, 3) AS effetti_cp_a1_mln,
    round(sum(dlb_integrato_cp_a1) / 1e6, 3) AS dlb_integrato_cp_a1_mln,
    round(sum(dlb_integrato_cp_a2) / 1e6, 3) AS dlb_integrato_cp_a2_mln,
    round(sum(dlb_integrato_cp_a3) / 1e6, 3) AS dlb_integrato_cp_a3_mln,
    round(sum(dlb_integrato_cs_a1) / 1e6, 3) AS dlb_integrato_cs_a1_mln
FROM clean_input
GROUP BY 1, 2, 3, 4, 5, 7
ORDER BY 1, 2, 3, 5, 7
