# Changelog - Bilancio Pubblico Intelligence

Questo changelog documenta le modifiche rilevanti al progetto.

## feat/bdap-dlb-spese-capitolo - DLB per capitolo, 2017-2027
Data: 2026-11-09

### Aggiunto
- **1 dataset** `bdap_dlb_spese_capitolo` (openbdap, 2017-2027): Disegno di Legge
  di Bilancio presentato, spese per capitolo con missione, programma, azione e CdR.
  Misure: PLB (legislazione vigente), rimodulazioni, riferimenti DEF, DLB Sezione II,
  effetti del DLB Sez. I e **DLB integrato**, su CP/CS triennali.
- **4 mart**: `mart_capitolo` (dettaglio), `mart_anno` (totali e quadratura),
  `mart_missione`, `mart_amministrazione`

### Note
- Perimetro dal 2017: è il primo anno dello schema a 59 colonne (con Azione e PLB).
  Il 2011-2016 usa 37 colonne, senza Azione e senza PLB, ed è escluso.
- Copre il buco tra il DLB aggregato (`bdap_dlb_spese_serie`, che si ferma al 2026
  e dipende da un package privato) e il Rendiconto per capitolo (`bdap_rnd_spese_capitolo`,
  che è il consuntivo). E' la **previsione** per capitolo.
- 2027: 5.181 capitoli, DLB integrato 1.222,3 mld CP anno 1.
- Identità `DLB integrato = PLB + rimodulazioni + rif. DEF + effetti` verificata
  dal 2018; nel 2017 la fonte non la rispetta (fino a 4,3 mld su Fondi da ripartire),
  documentato nella description del dataset.

## feat/note-integrative - Programmazione per obiettivi
Data: 2026-11-04

### Aggiunto
- **4 dataset** Note Integrative (openbdap, 2018-2025):
  `bdap_ni_azioni` (DLB+LB+RND), `bdap_ni_indicatori` (DLB+LB+RND),
  `bdap_ni_obiettivi` (DLB+LB), `bdap_ni_priorita` (LB+RND)
- **1 support dataset** `bdap_ni_amministrazioni` (anagrafica STP → denominazione, 1 file per anno)
- **5 mart**: priorità per amministrazione, obiettivi per natura, azioni con catena
  DLB → LB → Rendiconto, indicatori con target numerico e % raggiunta, anagrafica
- **Parsing dei target**: `target_anno1_valore` / `valore_rendiconto_valore` popolati
  solo per valori numerici singoli (con eventuale operatore `>=`, `<=`, `>`, `<`),
  normalizzando virgola decimale e punto delle migliaia

### Note
- Perimetro dal 2018: è l'anno in cui il bilancio è articolato in azioni e le Note
  Integrative seguono missione → programma → azione. Il 2016-2017 usa uno schema diverso.
- Il totale degli stanziamenti per azione coincide con `bdap_lb_spese_missione`
  (2024: 1.215,1 mld CP): le due viste sono joinabili.
- Fasi incluse solo dove aggiungono informazione: il rendiconto è escluso dagli
  obiettivi (copia della LB) e il disegno di legge dalle priorità (copertura
  incompleta, 6-12 ministeri su 15). Il DLB resta su azioni e indicatori perché
  cambia il perimetro (16,7-22,0% degli importi, 11,9-29,7% delle chiavi), non perché
  sposti i target numerici (8-12%).
- Chiavi composite obbligatorie: i codici ripartono dentro il livello padre
  (azione per programma, obiettivo per CdR, indicatore per obiettivo).
- Ogni mart espone `n_ministri_coperti` per rendere visibile la copertura della fase.

## v1.0 - Bilancio Intelligence (feat/bilancio-intelligence-setup)
Data: 2026-08-30

### Aggiunto
- **5 dataset** con pipeline toolkit: saldi, entrate, spese, pagamenti, LB spese missione
- **16 mart analitici**: composizione spesa, avanzo primario, trend tributarie, investimenti vs trasferimenti, costo debito bilancio, LB vs rendiconto, e altri
- **Dashboard Streamlit** con 7 pagine: Panoramica, Composizione Spesa, Entrate, Spese per Missione, Pagamenti e Debito, Promesse vs Realtà, Query SQL
- **Confronto LB vs Rendiconto** per 34 missioni × 10 anni (2017-2026)
- **Smoke test** (10 test) per validazione dashboard
- **CI/CD**: check.yml (validazione + test) e pipeline.yml (run mensile)
- **Inventario UUID BDAP** (149 dataset LB, 3849 dataset totali)

### Dataset
- bdap_saldi_stato: saldi aggregati 2003-2025 (23 anni)
- bdap_entrate_stato: entrate per titolo/natura 2008-2025 (18 anni)
- bdap_spese_stato: spese per missione/macroaggregato 2008-2025 (18 anni)
- bdap_pagamenti_stato: consuntivo pagamenti 2014-2025 (12 anni)
- bdap_lb_spese_missione: Legge di Bilancio per missione DPCM Art.3 2017-2026 (10 anni)

### Rimosso
- .github/seed-issues (obsoleto)
- WORKFLOW.md (obsoleto)
- scripts/ (spostato in _local/)

## v0.4 - Chiusura perimetro legacy
Data: 2026-03-10

### Modificato
- perimetro del progetto fissato su saldi + spese
- documentazione aggiornata per trattare il repo come legacy project stabile
- layer mart descritto in modo coerente con il ruolo dei notebook

## v0.3 - Notebooks discussion-linked
Data: 2026-03-10

### Aggiunto
- notebook di risposta alle Discussions #9, #10, #16, #17 importati nel repo

## v0.2 - Miglioramenti
Data: 2026-02-05

### Modificato
- miglioramenti alla documentazione e al workflow di partenza del repo

## v0.1 - MVP iniziale
Data: 2026-01-26

### Aggiunto
- prima versione dell'output pubblico
- metodo iniziale
