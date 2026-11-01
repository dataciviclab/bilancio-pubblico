-- mart_capitolo.sql — dettaglio per capitolo di spesa
SELECT
    anno,
    amministrazione,
    capitolo,
    max(denominazione_capitolo) AS denominazione_capitolo,
    max(codice_missione)        AS codice_missione,
    max(missione)               AS missione,
    max(codice_programma)       AS codice_programma,
    max(programma)              AS programma,
    max(categoria)              AS categoria,
    round(sum(prev_def_cp) / 1e6, 3) AS prev_def_cp_mln,
    round(sum(pagato_cp) / 1e6, 3)   AS pagato_cp_mln,
    round(sum(rimasto_cp) / 1e6, 3)  AS rimasto_cp_mln,
    round(sum(totale_cp) / 1e6, 3)   AS totale_cp_mln,
    round(sum(economie_cp) / 1e6, 3) AS economie_cp_mln,
    round(sum(prev_def_cs) / 1e6, 3) AS prev_def_cs_mln,
    round(sum(pagato_cs) / 1e6, 3)   AS pagato_cs_mln,
    round(sum(prev_def_rs) / 1e6, 3) AS prev_def_rs_mln,
    round(sum(pagato_rs) / 1e6, 3)   AS pagato_rs_mln,
    round(sum(rimasto_rs) / 1e6, 3)  AS rimasto_rs_mln
FROM clean_input
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3
