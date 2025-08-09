import streamlit as st

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
