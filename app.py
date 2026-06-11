import streamlit as st
import pandas as pd
from io import BytesIO
import requests

# Wide corporate workspace configuration
st.set_page_config(
    page_title="Berger Protecton Elite Tracker",
    page_icon="🏗️",
    layout="wide"
)

# Application Top Banner Display
st.markdown("""
    <div style="background: linear-gradient(135deg, #1A365D 0%, #2A4365 50%, #1A202C 100%); padding: 22px; border-radius: 8px; margin-bottom: 25px; border-bottom: 4px solid #3182ce;">
        <h1 style="color: white; margin: 0; font-family: 'Segoe UI', sans-serif; font-size: 26px;">
            BERGER PROTECTON (ADMIXTURE) — NORTH DIVISION MASTER TRACKER
        </h1>
        <p style="color: #90CDF4; margin: 4px 0 0 0; font-size: 13px; uppercase; letter-spacing: 1px; font-weight: 500;">
            Grade ML1 — Institutional Key Account Automation Workspace
        </p>
    </div>
""", unsafe_allow_html=True)

# Master Data Initialization Setup
@st.cache_data
def load_baseline_data():
    columns = [
        "Project ID", "State / Hub", "Client Category", "Project Name", "Lifecycle Stage",
        "Primary EPC Contractor", "Key Decision Maker", "Structural Consultant",
        "QC / Plant Lead", "Incumbent Competitor", "Target Application Zone",
        "Berger Counterweapon", "Latest Action Update", "Next Concrete Action Required",
        "Target Date", "Win Probability (%)"
    ]
    data = [
        ["PRJ-01", "Delhi-NCR", "Metro Rail", "Delhi Metro Phase IV (Golden Line)", "Upcoming", "L&T Construction", "Arjun Mehta (Procurement Head)", "DMRC Design Board", "S. Sharma (QC Manager)", "Sika India", "Underground Cut-&-Cover Tunnels", "ProHyperplast SP & HS ProCrystal 100", "Bidding stage active. Structural drawing pulled.", "Schedule technical meeting with DMRC Consultant for spec-in", "2026-07-15", 65],
        ["PRJ-02", "Uttar Pradesh", "NHAI / Expressways", "Ganga Expressway (Phase 2 Pours)", "Ongoing", "PNC Infratech", "V. K. Singh (Project Director)", "L N Malviya Infra", "R. Chaudhary (Plant QC)", "Fosroc India", "Mass road beds & bridge decks", "ProSuperplast RT", "Trial mix requested due to slump loss complaints in summer heat.", "Deliver product samples to site batching yard for initial trial mix", "2026-06-25", 80],
        ["PRJ-03", "Delhi-NCR", "Mega Private Projects", "DLF Cybercity Phase 2 Expansion", "Upcoming", "Tata Projects", "Rajesh Kapoor (VP Infrastructure)", "Mantec Consultants", "Amit Pal (Site In-charge)", "MC-Bauchemie", "Deep basement rafts & structural foundation piles", "Hs ProCrystal 100 & HS ProCem CI", "Architectural blueprint finalized. Sub-surface parameters mapped.", "Pitch crystalline integration benefits directly to Mantec Lead", "2026-07-20", 50],
        ["PRJ-04", "Jammu & Kashmir", "Metro Rail", "Jammu Metro Neo Elevated viaducts", "Upcoming", "Designated Concessionaire", "TBD (Tender Stage)", "RITES Limited", "TBD", "CAC (Additives)", "Elevated Viaduct Precast Segments", "HS ProCem 9000 AB/PC", "Casting yard layout approvals active.", "Submit technical datasheet of HS ProCem 9000 to RITES approval board", "2026-08-10", 70],
        ["PRJ-05", "Uttar Pradesh", "Metro Rail", "Agra Metro Underground Corridors", "Ongoing", "Afcons Infrastructure", "S. Mukherjee (Project Head)", "UPMRC Technical Cell", "K. Dwivedi (QC Lead)", "Sika India", "Diaphragm walls & tunnel segment casting", "ProHyperplast series", "Continuous pours active. Incumbent experiencing mild bleeding issues.", "Execute on-site comparison mix demonstrating superior cohesion", "2026-06-30", 75],
        ["PRJ-06", "Punjab", "PWD", "Amritsar Smart Parking Complex", "Completion Stage", "Local Grade-A Contractor", "G. S. Dhillon (Executive Engineer)", "Punjab PWD Design Cell", "Harpreet Singh (Site Lead)", "Dr. Fixit (Pidilite)", "Finished structural piers & multi-level basement decks", "Protecton Coatings & Expansion Joint Sealants", "Core structural framework handovers complete. Moving to finishing.", "Present anti-carbonation coatings and PU flooring specifications", "2026-07-05", 85]
    ]
    return pd.DataFrame(data, columns=columns)

