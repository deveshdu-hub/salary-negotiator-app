import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Salary & Negotiation Advisor", layout="wide")

st.title("🛡️ Career Leverage & Salary Negotiation Advisor")
st.caption("Built for Young India: Data-driven comparison, structural analytics, and zero-sugarcoat career advisory.")
st.markdown("---")

# Layout: Two Input Columns
col1, col2 = st.columns(2)

with col1:
    st.header("🏢 Current Track")
    current_name = st.text_input("Current Company", value="Asian Paints")
    current_fixed = st.number_input("Monthly Fixed Gross (₹)", value=163190, step=5000)
    current_variable = st.number_input("Annual Variable Pay (₹)", value=449000, step=10000)
    
    st.subheader("🔮 Target Promotion Track")
    has_promo = st.checkbox("Track upcoming internal promotion?", value=True)
    if has_promo:
        promo_months = st.slider("Months until promotion", min_value=1, max_value=12, value=7)
        promo_ctc = st.number_input("Expected Promotional CTC (Annualized ₹)", value=3000000, step=50000)
    else:
        promo_months, promo_ctc = 0, 0

with col2:
    st.header("🦅 New Offer Track")
    new_name = st.text_input("New Company / Division", value="Berger Protecton")
    new_fixed = st.number_input("Offered Monthly Fixed Gross (₹)", value=218474, step=5000)
    new_variable = st.number_input("Offered Annual Variable Pay (₹)", value=224000, step=10000)
    
    st.subheader("⚠️ Segment Realities")
    segment_type = st.selectbox(
        "Division Strategic Alignment",
        ["Niche Portfolio in a Mismatched Core Division", "Core Alignment (Dedicated Sector)"]
    )
    has_relocation = st.checkbox("Relocation / Base Shift Required?", value=True)

# Calculations
current_annual_fixed = current_fixed * 12
current_total_ctc = current_annual_fixed + current_variable

new_annual_fixed = new_fixed * 12
new_total_ctc = new_annual_fixed + new_variable
absolute_hike = new_total_ctc - current_total_ctc
hike_percentage = (absolute_hike / current_total_ctc) * 100

# App Layout: Metrics Display
st.markdown("### 📊 Side-by-Side Financial Comparison")
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

m_col1.metric(label=f"{current_name} Current CTC", value=f"₹{current_total_ctc:,.2f}")
m_col2.metric(label=f"{new_name} Offered CTC", value=f"₹{new_total_ctc:,.2f}", delta=f"₹{absolute_hike:,.2f}")
m_col3.metric(label="Total Hike Percentage", value=f"{hike_percentage:.2%}")
m_col4.metric(label=f"{new_name} Monthly Liquidity", value=f"₹{new_fixed:,.2f}", 
              delta=f"₹{new_fixed - current_fixed:,.2f} / month gain")

st.markdown("---")

# AUTOMATED ADVISORY ENGINE 
st.header("🧠 Automated Reality-Check & Strategic Steps")

# 1. Financial Timeline Trajectory Fact-Check
if has_promo and promo_ctc > 0:
    st.subheader("⏳ The Promotion Timeline Factor")
    if new_total_ctc >= promo_ctc:
        st.success(
            f"**Fact Check:** The new offer from {new_name} (₹{new_total_ctc:,.2f}) completely clears your "
            f"expected promotional milestone at {current_name} (₹{promo_ctc:,.2f}). You bypass waiting {promo_months} months "
            f"for a projected number by securing immediate cash-in-hand liquidity."
        )
    else:
        st.warning(
            f"**Fact Check:** Moving right now incurs an opportunity cost. In {promo_months} months, "
            f"{current_name} is projected to clear ₹{promo_ctc - new_total_ctc:,.2f} MORE than your current {new_name} offer. "
            f"Ensure you negotiate the entry tier higher or value the regional shift accordingly."
        )

# 2. Structural Breakdown (Fixed vs Variable Cash-flow)
current_fixed_ratio = current_annual_fixed / current_total_ctc
new_fixed_ratio = new_annual_fixed / new_total_ctc

st.subheader("💵 Structure & Cashflow Dynamics")
if new_fixed_ratio > current_fixed_ratio:
    st.info(
        f"**Structure Hard Fact:** {new_name} offers a more predictable structure. **{new_fixed_ratio:.1%}** of your compensation is guaranteed "
        f"monthly fixed liquidity, compared to **{current_fixed_ratio:.1%}** at {current_name}. This significantly minimizes exposure to delayed performance bonuses."
    )
else:
    st.warning(
        f"**Structure Risk:** {new_name} is shifting your payout weight into variable performance brackets (**{(1-new_fixed_ratio):.1%}**). "
        f"If the business sector faces project delays or cycles stall, your actual bank credits could experience high volatility."
    )

# 3. Operational Risk Profile
st.subheader("⚖️ Strategic Pros & Cons")
pro_col, con_col = st.columns(2)

with pro_col:
    st.markdown("#### ✅ Core Advantages")
    st.markdown(f"- **Liquidity Upgrade:** Direct increment of **₹{(new_fixed - current_fixed):,.2f}** in monthly cash flow.")
    if has_relocation:
        st.markdown("- **Network Leverage:** Moves you to a primary base territory (Delhi-NCR/North) where 7 years of prior relationships can be activated.")
    st.markdown("- **Market Ownership:** Shifting from a technical formulation profile into active regional commercial P&L expansion.")

with con_col:
    st.markdown("#### ❌ Critical Risk Factors")
    if segment_type == "Niche Portfolio in a Mismatched Core Division":
        st.markdown(
            f"- **Division Priority Drift:** Entering an Industrial Protective/Anti-Corrosion coating division as an admixture/grout specialist. "
            f"You will need to aggressively champion internal focus, inventory support, and technical lab backings against high-value legacy paint lines."
        )
    st.markdown("- **Long-Cycle Institutional B2B Demands:** High reliance on project approvals, consultant specifications (EIL, NTPC, DMRC), and bureaucratic payment terms.")
    st.markdown("- **Zero-Base Internal Track Record:** Immediate operational pressure to prove sales pipeline viability in the first two quarters.")

st.markdown("---")

# THE STEP-BY-STEP NEGOTIATION SCRIPT GENERATOR
st.subheader("🔥 Data-Driven Final Negotiation Playbook")
suggested_counter = max(new_total_ctc, promo_ctc) * 1.05

st.markdown("Copy, customize, and issue this direct, objective response to HR if you are executing a final validation counter:")
negotiation_script = f"""
"Dear [HR Name],

Thank you for working with the management team to share the revised package structure of ₹{new_total_ctc:,.2f}. 

To maintain clear transparency, I am currently tracking an upcoming internal promotional horizon at {current_name} slated for the next {promo_months} months, projecting compensation scales to ₹{promo_ctc:,.2f}. While I am completely aligned with taking over the regional expansion mandates for the admixture and grout portfolios at {new_name}, managing this immediate transition necessitates completely covering that performance equity gap.

If the organization can adjust the final parameters to ₹{suggested_counter:,.2f} to completely insulate against this near-term trajectory and cover the friction of immediate transition, I will finalize the offer acceptance today and initiate the formal resignation process."
"""
st.code(negotiation_script, language="markdown")
