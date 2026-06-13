import streamlit as st
import pandas as pd
from io import BytesIO
import requests
from datetime import datetime

# Wide workspace corporate configuration
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
                Grade ML1 — Institutional Key Account & Venture Growth Automation Workspace
            </p>
        </div>
    """, unsafe_allow_html=True)

    tab_pipeline, tab_intel, tab_ministry = st.tabs([
        "📋 Active Pipeline Matrix", 
        "🔍 Dynamic Institutional Directory Finder", 
        "🏛️ Investor Ministry Growth Console"
    ])

    # Master Dataset Matrix Initialization
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
            ["PRJ-02", "Uttar Pradesh", "NHAI / Expressways", "Ganga Expressway (Phase 2 Pours)", "Ongoing", "PNC Infratech", "V. K. Singh (Project Director)", "L N Malviya Infra", "R. Chaudhary (Plant QC)", "Fosroc India", "Mass road beds & bridge decks", "ProSuperplast RT", "Trial mix requested due to slump loss complaints in summer heat.", "Deliver product samples to site batching yard for initial trial mix", "2026-06-25", 80],
            ["PRJ-03", "Punjab", "Farmer Segment", "NABARD Mega Grain Silos Complex (Punjab Node)", "Upcoming", "Agro-Infrastructure Corp", "Baljit Singh (Director Operations)", "RITES Rural Cell", "G. Dhillon (Quality Lead)", "Local Admixtures", "Mass slipform foundation raft concrete", "ProHyperplast SP & ProCem CI", "Initial site topography finalized. Soil retention evaluation active.", "Pitch high-slump flow retention benefits directly to RITES lead.", "2026-08-01", 55],
            ["PRJ-04", "Uttar Pradesh", "Farmer Segment", "Jal Jeevan Mission Rural Tank Network (West UP)", "Ongoing", "Varanasi Infra Contracts", "A. K. Mishra (Executive Engineer)", "State Water Board Cell", "V. K. Yadav (Plant Inspector)", "Fosroc India", "Elevated Storage Reservoirs (ESR) & Precast Pipes", "Hs ProCrystal 100 & ProSuperplast", "Casting matrix parameters approved. Continuous pouring scheduled.", "Deliver crystalline integration waterproofing batches to regional yard.", "2026-07-22", 75]
        ]
        return pd.DataFrame(data, columns=columns)

    if "df" not in st.session_state:
        st.session_state.df = load_baseline_data()

    # ==========================================
    # 📋 TAB 1: DATA EDITING & EXCEL SYNC ENGINE
    # ==========================================
    with tab_pipeline:
        st.subheader("🔄 Weekly Excel Data Synchronization & Append Hub")
        uploaded_file = st.file_uploader("Drop newly received or edited client sheets here to update baseline records:", type=["xlsx", "xls"])

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
                        st.success("Sync complete! Data matrix compiled.")
                else:
                    st.error("Invalid File Format: Missing structural 'Project ID' mapping column.")
            except Exception as e:
                st.error(f"Sync Interrupted: {str(e)}")

        st.markdown("---")
        st.subheader("📋 Active Territory Pipeline Matrix")
        
        edited_df = st.data_editor(
            st.session_state.df,
            use_container_width=True,
            num_rows="dynamic",
            key="pipeline_editor_v_final_prod",
            column_config={
                "Win Probability (%)": st.column_config.ProgressColumn("Win Probability (%)", format="%d%%", min_value=0, max_value=100),
                "Lifecycle Stage": st.column_config.SelectboxColumn("Lifecycle Stage", options=["Upcoming", "Ongoing", "Completion Stage"], required=True)
            }
        )

        c1, c2 = st.columns([1, 5])
        with c1:
            if st.button("💾 Sync Matrix Updates", type="primary"):
                st.session_state.df = edited_df.copy()
                st.success("Internal changes committed to RAM!")
        with c2:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                edited_df.to_excel(writer, index=False, sheet_name='North_Div_Pipeline')
            st.download_button(label="📥 Export Current View to Excel", data=output.getvalue(), file_name="Company_North_Division_Pipeline_Export.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # ==========================================
    # 🔍 TAB 2: LEGAL EXECUTIVE SEARCH & DIRECTORY FINDER
    # ==========================================
    with tab_intel:
        st.subheader("🎯 B2B Target Domain & Switchboard Directory Pattern Generator")
        st.markdown("Calculates layout formatting probabilities for corporate/government accounts and processes public record listings safely.")

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
                
                guessed_domain = clean_company.replace(" ", "") + ".com"
                is_govt_node = False
                extra_notes = "Standard private sector enterprise configuration parameters mapped."
                
                if "nhai" in clean_company or "highways authority" in clean_company:
                    guessed_domain = "nhai.org"
                    is_govt_node = True
                    extra_notes = "Verified Central Government Node. Designation parameters active (chairman@nhai.org) alongside National Informatics Centre (NIC) user allocations."
                elif "dmrc" in clean_company or "metro rail" in clean_company:
                    guessed_domain = "delhimetrorail.com"
                    is_govt_node = True
                    extra_notes = "Urban Rapid Transit segment infrastructure rules mapping applied."
                elif "pwd" in clean_company or "government" in clean_company or "nic" in clean_company:
                    guessed_domain = "gov.in"
                    is_govt_node = True
                    extra_notes = "Public Works Department/Central Civil State node format architecture matching."
                elif "nabard" in clean_company:
                    guessed_domain = "nabard.org"
                    extra_notes = "National Bank for Agriculture and Rural Development. Institutional financing node for rural expansion pours."
                elif "jal jeevan" in clean_company or "jjm" in clean_company or "drinking water" in clean_company:
                    guessed_domain = "jaljeevanmission.gov.in"
                    is_govt_node = True
                    extra_notes = "Jal Jeevan Mission Framework. Focuses on mass rural storage installations, precast concrete conduits, and water management infrastructure grids."
                elif "iffco" in clean_company or "fertilizer" in clean_company:
                    guessed_domain = "iffco.in"
                    extra_notes = "Major agricultural cooperative multi-state framework network tracker node."

                elif "infra" in clean_company or "hella" in clean_company:
                    guessed_domain = "infra.market"
                    extra_notes = "Industrial Aggregator Matrix Account. Main office includes RDC Concrete division offices."
                elif "rdc" in clean_company:
                    guessed_domain = "rdcconcrete.com"
                elif "l&t" in clean_company or "larsen" in clean_company:
                    guessed_domain = "lntecc.com"

                if is_govt_node and "nhai" in clean_company:
                    format_1 = f"chairman@{guessed_domain} (Designation Structural Handle)"
                    format_2 = f"{first}.{last}@nic.in (IAS Core Individual NIC Mail)"
                    format_3 = f"{first}{last[0] if last else ''}@{guessed_domain}"
                    format_4 = f"{first}@{guessed_domain}"
                elif "jal jeevan" in clean_company or "jjm" in clean_company:
                    format_1 = f"md-jjm@gov.in (Mission Director Executive Desk)"
                    format_2 = f"{first}.{last}@nic.in"
                    format_3 = f"{first}@{guessed_domain}"
                    format_4 = f"{first}.{last}@{guessed_domain}"
                elif "iffco" in clean_company:
                    format_1 = f"{first}{last[0] if last else ''}@iffco.in"
                    format_2 = f"{first}.{last}@iffco.in"
                    format_3 = f"{first}@iffco.in"
                    format_4 = f"{last}{first}@iffco.in"
                else:
                    format_1 = f"{first}@{guessed_domain}"
                    format_2 = f"{first}.{last}@{guessed_domain}" if last else "N/A"
                    format_3 = f"{first}{last}@{guessed_domain}" if last else "N/A"
                    format_4 = f"{first[0] if first else ''}{last}@{guessed_domain}" if last else "N/A"

                snippet_records = []
                try:
                    search_string = f"{input_company} corporate head office address phone contact landline switchboard"
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

                st.markdown("---")
                st.success(f"### 🎯 Found Entry Blueprint: {input_name.title()} ({input_company.upper()})")
                
                c_panel1, c_panel2 = st.columns(2)
                with c_panel1:
                    st.markdown(f"""
                    **📋 Target Profile Meta Information**
                    * **Name Input Parameters:** {input_name.title()}
                    * **Segment Category Identification:** {"🏛️ Public Institutional Government Node" if is_govt_node else "🏢 Private Commercial Entity Matrix"}
                    * **Identified System Domain Root:** `{guessed_domain}`
                    
                    ---
                    **📧 Structural Mail Mapping Probability Matrix:**
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
                        st.warning("No automated public phone snippets found. Use the manual verification window option below.")
                    
                    manual_link = f"https://www.google.com/search?q={input_company.replace(' ', '+')}+official+contact+directory+phone+number"
                    st.markdown(f'👉 [Launch External Live Verification Window]({manual_link})')
                
                st.caption(f"💡 **Strategic Account Note:** {extra_notes}")
            else:
                st.error("Missing Parameters: Type target metrics into both fields to process execution loop.")

    # ==========================================
    # 🏛️ TAB 3: INVESTOR MINISTRY GROWTH CONSOLE
    # ==========================================
    with tab_ministry:
        st.subheader("🏛️ Multi-Venture Execution Panel (Target: ₹1,00,000/Month)")
        
        # 1. Display the 24-Hour Time-Block Schedule Matrix
        st.markdown("### 🕒 Strategic 24-Hour Optimization Timeline")
        
        schedule_data = [
            {"Time Block": "06:00 - 09:00", "Focus Node": "🧠 DEEP ASSET CREATION", "Deliverable / Actions": "FutureHQ architecture build, premium video scripting, workflow programming."},
            {"Time Block": "09:00 - 10:00", "Focus Node": "🥪 FUEL & LOGISTICS", "Deliverable / Actions": "Pack & label open orders, coordinate courier handover, update manifest."},
            {"Time Block": "10:00 - 13:00", "Focus Node": "📈 SCALE & EXPANSION", "Deliverable / Actions": "Bulk upload 3-5 new optimized catalogs/variants onto Meesho marketplace."},
            {"Time Block": "13:00 - 14:00", "Focus Node": "🍛 RECOVERY BREAK", "Deliverable / Actions": "System reset, offline break, processing check."},
            {"Time Block": "14:00 - 17:00", "Focus Node": "🎯 TRAFFIC & DISTRIBUTION", "Deliverable / Actions": "Build landing funnels, update digital bio-links, edit & render traffic content."},
            {"Time Block": "17:00 - 19:00", "Focus Node": "🤝 HIGH-TICKET OUTREACH", "Deliverable / Actions": "Pitch digital service packages (minimum threshold ₹1,500 - ₹3,000 value)."},
            {"Time Block": "19:00 - 20:00", "Focus Node": "📊 INVESTOR MINISTRY DEBRIEF", "Deliverable / Actions": "Log metrics, compile daily data brief, review alignment strategies."},
            {"Time Block": "20:00 - 06:00", "Focus Node": "💤 MANDATORY OFFLINE RESET", "Deliverable / Actions": "Deep sleep, physical recovery, zero system activity."}
        ]
        st.table(pd.DataFrame(schedule_data))

        st.markdown("---")
        st.markdown("### 📝 Interactive Evening Reporting Console")
        st.caption("Fill out your metrics at 19:00 daily to format your direct tracking output.")

        # Interactive form variables
        with st.form("ministry_report_form"):
            date_col = st.date_input("Reporting Cycle Date:", datetime.now())
            
            st.markdown("**1. Asset Generation Metrics (FutureHQ & Content)**")
            f_views = st.number_input("FutureHQ Instagram Aggregate Views Today:", min_value=0, step=100)
            f_clicks = st.number_input("Bio-Link Traffic Clicks Logged:", min_value=0, step=1)
            f_reels = st.number_input("Number of Reels Processed & Launched:", min_value=0, step=1)
            
            st.markdown("**2. Marketplace Footprint Metrics (CarryMe)**")
            c_catalogs = st.number_input("Total Active Catalogs on Meesho Grid:", min_value=0, step=1)
            c_new_cat = st.number_input("New Product Configurations Uploaded Today (Target: 3-5):", min_value=0, step=1)
            c_orders = st.number_input("New Inbound Orders Received:", min_value=0, step=1)
            c_status = st.selectbox("Current Shipping/Logistics Status:", ["All Orders Clear & Dispatched", "Shipments Pending Pick-Up", "No Open Orders"])
            
            st.markdown("**3. High-Ticket Monetization**")
            m_pitches = st.number_input("High-Ticket Cold Pitches Transmitted (Min ₹1,500 value):", min_value=0, step=1)
            m_rev = st.number_input("Total Revenue Confirmed/Locked Today (₹):", min_value=0, step=50)
            
            st.markdown("**4. System Integrity Flags**")
            sys_adhere = st.radio("Did you maintain 100% adherence to the 24-Hour Matrix constraints?", ["Yes, full discipline maintained.", "No, encountered time deviations."])
            sys_bottleneck = st.text_area("Identify the core operational bottleneck encountered today:")
            
            submit_report = st.form_submit_button("📊 Compile & Format Ministry Report")

        # Code block output generation
        if submit_report:
            formatted_string = f"""
### 📊 MINISTRY DAILY RESULTS BRIEF: {date_col.strftime('%d-%m-%Y')}

#### 1. ASSET GENERATION ENGINE (FutureHQ & Content)
* FutureHQ Instagram Total Views Today: {f_views}
* Bio-Link Clicks / Traffic Captured: {f_clicks}
* Number of Content Pieces/Reels Produced: {f_reels}
* Status of Video Funnel Hook: Functional

#### 2. MARKETPLACE VOLUMETRIC FOOTPRINT (CarryMe)
* Total Active Catalogs on Meesho: {c_catalogs}
* New Catalogs Added Today: {c_new_cat}
* New Orders Received Today: {c_orders}
* Dispatch & Logistics Status of Existing Orders: {c_status}

#### 3. MONETIZATION & HIGH-TICKET FREELANCING
* Number of Cold Pitches Sent out (Min ₹1,500 value): {m_pitches}
* Total Revenue Locked-in Today: ₹{m_rev}

#### 4. SYSTEM AUTOCORRECT CHECK
* Did I adhere 100% to the 24-Hour Matrix today? {sys_adhere}
* Major operational bottleneck encountered today: {sys_bottleneck if sys_bottleneck else "None logged."}
            """
            st.success("### 📜 Final Report Compiled successfully!")
            st.markdown("Copy the text inside the box below and submit it directly to your Investor Ministry feedback session:")
            st.code(formatted_string, language="text")

    # ==========================================
    # 🌐 SIDEBAR UTILITY RUN CONTROL ENGINE
    # ==========================================
    st.sidebar.header("🕹️ Control & Search Panel")
    st.sidebar.caption("System Status: Local Secure Node Active.")
    
    st.sidebar.markdown("---")
    st.sidebar.header("🌐 Govt Infrastructure Search Engine")
    sidebar_search = st.sidebar.text_input("Verify Project Pipeline/Tenders:", key="side_search_key_prod")
    
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
