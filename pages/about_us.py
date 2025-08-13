import streamlit as st

st.image("images/about_us.svg", width=250)

with st.expander("⚠️ Important Notice", expanded=True):
    st.write("""
    This web application is a prototype developed for educational purposes only. 
    The information provided here is NOT intended for real-world usage and should not be relied upon 
    for making any decisions, especially those related to financial, legal, or healthcare matters.

    Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. 
    You assume full responsibility for how you use any generated output.

    Always consult with qualified professionals for accurate and personalized advice.
    """)

with st.container():
    st.markdown("## Need Declare Anot")
    st.markdown(
        """
        <span style='font-size:1.11rem; font-weight:400;'>
        Designed to make travel declarations in Singapore <b>effortless</b> — for locals and visitors alike.<br>
        Skip the confusion. Get instant, clear answers when you need them most.
        </span>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")  # Spacer

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            **📝 Declaration Assessment**  
            Instantly know if you need to declare your items.  
            Just answer a few simple questions.
            """
        )
    with col2:
        st.markdown(
            """
            **💬 Ask The Assistant**  
            Your personal customs chatbot — ready to answer GST, duties, and declaration questions 24/7.
            """
        )

    st.markdown("---")
    st.markdown("#### Objectives")
    st.markdown(
        """
        - Reduce uncertainty by clarifying what must be declared.
        - Summarise official info from Singapore Customs & HSA into plain English.
        - Empower travellers — so everyone can travel confidently, without surprises.
        """
    )
