import streamlit as st

st.header("Declaration Assessment")
st.markdown(
    """
    This assessment will help you determine if you are required to declare your goods or are eligible for duty-free concessions.
    Please answer the following questions to receive a clear and personalised assessment of your customs requirements.
    """
)

col1, col2 = st.columns(2)
with col1:
    citizenship = st.radio(
        "Your status:",
        ["Singapore Citizen/PR", "Pass Holder", "Visitor/Tourist"],
        horizontal=True,
        key="ndn_citizenship",
        help="Pass Holders include Student Pass, Dependant Pass, Long-Term Visit Pass, Work Permit, S Pass, Employment Pass, etc."
    )
with col2:
    away_48 = st.radio(
        "How long were you outside Singapore?",
        ["Less than 48 hours", "48 hours or more"],
        horizontal=True,
        key="ndn_away_48"
    )

from_malaysia = st.radio(
    "Are you arriving from Malaysia?",
    ["No", "Yes"], horizontal=True, key="ndn_from_malaysia"
)

bringing_liquor = st.radio(
    "Are you bringing liquor into Singapore?",
    ["No", "Yes"], horizontal=True, key="ndn_bringing_liquor"
)

check_btn = st.button("Check My Allowance", use_container_width=True, key="ndn_check_btn")

if check_btn:
    # GST Import Relief
    if citizenship == "Pass Holder":
        gst_msg = "Pass holders are not eligible for GST import relief."
        st.error(gst_msg)
    elif away_48 == "48 hours or more":
        gst_msg = "GST import relief: S$500"
        st.info(gst_msg)
    else:
        gst_msg = "GST import relief: S$100"
        st.info(gst_msg)

    # Liquor Duty-Free Allowance
    liquor_eligible = (
        bringing_liquor == "Yes"
        and away_48 == "48 hours or more"
        and from_malaysia == "No"
    )

    st.subheader("Liquor Duty-Free Allowance")
    if bringing_liquor == "No":
        st.success("You do not need to declare liquor. Please proceed through the Green Channel.")
    elif liquor_eligible:
        st.success(
            """You are eligible for **one** of the following duty-free options:
- 1L Spirits + 1L Wine
- 1L Spirits + 1L Beer
- 1L Wine + 1L Beer
- 2L Wine
- 2L Beer

Please select only one option. Any excess must be declared at the Red Channel and will be subject to duty and GST."""
        )
    else:
        st.error("You are not eligible for duty-free liquor concessions. All liquor must be declared at the Red Channel.")

    # Cigarettes and Tobacco
    st.subheader("Cigarettes and Tobacco")
    st.warning(
        "There is no duty-free concession for cigarettes or tobacco products. All must be declared and are subject to duty and GST, even if purchased in Singapore."
    )

    st.markdown(
        """<div style="width:100%; text-align:center; margin-top:1.6rem;">
            <span style="font-size:1.04rem; color:#2563eb; font-weight:500;">
            Still unsure? Try the 'Ask The Assistant' feature for a more detailed response.
            </span>
        </div>""", unsafe_allow_html=True
    )
