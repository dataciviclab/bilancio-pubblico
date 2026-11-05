-- clean.sql — bdap_ni_indicatori
-- Note Integrative — sezione "Indicatori": il target triennale e, a
-- rendiconto, il valore effettivo. È il punto in cui la programmazione
-- diventa misurabile.
--
-- Due schemi convivono, distinti dalla fase:
--   DLB / LB   Valore anno 1/2/3            (target)
--   RND        Valore anno 1 a LB           (target, ripreso dalla LB)
--              Valore a Rendiconto          (risultato)
--
-- I valori sono testo libero: ">= 91%", "91,50%", "3.020.000,00", "SI",
-- "25% <= x <= 50%". Il parsing numerico è volutamente stretto: accetta solo
-- un numero singolo con eventuale operatore e unità, e lascia NULL tutto il
-- resto (intervalli, booleani, prosa). Il testo originale resta sempre.

WITH base AS (
    SELECT
        cast_int(r."Anno")                                   AS anno,
        normalize_string(r.fase_codice)                      AS fase,
        LPAD(normalize_string(r."STP"), 2, '0')              AS stp,
        normalize_string(r."Descrizione Amministrazione")    AS amministrazione,
        LPAD(normalize_string(r."Codice Missione"), 3, '0')  AS missione_codice,
        normalize_string(r."Missione")                       AS missione,
        LPAD(normalize_string(r."Codice Programma"), 3, '0') AS programma_codice,
        normalize_string(r."Programma")                      AS programma,
        normalize_string(r."Codice CdR")                     AS cdr_codice,
        normalize_string(r."CdR")                            AS cdr,
        normalize_string(r."Codice Obiettivo")               AS obiettivo_codice,
        normalize_string(r."Obiettivo")                      AS obiettivo,
        normalize_string(r."Codice Indicatore")              AS indicatore_codice,
        normalize_string(r."Indicatore")                     AS indicatore,
        normalize_string(r."Descrizione Indicatore")         AS descrizione_indicatore,
        normalize_string(COALESCE(r."Tipo Valore", r."Tipo Indicatore"))       AS tipo_indicatore,
        normalize_string(COALESCE(r."Tipo Misura", r."Tipo Misura Ind."))       AS tipo_misura,
        normalize_string(COALESCE(r."Unità di misura", r."Unità di misura Ind.")) AS unita_misura,
        normalize_string(r."Metodo di calcolo Ind.")         AS metodo_calcolo,
        normalize_string(COALESCE(r."Fonte del dato", r."Fonte Indicatore"))   AS fonte,
        normalize_string(COALESCE(r."Valore anno 1", r."Valore anno 1 a LB"))  AS target_anno1,
        normalize_string(r."Valore anno 2")                  AS target_anno2,
        normalize_string(r."Valore anno 3")                  AS target_anno3,
        normalize_string(r."Valore a Rendiconto")            AS valore_rendiconto,
        normalize_string(r."Nota mancanza valori target")    AS nota_mancanza_target,
        -- La nota cambia nome nel 2019 ("mancanza" → "mancata") e nel 2018
        -- esiste solo la variante vecchia: accesso JSON per tollerare l'assenza.
        normalize_string(
            COALESCE(
                to_json(r) ->> 'Nota mancata consuntivazione',
                to_json(r) ->> 'Nota mancanza consuntivazione'
            )
        ) AS nota_mancata_consuntivazione,
        normalize_string(r."Nota scostamento")               AS nota_scostamento,
        normalize_string(r."Valore di riferimento")          AS valore_riferimento,
        normalize_string(r."Descrizione e provenienza")      AS descrizione_provenienza,
        normalize_string(COALESCE(r."Indicatore trasversale", r."Codice Indicatore trasversale")) AS indicatore_trasversale,
        normalize_string(r."Data Osservazione")              AS data_osservazione
    FROM raw_input r
),
tok AS (
    -- Estrae operatore e numero solo se il valore è un singolo numero
    -- (con eventuale >=, <=, >, <, = e unità % / € / euro).
    SELECT
        b.*,
        CASE WHEN regexp_matches(trim(b.target_anno1), '^(>=|<=|>|<|=)?\s*-?[0-9][0-9.,]*\s*(%|€|euro)?$')
             THEN regexp_extract(trim(b.target_anno1), '^(>=|<=|>|<|=)?\s*(-?[0-9][0-9.,]*)', 1) END AS t1_op,
        CASE WHEN regexp_matches(trim(b.target_anno1), '^(>=|<=|>|<|=)?\s*-?[0-9][0-9.,]*\s*(%|€|euro)?$')
             THEN regexp_extract(trim(b.target_anno1), '^(>=|<=|>|<|=)?\s*(-?[0-9][0-9.,]*)', 2) END AS t1_num,
        CASE WHEN regexp_matches(trim(b.valore_rendiconto), '^(>=|<=|>|<|=)?\s*-?[0-9][0-9.,]*\s*(%|€|euro)?$')
             THEN regexp_extract(trim(b.valore_rendiconto), '^(>=|<=|>|<|=)?\s*(-?[0-9][0-9.,]*)', 1) END AS r1_op,
        CASE WHEN regexp_matches(trim(b.valore_rendiconto), '^(>=|<=|>|<|=)?\s*-?[0-9][0-9.,]*\s*(%|€|euro)?$')
             THEN regexp_extract(trim(b.valore_rendiconto), '^(>=|<=|>|<|=)?\s*(-?[0-9][0-9.,]*)', 2) END AS r1_num
    FROM base b
),
num AS (
    -- Normalizza il formato numerico: virgola decimale italiana, punto
    -- delle migliaia solo quando il pattern è inequivocabile (1.234 / 1.234.567).
    SELECT
        t.*,
        CASE
            WHEN t.t1_num IS NULL THEN NULL
            WHEN t.t1_num LIKE '%,%' THEN TRY_CAST(replace(replace(t.t1_num, '.', ''), ',', '.') AS DOUBLE)
            WHEN regexp_matches(t.t1_num, '^-?[0-9]{1,3}(\.[0-9]{3})+$') THEN TRY_CAST(replace(t.t1_num, '.', '') AS DOUBLE)
            ELSE TRY_CAST(t.t1_num AS DOUBLE)
        END AS t1_val,
        CASE
            WHEN t.r1_num IS NULL THEN NULL
            WHEN t.r1_num LIKE '%,%' THEN TRY_CAST(replace(replace(t.r1_num, '.', ''), ',', '.') AS DOUBLE)
            WHEN regexp_matches(t.r1_num, '^-?[0-9]{1,3}(\.[0-9]{3})+$') THEN TRY_CAST(replace(t.r1_num, '.', '') AS DOUBLE)
            ELSE TRY_CAST(t.r1_num AS DOUBLE)
        END AS r1_val
    FROM tok t
)

