import streamlit as st

st.set_page_config(page_title="Declaration Assessment", layout="centered")

st.header("🛃 Declaration Assessment")
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

def render_channel_section(channel, content):
    color = "#d1fae5" if channel == "Green" else "#fee2e2"
    border = "#10b981" if channel == "Green" else "#ef4444"
    st.markdown(f"""
    <div style="background-color:{color}; border-left: 8px solid {border}; padding: 1.2rem; border-radius: 8px; margin-top:1rem;">
        <h4 style='margin-top:0;'>{'🟢' if channel == 'Green' else '🔴'} {channel} Channel</h4>
        {content}
    </div>
    """, unsafe_allow_html=True)

if check_btn:
    liquor_eligible = (
        bringing_liquor == "Yes"
        and away_48 == "48 hours or more"
        and from_malaysia == "No"
    )

    # === GST Section ===
    if citizenship == "Pass Holder":
        gst_text = "❌ Pass holders are not eligible for GST import relief."
        render_channel_section("Red", gst_text)
    else:
        gst_relief = "S$500" if away_48 == "48 hours or more" else "S$100"
        gst_text = f"✅ <b>GST Relief</b>: You’re eligible for {gst_relief}"
        render_channel_section("Green", gst_text)

        # GST Payment Reminder
        st.markdown(f"""
        <div style="background-color:#fff4e5; border-left: 6px solid #f59e0b; padding: 1rem; margin-top: 0.8rem; border-radius: 6px;">
            <strong>💡 Reminder:</strong><br>
            If the total value of your goods exceeds <strong>{gst_relief}</strong>, you will need to pay <strong>9% GST</strong> on the excess amount.<br>
            Please proceed to the <strong>Customs Tax Payment Office</strong> upon arrival to make payment.
        </div>
        """, unsafe_allow_html=True)

    # === Liquor Section ===
    if bringing_liquor == "No":
        liquor_text = "✅ Not bringing liquor. No declaration needed."
        render_channel_section("Green", liquor_text)
    elif liquor_eligible:
        liquor_text = """
        ✅ You are eligible for one of the following duty-free options:<br>
        - 1L Spirits + 1L Wine<br>
        - 1L Spirits + 1L Beer<br>
        - 1L Wine + 1L Beer<br>
        - 2L Wine<br>
        - 2L Beer
        <br><br>
        📌 Please select only one option. Any excess must be declared.
        """
        render_channel_section("Green", liquor_text)
    else:
        liquor_text = "❌ <b>Liquor</b>: You are <b>not eligible</b> for duty-free liquor. All liquor must be declared."
        render_channel_section("Red", liquor_text)

    # === Cigarettes Section ===
    cigs_text = "❌ <b>Cigarettes and Tobacco</b>: No duty-free concession. All must be declared, even if purchased in Singapore."
    render_channel_section("Red", cigs_text)

    # === Footer Suggestion ===
    st.markdown(
        """<div style="width:100%; text-align:center; margin-top:2rem;">
        <span style="font-size:1.04rem; color:#2563eb; font-weight:500;">
        Still unsure? Try the <b>'Ask The Assistant'</b> feature for a more detailed response.
        </span></div>""",
        unsafe_allow_html=True
    )
