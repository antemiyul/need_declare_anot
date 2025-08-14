import streamlit as st

# ========================
#   METHODOLOGY PAGE
# ========================

st.title("Methodology")
st.write("""
This page outlines the technical implementation and data flows for the **Need Declare Anot** prototype.
It explains how the main features work and includes the process flow diagrams for each.
""")

# ------------------------
# DATA FLOW & IMPLEMENTATION
# ------------------------
st.subheader("Data Flow Overview")
st.markdown("""
The application has two main use cases:

1. **Declaration Assessment** – An interactive Q&A that helps travellers determine if they need to declare goods.
2. **Ask The Assistant** – An AI-powered chatbot that provides personalised customs guidance.

Both use cases rely on:

- **Frontend:** Streamlit for user interface and navigation.
- **Backend:** Python scripts for data handling, prompt formatting, and rule-based decision logic.
- **LLM:** OpenAI GPT-4 for natural language understanding and generation.
- **Knowledge Base:** Extracted from the official *Singapore Customs Guide for Travellers (2022)*, duty & GST rates, and relevant Health Sciences Authority (HSA) regulations.
""")

# ------------------------
# DECLARATION ASSESSMENT
# ------------------------
st.markdown("---")
st.header("Declaration Assessment")

flowchart_path = "images/declaration_assessment_flowchart.svg"
st.image(flowchart_path, caption="Declaration Assessment – Process Flow", use_container_width=True)

st.markdown("""
**Narrative:**
The Declaration Assessment feature guides the user through a series of questions about their citizenship status, travel duration, country of arrival, and whether they are bringing liquor.  
It then applies Singapore Customs rules to determine GST import relief, liquor duty-free eligibility, and shows a warning for cigarettes and tobacco.  
Finally, it suggests the user try **Ask The Assistant** for more detailed guidance.
""")

# ------------------------
# ASK THE ASSISTANT
# ------------------------
st.markdown("---")
st.header("Ask The Assistant")

# Placeholder for future flowchart
st.info("Flowchart and methodology for this feature will be added later.")

# ------------------------
# TECHNICAL NOTES
# ------------------------
st.markdown("---")
st.subheader("Technical Notes")
st.markdown("""
- **Programming Language:** Python 3.11
- **Framework:** Streamlit
- **LLM Provider:** OpenAI GPT-4 API
- **Data Processing:** Pandas for rule checks and LangChain for retrieval-based Q&A
- **Deployment:** Local prototype; can be hosted on Streamlit Community Cloud
""")

# ------------------------
# LIMITATIONS & NEXT STEPS
# ------------------------
st.subheader("Limitations & Future Improvements")
st.markdown("""
- The LLM may generate outdated or inaccurate responses if official rules change.
- No live integration with Singapore Customs' backend systems.
- Future versions could add:
    - Real-time API connections to official sources.
    - Multilingual support for travellers.
    - Mobile-friendly design improvements.
""")
