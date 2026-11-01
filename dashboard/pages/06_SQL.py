"""Query SQL — Interroga direttamente i dati."""

from lab_connectors.duckdb.sql_page import render_sql_query
from lab_connectors.registry import load_registry_github

render_sql_query(
    registry=load_registry_github("bilancio-pubblico"),
    prefix="bilancio-pubblico/",
    default_slug="bdap_saldi_stato",
    title="🧪 Query SQL",
    description=(
        "Interroga direttamente i dati. Scrivi SQL su ``clean_input`` — "
        "viene risolta automaticamente sui Parquet GCS."
    ),
)
