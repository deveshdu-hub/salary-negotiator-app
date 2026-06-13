import streamlit as st
import pandas as pd
from io import BytesIO
import traceback

# ==========================================
# ⚙️ SECURE INTERFACE & LAYOUT CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Self Assist Core",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS injector for complete mobile responsiveness and styling UI
st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }
    div[data-testid="stMetricValue"] > div { font-size: 24px !important; font-weight: bold; }
    .report-card { background-color: #f8fafc; border-left: 5px solid #0284c7; padding: 15px; border-radius: 4px; margin-bottom: 10px; }
    @media (max-width: 640px) {
        .responsive-title { font-size: 18px !important; }
        div[data-testid="stMetricValue"] > div { font-size: 18px !important; }
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🔑 SECURITY ACCESS CONTROL LAYER
# ==========================================
def authenticate_user():
    """Validates session login criteria to prevent unauthorized backend node access."""
    VALID_USER = "admin123"
    VALID_PASS = "CompanyNorth2026"

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.markdown("""
        <div style="max-width: 500px; margin: 40px auto; padding: 25px; background-color: #F8FAFC; border-radius: 8px; border-top: 4px solid #0284c7; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
            <h2 style="color: #0f172a; margin-top:0; font-family:sans-serif; text-align:center;">Self Assist Secure Portal</h2>
            <p style="color: #64748b; font-size:13px; text-align:center;">Venture Node Authorization Required — Level ML1 Compliance Gate.</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, col_center, _ = st.columns([1, 2, 1])
    with col_center:
        user_in = st.text_input("Venture Node User ID", key="ca_uid")
        pass_in = st.text_input("Security Access Key", type="password", key="ca_pwd")
        if st.button("Unlock Compliance Workspace", type="primary", use_container_width=True):
            if user_in == VALID_USER and pass_in == VALID_PASS:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Access Revoked: Invalid Gateway Key Credentials.")
    return False

# Execute App Block only if security handshake passes
if authenticate_user():

    # Persistent Global Session State Setup for Tracker Core
    if "ca_pipeline" not in st.session_state:
        st.session_state.ca_pipeline = pd.DataFrame([
            {"Client ID": "SA-01", "Client Name": "FutureHQ Node A", "Entity Type": "Proprietorship", "Service Stream": "ITR & Tax Audit", "FY 2025-26 Turnover (₹)": 1800000, "Estimated Tax Liability (₹)": 45000, "Filing Deadline": "2026-07-31", "Workflow Status": "Document Verification"},
            {"Client ID": "SA-02", "Client Name": "CarryMe Logistics", "Entity Type": "LLP / Startup", "Service Stream": "GST Reconciliation", "FY 2025-26 Turnover (₹)": 4200000, "Estimated Tax Liability (₹)": 756000, "Filing Deadline": "2026-06-25", "Workflow Status": "Pending Upload"}
        ])

    # ==========================================
    # 🏗️ HEADER ZONE INTERFACE
    # ==========================================
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 20px; border-radius: 6px; margin-bottom: 20px; border-bottom: 3px solid #0284c7;">
            <span style="float: right; background-color: #0369a1; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">📊 INTERNAL WORKSPACE v2026</span>
            <h1 class="responsive-title" style="color: white; margin: 0; font-family: sans-serif; font-size: 24px;">SELF ASSIST — DIGITAL OFFICE PIPELINE & PROJECTIONS ENGINE</h1>
            <p style="color: #94a3b8; margin: 4px 0 0 0; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Corporate Venture Structural Assessment Node</p>
        </div>
    """, unsafe_allow_html=True)

    # Tabs Router Configuration
    tab_dashboard, tab_calculator, tab_ministry = st.tabs([
        "📋 Client Management Matrix", 
        "🧮 AI Tax Structuring Engine", 
        "🏛️ Investor Ministry Growth Metrics"
    ])

    # ==========================================
    # 📋 TAB 1: CLIENT MANAGEMENT WORKSPACE
    # ==========================================
    with tab_dashboard:
        st.subheader("📋 Active Compliance Portfolio Management")
        
        try:
            # Main Client Data Grid
            edited_ca_df = st.data_editor(
                st.session_state.ca_pipeline,
                use_container_width=True,
                num_rows="dynamic",
                key="ca_grid_v1_2026",
                column_config={
                    "Entity Type": st.column_config.SelectboxColumn("Entity Type", options=["Proprietorship", "LLP / Startup", "Private Limited", "Freelancer"]),
                    "Service Stream": st.column_config.SelectboxColumn("Service Stream", options=["ITR & Tax Audit", "GST Reconciliation", "ROC Comp Filings", "CMA Report Drafting"]),
                    "Workflow Status": st.column_config.SelectboxColumn("Workflow Status", options=["Document Verification", "Pending Upload", "CA Review Pending", "Filing Complete"])
                }
            )
            
            col_act1, col_act2 = st.columns([1, 4])
            with col_act1:
                if st.button("💾 Sync Matrix", type="primary", use_container_width=True):
                    st.session_state.ca_pipeline = edited_ca_df.copy()
                    st.success("Changes Saved.")
            with col_act2:
                buffer_out = BytesIO()
                with pd.ExcelWriter(buffer_out, engine='openpyxl') as writer:
                    edited_ca_df.to_excel(writer, index=False, sheet_name='Self_Assist_Data')
                st.download_button(
                    label="📥 Export Compliance Book to Excel (.xlsx)",
                    data=buffer_out.getvalue(),
                    file_name="Self_Assist_Pipeline.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except Exception as err:
            st.error(f"Engine Error: {str(err)}")

    # ==========================================
    # 🧮 TAB 2: AI TAX STRUCTURING ENGINE
    # ==========================================
    with tab_calculator:
        st.subheader("🧮 Smart Tax Structuring Model")
        
        col_calc1, col_calc2 = st.columns([1, 1])
        
        with col_calc1:
            gross_revenue = st.number_input("Est. Gross Turnover (₹):", min_value=0, value=2400000, step=50000)
            declared_expenses = st.number_input("Operational Deductions (₹):", min_value=0, value=800000, step=25000)
            opt_presv = st.checkbox("Section 44AD Presumptive Rule (6%)")
            
        with col_calc2:
            try:
                if opt_presv:
                    net_taxable_income = gross_revenue * 0.06
                    calc_note = "Section 44AD (Digital) threshold applied."
                else:
                    net_taxable_income = max(0, gross_revenue - declared_expenses)
                    calc_note = "Standard Accounting framework active."

                tax_estimate = 0.0
                if net_taxable_income > 700000:
                    tax_estimate = (net_taxable_income - 700000) * 0.10 + 15000
                
                st.metric(label="Calculated Net Taxable Income", value=f"₹{net_taxable_income:,.0f}")
                st.metric(label="Approx Base Tax Liability", value=f"₹{tax_estimate:,.0f}")
                
                st.markdown(f"""
                    <div class="report-card">
                        <strong>📌 Self Assist Model Note:</strong><br>
                        {calc_note}<br><br>
                        <em>Provisional data. Finalize results with your designated CA before ITR transmission.</em>
                    </div>
                """, unsafe_allow_html=True)
                
            except Exception as calc_err:
                st.error(f"Calculation Error: {str(calc_err)}")

    # ==========================================
    # 🏛️ TAB 3: INVESTOR MINISTRY GROWTH CONSOLE
    # ==========================================
    with tab_ministry:
        st.subheader("🏛️ Multi-Venture Execution Panel (Goal: ₹1L/Month)")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric(label="CarryMe Meesho Vol", value="1 Active Order", delta="+₹50 Gigs")
        with col_m2:
            st.metric(label="FutureHQ Traffic", value="4,000 Views", delta="2 Reels")
        with col_m3:
            st.metric(label="Self Assist Registries", value=f"{len(st.session_state.ca_pipeline)} Clients", delta="Pipeline Active")
            
        st.markdown("---")
        st.markdown("### 🕒 Standardized 24-Hour Operations Matrix")
        
        ops_schedule = pd.DataFrame([
            {"Time Windows": "06:00 - 09:00", "Core Focus": "🧠 DEEP ASSET CREATION", "Work Package": "Code features and refine structures in FutureHQ/Self Assist."},
            {"Time Windows": "09:00 - 10:00", "Core Focus": "🥪 LOGISTICS", "Work Package": "Pack, prepare labels, and dispatch active Meesho orders."},
            {"Time Windows": "10:00 - 13:00", "Core Focus": "📈 VALUE SCALE", "Work Package": "Upload 3-5 new catalog asset variations onto Meesho dashboard."},
            {"Time Windows": "14:00 - 17:00", "Core Focus": "🎯 TRAFFIC FUNNEL", "Work Package": "Update digital bio-links; script short-form reels for CarryMe/FutureHQ."},
            {"Time Windows": "17:00 - 19:00", "Core Focus": "🤝 OUTREACH", "Work Package": "Pitches setting pricing floors above ₹1,500 - ₹3,000."}
        ])
        st.table(ops_schedule)

    # ==========================================
    # 🌐 CONTROL PANEL SIDEBAR CORE
    # ==========================================
    st.sidebar.header("🕹️ System Terminal")
    st.sidebar.info("Operational Status: Secure Connection.")
    
    if st.sidebar.button("🔐 Logout Node"):
        st.session_state.authenticated = False
        st.rerun()
