"""
Bilancio Pubblico Intelligence - Dashboard Streamlit
I dati del bilancio dello Stato italiano, resi interrogabili.
"""

import streamlit as st
from lab_connectors.branding import apply_branding

st.set_page_config(
    page_title="Bilancio Pubblico - Dashboard",
    page_icon="🇮🇹",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_branding(repo_name="bilancio-pubblico", repo_url="https://github.com/dataciviclab/bilancio-pubblico")

pages = {
    "": [
        st.Page("pages/01_Panoramica.py", title="Panoramica", icon="📊", default=True),
    ],
    "Analisi": [
        st.Page("pages/02_Composizione.py", title="Composizione Spesa", icon="🧩"),
        st.Page("pages/03_Entate.py", title="Entrate", icon="📈"),
        st.Page("pages/04_Spese.py", title="Spese per Missione", icon="💰"),
        st.Page("pages/05_Pagamenti.py", title="Pagamenti e Debito", icon="🏛️"),
        st.Page("pages/07_Promesse_vs_Realta.py", title="Promesse vs Realtà", icon="⚖️"),
        st.Page("pages/10_Programmazione.py", title="Cosa promette lo Stato", icon="🎯"),
        st.Page("pages/08_Catena.py", title="Catena del Bilancio", icon="🔗"),
        st.Page("pages/09_Consuntivo.py", title="Consuntivo", icon="🧾"),
    ],
    "Strumenti": [
        st.Page("pages/06_SQL.py", title="Query SQL", icon="🧪"),
    ],
}

pg = st.navigation(pages, position="sidebar")

st.sidebar.caption("Fonti: OpenBDAP RGS/MEF")
st.sidebar.caption(
    "Codice: [dataciviclab/bilancio-pubblico](https://github.com/dataciviclab/bilancio-pubblico)"
)

pg.run()
