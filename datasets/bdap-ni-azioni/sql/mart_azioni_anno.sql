-- mart_azioni_anno.sql — la catena DLB → LB → Rendiconto sugli stanziamenti
-- Per ogni amministrazione e fase: quanto vale la programmazione, quanto è
-- stato stanziato in via definitiva, quanto è stato impegnato e pagato.
-- stanziamento_cp_mld usa la grandezza omogenea tra le fasi:
--   DLB/LB → previsione_cp_anno1 (primo anno del triennio)
--   RND    → stanziamento_iniziale_cp (bilancio iniziale dell'anno)
-- n_ministri_coperti rende esplicita la copertura della fase.

WITH agg AS (
    SELECT
        anno,
        fase,
        stp,
        MAX(amministrazione) AS amministrazione,
        COUNT(*)             AS n_azioni,
        SUM(COALESCE(previsione_cp_anno1, stanziamento_iniziale_cp)) AS cp,
        SUM(COALESCE(previsione_cs_anno1, stanziamento_iniziale_cs)) AS cs,
        SUM(stanziamento_definitivo_cp) AS def_cp,
        SUM(impegnato_cp)               AS imp_cp,
        SUM(pagato_cp)                  AS pag_cp
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
    a.n_azioni,
    ROUND(a.cp / 1e9, 3)     AS stanziamento_cp_mld,
    ROUND(a.cs / 1e9, 3)     AS stanziamento_cs_mld,
    ROUND(a.def_cp / 1e9, 3) AS stanziamento_definitivo_cp_mld,
    ROUND(a.imp_cp / 1e9, 3) AS impegnato_cp_mld,
    ROUND(a.pag_cp / 1e9, 3) AS pagato_cp_mld,
    ROUND(100.0 * a.imp_cp / NULLIF(a.def_cp, 0), 2)   AS pct_impegnato_su_definitivo,
    ROUND(100.0 * a.def_cp / NULLIF(a.cp, 0), 2)      AS pct_definitivo_su_stanziamento,
    c.n_ministri_coperti
FROM agg a
JOIN cop c ON c.anno = a.anno AND c.fase = a.fase
ORDER BY a.anno, a.fase, a.stp
