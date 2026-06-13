
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

# Halt down execution completely if the user is not authenticated
if check_password():

    # ==========================================
    # 🏗️ MAIN DASHBOARD APPS INTERFACE (SECURED)
    # ==========================================
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1A365D 0%, #2A4365 50%, #1A202C 100%); padding: 22px; border-radius: 8px; margin-bottom: 25px; border-bottom: 4px solid #3182ce;">
            <div style="float: right;"><span style="background-color: #48BB78; color: white; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold;">🔐 SECURE NODE ACTIVE</span></div>
            <h1 class="responsive-title" style="color: white; margin: 0; font-family: 'Segoe UI', sans-serif; font-size: 26px;">
                COMPANY PROTECTON (ADMIXTURE) — NORTH DIVISION MASTER TRACKER
            </h1>
            <p style="color: #90CDF4; margin: 4px 0 0 0; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 500;">
                Grade ML1 — Institutional Key Account Automation Workspace
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Separate Workspace into Tabs for clean organization
    tab_pipeline, tab_intel = st.tabs(["📋 Active Pipeline Matrix", "🔍 B2B Contact Format Generator"])

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
            ["PRJ-02", "Uttar Pradesh", "NHAI / Expressways", "Ganga Expressway (Phase 2 Pours)", "Ongoing", "PNC Infratech", "V. K. Singh (Project Director)", "L N Malviya Infra", "R. Chaudhary (Plant QC)", "Fosroc India", "Mass road beds & bridge decks", "ProSuperplast RT", "Trial mix requested due to slump loss complaints in summer heat.", "Deliver product samples to site batching yard for initial trial mix", "2026-06-25", 80],
            ["PRJ-03", "Delhi-NCR", "Mega Private Projects", "DLF Cybercity Phase 2 Expansion", "Upcoming", "Tata Projects", "Rajesh Kapoor (VP Infrastructure)", "Mantec Consultants", "Amit Pal (Site In-charge)", "MC-Bauchemie", "Deep basement rafts & structural foundation piles", "Hs ProCrystal 100 & HS ProCem CI", "Architectural blueprint finalized. Sub-surface parameters mapped.", "Pitch crystalline integration benefits directly to Mantec Lead", "2026-07-20", 50]
        ]
        return pd.DataFrame(data, columns=columns)

    if "df" not in st.session_state:
        st.session_state.df = load_baseline_data()

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

        # Filter Panel Sidebars safely checked
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
        st.markdown("Type in an executive's name and company to generate their corporate email format and official switchboard routes.")

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
                    extra_notes = "Major infrastructure aggregator. Operates alongside RDC Concrete division (+91 22 6716 5100)."
                
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
                    extra_notes = "Admixture sector incumbent competitor routing blueprint."
                
                else:
                    domain_guess = clean_company.replace(" ", "") + ".com"
                    email_domain = domain_guess
                    email_format = "[first_name].[last_name]@" + domain_guess
                    predicted_email = f"{first}.{last}@{domain_guess}" if last else f"{first}@{domain_guess}"
                    switchboard = "Verify via central website contact tab."
                    extra_notes = "Standard generic global commercial domain architecture applied."

                st.markdown("---")
                st.success(f"### 🎯 Found Format Match for {input_company.upper()}")
                
                c_out1, c_out2 = st.columns(2)
                with c_out1:
                    st.markdown(f"""
                    <div style="background-color: #f0fdf4; padding: 15px; border-radius: 5px; border-left: 4px solid #16a34a;">
                        <strong>📁 Target Executive:</strong> {input_name.title()}<br>
                        <strong>🏢 Company:</strong> {input_company.title()}<br><br>
                        <strong>🌐 Corporate Domain:</strong> <code>{email_domain}</code><br>
                        <strong>⚙️ Standard Format:</strong> <code>{email_format}</code>
                    </div>
                    """, unsafe_allow_html=True)
                
                with c_out2:
                    st.markdown(f"""
                    <div style="background-color: #f8fafc; padding: 15px; border-radius: 5px; border-left: 4px solid #475569;">
                        <strong>📧 Estimated Email Address:</strong> <code>{predicted_email}</code><br><br>
                        <strong>📞 Official Switchboard Line:</strong> {switchboard}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.caption(f"💡 **Strategic Intelligence Note:** {extra_notes}")
            else:
                st.error("Missing Input Parameters: Please fill in both fields.")

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
