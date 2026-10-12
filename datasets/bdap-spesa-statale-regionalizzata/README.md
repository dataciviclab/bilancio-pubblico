# bdap-spesa-statale-regionalizzata

## Domanda guida

Come si distribuisce la spesa dello Stato tra i territori italiani?

## Fonte

OpenBDAP — RGS / SRS_SPE_BIL_SPESR_001

## Perimetro

- Annualità: `2008–2023` (16 anni, tutti i dump UUID recuperati)
- Grano: anno × territorio × titolo × categoria × missione × misura
- Territori: Italia + 5 ripartizioni + 20 regioni

## NOTA semantica

1. Italia, ripartizioni e regioni sono livelli **sovrapposti** — non sommarli.
2. Le 4 misure sono distinte (mln assoluti, % PIL, €/ab, €/kmq).
3. Schema e categorie variano tra annualità (drift dichiarato dalla fonte).
4. Non è grain programma/macroaggregato: è titolo/categoria/missione territorializzato.
5. Al netto degli interessi sul debito — quota regionalizzata (non confrontabile 1:1 con bdap_spese_stato per tutte le missioni, es. 034 debito quasi assente).

## Schema

7 colonne. Le principali:

| Colonna | Tipo | Ruolo | Descrizione |
|---|---|---|---|
| `anno` | INTEGER | dimension | Anno di interesse |
| `territorio` | VARCHAR | dimension | Italia / Ripartizione / Regione |
| `livello_territoriale` | VARCHAR | dimension | Italia / Ripartizione / Regione |
| `titolo` | VARCHAR | dimension | TITOLO I/II/III |
| `categoria` | VARCHAR | dimension | Categoria economica |
| `codice_missione` | VARCHAR | dimension | Codice missione (003, 022, ...) |
| `missione` | VARCHAR | dimension | Descrizione missione |
| `misura` | VARCHAR | dimension | Tipo misura (mln, %PIL, €/ab, €/kmq) |
| `importo` | DOUBLE | metric | Importo |

## Layer

- **Clean**: ~20.000 righe/anno, 7 colonne.
- **Mart**: `mart_per_missione_italia`, `mart_per_missione_regione`.

## Output

- `out/data/clean/bdap_spesa_statale_regionalizzata/{year}/bdap_spesa_statale_regionalizzata_{year}_clean.parquet`
- `out/data/mart/bdap_spesa_statale_regionalizzata/{year}/mart_per_missione_*.parquet`

## Run

```bash
toolkit run -c datasets/bdap-spesa-statale-regionalizzata/dataset.yml -y 2022
```

## Stato

`runnable` — pipeline completa, 16 anni.
