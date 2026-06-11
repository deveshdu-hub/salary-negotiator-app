import streamlit as st
import pandas as pd
from io import BytesIO
import requests

# Wide workspace layout configuration
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

# Stop execution completely if the user is not authenticated
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
            <p style="color: #90CDF4; margin: 4px 0 0 0; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 500;">
                Grade ML1 — Institutional Key Account Automation Workspace
            </p>
        </div>
    """, unsafe_allow_html=True)

    tab_pipeline, tab_intel = st.tabs(["📋 Active Pipeline Matrix", "🔍 Dynamic Institutional Directory Finder"])

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
    # 📋 TAB 1: MASTER PIEPELINE TRACKER WORKSPACE
    # ==========================================
    with tab_pipeline:
        st.subheader("📋 Dynamic Territory Pipeline Matrix")
        edited_df = st.data_editor(
            st.session_state.df,
            use_container_width=True,
            num_rows="dynamic",
            key="pipeline_editor_v_prod",
            column_config={
                "Win Probability (%)": st.column_config.ProgressColumn("Win Probability (%)", format="%d%%", min_value=0, max_value=100),
                "Lifecycle Stage": st.column_config.SelectboxColumn("Lifecycle Stage", options=["Upcoming", "Ongoing", "Completion Stage"], required=True)
            }
        )

        c1, c2 = st.columns([1, 5])
        with c1:
            if st.button("💾 Sync Matrix Updates", type="primary"):
                st.session_state.df = edited_df.copy()
                st.success("Internal changes committed!")
        with c2:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                edited_df.to_excel(writer, index=False, sheet_name='North_Div_Pipeline')
            st.download_button(label="📥 Export Current View to Excel", data=output.getvalue(), file_name="Company_North_Division_Pipeline_Export.xlsx")

    # ==========================================
    # 🔍 TAB 2: COMPLIANT INSTITUTIONAL DIRECTORY FINDER
    # ==========================================
    with tab_intel:
        st.subheader("🎯 B2B Target Domain & Switchboard Directory Pattern Generator")
        st.markdown("Generates legal structural formatting records and queries open, public search snippets on demand.")

        # User Configuration Form Data
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            input_name = st.text_input("Target Individual Full Name:", placeholder="e.g., Santosh Kumar Yadav")
        with col_in2:
            input_company = st.text_input("Organization / Enterprise Node Name:", placeholder="e.g., NHAI")

        if st.button("⚡ Generate Structuring File", type="primary"):
            if input_name and input_company:
                clean_name = input_name.strip().lower()
                clean_company = input_company.strip().lower()
                name_parts = clean_name.split()
                
                first = name_parts[0] if len(name_parts) > 0 else ""
                last = name_parts[-1] if len(name_parts) > 1 else ""
                
                # Default formatting logic strings
                guessed_domain = clean_company.replace(" ", "") + ".com"
                is_govt_node = False
                extra_notes = "Standard private enterprise lookup parameters mapped."
                
                # 🏛️ GOVERNMENT ENTITY LEGAL DISPATCH REGISTRY RULES
                if "nhai" in clean_company or "highways authority" in clean_company:
                    guessed_domain = "nhai.org"
                    is_govt_node = True
                    extra_notes = "Verified National Government Authority. Direct communications route via official designators (chairman@nhai.org) or standard National Informatics Centre (NIC) emails."
                elif "dmrc" in clean_company or "metro rail" in clean_company:
                    guessed_domain = "delhimetrorail.com"
                    is_govt_node = True
                    extra_notes = "Urban Transit Node infrastructure layout domain rule active."
                elif "pwd" in clean_company or "government" in clean_company or "nic" in clean_company:
                    guessed_domain = "gov.in"
                    is_govt_node = True
                    extra_notes = "Public Works Department/Central Government structural node data format."
                
                # 🏢 B2B PRIVATE MARKET KEY ACCOUNT CONGRUENCE OVERRIDES
                elif "infra" in clean_company or "hella" in clean_company:
                    guessed_domain = "infra.market"
                    extra_notes = "Industrial Aggregator Matrix Account. Main switchboard includes RDC Concrete division offices."
                elif "rdc" in clean_company:
                    guessed_domain = "rdcconcrete.com"
                elif "l&t" in clean_company or "larsen" in clean_company:
                    guessed_domain = "lntecc.com"

                # Calculate domain layout predictions based on legal structural boundaries
                if is_govt_node and "nhai" in clean_company:
                    format_1 = f"chairman@{guessed_domain} (Designation Structural Handle)"
                    format_2 = f"{first}.{last}@nic.in (IAS Core Individual NIC Mail)"
                    format_3 = f"{first}{last[0] if last else ''}@{guessed_domain}"
                    format_4 = f"{first}@{guessed_domain}"
                else:
                    format_1 = f"{first}@{guessed_domain}"
                    format_2 = f"{first}.{last}@{guessed_domain}" if last else "N/A"
                    format_3 = f"{first}{last}@{guessed_domain}" if last else "N/A"
                    format_4 = f"{first[0] if first else ''}{last}@{guessed_domain}" if last else "N/A"

                # Compliant Web Scraper Utility (Queries public search listings only)
                snippet_records = []
                try:
                    search_string = f"{input_company} corporate head office address phone contact landline switchboard"
                    # Safe HTML query route avoiding heavy browser scraping engines
                    url = f"https://html.duckduckgo.com/html/?q={search_string.replace(' ', '+')}"
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                    res = requests.get(url, headers=headers, timeout=5)
                    
                    if res.status_code == 200:
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(res.text, "html.parser")
                        snippets = soup.find_all("a", class_="result__snippet", limit=3)
                        for snip in snippets:
                            snippet_records.append(snip.text.strip())
                except Exception:
                    pass

                # Display Processed Output Cards
                st.markdown("---")
                st.success(f"### 🎯 Found Entry Blueprint: {input_name.title()} ({input_company.upper()})")
                
                c_panel1, c_panel2 = st.columns(2)
                with c_panel1:
                    st.markdown(f"""
                    **📋 Target Profile Meta Information**
                    * **Name Input:** {input_name.title()}
                    * **Classification:** {"🏛️ Public Government Node" if is_govt_node else "🏢 Commercial Enterprise"}
                    * **Identified Domain Root:** `{guessed_domain}`
                    
                    ---
                    **📧 Structural Mail Mapping Matrix:**
                    1. **Priority Option Alpha:** `{format_1}`
                    2. **Priority Option Beta:** `{format_2}`
                    3. **Priority Option Gamma:** `{format_3}`
                    4. **Priority Option Delta:** `{format_4}`
                    """)
                
                with c_panel2:
                    st.markdown("**🌐 Public Records & Switchboard Directories Found:**")
                    if snippet_records:
                        for idx, record in enumerate(snippet_records):
                            st.info(f"📍 **Index Snippet #{idx+1}:**\n\n{record}")
                    else:
                        st.warning("No automated public phone snippets found. Use the verification escape link below.")
                    
                    manual_link = f"https://www.google.com/search?q={input_company.replace(' ', '+')}+official+contact+directory+phone+number"
                    st.markdown(f'👉 [Launch External Live Verification Window]({manual_link})')
                
                st.caption(f"💡 **Strategic Account Note:** {extra_notes}")
            else:
                st.error("Missing Parameters: Complete both entry locks to index correctly.")

    # ==========================================
    # 🌐 SIDEBAR UTILITY SYSTEM
    # ==========================================
    st.sidebar.header("🕹️ Control & Search Panel")
    st.sidebar.caption("System Status: Local Secure Node Active.")
    
    # Persistent Sidebar Live Government Pipeline Search Engine Tool
    st.sidebar.markdown("---")
    st.sidebar.header("🌐 Govt Infrastructure Search Engine")
    sidebar_search = st.sidebar.text_input("Verify Project Pipeline/Tenders:", key="side_search_key")
    
    if sidebar_search:
        st.sidebar.markdown(f"**Latest Public Listings for:** *'{sidebar_search}'*")
        try:
            url = f"https://html.duckduckgo.com/html/?q={sidebar_search.replace(' ', '+')}+site:gov.in"
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
            st.sidebar.markdown(f"[🔗 Launch External Live Government Verification Link](https://www.google.com/search?q={sidebar_search.replace(' ', '+')}+site:gov.in)")
