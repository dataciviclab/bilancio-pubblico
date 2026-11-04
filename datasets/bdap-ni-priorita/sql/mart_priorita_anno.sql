-- mart_priorita_anno.sql — priorità politiche per amministrazione e anno
-- Quante priorità dichiara ogni ministero, quanto sono lunghe, quante citano
-- il PNRR. n_ministri_coperti rende esplicito un limite della fonte: la
-- copertura non è uniforme per anno e fase (il DLB arriva a 6 ministeri su 15),
-- quindi un confronto tra fasi va letto insieme a questa colonna.

WITH agg AS (
    SELECT
        anno,
        fase,
        stp,
        MAX(amministrazione)                     AS amministrazione,
        COUNT(*)                                 AS n_priorita,
        COUNT(DISTINCT codice_priorita)          AS n_priorita_distinte,
        ROUND(AVG(length(contenuto)), 0)         AS lunghezza_media_contenuto,
        SUM(CASE WHEN contenuto ILIKE '%PNRR%' THEN 1 ELSE 0 END) AS n_con_pnrr
    FROM clean_input
    GROUP BY 1, 2, 3
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
    a.n_priorita,
    a.n_priorita_distinte,
    a.lunghezza_media_contenuto,
    a.n_con_pnrr,
    c.n_ministri_coperti
FROM agg a
JOIN cop c ON c.anno = a.anno AND c.fase = a.fase
ORDER BY a.anno, a.fase, a.stp
