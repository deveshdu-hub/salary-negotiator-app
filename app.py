import streamlit as st
import pandas as pd
from io import BytesIO
import requests
from datetime import datetime

# ==========================================
# ⚙️ SECURE INTERFACE & LAYOUT CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Self Assist Core",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile responsiveness and UI component rendering
st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }
    div[data-testid="stMetricValue"] > div { font-size: 24px !important; font-weight: bold; }
    .report-card { background-color: #f8fafc; border-left: 5px solid #1A365D; padding: 15px; border-radius: 4px; margin-bottom: 10px; }
    @media (max-width: 640px) {
        .responsive-title { font-size: 18px !important; }
        div[data-testid="stMetricValue"] > div { font-size: 18px !important; }
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🔑 SECURITY & LOGIN ACCESS CONTROL LAYER
# ==========================================
def check_password():
    """Returns True if the user enters the correct User ID and Password."""
    VALID_USERNAME = "admin123"
    VALID_PASSWORD = "CompanyNorth2026"

    # Explicitly verify st namespace is available in this scope
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.markdown("""
        <div style="max-width: 450px; margin: 50px auto; padding: 30px; background-color: #F7FAFC; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 5px solid #1A365D;">
            <h2 style="color: #1A365D; margin-top: 0; font-family: 'Segoe UI', sans-serif; text-align: center;">Secure Gateway Access</h2>
            <p style="color: #718096; font-size: 13px; text-align: center;">Enter North Division corporate credentials to initialize workspace.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("User ID / Login", key="input_user")
        password = st.text_input("Password", type="password", key="input_pass")
        
        if st.button("Verify & Authenticate Entry", type="primary", use_container_width=True):
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Authentication Failed: Invalid User ID or Password Verification Key.")
                
    return False

# Execute App Block only if security handshake passes
if check_password():

    # ==========================================
    # 🏗️ DATA INITIALIZATION BLOCK (SESSION STATE)
    # ==========================================
    if "df" not in st.session_state:
        columns = [
            "Project ID", "State / Hub", "Client Category", "Project Name", "Lifecycle Stage",
            "Primary EPC Contractor", "Key Decision Maker", "Structural Consultant",
            "QC / Plant Lead", "Incumbent Competitor", "Target Application Zone",
            "Company Counterweapon", "Latest Action Update", "Next Concrete Action Required",
            "Target Date", "Win Probability (%)"
        ]
        data = [
            ["PRJ-01", "Delhi-NCR", "Metro Rail", "Delhi Metro Phase IV (Golden Line)", "Upcoming", "L&T Construction", "Arjun Mehta (Procurement Head)", "DMRC Design Board", "S. Sharma (QC Manager)", "Sika India", "Underground Cut-&-Cover Tunnels", "ProHyperplast SP & HS ProCrystal 100", "Bidding stage active. Structural drawing pulled.", "Schedule technical meeting with DMRC Consultant for spec-in", "2026-07-15", 65],
            ["PRJ-02", "Uttar Pradesh", "NHAI / Expressways", "Ganga Expressway (Phase 2 Pours)", "Ongoing", "PNC Infratech", "V. K. Singh (Project Director)", "L N Malviya Infra", "R. Chaudhary (Plant QC)", "Fosroc India", "Mass road beds & bridge decks", "ProSuperplast RT", "Trial mix requested due to slump loss complaints in summer heat.", "Deliver product samples to site batching yard for initial trial mix", "2026-06-25", 80],
            ["PRJ-03", "Delhi-NCR", "Mega Private Projects", "DLF Cybercity Phase 2 Expansion", "Upcoming", "Tata Projects", "Rajesh Kapoor (VP Infrastructure)", "Mantec Consultants", "Amit Pal (Site In-charge)", "MC-Bauchemie", "Deep basement rafts & structural foundation piles", "Hs ProCrystal 100 & HS ProCem CI", "Architectural blueprint finalized. Sub-surface parameters mapped.", "Pitch crystalline integration benefits directly to Mantec Lead", "2026-07-20", 50]
        ]
        st.session_state.df = pd.DataFrame(data, columns=columns)

    if "ca_pipeline" not in st.session_state:
        st.session_state.ca_pipeline = pd.DataFrame([
            {"Client ID": "SA-01", "Client Name": "FutureHQ Node A", "Entity Type": "Proprietorship", "Service Stream": "ITR & Tax Audit", "FY 2025-26 Turnover (₹)": 1800000, "Estimated Tax Liability (₹)": 45000, "Filing Deadline": "2026-07-31", "Workflow Status": "Document Verification"},
            {"Client ID": "SA-02", "Client Name": "CarryMe Logistics", "Entity Type": "LLP / Startup", "Service Stream": "GST Reconciliation", "FY 2025-26 Turnover (₹)": 4200000, "Estimated Tax Liability (₹)": 756000, "Filing Deadline": "2026-06-25", "Workflow Status": "Pending Upload"}
        ])

    # ==========================================
    # 🏙️ MAIN DASHBOARD APPS INTERFACE
    # ==========================================
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1A365D 0%, #2A4365 50%, #1A202C 100%); padding: 22px; border-radius: 8px; margin-bottom: 25px; border-bottom: 4px solid #3182ce;">
            <div style="float: right;"><span style="background-color: #48BB78; color: white; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold;">🔐 SECURE NODE ACTIVE</span></div>
            <h1 class="responsive-title" style="color: white; margin: 0; font-family: 'Segoe UI', sans-serif; font-size: 26px;">
                COMPANY PROTECTON (ADMIXTURE) — NORTH DIVISION MASTER TRACKER
            </h1>
            <p style="color: #90CDF4; margin: 4px 0 0 0; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 500;">
                Grade ML1 — Multi-Venture Execution & Account Automation Workspace
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Tabs Router Layout
    tab_pipeline, tab_intel, tab_calculator, tab_ministry = st.tabs([
        "📋 Active Pipeline Matrix", 
        "🔍 B2B Contact Format Generator",
        "🧮 AI Tax Structuring Engine",
        "🏛️ Investor Ministry Growth Console"
    ])

    # ==========================================
    # 📋 TAB 1: CORE PIPELINE TRACKER
    # ==========================================
    with tab_pipeline:
        st.subheader("🔄 Weekly Government Excel Synchronization Hub")
        uploaded_file = st.file_uploader("Drop newly received or edited client sheets here:", type=["xlsx", "xls"])

        if uploaded_file is not None:
            try:
                incoming_df = pd.read_excel(uploaded_file)
                if "Project ID" in incoming_df.columns:
                    if st.button("⚡ Execute Deep Sync & Merge Records"):
                        st.session_state.df.set_index("Project ID", inplace=True, drop=False)
                        incoming_df.set_index("Project ID", inplace=True, drop=False)
                        for idx in incoming_df.index:
                            st.session_state.df.loc[idx] = incoming_df.loc[idx]
                        st.session_state.df.reset_index(drop=True, inplace=True)
                        st.success("Sync complete!")
                else:
                    st.error("Invalid File Format: Missing 'Project ID' column.")
            except Exception as e:
                st.error(f"Sync Interrupted: {str(e)}")

        available_options = st.session_state.df["State / Hub"].unique()
        filter_state = st.sidebar.multiselect("Select State / Hub:", options=available_options, default=available_options)
        filtered_df = st.session_state.df[st.session_state.df["State / Hub"].isin(filter_state)]

        st.subheader("📋 Active Territory Pipeline Matrix")
        edited_df = st.data_editor(
            filtered_df,
            use_container_width=True,
            num_rows="dynamic",
            key="pipeline_editor_v6",
            column_config={
                "Win Probability (%)": st.column_config.ProgressColumn("Win Probability (%)", format="%d%%", min_value=0, max_value=100),
                "Lifecycle Stage": st.column_config.SelectboxColumn("Lifecycle Stage", options=["Upcoming", "Ongoing", "Completion Stage"], required=True)
            }
        )

        c1, c2 = st.columns([1, 5])
        with c1:
            if st.button("💾 Sync Matrix Updates", type="primary"):
                st.session_state.df.set_index("Project ID", inplace=True, drop=False)
                for _, row in edited_df.iterrows():
                    idx = row["Project ID"]
                    st.session_state.df.loc[idx] = row
                st.session_state.df.reset_index(drop=True, inplace=True)
                st.success("Saved!")

        with c2:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                edited_df.to_excel(writer, index=False, sheet_name='North_Div_Pipeline')
            st.download_button(label="📥 Export Current View to Excel", data=output.getvalue(), file_name="Company_North_Division_Pipeline_Export.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # ==========================================
    # 🔍 TAB 2: B2B CONTACT FORMAT GENERATOR
    # ==========================================
    with tab_intel:
        st.subheader("🎯 Executive Contact Finder & Domain Matcher")
        
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            input_name = st.text_input("Enter Target Executive Name:", placeholder="e.g., Souvik Sengupta")
        with col_in2:
            input_company = st.text_input("Enter Company Name:", placeholder="e.g., Infra Market")

        if st.button("🔍 Generate Corporate Contact Profile", type="primary"):
            if input_name and input_company:
                clean_name = input_name.strip().lower()
                clean_company = input_company.strip().lower()
                name_parts = clean_name.split()
                first = name_parts[0] if len(name_parts) > 0 else ""
                last = name_parts[1] if len(name_parts) > 1 else ""

                email_domain = "company.com"
                email_format = "[first_name].[last_name]@company.com"
                predicted_email = "Not Computed"
                switchboard = "Not Found"
                extra_notes = "Standard corporate pattern applied."

                if "infra" in clean_company or "hella" in clean_company:
                    email_domain = "infra.market"
                    email_format = "[first_name]@infra.market"
                    predicted_email = f"{first}@{email_domain}"
                    switchboard = "+91 22 6844 5555 / +91 84509 95099"
                    extra_notes = "Major infrastructure aggregator. Operates alongside RDC Concrete division."
                elif "rdc" in clean_company or "concrete" in clean_company:
                    email_domain = "rdcconcrete.com"
                    email_format = "[first_name].[last_name]@rdcconcrete.com"
                    predicted_email = f"{first}.{last}@{email_domain}" if last else f"{first}@{email_domain}"
                    switchboard = "+91 22 6716 5100"
                    extra_notes = "Sub-entity of Infra Market house of brands."
                elif "l&t" in clean_company or "larsen" in clean_company:
                    email_domain = "lntecc.com"
                    email_format = "[first_name][last_name]@lntecc.com"
                    predicted_email = f"{first}{last}@{email_domain}"
                    switchboard = "+91 44 2252 6000"
                    extra_notes = "Primary tier-1 infrastructure contractor company configuration."
                elif "sika" in clean_company:
                    email_domain = "in.sika.com"
                    email_format = "[last_name].[first_name]@in.sika.com"
                    predicted_email = f"{last}.{first}@{email_domain}" if last else f"{first}@{email_domain}"
                    switchboard = "+91 22 6230 7700"
                    extra_notes = "Admixture sector competitor routing blueprint."
                else:
                    domain_guess = clean_company.replace(" ", "") + ".com"
                    email_domain = domain_guess
                    email_format = "[first_name].[last_name]@" + domain_guess
                    predicted_email = f"{first}.{last}@{domain_guess}" if last else f"{first}@{domain_guess}"
                    switchboard = "Verify via website contact page."
                    extra_notes = "Standard global commercial domain routing architecture."

                st.markdown("---")
                st.success(f"### 🎯 Found Format Match for {input_company.upper()}")
                
                c_out1, c_out2 = st.columns(2)
                with c_out1:
                    st.markdown(f"""
                    <div style="background-color: #f0fdf4; padding: 15px; border-radius: 5px; border-left: 4px solid #16a34a; color: #1e293b;">
                        <strong>📁 Target Executive:</strong> {input_name.title()}<br>
                        <strong>🏢 Company:</strong> {input_company.title()}<br><br>
                        <strong>🌐 Corporate Domain:</strong> <code>{email_domain}</code><br>
                        <strong>⚙️ Standard Format:</strong> <code>{email_format}</code>
                    </div>
                    """, unsafe_allow_html=True)
                
                with c_out2:
                    st.markdown(f"""
                    <div style="background-color: #f8fafc; padding: 15px; border-radius: 5px; border-left: 4px solid #475569; color: #1e293b;">
                        <strong>📧 Estimated Email Address:</strong> <code>{predicted_email}</code><br><br>
                        <strong>📞 Official Switchboard Line:</strong> {switchboard}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("Missing Input Parameters: Fill in both fields.")

    # ==========================================
    # 🧮 TAB 3: SELF ASSIST TAX ENGINE
    # ==========================================
    with tab_calculator:
        st.subheader("📋 Active Self Assist Portfolio & Tax Structuring Model")
        try:
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
            
            ca_col1, ca_col2 = st.columns([1, 4])
            with ca_col1:
                if st.button("💾 Save Portfolio Changes", key="save_ca_portfolio"):
                    st.session_state.ca_pipeline = edited_ca_df.copy()
                    st.success("Portfolio Records Updated.")
            with ca_col2:
                buffer_out = BytesIO()
                with pd.ExcelWriter(buffer_out, engine='openpyxl') as writer:
                    edited_ca_df.to_excel(writer, index=False, sheet_name='Self_Assist_Data')
                st.download_button(label="📥 Export Portfolio Book to Excel", data=buffer_out.getvalue(), file_name="Self_Assist_Pipeline.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        except Exception as e:
            st.error(f"Portfolio Engine Error: {str(e)}")

        st.markdown("---")
        st.subheader("🧮 Instant AI Tax Projection Modeler")
        col_calc1, col_calc2 = st.columns([1, 1])
        with col_calc1:
            gross_revenue = st.number_input("Est. Gross Turnover (₹):", min_value=0, value=2400000, step=50000)
            declared_expenses = st.number_input("Operational Deductions (₹):", min_value=0, value=800000, step=25000)
            opt_presv = st.checkbox("Section 44AD Presumptive Tax Framework Rule (Lock at 6% Margin)")
            
        with col_calc2:
            try:
                if opt_presv:
                    net_taxable_income = gross_revenue * 0.06
                    calc_note = "Section 44AD baseline rules deployed."
                else:
                    net_taxable_income = max(0, gross_revenue - declared_expenses)
                    calc_note = "Standard Book-Accounting tracking ledger mode active."

                tax_estimate = 0.0
                if net_taxable_income > 700000:
                    tax_estimate = (net_taxable_income - 700000) * 0.10 + 15000
                
                st.metric(label="Calculated Net Taxable Profit", value=f"₹{net_taxable_income:,.0f}")
                st.metric(label="Approx Base Tax Due Liability", value=f"₹{tax_estimate:,.0f}")
                
                st.markdown(f"""
                    <div class="report-card">
                        <strong>📌 Self Assist System Parameter Note:</strong><br>
                        {calc_note}<br><br>
                        <em>Provisional analytical sheet. Validate metrics with authorized legal CAs before filing.</em>
                    </div>
                """, unsafe_allow_html=True)
            except Exception as calc_err:
                st.error(f"Calculation Interrupted: {str(calc_err)}")

    # ==========================================
    # 🏛️ TAB 4: INVESTOR MINISTRY REVENUE CONSOLE
    # ==========================================
    with tab_ministry:
        st.subheader("🏛️ Multi-Venture Execution Tracker Console (Goal: ₹1,00,000/Month)")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric(label="CarryMe Marketplace Node", value="1 Active Order", delta="+₹50 Gigs")
        with col_m2:
            st.metric(label="FutureHQ Content Node", value="4,000 Views", delta="2 Active Reels")
        with col_m3:
            st.metric(label="Self Assist App Venture", value=f"{len(st.session_state.ca_pipeline)} Active Profiles", delta="System Online")
            
        st.markdown("---")
        st.markdown("### 🕒 Standardized Corporate/Venture 24-Hour Schedule Matrix")
        
        ops_schedule = pd.DataFrame([
            {"Time Windows": "06:00 - 09:00", "Core Focus": "🧠 DEEP ASSET CREATION", "Work Package": "Build features and refine modules inside FutureHQ/Self Assist."},
            {"Time Windows": "09:00 - 10:00", "Core Focus": "🥪 LOGISTICS CONTROL", "Work Package": "Fulfill, pack, label, and hand over active open orders to Meesho courier lines."},
            {"Time Windows": "10:00 - 13:00", "Core Focus": "📈 VALUE FOOTPRINT SCALE", "Work Package": "Bulk upload 3-5 new catalog asset structural variations onto Meesho dashboard grids."},
            {"Time Windows": "14:00 - 17:00", "Core Focus": "🎯 TRAFFIC FUNNEL ENGINE", "Work Package": "Map active bio-links; shoot and process high-hook short-form video reels."},
            {"Time Windows": "17:00 - 19:00", "Core Focus": "🤝 HIGH-TICKET OUTREACH", "Work Package": "Pitch digital business services setting contract floors above ₹1,500 - ₹3,000."}
        ])
        st.table(ops_schedule)

        st.markdown("---")
        st.markdown("### 📝 Interactive Evening Reporting Console")
        with st.form("ministry_report_form"):
            date_col = st.date_input("Reporting Cycle Date:", datetime.now())
            f_views = st.number_input("FutureHQ Instagram Aggregate Views Today:", min_value=0, step=100)
            f_clicks = st.number_input("Bio-Link Traffic Clicks Logged:", min_value=0, step=1)
            c_new_cat = st.number_input("New Product Configurations Uploaded Today:", min_value=0, step=1)
            c_orders = st.number_input("New Inbound Orders Received:", min_value=0, step=1)
            m_rev = st.number_input("Total Revenue Confirmed/Locked Today (₹):", min_value=0, step=50)
            sys_bottleneck = st.text_area("Identify the core operational bottleneck encountered today:")
            submit_report = st.form_submit_button("📊 Compile & Format Ministry Report")

        if submit_report:
            formatted_string = f"""
### 📊 MINISTRY DAILY RESULTS BRIEF: {date_col.strftime('%d-%m-%Y')}
#### 1. ASSET GENERATION ENGINE (FutureHQ)
* Instagram Total Views Today: {f_views}
* Bio-Link Clicks Captured: {f_clicks}
#### 2. MARKETPLACE VOLUMETRIC FOOTPRINT (CarryMe)
* New Catalogs Added: {c_new_cat}
* New Orders Received: {c_orders}
#### 3. MONETIZATION
* Revenue Locked-in Today: ₹{m_rev}
#### 4. SYSTEM AUTOCORRECT CHECK
* Bottleneck: {sys_bottleneck if sys_bottleneck else "None logged."}
            """
            st.success("### 📜 Final Report Compiled successfully!")
            st.code(formatted_string, language="text")

    # ==========================================
    # 🌐 SIDEBAR PUBLIC SEARCH UTILITY
    # ==========================================
    st.sidebar.markdown("---")
    st.sidebar.header("🌐 Govt Infrastructure Search Engine")
    search_query = st.sidebar.text_input("Type Client/Project:")

    if search_query:
        st.sidebar.markdown(f"**Latest Public Listings for:** *'{search_query}'*")
        try:
            url = f"https://html.duckduckgo.com/html/?q={search_query.replace(' ', '+')}+site:gov.in"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(res.text, "html.parser")
                links = soup.find_all("a", class_="result__url", limit=4)
                titles = soup.find_all("a", class_="result__snippet", limit=4)
                if links:
                    for idx, (link, title) in enumerate(zip(links, titles)):
                        st.sidebar.info(f"🔗 **[Gov Link #{idx+1}]** ({link.text.strip()})\n\n{title.text.strip()[:140]}...")
                else:
                    st.sidebar.warning("No active public listings found matching criteria.")
        except Exception:
            st.sidebar.markdown(f"[🔗 Launch External Live Government Verification Link](https://www.google.com/search?q={search_query.replace(' ', '+')}+site:gov.in)")

    if st.sidebar.button("🔐 Logout Node"):
        st.session_state.authenticated = False
        st.rerun()
