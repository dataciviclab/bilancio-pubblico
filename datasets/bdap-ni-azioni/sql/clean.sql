-- clean.sql — bdap_ni_azioni
-- Note Integrative — sezione "Azioni": l'unità elementare del bilancio per
-- finalità, introdotta dal DLB 2018. È il livello in cui la programmazione
-- incontra i soldi.
--
-- Due schemi convivono nel dataset, distinti dalla fase:
--   DLB / LB   stanziamenti triennali di competenza e cassa + criteri
--   RND        stanziamento iniziale/definitivo, impegnato e pagato
-- Le colonne non comuni restano NULL: il confronto tra fasi si fa su
-- "stanziamento iniziale" (previsione_cp_anno1 per DLB/LB, stanziamento
-- iniziale per RND), che è la grandezza omogenea.

SELECT
    cast_int(r."Anno")                                    AS anno,
    normalize_string(r.fase_codice)                       AS fase,
    LPAD(normalize_string(r."STP"), 2, '0')               AS stp,
    normalize_string(r."Descrizione Amministrazione")     AS amministrazione,
    LPAD(normalize_string(r."Codice Missione"), 3, '0')   AS missione_codice,
    normalize_string(r."Missione")                        AS missione,
    LPAD(normalize_string(r."Codice Programma"), 3, '0')  AS programma_codice,
    normalize_string(r."Programma")                       AS programma,
    normalize_string(r."Codice Azione")                   AS azione_codice,
    normalize_string(r."Azione")                          AS azione,
    CAST(cast_double(r."Stanziamento CP 1 anno") AS DOUBLE) AS previsione_cp_anno1,
    CAST(cast_double(r."Stanziamento CP 2 anno") AS DOUBLE) AS previsione_cp_anno2,
    CAST(cast_double(r."Stanziamento CP 3 anno") AS DOUBLE) AS previsione_cp_anno3,
    CAST(cast_double(r."Stanziamento CS 1 anno") AS DOUBLE) AS previsione_cs_anno1,
    CAST(cast_double(r."Stanziamento CS 2 anno") AS DOUBLE) AS previsione_cs_anno2,
    CAST(cast_double(r."Stanziamento CS 3 anno") AS DOUBLE) AS previsione_cs_anno3,
    CAST(cast_double(r."Stanziamento iniziale CP") AS DOUBLE)   AS stanziamento_iniziale_cp,
    CAST(cast_double(r."Stanziamento iniziale CS") AS DOUBLE)   AS stanziamento_iniziale_cs,
    CAST(cast_double(r."Stanziamento definitivo CP") AS DOUBLE) AS stanziamento_definitivo_cp,
    CAST(cast_double(r."Stanziamento definitivo CS") AS DOUBLE) AS stanziamento_definitivo_cs,
    CAST(cast_double(r."Totale impegnato CP") AS DOUBLE)  AS impegnato_cp,
    CAST(cast_double(r."Totale Pagato CP") AS DOUBLE)     AS pagato_cp,
    CAST(cast_double(r."Totale Pagato CS") AS DOUBLE)     AS pagato_cs,
    normalize_string(r."Criteri")                         AS criteri,
    normalize_string(r."Principali fatti di gestione")    AS note_gestione,
    normalize_string(r."Data Osservazione")               AS data_osservazione
FROM raw_input r
WHERE cast_int(r."Anno") IS NOT NULL
  AND normalize_string(r."STP") IS NOT NULL
  AND normalize_string(r."Codice Azione") IS NOT NULL
