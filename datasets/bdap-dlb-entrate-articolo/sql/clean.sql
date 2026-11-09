-- DLB presentato — entrate per capitolo e articolo, 2017-2027.
-- Struttura: 52 colonne dal 2018; nel 2017 mancano le 7 "Nuove norme DLB Sez. II"
-- e ci sono 3 "Variazioni proposte" (mappate, le altre restano NULL).
-- Identità verificata su 11/11 anni: DLB integrato = DLB Sezione II + effetti
-- fin. DLB Sez. I. "Nuove norme" è vuota in tutti gli anni (0 righe valorizzate).
with base as (
    select
        cast_int("Esercizio Finanziario") as anno,
        normalize_string("Stato di Previsione") as stato_previsione,
        normalize_string("Centro Responsabilità") as centro_responsabilita,
        normalize_string("Amministrazione") as amministrazione,
        normalize_string("Numero Capitolo di Entrata") as numero_capitolo,
        normalize_string("Capitolo di Entrata") as denominazione_capitolo,
        normalize_string("Numero Articolo") as numero_articolo,
        normalize_string("Articolo") as articolo,
        normalize_string("Codice Titolo") as codice_titolo,
        normalize_string("Titolo") as titolo,
        normalize_string("Codice Natura") as codice_natura,
        normalize_string("Natura") as natura,
        normalize_string("Codice Tipologia") as codice_tipologia,
        normalize_string("Tipologia") as tipologia,
        normalize_string("Codice Attività/Provento") as codice_attivita_provento,
        normalize_string("Attività/Provento") as attivita_provento,
        normalize_string("Codice Categoria") as codice_categoria,
        normalize_string("Categoria") as categoria,
        normalize_string("Codice Puntato SEC95") as codice_puntato_sec95,

        cast_double("Prev. Bil. Esercizio prec. CP") as prev_bil_prec_cp,
        cast_double("Prev. Bil. Esercizio prec. CS") as prev_bil_prec_cs,
        cast_double("Prev. Bil. Esercizio prec. RS") as prev_bil_prec_rs,
        cast_double("Ass. Bil. Esercizio prec. CP") as ass_bil_prec_cp,
        cast_double("Ass. Bil. Esercizio prec. CS") as ass_bil_prec_cs,
        cast_double("Ass. Bil. Esercizio prec. RS") as ass_bil_prec_rs,

        cast_double("DLB Sezione II CP A1") as dlb_sez2_cp_a1,
        cast_double("DLB Sezione II CP A2") as dlb_sez2_cp_a2,
        cast_double("DLB Sezione II CP A3") as dlb_sez2_cp_a3,
        cast_double("DLB Sezione II CS A1") as dlb_sez2_cs_a1,
        cast_double("DLB Sezione II CS A2") as dlb_sez2_cs_a2,
        cast_double("DLB Sezione II CS A3") as dlb_sez2_cs_a3,
        cast_double("DLB Sezione II RS A1") as dlb_sez2_rs_a1,

        -- dal 2018; vuote in tutti gli anni (documentato)
        cast_double("Nuove norme DLB Sez. II CP A1") as nuove_norme_cp_a1,
        cast_double("Nuove norme DLB Sez. II CP A2") as nuove_norme_cp_a2,
        cast_double("Nuove norme DLB Sez. II CP A3") as nuove_norme_cp_a3,
        cast_double("Nuove norme DLB Sez. II CS A1") as nuove_norme_cs_a1,
        cast_double("Nuove norme DLB Sez. II CS A2") as nuove_norme_cs_a2,
        cast_double("Nuove norme DLB Sez. II CS A3") as nuove_norme_cs_a3,
        cast_double("Nuove norme DLB Sez. II RS A1") as nuove_norme_rs_a1,

        -- solo 2017: l'analogo delle "Nuove norme" nel modello precedente
        cast_double("Variazioni proposte CP A1") as variazioni_proposte_cp_a1,
        cast_double("Variazioni proposte CS A1") as variazioni_proposte_cs_a1,
        cast_double("Variazioni proposte RS A1") as variazioni_proposte_rs_a1,

        cast_double("Effetti fin. DLB Sez. I CP A1") as effetti_dlb_sez1_cp_a1,
        cast_double("Effetti fin. DLB Sez. I CP A2") as effetti_dlb_sez1_cp_a2,
        cast_double("Effetti fin. DLB Sez. I CP A3") as effetti_dlb_sez1_cp_a3,
        cast_double("Effetti fin. DLB Sez. I CS A1") as effetti_dlb_sez1_cs_a1,
        cast_double("Effetti fin. DLB Sez. I CS A2") as effetti_dlb_sez1_cs_a2,
        cast_double("Effetti fin. DLB Sez. I CS A3") as effetti_dlb_sez1_cs_a3,

        cast_double("DLB Integrato CP A1") as dlb_integrato_cp_a1,
        cast_double("DLB Integrato CP A2") as dlb_integrato_cp_a2,
        cast_double("DLB Integrato CP A3") as dlb_integrato_cp_a3,
        cast_double("DLB Integrato CS A1") as dlb_integrato_cs_a1,
        cast_double("DLB Integrato CS A2") as dlb_integrato_cs_a2,
        cast_double("DLB Integrato CS A3") as dlb_integrato_cs_a3,
        cast_double("DLB Integrato RS A1") as dlb_integrato_rs_a1
    from raw_input
)

select
    *,
    -- controllo: DLB integrato = DLB Sezione II + effetti fin. DLB Sez. I
    round(
        coalesce(dlb_sez2_cp_a1, 0)
        + coalesce(effetti_dlb_sez1_cp_a1, 0)
        - coalesce(dlb_integrato_cp_a1, 0),
        2
    ) as quadratura_cp_a1
from base
where anno is not null