SELECT
    anno,
    fase,
    stp,
    amministrazione,
    missione_codice,
    missione,
    programma_codice,
    programma,
    cdr_codice,
    cdr,
    obiettivo_codice,
    obiettivo,
    indicatore_codice,
    indicatore,
    descrizione_indicatore,
    tipo_indicatore,
    tipo_misura,
    unita_misura,
    metodo_calcolo,
    fonte,
    target_anno1,
    target_anno2,
    target_anno3,
    NULLIF(t1_op, '')  AS target_anno1_operatore,
    t1_val             AS target_anno1_valore,
    CASE
        WHEN strpos(target_anno1, '%') > 0 THEN '%'
        WHEN strpos(lower(target_anno1), 'euro') > 0 OR strpos(target_anno1, '€') > 0 THEN 'EUR'
    END                AS target_anno1_unita,
    valore_rendiconto,
    r1_val             AS valore_rendiconto_valore,
    CASE
        WHEN strpos(valore_rendiconto, '%') > 0 THEN '%'
        WHEN strpos(lower(valore_rendiconto), 'euro') > 0 OR strpos(valore_rendiconto, '€') > 0 THEN 'EUR'
    END                AS valore_rendiconto_unita,
    nota_mancanza_target,
    nota_mancata_consuntivazione,
    nota_scostamento,
    valore_riferimento,
    descrizione_provenienza,
    indicatore_trasversale,
    data_osservazione
FROM num
WHERE anno IS NOT NULL
  AND stp IS NOT NULL
  AND indicatore_codice IS NOT NULL
