import streamlit as st

st.set_page_config(page_title="Declaration Assessment", layout="centered")

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

check_btn = st.button("✅ Check My Allowance", use_container_width=True, key="ndn_check_btn")

def get_channel_icon(channel):
    return "🟢 Green Channel" if channel == "Green" else "🔴 Red Channel"

if check_btn:
    # Determine GST outcome
    if citizenship == "Pass Holder":
        gst_status = "❌ Not eligible for GST relief."
        gst_channel = "Red"
    else:
        gst_limit = 500 if away_48 == "48 hours or more" else 100
        gst_status = f"✅ Eligible for S${gst_limit} GST relief. Declare if goods exceed this amount."
        gst_channel = "Green"

    # Determine Liquor outcome
    liquor_eligible = (
        bringing_liquor == "Yes"
        and away_48 == "48 hours or more"
        and from_malaysia == "No"
    )

    if bringing_liquor == "No":
        liquor_status = "✅ Not bringing liquor."
        liquor_channel = "Green"
    elif liquor_eligible:
        liquor_status = "✅ Eligible for duty-free (choose 1 option: 1L+1L or 2L total). Declare if you exceed."
        liquor_channel = "Green"
    else:
        liquor_status = "❌ Not eligible for duty-free liquor. Must declare."
        liquor_channel = "Red"

    # Determine Cigarettes outcome
    cigs_status = "❌ No duty-free concession for cigarettes or tobacco. Must declare."
    cigs_channel = "Red"

    # Visual Summary Output
    st.markdown("### 🧾 Summary of Your Declaration Requirements")

    for icon, label, status, channel in [
        ("💰", "GST Relief", gst_status, gst_channel),
        ("🍾", "Liquor", liquor_status, liquor_channel),
        ("🚬", "Cigarettes & Tobacco", cigs_status, cigs_channel),
    ]:
        st.markdown(f"""
        <div style="border: 2px solid {'#10b981' if channel == 'Green' else '#ef4444'}; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
            <h4 style="margin: 0 0 0.5rem 0;">{icon} {label}</h4>
            <p style="margin: 0.2rem 0; font-size: 0.95rem;">{status}</p>
            <strong style="font-size: 1rem;">{get_channel_icon(channel)}</strong>
        </div>
        """, unsafe_allow_html=True)

    # Footer Suggestion
    st.markdown(
        """<div style="width:100%; text-align:center; margin-top:2rem;">
        <span style="font-size:1.04rem; color:#2563eb; font-weight:500;">
        Still unsure? Try the <b>'Ask The Assistant'</b> feature for a more detailed response.
        </span></div>""",
        unsafe_allow_html=True
    )
