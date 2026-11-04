-- mart_obiettivi_anno.sql — obiettivi per amministrazione, natura e anno
-- Quanti obiettivi strategici (politiche di settore) e strutturali (attività
-- continuativa) dichiara ogni ministero, e su quante priorità/programmi/azioni
-- insiste. n_ministri_coperti rende esplicita la copertura della fase.

WITH agg AS (
    SELECT
        anno,
        fase,
        stp,
        MAX(amministrazione)             AS amministrazione,
        natura_obiettivo,
        COUNT(*)                         AS n_obiettivi,
        COUNT(DISTINCT obiettivo_codice) AS n_obiettivi_distinti,
        COUNT(DISTINCT priorita_codice)  AS n_priorita,
        COUNT(DISTINCT programma_codice) AS n_programmi,
        COUNT(DISTINCT azione_codice)    AS n_azioni
    FROM clean_input
    GROUP BY 1, 2, 3, 5
),
cop AS (
    SELECT anno, fase, COUNT(DISTINCT stp) AS n_ministri_coperti
    FROM clean_input
    GROUP BY 1, 2
)

SELECT
    a.anno,
    a.fase,
    a.stp,
    a.amministrazione,
    a.natura_obiettivo,
    a.n_obiettivi,
    a.n_obiettivi_distinti,
    a.n_priorita,
    a.n_programmi,
    a.n_azioni,
    c.n_ministri_coperti
FROM agg a
JOIN cop c ON c.anno = a.anno AND c.fase = a.fase
ORDER BY a.anno, a.fase, a.stp, a.natura_obiettivo
