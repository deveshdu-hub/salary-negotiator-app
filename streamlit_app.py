import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Career Leverage & Salary Advisor", layout="wide")

st.title("🛡️ Career Leverage & Salary Negotiation Advisor")
st.caption("Built for Young India: Clear data, zero sugarcoating, automated risk-and-reward advisory.")
st.markdown("---")

# Layout: Two Input Columns
col1, col2 = st.columns(2)

with col1:
    st.header("🏢 Current Company Path")
    current_name = st.text_input("Current Company Name", value="Asian Paints")
    current_fixed = st.number_input(f"Standard Monthly Fixed Gross (₹)", value=163190, step=5000)
    current_variable = st.number_input("Annual Variable Pay / Bonus (₹)", value=449000, step=10000)
    
    st.subheader("🔮 Near-Term Promotion Lever")
    has_promo = st.checkbox("Is there an upcoming promotion/increment tracked?", value=True)
    if has_promo:
        promo_months = st.slider("Months until promotion hits", min_value=1, max_value=12, value=7)
        promo_ctc = st.number_input("Expected Promotional CTC (Annualized ₹)", value=3000000, step=50000)
    else:
        promo_months, promo_ctc = 0, 0

with col2:
    st.header("🦅 New Offer Path")
    new_name = st.text_input("New Company Name", value="Berger Protecton")
    new_fixed = st.number_input("Offered Monthly Fixed Gross (₹)", value=218474, step=5000)
    new_variable = st.number_input("Offered Annual Variable Pay (₹)", value=224000, step=10000)
    
    st.subheader("⚠️ Segment & Operational Context")
    segment_type = st.selectbox(
        "Select Role Division Alignment",
        ["Core Alignment (Dedicated Sector)", "Niche Sector in a Mismatched Core Division"]
    )
    has_relocation = st.checkbox("Requires Relocation / Base Shift?", value=True)

# Math Processing
current_annual_fixed = current_fixed * 12
current_total_ctc = current_annual_fixed + current_variable

new_annual_fixed = new_fixed * 12
new_total_ctc = new_annual_fixed + new_variable
absolute_hike = new_total_ctc - current_total_ctc
hike_percentage = (absolute_hike / current_total_ctc) * 100

# App Layout: Metrics Display
st.markdown("### 📊 Side-by-Side Compensation Truths")
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

m_col1.metric(label=f"{current_name} Current CTC", value=f"₹{current_total_ctc:,.2f}")
m_col2.metric(label=f"{new_name} Offered CTC", value=f"₹{new_total_ctc:,.2f}", delta=f"₹{absolute_hike:,.2f}")
m_col3.metric(label="Absolute Percentage Hike", value=f"{hike_percentage:.2%}")
m_col4.metric(label=f"{new_name} Monthly Fixed Liquidity", value=f"₹{new_fixed:,.2f}", 
              delta=f"₹{new_fixed - current_fixed:,.2f} / month cash gain")

st.markdown("---")

# AUTOMATED ADVISORY ENGINE (The "No-Sugarcoat" Logic Layer)
st.header("🧠 Automated AI-Peer Advisory & Strategic Steps")

# 1. Financial Timeline Trajectory Fact-Check
if has_promo and promo_ctc > 0:
    st.subheader("⏳ The Promotion Timeline Trap")
    if new_total_ctc >= promo_ctc:
        st.success(
            f"**Fact Check:** The new offer from {new_name} (₹{new_total_ctc:,.2f}) completely clears or matches your "
            f"expected promotional milestone at {current_name} (₹{promo_ctc:,.2f}). You skip waiting {promo_months} months "
            f"for a promised number by banking higher cash-in-hand immediately."
        )
    else:
        st.warning(
            f"**Fact Check:** If you switch to {new_name}, you are taking a long-term deficit. In {promo_months} months, "
            f"{current_name} projects to pay you ₹{promo_ctc - new_total_ctc:,.2f} MORE than your new offer. "
            f"Unless the role gives massive strategic leverage, you are losing money on this switch."
        )

# 2. Structural Breakdown (Fixed vs Variable Cash-flow)
current_fixed_ratio = current_annual_fixed / current_total_ctc
new_fixed_ratio = new_annual_fixed / new_total_ctc

st.subheader("💵 Structure & Cashflow Analysis")
if new_fixed_ratio > current_fixed_ratio:
    st.info(
        f"**Structure Benefit:** {new_name} has a more secure structure. **{new_fixed_ratio:.1%}** of your CTC is guaranteed "
        f"monthly fixed cash, compared to **{current_fixed_ratio:.1%}** at {current_name}. Less money is locked behind annual performance bonuses."
    )
else:
    st.warning(
        f"**Structure Risk:** {new_name} is loading your package with performance-based variable pay (**{(1-new_fixed_ratio):.1%}**). "
        f"If the division misses targets or the market slows, your actual bank credit will drop sharply."
    )

# 3. Operational Risk Profile
st.subheader("⚖️ Operational Risks, Pros, & Cons")
pro_col, con_col = st.columns(2)

with pro_col:
    st.markdown("#### ✅ The Crucial Pros")
    st.markdown(f"- **Immediate Liquidity Jump:** Immediate increase of **₹{(new_fixed - current_fixed):,.2f}** in monthly cash flow.")
    if has_relocation:
        st.markdown("- **Territory / Personal Target Alignment:** Allows resetting of regional networks if moving back to a legacy strong zone.")
    st.markdown("- **Cross-Functional Profile Evolution:** Shifts you out of a specialized technical track into direct commercial P&L and market ownership.")

with con_col:
    st.markdown("#### ❌ The Brutal Cons")
    if segment_type == "Niche Sector in a Mismatched Core Division":
        st.markdown(
            f"- **Division DNA Mismatch:** You are moving into a division whose primary corporate revenue is driven by a completely "
            f"different product line. You risk being treated as a secondary product category, meaning you must fight harder internally for focus and stock allocations."
        )
    st.markdown("- **Long Bureaucratic Sales Cycles:** B2B project sales require multi-month, slow-moving vendor approval tracks.")
    st.markdown("- **Resetting Corporate Trust:** Zero internal track record means you start with high pressure to hit short-term delivery numbers.")

st.markdown("---")

# 🛠️ THE STEP-BY-STEP NEGOTIATION SCRIPT GENERATOR
st.subheader("🔥 Custom Scripted Step for Negotiation")

suggested_counter = max(new_total_ctc, promo_ctc) * 1.05

st.markdown(
    f"If you need to push back one final time to cover risks or offset the impending promotion track, copy and tweak this structured layout:"
)

negotiation_script = f"""
"Hi [HR Name], 

Thank you for working with the business to refine the package to ₹{new_total_ctc:,.2f}. 

To ensure complete transparency, I am currently lined up for an internal promotion track hitting within {promo_months} months at {current_name} that structures my compensation to ₹{promo_ctc:,.2f}. While I am deeply excited to take over the division challenges at {new_name}, making a switch right now requires offsetting this upcoming internal milestone and covering the immediate friction of structural adjustments.

If the organization can adjust the final structure to ₹{suggested_counter:,.2f} to completely offset this near-term trajectory, I will sign the offer today and initiate my formal notice period clearance."
"""

st.code(negotiation_script, language="markdown")
