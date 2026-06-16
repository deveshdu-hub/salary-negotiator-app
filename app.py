import streamlit as st
import pandas as pd
from io import BytesIO, StringIO
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

# ==========================================
# ⚙️ PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Self Assist Core | Berger · CarryMe · FutureHQ",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 📱 CUSTOM CSS – MOBILE RESPONSIVE
# ==========================================
st.markdown("""
    <style>
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    div[data-testid="stMetricValue"] > div { font-size: 24px !important; font-weight: bold; }
    .report-card { background-color: #f8fafc; border-left: 5px solid #1A365D; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
    .stDataFrame { overflow-x: auto; }
    @media (max-width: 640px) {
        .responsive-title { font-size: 18px !important; }
        div[data-testid="stMetricValue"] > div { font-size: 18px !important; }
        .stButton button { width: 100%; }
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 AUTHENTICATION LAYER
# ==========================================
def check_password():
    VALID_USERNAME = "admin123"
    VALID_PASSWORD = "CompanyNorth2026"

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.markdown("""
        <div style="max-width: 450px; margin: 40px auto; padding: 30px; background-color: #F7FAFC; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-top: 5px solid #1A365D;">
            <h2 style="color: #1A365D; margin-top: 0; font-family: 'Segoe UI', sans-serif; text-align: center;">🔐 Secure Gateway Access</h2>
            <p style="color: #718096; font-size: 13px; text-align: center;">North Division – Corporate credentials required</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("User ID", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Verify & Authenticate Entry", type="primary", use_container_width=True):
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Authentication Failed: Invalid credentials.")
    return False

# ==========================================
# 🧠 SESSION STATE INITIALIZATION
# ==========================================
def init_session_state():
    # Corporate B2B pipeline
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
            ["PRJ-02", "Uttar Pradesh", "NHAI / Expressways", "Ganga Expressway (Phase 2 Pours)", "Ongoing", "PNC Infratech", "V. K. Singh (Project Director)", "L N Malviya Infra", "R. Chaudhary (Plant QC)", "Fosroc India", "Mass road beds & bridge decks", "ProSuperplast RT", "Trial mix requested due to slump loss complaints.", "Deliver product samples to site batching yard", "2026-06-25", 80],
            ["PRJ-03", "Delhi-NCR", "Mega Private Projects", "DLF Cybercity Phase 2 Expansion", "Upcoming", "Tata Projects", "Rajesh Kapoor (VP Infrastructure)", "Mantec Consultants", "Amit Pal (Site In-charge)", "MC-Bauchemie", "Deep basement rafts & structural piles", "HS ProCrystal 100 & HS ProCem CI", "Blueprint finalized. Sub-surface mapped.", "Pitch crystalline integration to Mantec Lead", "2026-07-20", 50]
        ]
        df = pd.DataFrame(data, columns=columns)
        df = convert_pipeline_dtypes(df)
        st.session_state.df = df

    # CA / client portfolio
    if "ca_pipeline" not in st.session_state:
        st.session_state.ca_pipeline = pd.DataFrame([
            {"Client ID": "SA-01", "Client Name": "FutureHQ Node A", "Entity Type": "Proprietorship", "Service Stream": "ITR & Tax Audit", "FY 2025-26 Turnover (₹)": 1800000, "Estimated Tax Liability (₹)": 45000, "Filing Deadline": "2026-07-31", "Workflow Status": "Document Verification"},
            {"Client ID": "SA-02", "Client Name": "CarryMe Logistics", "Entity Type": "LLP / Startup", "Service Stream": "GST Reconciliation", "FY 2025-26 Turnover (₹)": 4200000, "Estimated Tax Liability (₹)": 756000, "Filing Deadline": "2026-06-25", "Workflow Status": "Pending Upload"}
        ])

    # Daily report log
    if "daily_logs" not in st.session_state:
        st.session_state.daily_logs = []

def convert_pipeline_dtypes(df):
    """Ensure correct dtypes for pipeline DataFrame"""
    df = df.copy()
    if "Target Date" in df.columns:
        df["Target Date"] = pd.to_datetime(df["Target Date"], errors="coerce").dt.date
    if "Win Probability (%)" in df.columns:
        df["Win Probability (%)"] = pd.to_numeric(df["Win Probability (%)"], errors="coerce").fillna(0).clip(0, 100).astype(int)
    allowed_stages = ["Upcoming", "Ongoing", "Completion Stage"]
    if "Lifecycle Stage" in df.columns:
        df["Lifecycle Stage"] = df["Lifecycle Stage"].apply(lambda x: x if x in allowed_stages else "Upcoming")
    return df

# ==========================================
# ✨ AUTO POLISH CONDUCTOR (RULE-BASED)
# ==========================================
def auto_polish_text(raw_text: str) -> str:
    """Improves raw operational notes into professional business language."""
    if not raw_text.strip():
        return "No input provided."
    
    text = raw_text.strip()
    # Common replacements
    replacements = {
        r"\b(late|delayed|slow)\b": "delayed",
        r"\b(issue|problem|glitch)\b": "bottleneck",
        r"\b(fix|solve|resolve)\b": "remediate",
        r"\b(tomorrow|next day)\b": "next working day",
        r"\b(urgent|asap)\b": "critical priority",
        r"\b(need|require|must have)\b": "required",
        r"\b(think|maybe|perhaps)\b": "proposed",
        r"\b(good|fine|okay)\b": "satisfactory",
        r"\b(bad|terrible|awful)\b": "suboptimal",
    }
    for pattern, repl in replacements.items():
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    
    # Capitalize first letter of each sentence
    text = re.sub(r'(^|\.\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), text)
    if not text.endswith(('.', '!', '?')):
        text += '.'
    return text

# ==========================================
# 🏙️ MAIN APP
# ==========================================
if check_password():
    init_session_state()

    # Header
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1A365D 0%, #2A4365 50%, #1A202C 100%); padding: 20px; border-radius: 12px; margin-bottom: 20px; border-bottom: 4px solid #3182ce;">
            <div style="float: right;"><span style="background-color: #48BB78; color: white; padding: 4px 12px; border-radius: 30px; font-size: 11px; font-weight: bold;">🔐 SECURE NODE ACTIVE</span></div>
            <h1 class="responsive-title" style="color: white; margin: 0; font-size: 24px;">🏗️ COMPANY PROTECTION (ADMIXTURE) – NORTH DIVISION MASTER TRACKER</h1>
            <p style="color: #90CDF4; margin: 5px 0 0 0; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Multi‑Venture Execution & Account Automation Workspace</p>
        </div>
    """, unsafe_allow_html=True)

    # Create tabs
    tab_pipeline, tab_intel, tab_calculator, tab_ministry = st.tabs([
        "📋 Active Pipeline Matrix",
        "🔍 B2B Contact Format Generator",
        "🧮 AI Tax Structuring Engine",
        "🏛️ Investor Ministry Growth Console"
    ])

    # ==========================================
    # TAB 1 – PIPELINE MATRIX (unchanged)
    # ==========================================
    with tab_pipeline:
        st.subheader("🔄 Weekly Government Excel Synchronization Hub")
        uploaded_file = st.file_uploader("Drop newly received/edited client sheets (.xlsx, .xls):", type=["xlsx", "xls"])
        if uploaded_file is not None:
            try:
                incoming_df = pd.read_excel(uploaded_file)
                if "Project ID" in incoming_df.columns:
                    if st.button("⚡ Execute Deep Sync & Merge Records"):
                        incoming_df = convert_pipeline_dtypes(incoming_df)
                        st.session_state.df = st.session_state.df.set_index("Project ID")
                        incoming_df = incoming_df.set_index("Project ID")
                        st.session_state.df.update(incoming_df)
                        new_rows = incoming_df[~incoming_df.index.isin(st.session_state.df.index)]
                        st.session_state.df = pd.concat([st.session_state.df, new_rows])
                        st.session_state.df.reset_index(inplace=True)
                        st.session_state.df = convert_pipeline_dtypes(st.session_state.df)
                        st.success("✅ Sync complete!")
                else:
                    st.error("❌ Missing 'Project ID' column.")
            except Exception as e:
                st.error(f"🚨 Sync failed: {str(e)}")

        available_states = st.session_state.df["State / Hub"].unique()
        selected_states = st.sidebar.multiselect("🔍 Filter by State / Hub", options=available_states, default=available_states)
        filtered_df = st.session_state.df[st.session_state.df["State / Hub"].isin(selected_states)].copy()
        filtered_df = convert_pipeline_dtypes(filtered_df)

        st.subheader("📋 Active Territory Pipeline Matrix")
        column_config = {
            "Win Probability (%)": st.column_config.ProgressColumn("Win Probability (%)", format="%d%%", min_value=0, max_value=100),
            "Lifecycle Stage": st.column_config.SelectboxColumn("Lifecycle Stage", options=["Upcoming", "Ongoing", "Completion Stage"], required=True),
            "Target Date": st.column_config.DateColumn("Target Date", format="YYYY-MM-DD")
        }
        try:
            edited_df = st.data_editor(filtered_df, use_container_width=True, num_rows="dynamic", key="pipeline_editor", column_config=column_config)
        except Exception:
            edited_df = st.data_editor(filtered_df, use_container_width=True, num_rows="dynamic", key="pipeline_editor_fallback")

        col_save, col_export = st.columns([1, 4])
        with col_save:
            if st.button("💾 Sync Matrix Updates", type="primary"):
                try:
                    st.session_state.df = st.session_state.df.set_index("Project ID")
                    edited_df = edited_df.set_index("Project ID")
                    st.session_state.df.update(edited_df)
                    new_rows = edited_df[~edited_df.index.isin(st.session_state.df.index)]
                    st.session_state.df = pd.concat([st.session_state.df, new_rows])
                    st.session_state.df.reset_index(inplace=True)
                    st.session_state.df = convert_pipeline_dtypes(st.session_state.df)
                    st.success("✅ Pipeline saved!")
                except Exception as e:
                    st.error(f"⚠️ Save error: {str(e)}")
        with col_export:
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                edited_df.reset_index().to_excel(writer, index=False, sheet_name="North_Div_Pipeline")
            st.download_button("📥 Export Current View to Excel", data=output.getvalue(), file_name=f"Pipeline_Export_{datetime.now().strftime('%Y%m%d')}.xlsx")

    # ==========================================
    # TAB 2 – B2B CONTACT GENERATOR (unchanged)
    # ==========================================
    with tab_intel:
        st.subheader("🎯 Executive Contact Finder & Domain Matcher")
        col_name, col_company = st.columns(2)
        with col_name:
            input_name = st.text_input("Target Executive Name:", placeholder="e.g., Souvik Sengupta")
        with col_company:
            input_company = st.text_input("Company Name:", placeholder="e.g., Infra Market")
        if st.button("🔍 Generate Corporate Contact Profile", type="primary"):
            if not input_name or not input_company:
                st.error("❌ Please fill both fields.")
            else:
                try:
                    name = input_name.strip().lower()
                    company = input_company.strip().lower()
                    parts = name.split()
                    first = parts[0] if parts else ""
                    last = parts[1] if len(parts) > 1 else ""
                    domain = "company.com"
                    fmt = "[first].[last]@company.com"
                    email = "Not available"
                    switch = "Check website"
                    notes = "Standard global pattern."
                    if "infra" in company or "hella" in company:
                        domain = "infra.market"
                        fmt = "[first]@infra.market"
                        email = f"{first}@{domain}"
                        switch = "+91 22 6844 5555"
                        notes = "Infrastructure aggregator"
                    elif "rdc" in company or "concrete" in company:
                        domain = "rdcconcrete.com"
                        fmt = "[first].[last]@rdcconcrete.com"
                        email = f"{first}.{last}@{domain}" if last else f"{first}@{domain}"
                        switch = "+91 22 6716 5100"
                        notes = "RDC Concrete"
                    elif "l&t" in company or "larsen" in company:
                        domain = "lntecc.com"
                        fmt = "[first][last]@lntecc.com"
                        email = f"{first}{last}@{domain}"
                        switch = "+91 44 2252 6000"
                        notes = "L&T – primary EPC"
                    elif "sika" in company:
                        domain = "in.sika.com"
                        fmt = "[last].[first]@in.sika.com"
                        email = f"{last}.{first}@{domain}" if last else f"{first}@{domain}"
                        switch = "+91 22 6230 7700"
                        notes = "Sika India"
                    else:
                        clean = re.sub(r'[^a-z0-9]', '', company) + ".com"
                        domain = clean
                        fmt = f"[first].[last]@{clean}"
                        email = f"{first}.{last}@{clean}" if last else f"{first}@{clean}"
                        notes = "Best‑guess domain"
                    st.markdown("---")
                    st.success(f"### 🎯 Format match for **{input_company.upper()}**")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"<div style='background:#f0fdf4; padding:15px; border-radius:10px; border-left:4px solid #16a34a;'><strong>📁 Executive:</strong> {input_name.title()}<br><strong>🏢 Company:</strong> {input_company.title()}<br><strong>🌐 Domain:</strong> <code>{domain}</code><br><strong>⚙️ Format:</strong> <code>{fmt}</code></div>", unsafe_allow_html=True)
                    with col_b:
                        st.markdown(f"<div style='background:#f8fafc; padding:15px; border-radius:10px; border-left:4px solid #475569;'><strong>📧 Estimated Email:</strong> <code>{email}</code><br><strong>📞 Switchboard:</strong> {switch}<br><em style='font-size:12px;'>{notes}</em></div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Contact generator error: {str(e)}")

    # ==========================================
    # TAB 3 – TAX ENGINE (unchanged)
    # ==========================================
    with tab_calculator:
        st.subheader("📋 Active Self Assist Portfolio & Tax Structuring Model")
        try:
            edited_ca = st.data_editor(
                st.session_state.ca_pipeline,
                use_container_width=True,
                num_rows="dynamic",
                key="ca_editor",
                column_config={
                    "Entity Type": st.column_config.SelectboxColumn("Entity Type", options=["Proprietorship", "LLP / Startup", "Private Limited", "Freelancer"]),
                    "Service Stream": st.column_config.SelectboxColumn("Service Stream", options=["ITR & Tax Audit", "GST Reconciliation", "ROC Comp Filings", "CMA Report Drafting"]),
                    "Workflow Status": st.column_config.SelectboxColumn("Workflow Status", options=["Document Verification", "Pending Upload", "CA Review Pending", "Filing Complete"])
                }
            )
            col_save_port, col_export_port = st.columns([1, 4])
            with col_save_port:
                if st.button("💾 Save Portfolio Changes", key="save_ca"):
                    st.session_state.ca_pipeline = edited_ca.copy()
                    st.success("✅ Portfolio updated.")
            with col_export_port:
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    edited_ca.to_excel(writer, index=False, sheet_name="Self_Assist_Portfolio")
                st.download_button("📥 Export Portfolio Book", data=buffer.getvalue(), file_name="Self_Assist_Portfolio.xlsx")
        except Exception as e:
            st.error(f"⚠️ Portfolio editor error: {str(e)}")

        st.markdown("---")
        st.subheader("🧮 Instant AI Tax Projection Modeler")
        col_rev, col_exp = st.columns(2)
        with col_rev:
            gross_revenue = st.number_input("📊 Est. Gross Turnover (₹)", min_value=0, value=2400000, step=50000)
        with col_exp:
            declared_expenses = st.number_input("📉 Operational Deductions (₹)", min_value=0, value=800000, step=25000)
        opt_presumptive = st.checkbox("✅ Section 44AD Presumptive Tax (6% deemed profit)")
        try:
            if opt_presumptive:
                taxable_income = gross_revenue * 0.06
                note = "Presumptive taxation under 44AD applied (6% of turnover)."
            else:
                taxable_income = max(0, gross_revenue - declared_expenses)
                note = "Standard book‑accounting method."
            tax = 0 if taxable_income <= 700000 else (taxable_income - 700000) * 0.10 + 15000
            st.metric("💸 Net Taxable Profit", f"₹{taxable_income:,.0f}")
            st.metric("🧾 Approx Base Tax Liability", f"₹{tax:,.0f}")
            st.info(f"📌 {note}\n\n*Provisional calculation – always consult your CA.*")
        except Exception as calc_err:
            st.error(f"Tax calculation error: {str(calc_err)}")

    # ==========================================
    # TAB 4 – INVESTOR MINISTRY CONSOLE (enhanced with Auto Polish)
    # ==========================================
    with tab_ministry:
        st.subheader("🏛️ Multi‑Venture Execution Tracker (Goal: ₹1,00,000/month)")
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("📦 CarryMe Marketplace", "1 Active Order", delta="+₹50 Gigs")
        with col_m2:
            st.metric("🎬 FutureHQ Content", "4,000 Views", delta="2 Active Reels")
        with col_m3:
            st.metric("🧠 Self Assist App", f"{len(st.session_state.ca_pipeline)} Profiles", delta="System Online")

        st.markdown("---")
        st.markdown("### 🕒 24‑Hour Schedule Matrix (Daily Ops)")
        schedule = pd.DataFrame([
            {"Time": "06:00 – 09:00", "Focus": "🧠 DEEP ASSET CREATION", "Tasks": "Build features, refine FutureHQ & Self Assist modules."},
            {"Time": "09:00 – 10:00", "Focus": "🥪 LOGISTICS CONTROL", "Tasks": "Fulfill, pack, label, hand over Meesho orders."},
            {"Time": "10:00 – 13:00", "Focus": "📈 VALUE FOOTPRINT SCALE", "Tasks": "Bulk upload 3‑5 catalog variations on Meesho."},
            {"Time": "14:00 – 17:00", "Focus": "🎯 TRAFFIC FUNNEL ENGINE", "Tasks": "Bio‑link mapping, shoot & edit short‑form reels."},
            {"Time": "17:00 – 19:00", "Focus": "🤝 HIGH‑TICKET OUTREACH", "Tasks": "Pitch digital services (₹1,500–₹3,000 contracts)."}
        ])
        st.dataframe(schedule, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### 📝 Interactive Evening Reporting Console")
        with st.form("daily_report_form"):
            report_date = st.date_input("Reporting Date", datetime.now())
            fh_views = st.number_input("FutureHQ Instagram Views", min_value=0, step=100)
            fh_clicks = st.number_input("Bio‑Link Clicks", min_value=0, step=1)
            cm_catalogs = st.number_input("New Catalog Uploads (CarryMe)", min_value=0, step=1)
            cm_orders = st.number_input("New Orders Received", min_value=0, step=1)
            revenue = st.number_input("Total Revenue Locked (₹)", min_value=0, step=50)
            raw_bottleneck = st.text_area("Core Operational Bottleneck Today")
            submitted = st.form_submit_button("📊 Compile Ministry Report")

        if submitted:
            polished_bottleneck = auto_polish_text(raw_bottleneck)
            report_text = f"""
### 📊 MINISTRY DAILY RESULTS – {report_date.strftime('%d-%m-%Y')}
#### 1. ASSET ENGINE (FutureHQ)
- Instagram Total Views : {fh_views}
- Bio‑Link Clicks       : {fh_clicks}

#### 2. MARKETPLACE (CarryMe)
- New Catalogs Added    : {cm_catalogs}
- New Orders Received   : {cm_orders}

#### 3. MONETIZATION
- Revenue Locked-in Today : ₹{revenue}

#### 4. AUTOCORRECT CHECK (Auto‑Polished)
- Raw input: {raw_bottleneck if raw_bottleneck.strip() else "None"}
- Polished: {polished_bottleneck}
            """
            st.success("✅ Report ready with auto‑polished bottleneck – copy below for daily audit (19:00)")
            st.code(report_text, language="text")
            st.session_state.daily_logs.append({"date": report_date, "report": report_text})

        # ✨ Standalone Auto Polish Conductor tool
        st.markdown("---")
        st.subheader("✨ Auto Polish Conductor (Standalone)")
        raw_note = st.text_area("Paste any raw operational note (e.g., 'late delivery, need fix tomorrow')", height=100)
        if st.button("Polish Note with AI Rules"):
            if raw_note.strip():
                polished = auto_polish_text(raw_note)
                st.success("**Polished version:**")
                st.code(polished, language="text")
            else:
                st.warning("Please enter some text to polish.")

    # ==========================================
    # SIDEBAR – GOV SEARCH + CODE SHARING
    # ==========================================
    st.sidebar.markdown("---")
    st.sidebar.header("🌐 Govt Infrastructure Search Engine")
    search_term = st.sidebar.text_input("Client/Project search", placeholder="e.g., Delhi Metro Phase IV")
    if search_term:
        st.sidebar.markdown(f"**Searching:** *{search_term}*")
        try:
            url = f"https://html.duckduckgo.com/html/?q={search_term.replace(' ', '+')}+site:gov.in"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            response = requests.get(url, headers=headers, timeout=8)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                links = soup.find_all("a", class_="result__url", limit=3)
                snippets = soup.find_all("a", class_="result__snippet", limit=3)
                if links:
                    for i, (link, snippet) in enumerate(zip(links, snippets), 1):
                        st.sidebar.info(f"🔗 [{i}] {link.text.strip()}\n\n{snippet.text.strip()[:150]}...")
                else:
                    st.sidebar.warning("No public gov listings found.")
            else:
                st.sidebar.warning("Search service unavailable.")
        except Exception:
            st.sidebar.markdown(f"[🔍 Fallback: Search Google for `{search_term} site:gov.in`](https://www.google.com/search?q={search_term.replace(' ', '+')}+site:gov.in)")

    # 📦 FULL CODE-SHARING FEATURE (in sidebar)
    st.sidebar.markdown("---")
    st.sidebar.header("📦 Full Code‑Sharing")
    if st.sidebar.button("📥 Download app.py Source Code"):
        # Read the current script file
        try:
            with open(__file__, "r", encoding="utf-8") as f:
                source_code = f.read()
            st.sidebar.download_button(
                label="⬇️ Click to Save app.py",
                data=source_code,
                file_name="self_assist_core_app.py",
                mime="text/x-python",
                use_container_width=True
            )
            st.sidebar.success("Ready to download!")
        except Exception as e:
            st.sidebar.error(f"Could not read source: {e}")

    # Logout button
    if st.sidebar.button("🔐 Logout Node", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

    # Footer
    st.markdown("---")
    st.caption("⚡ Self Assist Core v3.0 | Auto Polish Conductor + Code Sharing | Berger · CarryMe · FutureHQ")
