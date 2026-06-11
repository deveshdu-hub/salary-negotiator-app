import streamlit as st
import pandas as pd

# Set up clean, wide corporate page layout
st.set_page_config(
    page_title="Berger Protecton Master Tracker",
    page_icon="🏗️",
    layout="wide"
)

# Application Header Banner
st.markdown("""
    <div style="background: linear-gradient(135deg, #1A365D 0%, #2A4365 100%); padding: 25px; border-radius: 8px; margin-bottom: 25px; border-bottom: 4px solid #3182ce;">
        <h1 style="color: white; margin: 0; font-family: 'Segoe UI', sans-serif; font-size: 28px;">
            BERGER PROTECTON (ADMIXTURE) — NORTH DIVISION
        </h1>
        <p style="color: #90CDF4; margin: 5px 0 0 0; font-size: 14px; uppercase; letter-spacing: 1px;">
            Institutional Key Account & Infrastructure Pipeline Master Workstation
        </p>
    </div>
""", unsafe_allow_html=True)

# 1. Master Baseline Data (No RMC Accounts Included)
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

# Load data into session state to allow persistence during updates
if "df" not in st.session_state:
    st.session_state.df = load_baseline_data()

# 2. Key High-Level Summary Metrics
total_projects = len(st.session_state.df)
upcoming_count = len(st.session_state.df[st.session_state.df["Lifecycle Stage"] == "Upcoming"])
ongoing_count = len(st.session_state.df[st.session_state.df["Lifecycle Stage"] == "Ongoing"])
avg_prob = int(st.session_state.df["Win Probability (%)"].mean())

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Institutional Pipelines", total_projects)
m2.metric("Upcoming (Spec-In Focus)", upcoming_count)
m3.metric("Ongoing (Active Site Trials)", ongoing_count)
m4.metric("Average Win Probability", f"{avg_prob}%")

st.markdown("---")

# 3. Interactive Filtering Command Center (Sidebar)
st.sidebar.header("🔍 Pipeline Control Center")

filter_state = st.sidebar.multiselect(
    "Select State / Hub:",
    options=st.session_state.df["State / Hub"].unique(),
    default=st.session_state.df["State / Hub"].unique()
)

filter_client = st.sidebar.multiselect(
    "Select Client Category:",
    options=st.session_state.df["Client Category"].unique(),
    default=st.session_state.df["Client Category"].unique()
)

filter_stage = st.sidebar.multiselect(
    "Select Lifecycle Stage:",
    options=st.session_state.df["Lifecycle Stage"].unique(),
    default=st.session_state.df["Lifecycle Stage"].unique()
)

# Apply active filters to the matrix
filtered_df = st.session_state.df[
    (st.session_state.df["State / Hub"].isin(filter_state)) &
    (st.session_state.df["Client Category"].isin(filter_client)) &
    (st.session_state.df["Lifecycle Stage"].isin(filter_stage))
]

# 4. Main Matrix View & Inline Editing Engine
st.subheader("📋 Active Territory Pipeline Matrix")
st.markdown("*Double-click on any field below to update updates, targets, or contacts instantly with your team.*")

# Render table inside an editable data editor UI component
edited_df = st.data_editor(
    filtered_df,
    use_container_width=True,
    num_rows="dynamic",
    column_config={
        "Win Probability (%)": st.column_config.ProgressColumn(
            "Win Probability (%)",
            help="Team confidence index to close project",
            format="%d%%",
            min_value=0,
            max_value=100
        ),
        "Lifecycle Stage": st.column_config.SelectboxColumn(
            "Lifecycle Stage",
            options=["Upcoming", "Ongoing", "Completion Stage"],
            required=True
        ),
        "Target Date": st.column_config.DateColumn("Target Date")
    }
)

# Save Updates Button Mechanism
if st.button("💾 Save Local Matrix Updates", type="primary"):
    st.session_state.df.update(edited_df)
    st.success("Territory data pipeline successfully saved and synced!")

st.markdown("---")

# 5. Core Tactical Playbook Reference Section
st.subheader("🛡️ Product Entry Quick Guide for Meetings")
col_p1, col_p2, col_p3 = st.columns(3)

with col_p1:
    st.info("⚡ **Precast Yards / Metros**\n\nLead with **HS ProCem 9000 AB/PC**. Pitch faster mold rotation without the massive utility bills of steam curing.")

with col_p2:
    st.warning("☀️ **Civil Highway Spans**\n\nLead with **ProSuperplast RT**. Resolve setting and slump-loss issues over long transits in hot environments.")

with col_p3:
    st.success("🌊 **Deep Basements / Foundations**\n\nLead with **Hs ProCrystal 100**. Crystalline structures that resist up to 15 Bars of water pressure.")
