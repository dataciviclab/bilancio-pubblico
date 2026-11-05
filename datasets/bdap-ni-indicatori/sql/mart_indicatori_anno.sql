-- mart_indicatori_anno.sql — indicatori, target e risultato per amministrazione
-- Per ogni anno, fase e tipo di indicatore:
--   n_indicatori            quanti indicatori dichiarati
--   pct_target_numerico     quota con un target numerico interpretabile
--                           (il resto è testo, intervallo o booleano)
--   n_confrontabili         target e rendiconto entrambi numerici, stessa unità
--   pct_target_raggiunto    quota di target centrati (solo fase Rendiconto)
--
-- Il confronto usa l'operatore dichiarato: ">= 90" è centrato se il valore
-- è almeno 90, "< 5" se il valore è sotto 5. Senza operatore vale ">=".
-- n_ministri_coperti rende esplicita la copertura della fase.

WITH base AS (
    SELECT
        anno,
        fase,
        stp,
        amministrazione,
        tipo_indicatore,
        target_anno1_valore,
        valore_rendiconto_valore,
        COALESCE(target_anno1_unita, '') = COALESCE(valore_rendiconto_unita, '') AS unita_coerenti,
        CASE
            WHEN target_anno1_valore IS NULL OR valore_rendiconto_valore IS NULL THEN NULL
            WHEN target_anno1_operatore = '<'
                 THEN valore_rendiconto_valore < target_anno1_valore
            WHEN target_anno1_operatore = '<='
                 THEN valore_rendiconto_valore <= target_anno1_valore
            WHEN target_anno1_operatore = '>'
                 THEN valore_rendiconto_valore > target_anno1_valore
            ELSE valore_rendiconto_valore >= target_anno1_valore
        END AS target_raggiunto
    FROM clean_input
),
agg AS (
    SELECT
        anno,
        fase,
        stp,
        MAX(amministrazione) AS amministrazione,
        tipo_indicatore,
        COUNT(*) AS n_indicatori,
        SUM(CASE WHEN target_anno1_valore IS NOT NULL THEN 1 ELSE 0 END) AS n_target_numerico,
        SUM(CASE WHEN unita_coerenti AND target_raggiunto IS NOT NULL THEN 1 ELSE 0 END) AS n_confrontabili,
        SUM(CASE WHEN unita_coerenti AND target_raggiunto THEN 1 ELSE 0 END) AS n_target_raggiunto
    FROM base
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
    a.tipo_indicatore,
    a.n_indicatori,
    a.n_target_numerico,
    ROUND(100.0 * a.n_target_numerico / NULLIF(a.n_indicatori, 0), 1) AS pct_target_numerico,
    a.n_confrontabili,
    a.n_target_raggiunto,
    ROUND(100.0 * a.n_target_raggiunto / NULLIF(a.n_confrontabili, 0), 1) AS pct_target_raggiunto,
    c.n_ministri_coperti
FROM agg a
JOIN cop c ON c.anno = a.anno AND c.fase = a.fase
ORDER BY a.anno, a.fase, a.stp, a.tipo_indicatore
