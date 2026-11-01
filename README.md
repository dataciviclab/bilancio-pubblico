# Bilancio Pubblico Intelligence

**Quanto spende lo Stato italiano, come lo finanzia, e cosa resta per gli investimenti?**

Sistema di intelligence sul bilancio dello Stato italiano: raccoglie i dati ufficiali BDAP (RGS/MEF),
li trasforma in mart analitici e li rende interrogabili via dashboard Streamlit.

- **Fonte**: [OpenBDAP - RGS/MEF](https://bdap-opendata.rgs.mef.gov.it/)
- **Copertura**: 2003-2026 (a seconda del dataset)
- **Livello**: Nazionale - Stato centrale
- **Output pubblico**: Dashboard Streamlit + Discussion

## Cosa risponde

1. **Lo Stato è strutturalmente in deficit?** → saldi storici 2003-2025
2. **Le spese correnti comprimono gli investimenti?** → composizione spesa per macroaggregato (trasferimenti/investimenti/debito/funzionamento)
3. **Quanto pesano le entrate tributarie?** → trend entrate per titolo/natura
4. **Quanto costa il debito a bilancio?** → consuntivo pagamenti missione 034
5. **Come varia la spesa per missione?** → spese per DPCM Art.3
6. **Il governo mantiene le promesse?** → confronto Legge di Bilancio vs Rendiconto per 34 missioni

## Dataset

| Dataset | Anni | Mart | Descrizione |
|---|---|---|---|
| bdap_saldi_stato | 2003-2025 | 3 | Saldi aggregati: deficit, avanzo primario, ricorso mercato |
| bdap_entrate_stato | 2008-2025 | 3 | Entrate per Titolo/Natura/Tipologia/Provento |
| bdap_spese_stato | 2008-2025 | 3 | Spese per Missione/Programma/Macroaggregato |
| bdap_pagamenti_stato | 2014-2025 | 3x12 | Consuntivo pagamenti per Amministrazione/Missione/Categoria |
| bdap_lb_spese_missione | 2017-2026 | 2 | Legge di Bilancio per missione DPCM Art.3 |
| bdap_spesa_statale_regionalizzata | 2008-2023 (16 anni) | 2 | Spesa Stato per territorio destinatario (SRS bilancio) |
| bdap_rnd_spese_serie | 2008-2025 | 3 | Rendiconto: spese per amministrazione/missione/programma/macroaggregato (previsioni definitive) |
| bdap_lb_spese_serie | 2003-2026 | 3 | Legge di Bilancio: spese per amministrazione/missione/programma/macroaggregato, triennio A1/A2/A3 |
| bdap_dlb_spese_serie | 2003-2026 | 3 | Disegno di Legge di Bilancio: spese per amministrazione/missione/programma/macroaggregato, triennio A1/A2/A3 |
| bdap_rnd_spese_capitolo | 2011-2025 | 4 | Consuntivo di competenza per capitolo: previsione definitiva, pagato, rimasto da pagare, economie |
| bdap_rnd_entrate_articolo | 2011-2025 | 4 | Consuntivo entrate per articolo: previsione definitiva, accertato, versato, residui |

> **Nota 2017**: la vista BDAP aggregata per missione/programma/macroaggregato (`bdap_spese_stato`) omette una quota del programma "Garanzia dei diritti dei cittadini" finanziata dal Ministero dell'Economia (~10,4 mld CS). La vista per amministrazione (`bdap_rnd_spese_serie`) la include: per il 2017 il totale CS è 914,8 mld contro 904,2 della vista aggregata. Il delta è documentato, non corretto a valle.

> **Nota 2024 (entrate)**: la vista aggregata per titolo/natura/tipologia/provento (`bdap_entrate_stato`) perde ~3,8 mld di previsione definitiva CP nel 2024 rispetto al dettaglio per articolo (`bdap_rnd_entrate_articolo`). Sugli altri anni i totali coincidono.

### Mart analitici (33 totali)

**Saldi** (3): mart_saldi_anno, mart_composizione_spesa, mart_avanzo_primario

**Entrate** (3): mart_entrate_titolo_natura_anno, mart_entrate_anno, mart_trend_tributarie

**Spese** (3): mart_spese_missione_anno, mart_spese_anno, mart_investimenti_vs_corrente

**Pagamenti** (3x12): mart_pagamenti_missione_categoria, mart_pagamenti_anno, mart_costo_debito_bilancio

**LB** (2): mart_lb_spese_anno, mart_lb_vs_rendiconto

**Serie a tre stadi** (9): per ciascuno di DLB, LB e Rendiconto — mart_*_spese_anno, mart_*_spese_missione, mart_*_spese_amministrazione

**Consuntivo capitolo** (4): mart_capitolo, mart_anno, mart_missione, mart_amministrazione

**Consuntivo entrate** (4): mart_articolo, mart_anno, mart_titolo, mart_amministrazione

## Dashboard

Dashboard Streamlit con 7 pagine:

| Pagina | Contenuto |
|---|---|
| Panoramica | KPI deficit, avanzo, previsione governo + trend saldi + composizione |
| Composizione Spesa | Trend trasferimenti/investimenti/debito/funzionamento (2008-2025) |
| Entrate | Trend totali, quote tributarie, top titoli per titolo/natura |
| Spese per Missione | Top10 missioni per importo, trend spese totali |
| Pagamenti e Debito | Trend pagati, costo debito (missione 034), top10 missioni |
| Query SQL | Query libere su tutti i mart |
| Promesse vs Realtà | Gap LB → consuntivo per missione: dove la promessa è stata disattesa (2011-2025) |
| Catena del Bilancio | Waterfall degli scostamenti DLB → LB → definitiva → impegnato → pagato |
| Consuntivo | Pagato, residui, economie di spesa e accertato/versato delle entrate (2011-2025) |

## Come si usa

```bash
# Setup
pip install -r requirements.txt

# Validare config
make check

# Eseguire tutte le pipeline
make run

# Dashboard
cd dashboard && streamlit run app.py
```

## Struttura

```
.github/workflows/          # CI/CD (check + pipeline reusable)
datasets/                   # Pipeline toolkit (9 dataset)
  bdap-saldi-stato/
  bdap-entrate-stato/
  bdap-spese-stato/
  bdap-pagamenti-stato/
  bdap-lb-spese-missione/
  bdap-spesa-statale-regionalizzata/
  bdap-rnd-spese-serie/
  bdap-lb-spese-serie/
  bdap-dlb-spese-serie/
  bdap-rnd-spese-capitolo/
  bdap-rnd-entrate-articolo/
dashboard/                  # Streamlit (7 pagine)
notebooks/                  # Analisi legacy (Discussion)
Makefile                    # PREFIX=bdap, YEARS=all
```

## CI/CD

- **check.yml**: Valida i config YAML su ogni PR/push (reusable workflow)
- **pipeline.yml**: Esegue le pipeline, sync GCS, aggiorna registry (reusable workflow, trigger: PR merged + 1 del mese)

## Domande civiche (Discussions)

Il repo eredita 6 Discussion dal progetto originale:

- [#9](https://github.com/dataciviclab/openbdap-saldi-storico-stato/discussions/9) Lo Stato e strutturalmente in deficit?
- [#10](https://github.com/dataciviclab/openbdap-saldi-storico-stato/discussions/10) Le spese correnti comprimono gli investimenti?
- [#12](https://github.com/dataciviclab/openbdap-saldi-storico-stato/discussions/12) Le entrate tributarie coprono la macchina dello Stato?
- [#14](https://github.com/dataciviclab/openbdap-saldi-storico-stato/discussions/14) L'avanzo primario e un mito o una realta?
- [#15](https://github.com/dataciviclab/openbdap-saldi-storico-stato/discussions/15) Discussion di partenza sul bilancio
- [#16](https://github.com/dataciviclab/openbdap-saldi-storico-stato/discussions/16) Il ricorso al mercato e una costante?
- [#17](https://github.com/dataciviclab/openbdap-saldi-storico-stato/discussions/17) Quanto paga lo Stato in interessi?

## License

MIT License - [DataCivicLab](https://dataciviclab.org/)
