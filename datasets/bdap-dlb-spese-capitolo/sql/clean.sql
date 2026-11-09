-- DLB presentato — spese per capitolo, 2017-2027.
-- Modello stabile dal 2017 (59 colonne); il 2011-2016 ha 37 colonne, senza
-- Azione e senza PLB, ed è fuori perimetro.
-- Misure: PLB = legislazione vigente, Rimodulazioni, Rif. Def. Rip., DLB Sez. II
-- (manovra), Effetti fin. DLB Sez. I, DLB Integrato. A1/A2/A3 = anni della
-- previsione; CP competenza, CS cassa, RS residui.
with base as (
    select
        cast_int("Esercizio Finanziario") as anno,
        normalize_string("Stato di Previsione") as stato_previsione,
        normalize_string("Amministrazione") as amministrazione,
        normalize_string("Unità di voto 1° livello") as unita_voto_1,
        normalize_string("Unità di voto 2° livello") as unita_voto_2,
        normalize_string("Numero Capitolo di Spesa") as numero_capitolo,
        normalize_string("Capitolo di Spesa") as denominazione_capitolo,
        normalize_string("Codice Titolo") as codice_titolo,
        normalize_string("Titolo") as titolo,
        normalize_string("Codice Categoria") as codice_categoria,
        normalize_string("Categoria") as categoria,
        normalize_string("Codice Puntato CE") as codice_puntato_ce,
        normalize_string("Codice Missione") as codice_missione,
        normalize_string("Missione") as missione,
        normalize_string("Codice Programma") as codice_programma,
        normalize_string("Programma") as programma,
        normalize_string("Codice Centro Responsabilità") as codice_cdr,
        normalize_string("Centro Responsabilità") as cdr,
        normalize_string("Codice Azione") as codice_azione,
        normalize_string("Azione") as azione,

        cast_double("PLB legislazione vigente CP A1") as plb_vigente_cp_a1,
        cast_double("PLB legislazione vigente CP A2") as plb_vigente_cp_a2,
        cast_double("PLB legislazione vigente CP A3") as plb_vigente_cp_a3,
        cast_double("PLB legislazione vigente CS A1") as plb_vigente_cs_a1,
        cast_double("PLB legislazione vigente CS A2") as plb_vigente_cs_a2,
        cast_double("PLB legislazione vigente CS A3") as plb_vigente_cs_a3,
        cast_double("PLB legislazione vigente RS A1") as plb_vigente_rs_a1,

        cast_double("Rimodulazioni CP A1") as rimodulazioni_cp_a1,
        cast_double("Rimodulazioni CP A2") as rimodulazioni_cp_a2,
        cast_double("Rimodulazioni CP A3") as rimodulazioni_cp_a3,
        cast_double("Rimodulazioni CS A1") as rimodulazioni_cs_a1,
        cast_double("Rimodulazioni CS A2") as rimodulazioni_cs_a2,
        cast_double("Rimodulazioni CS A3") as rimodulazioni_cs_a3,

        -- 2017 ha "Var. Manovra Sez. II" al posto di "Rif. Def. Rip." (stesse
        -- posizioni 34-39): è il terzo addendo dell'identità, rinominato.
        cast_double("Var. Manovra Sez. II CP A1") as var_manovra_sez2_cp_a1,
        cast_double("Var. Manovra Sez. II CP A2") as var_manovra_sez2_cp_a2,
        cast_double("Var. Manovra Sez. II CP A3") as var_manovra_sez2_cp_a3,
        cast_double("Var. Manovra Sez. II CS A1") as var_manovra_sez2_cs_a1,
        cast_double("Var. Manovra Sez. II CS A2") as var_manovra_sez2_cs_a2,
        cast_double("Var. Manovra Sez. II CS A3") as var_manovra_sez2_cs_a3,

        cast_double("Rif. Def. Rip. CP A1") as rif_def_rip_cp_a1,
        cast_double("Rif. Def. Rip. CP A2") as rif_def_rip_cp_a2,
        cast_double("Rif. Def. Rip. CP A3") as rif_def_rip_cp_a3,
        cast_double("Rif. Def. Rip. CS A1") as rif_def_rip_cs_a1,
        cast_double("Rif. Def. Rip. CS A2") as rif_def_rip_cs_a2,
        cast_double("Rif. Def. Rip. CS A3") as rif_def_rip_cs_a3,

        cast_double("DLB Sezione II CP A1") as dlb_sez2_cp_a1,
        cast_double("DLB Sezione II CP A2") as dlb_sez2_cp_a2,
        cast_double("DLB Sezione II CP A3") as dlb_sez2_cp_a3,
        cast_double("DLB Sezione II CS A1") as dlb_sez2_cs_a1,
        cast_double("DLB Sezione II CS A2") as dlb_sez2_cs_a2,
        cast_double("DLB Sezione II CS A3") as dlb_sez2_cs_a3,
        cast_double("DLB Sezione II RS A1") as dlb_sez2_rs_a1,

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
    -- controllo: DLB integrato = PLB + Rimodulazioni + terzo addendo + Effetti.
    -- Il terzo addendo è "Rif. Def. Rip." dal 2018 e "Var. Manovra Sez. II" nel
    -- 2017: stesso ruolo, nome diverso.
    coalesce(rif_def_rip_cp_a1, var_manovra_sez2_cp_a1) as terzo_addendo_cp_a1,
    round(
        coalesce(plb_vigente_cp_a1, 0)
        + coalesce(rimodulazioni_cp_a1, 0)
        + coalesce(rif_def_rip_cp_a1, var_manovra_sez2_cp_a1, 0)
        + coalesce(effetti_dlb_sez1_cp_a1, 0)
        - coalesce(dlb_integrato_cp_a1, 0),
        2
    ) as quadratura_cp_a1
from base
where anno is not null
