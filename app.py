import streamlit as st
import pandas as pd
from io import BytesIO
import requests

# Wide corporate workspace configuration
st.set_page_config(
    page_title="Company Protecton Elite Tracker",
    page_icon="🏗️",
    layout="wide"
)

# ==========================================
# 🔑 SECURITY & LOGIN ACCESS CONTROL LAYER
# ==========================================
def check_password():
    """Returns True if the user enters the correct User ID and Password."""
    VALID_USERNAME = "admin123"
    VALID_PASSWORD = "CompanyNorth2026"

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

# Halt execution completely if the user is not authenticated
if check_password():

    # ==========================================
    # 🏗️ MAIN DASHBOARD APPS INTERFACE (SECURED)
    # ==========================================
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1A365D 0%, #2A4365 50%, #1A202C 100%); padding: 22px; border-radius: 8px; margin-bottom: 25px; border-bottom: 4px solid #3182ce;">
            <div style="float: right;"><span style="background-color: #48BB78; color: white; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold;">🔐 SECURE NODE ACTIVE</span></div>
            <h1 style="color: white; margin: 0; font-family: 'Segoe UI', sans-serif; font-size: 26px;">
                COMPANY PROTECTON (ADMIXTURE) — NORTH DIVISION MASTER TRACKER
            </h1>
            <p style="color: #90CDF4; margin: 4px 0 0 0; font-size: 13px; uppercase; letter-spacing: 1px; font-weight: 500;">
                Grade ML1 — Institutional Key Account Automation Workspace
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Separate Workspace into Tabs for clean organization
    tab_pipeline, tab_intel = st.tabs(["📋 Active Pipeline Matrix", "🔍 Dynamic Executive Search Engine"])

    # Baseline Dataset for Pipeline Tab
    @st.cache_data
    def load_baseline_data():
        columns = [
            "Project ID", "State / Hub", "Client Category", "Project Name", "Lifecycle Stage",
            "Primary EPC Contractor", "Key Decision Maker", "Structural Consultant",
            "QC / Plant Lead", "Incumbent Competitor", "Target Application Zone",
            "Company Counterweapon", "Latest Action Update", "Next Concrete Action Required",
            "Target Date", "Win Probability (%)"
        ]
        data = [
            ["PRJ-01", "Delhi-NCR", "Metro Rail", "Delhi Metro Phase IV (Golden Line)", "Upcoming", "L&T Construction", "Arjun Mehta (Procurement Head)", "DMRC Design Board", "S. Sharma (QC Manager)", "Sika India", "Underground Cut-&-Cover Tunnels", "ProHyperplast SP & HS ProCrystal 100", "Bidding stage active. Structural drawing pulled.", "Schedule technical meeting with DMRC Consultant for spec-in", "2026-07-15", 65],
            ["PRJ-02", "Uttar Pradesh", "NHAI / Expressways", "Ganga Expressway (Phase 2 Pours)", "Ongoing", "PNC Infratech", "V. K. Singh (Project Director)", "L N Malviya Infra", "R. Chaudhary (Plant QC)", "Fosroc India", "Mass road beds & bridge decks", "ProSuperplast RT", "Trial mix requested due to slump loss complaints in summer heat.", "Deliver product samples to site batching yard for initial trial mix", "2026-06-25", 80]
        ]
        return pd.DataFrame(data, columns=columns)

    if "df" not in st.session_state:
        st.session_state.df = load_baseline_data()

    # ==========================================
    # 📋 TAB 1: CORE PIPELINE TRACKER
    # ==========================================
    with tab_pipeline:
        st.subheader("📋 Active Territory Pipeline Matrix")
        edited_df = st.data_editor(
            st.session_state.df,
            use_container_width=True,
            num_rows="dynamic",
            key="pipeline_editor_v7",
            column_config={
                "Win Probability (%)": st.column_config.ProgressColumn("Win Probability (%)", format="%d%%", min_value=0, max_value=100),
                "Lifecycle Stage": st.column_config.SelectboxColumn("Lifecycle Stage", options=["Upcoming", "Ongoing", "Completion Stage"], required=True)
            }
        )

        c1, c2 = st.columns([1, 5])
        with c1:
            if st.button("💾 Sync Matrix Updates", type="primary"):
                st.session_state.df = edited_df.copy()
                st.success("Saved!")
        with c2:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                edited_df.to_excel(writer, index=False, sheet_name='North_Div_Pipeline')
            st.download_button(label="📥 Export to Excel", data=output.getvalue(), file_name="Company_North_Division_Pipeline_Export.xlsx")

    # ==========================================
    # 🔍 TAB 2: UNIVERSAL EXECUTIVE SEARCH ENGINE
    # ==========================================
    with tab_intel:
        st.subheader("🎯 Universal Executive Intelligence & Data Matcher")
        st.markdown("Type any name and company below. The engine will calculate standard email syntax variables and run a deep real-time corporate validation search.")

        # Real-time search inputs
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            input_name = st.text_input("Executive Full Name:", placeholder="e.g., Pralhad Majumdar")
        with col_in2:
            input_company = st.text_input("Target Corporate/Company Name:", placeholder="e.g., Hella Infra Market")

        if st.button("⚡ Execute Universal Deep Search", type="primary"):
            if input_name and input_company:
                # 1. Standardize string arguments for formula processing
                clean_name = input_name.strip().lower()
                clean_company = input_company.strip().lower()
                name_parts = clean_name.split()
                
                first = name_parts[0] if len(name_parts) > 0 else ""
                last = name_parts[1] if len(name_parts) > 1 else ""
                
                # Guess primary domain syntax based on input
                guessed_domain = clean_company.replace(" ", "").replace("limited", "").replace("pvt", "") + ".com"
                
                # Manual overrides for established industry players
                if "infra" in clean_company or "hella" in clean_company:
                    guessed_domain = "infra.market"
                elif "rdc" in clean_company:
                    guessed_domain = "rdcconcrete.com"
                elif "l&t" in clean_company or "larsen" in clean_company:
                    guessed_domain = "lntecc.com"

                # 2. Construct the 4 Most Common Indian B2B Corporate Email Combinations
                format_1 = f"{first}@{guessed_domain}"                                # first name only
                format_2 = f"{first}.{last}@{guessed_domain}" if last else "N/A"        # first.last
                format_3 = f"{first}{last}@{guessed_domain}" if last else "N/A"         # firstlast
                format_4 = f"{first[0] if first else ''}{last}@{guessed_domain}" if last else "N/A" # flast

                # 3. Live Web Scraping Intelligence Layer (Fetches official info from public listings)
                switchboard_found = "Verify via central web desk"
                snippet_records = []
                
                try:
                    # Search query tailored to pull contact numbers, corporate offices, and directories
                    search_string = f"{input_company} corporate head office contact phone number switchboard"
                    url = f"https://html.duckduckgo.com/html/?q={search_string.replace(' ', '+')}"
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                    res = requests.get(url, headers=headers, timeout=6)
                    
                    if res.status_code == 200:
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(res.text, "html.parser")
                        snippets = soup.find_all("a", class_="result__snippet", limit=3)
                        for snip in snippets:
                            snippet_records.append(snip.text.strip())
                except Exception:
                    pass

                # Display Results Card
                st.markdown("---")
                st.success(f"### 🎯 Search Summary Matrix: {input_name.title()} ({input_company.title()})")
                
                c_panel1, c_panel2 = st.columns(2)
                with c_panel1:
                    st.markdown(f"""
                    **📋 Target Profile Summary**
                    * **Full Name:** {input_name.title()}
                    * **Company Node:** {input_company.title()}
                    * **Identified Domain Root:** `{guessed_domain}`
                    
                    ---
                    **📧 Calculated Probability Email Matrices:**
                    1. **Primary Syntax (High Probability):** `{format_1}`
                    2. **Secondary Syntax:** `{format_2}`
                    3. **Alternative Syntax 1:** `{format_3}`
                    4. **Alternative Syntax 2:** `{format_4}`
                    """)
                
                with c_panel2:
                    st.markdown("**🌐 Real-time Corporate Intelligence & Switchboard Mentions:**")
                    if snippet_records:
                        for idx, record in enumerate(snippet_records):
                            st.info(f"🔍 **Public Listing Data #{idx+1}:**\n\n{record}")
                    else:
                        st.warning("No automated public phone snippets found. Click the direct link below to parse the live index manually.")
                    
                    # Direct, secure verification link escape route
                    manual_link = f"https://www.google.com/search?q={input_company.replace(' ', '+')}+corporate+head+office+contact+number"
                    st.markdown(f'👉 [Launch Manual Verification Window]({manual_link})')
            else:
                st.error("Missing Input: Please enter both the executive name and company name to execute the generator loops.")

    # ==========================================
    # 🌐 SIDEBAR SYSTEM UTILITY
    # ==========================================
    st.sidebar.markdown("---")
    st.sidebar.caption("System Status: Secure Local Matrix Operations Active.")
