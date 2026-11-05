-- mart_amministrazioni.sql — anagrafica STP per anno
-- Mart per-anno (una tabella per anno di run).
-- Fonte: sezione "Amministrazioni" del Rendiconto, la fase con la copertura
-- più completa. Una riga per ministero, senza distinzione di fase.

SELECT
    anno,
    stp,
    amministrazione,
    amministrazione_breve
FROM clean_input
ORDER BY anno, stp
