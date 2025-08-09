import streamlit as st
from utilities import gated_page

# ========================
#   PASSWORD PROTECTION
# ========================
gated_page()

# ========================
#        PAGE SETUP
# ========================
about_us_page = st.Page(
    page="pages/about_us.py",
    title="About Us",
    icon=":material/favorite:",
)

methodology_page = st.Page(
    page="pages/methodology.py",
    title="Methodology",
    icon=":material/bar_chart:",
)

declaration_assessment_page = st.Page(
    page="pages/declaration_assessment.py",
    title="Declaration Assessment",
    icon=":material/checklist:",
)

ask_the_assistant_page = st.Page(
    page="pages/ask_the_assistant.py",
    title="Ask The Assistant",
    icon=":material/smart_toy:",
)

# ========================
#        NAVIGATION
# ========================
pg = st.navigation({
    "Info": [about_us_page, methodology_page],
    "Projects": [declaration_assessment_page, ask_the_assistant_page],
})

pg.run()