if "df" not in st.session_state:
    st.session_state.df = load_baseline_data()

# ==========================================
# 🔄 SECTION 1: WEEKLY EXCEL SYNC & IMPORT ENGINE
# ==========================================
st.subheader("🔄 Weekly Government Excel Synchronization Hub")
uploaded_file = st.file_uploader("Drop newly received or edited client sheets here to dynamically update the master base:", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        incoming_df = pd.read_excel(uploaded_file)
        if "Project ID" in incoming_df.columns:
            if st.button("⚡ Execute Deep Sync & Merge Records"):
                # Align structural mapping to index
                st.session_state.df.set_index("Project ID", inplace=True, drop=False)
                incoming_df.set_index("Project ID", inplace=True, drop=False)
                
                # Execute safe row overwrites for existing keys
                for idx in incoming_df.index:
                    st.session_state.df.loc[idx] = incoming_df.loc[idx]
                
                st.session_state.df.reset_index(drop=True, inplace=True)
                st.success("Sync complete! Weekly data models cross-aligned and appended successfully.")
        else:
            st.error("Invalid File Format: Uploaded document must contain a 'Project ID' index column to ensure data safety alignment.")
    except Exception as e:
        st.error(f"Sync Interrupted: {str(e)}")

st.markdown("---")

# Metrics Analytics Bar
m1, m2, m3 = st.columns(3)
m1.metric("Active Pipelines Tracked", len(st.session_state.df))
m2.metric("Upcoming Spec-In Windows", len(st.session_state.df[st.session_state.df["Lifecycle Stage"] == "Upcoming"]))
m3.metric("Ongoing Active Site Trials", len(st.session_state.df[st.session_state.df["Lifecycle Stage"] == "Ongoing"]))

st.markdown("---")

# ==========================================
# 🔍 SECTION 2: SIDEBAR FILTERS & GOVT LOOKUP SEARCH ENGINE
# ==========================================
st.sidebar.header("🕹️ Control & Target Panel")

# Standard filtering tools
filter_state = st.sidebar.multiselect("Select State / Hub:", options=st.session_state.df["State / Hub"].unique(), default=st.session_state.df["State / Hub"].unique())
filtered_df = st.session_state.df[st.session_state.df["State / Hub"].isin(filter_state)]

st.sidebar.markdown("---")
st.sidebar.header("🌐 Govt Infrastructure Search Engine")
search_query = st.sidebar.text_input("Type Client/Project (e.g., 'NHAI Ganga Expressway tender'):")

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

# ==========================================
# 📋 SECTION 3: MAIN DYNAMIC WORKSPACE MATRIX VIEW
# ==========================================
st.subheader("📋 Active Territory Pipeline Matrix")
edited_df = st.data_editor(
    filtered_df,
    use_container_width=True,
    num_rows="dynamic",
    key="pipeline_editor_v3",
    column_config={
        "Win Probability (%)": st.column_config.ProgressColumn("Win Probability (%)", format="%d%%", min_value=0, max_value=100),
        "Lifecycle Stage": st.column_config.SelectboxColumn("Lifecycle Stage", options=["Upcoming", "Ongoing", "Completion Stage"], required=True)
    }
)

# Control Action Hub Buttons
c1, c2 = st.columns([1, 5])
with c1:
    if st.button("💾 Sync Matrix Updates", type="primary"):
        st.session_state.df.set_index("Project ID", inplace=True, drop=False)
        for idx in edited_df["Project ID"]:
            st.session_state.df.loc[idx] = edited_df.set_index("Project ID", drop=False).loc[idx]
        st.session_state.df.reset_index(drop=True, inplace=True)
        st.success("Matrix successfully saved and synchronized!")

with c2:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        edited_df.to_excel(writer, index=False, sheet_name='North_Div_Pipeline')
    processed_data = output.getvalue()
    
    st.download_button(
        label="📥 Export Current View to Excel",
        data=processed_data,
        file_name="Berger_North_Division_Pipeline_Export.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
