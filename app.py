import streamlit as st
import pandas as pd
from io import BytesIO, StringIO
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import json
import base64
from typing import Dict, Any, List
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# ⚙️ PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Self Assist Core | Billionaire Orchestrator",
    page_icon="🚀",
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
    .armour-badge { background: #1a1a2e; color: #e0e0e0; padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; display: inline-block; }
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
            <h2 style="color: #1A365D; margin-top: 0; font-family: 'Segoe UI', sans-serif; text-align: center;">🚀 Billionaire Gateway</h2>
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
            "Target Date", "Win Probability (%)", "Estimated Contract Value (₹ Cr)"
        ]
        data = [
            ["PRJ-01", "Delhi-NCR", "Metro Rail", "Delhi Metro Phase IV (Golden Line)", "Upcoming", "L&T Construction", "Arjun Mehta (Procurement Head)", "DMRC Design Board", "S. Sharma (QC Manager)", "Sika India", "Underground Cut-&-Cover Tunnels", "ProHyperplast SP & HS ProCrystal 100", "Bidding stage active. Structural drawing pulled.", "Schedule technical meeting with DMRC Consultant for spec-in", "2026-07-15", 65, 12.5],
            ["PRJ-02", "Uttar Pradesh", "NHAI / Expressways", "Ganga Expressway (Phase 2 Pours)", "Ongoing", "PNC Infratech", "V. K. Singh (Project Director)", "L N Malviya Infra", "R. Chaudhary (Plant QC)", "Fosroc India", "Mass road beds & bridge decks", "ProSuperplast RT", "Trial mix requested due to slump loss complaints.", "Deliver product samples to site batching yard", "2026-06-25", 80, 8.2],
            ["PRJ-03", "Delhi-NCR", "Mega Private Projects", "DLF Cybercity Phase 2 Expansion", "Upcoming", "Tata Projects", "Rajesh Kapoor (VP Infrastructure)", "Mantec Consultants", "Amit Pal (Site In-charge)", "MC-Bauchemie", "Deep basement rafts & structural piles", "HS ProCrystal 100 & HS ProCem CI", "Blueprint finalized. Sub-surface mapped.", "Pitch crystalline integration to Mantec Lead", "2026-07-20", 50, 4.7]
        ]
        df = pd.DataFrame(data, columns=columns)
        df = convert_pipeline_dtypes(df)
        st.session_state.df = df

    # E‑commerce / CarryMe data
    if "ecommerce_orders" not in st.session_state:
        st.session_state.ecommerce_orders = pd.DataFrame([
            {"Order ID": "ORD-001", "Product": "Waterproof Backpack", "Quantity": 2, "Revenue (₹)": 1200, "Status": "Shipped", "Date": datetime(2026, 6, 15).date()},
            {"Order ID": "ORD-002", "Product": "LED Desk Lamp", "Quantity": 5, "Revenue (₹)": 2500, "Status": "Processing", "Date": datetime(2026, 6, 16).date()},
            {"Order ID": "ORD-003", "Product": "Wireless Earbuds", "Quantity": 3, "Revenue (₹)": 3000, "Status": "Delivered", "Date": datetime(2026, 6, 14).date()},
        ])
    if "ecommerce_products" not in st.session_state:
        st.session_state.ecommerce_products = pd.DataFrame([
            {"SKU": "SKU-001", "Product Name": "Waterproof Backpack", "Price (₹)": 600, "Stock": 20, "Category": "Bags"},
            {"SKU": "SKU-002", "Product Name": "LED Desk Lamp", "Price (₹)": 500, "Stock": 15, "Category": "Home"},
            {"SKU": "SKU-003", "Product Name": "Wireless Earbuds", "Price (₹)": 1000, "Stock": 8, "Category": "Electronics"},
        ])

    # Daily report log
    if "daily_logs" not in st.session_state:
        st.session_state.daily_logs = []

    # Audit trail
    if "audit_log" not in st.session_state:
        st.session_state.audit_log = []

    # Strategic Armour PIN
    if "armour_pin" not in st.session_state:
        st.session_state.armour_pin = "1234"

    # Agent settings
    if "agent_settings" not in st.session_state:
        st.session_state.agent_settings = {
            "use_llm": False,
            "llm_api_key": "",
            "llm_model": "gpt-3.5-turbo"
        }

def convert_pipeline_dtypes(df):
    df = df.copy()
    if "Target Date" in df.columns:
        df["Target Date"] = pd.to_datetime(df["Target Date"], errors="coerce").dt.date
    if "Win Probability (%)" in df.columns:
        df["Win Probability (%)"] = pd.to_numeric(df["Win Probability (%)"], errors="coerce").fillna(0).clip(0, 100).astype(int)
    allowed_stages = ["Upcoming", "Ongoing", "Completion Stage"]
    if "Lifecycle Stage" in df.columns:
        df["Lifecycle Stage"] = df["Lifecycle Stage"].apply(lambda x: x if x in allowed_stages else "Upcoming")
    if "Estimated Contract Value (₹ Cr)" in df.columns:
        df["Estimated Contract Value (₹ Cr)"] = pd.to_numeric(df["Estimated Contract Value (₹ Cr)"], errors="coerce").fillna(0)
    return df

# ==========================================
# ✨ AUTO POLISH CONDUCTOR
# ==========================================
def auto_polish_text(raw_text: str) -> str:
    if not raw_text.strip():
        return "No input provided."
    text = raw_text.strip()
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
    text = re.sub(r'(^|\.\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), text)
    if not text.endswith(('.', '!', '?')):
        text += '.'
    return text

# ==========================================
# 🛡️ STRATEGIC ARMOUR – DATA PERSISTENCE & AUDIT
# ==========================================
def save_state_to_json():
    state = {
        "df": st.session_state.df.to_dict(orient="records"),
        "ecommerce_orders": st.session_state.ecommerce_orders.to_dict(orient="records"),
        "ecommerce_products": st.session_state.ecommerce_products.to_dict(orient="records"),
        "daily_logs": st.session_state.daily_logs,
        "audit_log": st.session_state.audit_log,
        "agent_settings": st.session_state.agent_settings,
        "armour_pin": st.session_state.armour_pin
    }
    return json.dumps(state, default=str)

def load_state_from_json(json_str):
    try:
        data = json.loads(json_str)
        st.session_state.df = pd.DataFrame(data["df"])
        st.session_state.df = convert_pipeline_dtypes(st.session_state.df)
        st.session_state.ecommerce_orders = pd.DataFrame(data["ecommerce_orders"])
        st.session_state.ecommerce_products = pd.DataFrame(data["ecommerce_products"])
        st.session_state.daily_logs = data.get("daily_logs", [])
        st.session_state.audit_log = data.get("audit_log", [])
        st.session_state.agent_settings = data.get("agent_settings", st.session_state.agent_settings)
        st.session_state.armour_pin = data.get("armour_pin", "1234")
        log_audit("RESTORE", "Full state restored from JSON backup.")
        return True
    except Exception as e:
        st.error(f"Restore failed: {str(e)}")
        return False

def log_audit(action: str, details: str):
    entry = {"timestamp": datetime.now().isoformat(), "action": action, "details": details}
    st.session_state.audit_log.append(entry)

# ==========================================
# 🤖 ORCHESTRATOR AGENT – DUAL CORE (B2B + E‑COMMERCE)
# ==========================================
def strategic_advisor(df: pd.DataFrame) -> Dict[str, Any]:
    if df.empty:
        return {"recommendations": ["No B2B projects in pipeline."], "insights": {}}
    total_value = df["Estimated Contract Value (₹ Cr)"].sum()
    weighted_value = (df["Estimated Contract Value (₹ Cr)"] * df["Win Probability (%)"] / 100).sum()
    high_win = df[df["Win Probability (%)"] >= 70]
    critical_actions = df[df["Next Concrete Action Required"].notna()]
    recs = []
    if high_win.empty:
        recs.append("No high‑probability B2B projects (>70%). Focus on nurturing existing leads.")
    else:
        recs.append(f"🔑 {len(high_win)} high‑probability projects: {', '.join(high_win['Project Name'].tolist())}")
    if not critical_actions.empty:
        recs.append(f"⏰ {len(critical_actions)} projects require immediate action: {', '.join(critical_actions['Project Name'].tolist())}")
    if total_value > 0:
        recs.append(f"💰 Total B2B pipeline value: ₹{total_value:.1f} Cr, weighted: ₹{weighted_value:.1f} Cr.")
    df["Priority Score"] = (df["Win Probability (%)"] / 100) * df["Estimated Contract Value (₹ Cr)"]
    top = df.nlargest(1, "Priority Score")
    if not top.empty:
        recs.append(f"🎯 Top B2B priority: **{top.iloc[0]['Project Name']}** (score: {top.iloc[0]['Priority Score']:.2f})")
    return {"recommendations": recs, "insights": {"total_value": total_value, "weighted_value": weighted_value}}

def ecommerce_analyst(orders_df: pd.DataFrame, products_df: pd.DataFrame) -> Dict[str, Any]:
    if orders_df.empty:
        return {"recommendations": ["No e‑commerce orders yet. Start listing products!"], "insights": {}}
    total_revenue = orders_df["Revenue (₹)"].sum()
    total_orders = len(orders_df)
    avg_order_value = total_revenue / total_orders if total_orders else 0
    top_product = orders_df.groupby("Product")["Revenue (₹)"].sum().idxmax() if not orders_df.empty else "N/A"
    status_counts = orders_df["Status"].value_counts().to_dict()
    recs = []
    recs.append(f"📦 Total Orders: {total_orders}, Revenue: ₹{total_revenue:,.0f}, AOV: ₹{avg_order_value:,.0f}")
    recs.append(f"🏆 Top Product: {top_product}")
    if "Processing" in status_counts and status_counts["Processing"] > 0:
        recs.append(f"⏳ {status_counts['Processing']} orders are processing – ensure timely fulfilment.")
    if products_df is not None and not products_df.empty:
        low_stock = products_df[products_df["Stock"] < 5]
        if not low_stock.empty:
            recs.append(f"⚠️ Low stock for: {', '.join(low_stock['Product Name'].tolist())}. Reorder now.")
    return {"recommendations": recs, "insights": {"total_revenue": total_revenue, "total_orders": total_orders, "avg_order_value": avg_order_value}}

def orchestrator_agent(b2b_df: pd.DataFrame, orders_df: pd.DataFrame, products_df: pd.DataFrame) -> str:
    b2b = strategic_advisor(b2b_df)
    eco = ecommerce_analyst(orders_df, products_df)
    combined = []
    combined.append("🚀 **Billionaire Orchestrator – Daily Brief**")
    combined.append("\n## B2B Corporate Engine")
    for r in b2b["recommendations"]:
        combined.append(f"- {r}")
    combined.append("\n## E‑commerce Growth Engine")
    for r in eco["recommendations"]:
        combined.append(f"- {r}")
    return "\n".join(combined)

# ==========================================
# 🏙️ MAIN APP
# ==========================================
if check_password():
    init_session_state()

    # Header
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1A365D 0%, #2A4365 50%, #1A202C 100%); padding: 20px; border-radius: 12px; margin-bottom: 20px; border-bottom: 4px solid #3182ce;">
            <div style="float: right;"><span class="armour-badge">🚀 BILLIONAIRE ORCHESTRATOR</span></div>
            <h1 class="responsive-title" style="color: white; margin: 0; font-size: 24px;">🏗️ CORPORATE + E‑COMMERCE GROWTH SYSTEM</h1>
            <p style="color: #90CDF4; margin: 5px 0 0 0; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Berger · CarryMe · FutureHQ – Unified Command Centre</p>
        </div>
    """, unsafe_allow_html=True)

    # Tabs: Armour, Pipeline, Contact, E‑commerce, Ministry
    tab_armour, tab_pipeline, tab_intel, tab_ecommerce, tab_ministry = st.tabs([
        "🛡️ Armour & Agent",
        "📋 B2B Pipeline",
        "🔍 Contact Generator",
        "🛒 E‑commerce Growth",
        "🏛️ Ministry Console"
    ])

    # ==========================================
    # 🛡️ TAB 0 – ARMOUR & ORCHESTRATOR AGENT
    # ==========================================
    with tab_armour:
        st.subheader("🛡️ Strategic Armour – Data Security & Orchestrator")

        col_arm1, col_arm2, col_arm3 = st.columns(3)
        with col_arm1:
            if st.button("📥 Export Full State (JSON)", use_container_width=True):
                json_data = save_state_to_json()
                b64 = base64.b64encode(json_data.encode()).decode()
                href = f'<a href="data:application/json;base64,{b64}" download="orchestrator_backup_{datetime.now().strftime("%Y%m%d")}.json">Download Backup</a>'
                st.markdown(href, unsafe_allow_html=True)
                st.success("Ready to download.")
        with col_arm2:
            uploaded_backup = st.file_uploader("Restore from Backup (JSON)", type=["json"])
            if uploaded_backup is not None:
                try:
                    content = uploaded_backup.read().decode()
                    pin = st.text_input("Enter Armour PIN", type="password", key="restore_pin")
                    if st.button("Restore State", use_container_width=True):
                        if pin == st.session_state.armour_pin:
                            if load_state_from_json(content):
                                st.success("✅ State restored!")
                                st.rerun()
                            else:
                                st.error("Restore failed.")
                        else:
                            st.error("❌ Incorrect PIN.")
                except Exception as e:
                    st.error(f"Error reading file: {e}")
        with col_arm3:
            st.metric("Audit Trail Entries", len(st.session_state.audit_log))

        with st.expander("📋 Audit Log (last 50)"):
            if st.session_state.audit_log:
                audit_df = pd.DataFrame(st.session_state.audit_log[-50:])
                st.dataframe(audit_df, use_container_width=True)
            else:
                st.info("No audit entries yet.")

        st.markdown("---")
        st.subheader("🤖 Billionaire Orchestrator Agent – Daily Brief")
        if st.button("🚀 Generate Orchestrator Brief", use_container_width=True):
            with st.spinner("Synthesising B2B + E‑commerce..."):
                brief = orchestrator_agent(
                    st.session_state.df,
                    st.session_state.ecommerce_orders,
                    st.session_state.ecommerce_products
                )
                st.code(brief, language="text")
                log_audit("ORCHESTRATOR", "Orchestrator brief generated.")

        with st.expander("⚙️ Agent Settings (Optional LLM)"):
            use_llm = st.checkbox("Enable LLM (OpenAI)", value=st.session_state.agent_settings["use_llm"])
            if use_llm:
                api_key = st.text_input("API Key", type="password", value=st.session_state.agent_settings["llm_api_key"])
                model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4"], index=0)
                st.session_state.agent_settings.update({"use_llm": True, "llm_api_key": api_key, "llm_model": model})
                st.info("LLM will enhance agent outputs.")
            else:
                st.session_state.agent_settings["use_llm"] = False
                st.info("Using rule‑based agents (no API).")

        with st.expander("🔐 Change Armour PIN"):
            old = st.text_input("Current PIN", type="password")
            new = st.text_input("New PIN (4 digits)", type="password")
            if st.button("Update PIN"):
                if old == st.session_state.armour_pin and len(new) == 4 and new.isdigit():
                    st.session_state.armour_pin = new
                    log_audit("PIN_CHANGE", "PIN updated.")
                    st.success("PIN updated!")
                else:
                    st.error("Invalid current PIN or new PIN format.")

    # ==========================================
    # TAB 1 – B2B PIPELINE (unchanged)
    # ==========================================
    with tab_pipeline:
        st.subheader("🔄 B2B Pipeline – Excel Sync & Management")
        uploaded_file = st.file_uploader("Upload client sheet (.xlsx/.xls):", type=["xlsx", "xls"])
        if uploaded_file is not None:
            try:
                incoming_df = pd.read_excel(uploaded_file)
                if "Project ID" in incoming_df.columns:
                    if st.button("⚡ Sync & Merge"):
                        incoming_df = convert_pipeline_dtypes(incoming_df)
                        st.session_state.df = st.session_state.df.set_index("Project ID")
                        incoming_df = incoming_df.set_index("Project ID")
                        st.session_state.df.update(incoming_df)
                        new_rows = incoming_df[~incoming_df.index.isin(st.session_state.df.index)]
                        st.session_state.df = pd.concat([st.session_state.df, new_rows])
                        st.session_state.df.reset_index(inplace=True)
                        st.session_state.df = convert_pipeline_dtypes(st.session_state.df)
                        log_audit("SYNC", f"B2B sync: {len(new_rows)} new rows.")
                        st.success("✅ Pipeline updated.")
                else:
                    st.error("Missing 'Project ID' column.")
            except Exception as e:
                st.error(f"Sync failed: {str(e)}")

        available_states = st.session_state.df["State / Hub"].unique()
        selected_states = st.sidebar.multiselect("Filter by State / Hub", options=available_states, default=available_states)
        filtered_df = st.session_state.df[st.session_state.df["State / Hub"].isin(selected_states)].copy()
        filtered_df = convert_pipeline_dtypes(filtered_df)

        st.subheader("📋 Active B2B Pipeline")
        column_config = {
            "Win Probability (%)": st.column_config.ProgressColumn("Win %", format="%d%%", min_value=0, max_value=100),
            "Lifecycle Stage": st.column_config.SelectboxColumn("Stage", options=["Upcoming", "Ongoing", "Completion Stage"], required=True),
            "Target Date": st.column_config.DateColumn("Target Date", format="YYYY-MM-DD"),
            "Estimated Contract Value (₹ Cr)": st.column_config.NumberColumn("Value (₹ Cr)", min_value=0, step=0.1, format="%.1f")
        }
        try:
            edited_df = st.data_editor(filtered_df, use_container_width=True, num_rows="dynamic", key="pipeline_editor", column_config=column_config)
        except Exception:
            edited_df = st.data_editor(filtered_df, use_container_width=True, num_rows="dynamic", key="pipeline_editor_fallback")

        col_save, col_export = st.columns([1, 4])
        with col_save:
            if st.button("💾 Save Updates", type="primary"):
                try:
                    st.session_state.df = st.session_state.df.set_index("Project ID")
                    edited_df = edited_df.set_index("Project ID")
                    st.session_state.df.update(edited_df)
                    new_rows = edited_df[~edited_df.index.isin(st.session_state.df.index)]
                    st.session_state.df = pd.concat([st.session_state.df, new_rows])
                    st.session_state.df.reset_index(inplace=True)
                    st.session_state.df = convert_pipeline_dtypes(st.session_state.df)
                    log_audit("EDIT", "B2B pipeline manual update.")
                    st.success("Saved!")
                except Exception as e:
                    st.error(f"Save error: {str(e)}")
        with col_export:
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                edited_df.reset_index().to_excel(writer, index=False, sheet_name="B2B_Pipeline")
            st.download_button("📥 Export to Excel", data=output.getvalue(), file_name=f"B2B_Pipeline_{datetime.now().strftime('%Y%m%d')}.xlsx")

    # ==========================================
    # TAB 2 – CONTACT GENERATOR (unchanged)
    # ==========================================
    with tab_intel:
        st.subheader("🎯 B2B Contact Finder")
        col_name, col_company = st.columns(2)
        with col_name:
            input_name = st.text_input("Executive Name:", placeholder="e.g., Souvik Sengupta")
        with col_company:
            input_company = st.text_input("Company Name:", placeholder="e.g., Infra Market")

        if st.button("🔍 Generate Contact", type="primary"):
            if not input_name or not input_company:
                st.error("Fill both fields.")
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
                        notes = "Infra.Market / RDC Concrete"
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
                        notes = "Larsen & Toubro"
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
                    st.success(f"### 🎯 Match for **{input_company.upper()}**")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"<div style='background:#f0fdf4; padding:15px; border-radius:10px; border-left:4px solid #16a34a;'><strong>📁 Executive:</strong> {input_name.title()}<br><strong>🏢 Company:</strong> {input_company.title()}<br><strong>🌐 Domain:</strong> <code>{domain}</code><br><strong>⚙️ Format:</strong> <code>{fmt}</code></div>", unsafe_allow_html=True)
                    with col_b:
                        st.markdown(f"<div style='background:#f8fafc; padding:15px; border-radius:10px; border-left:4px solid #475569;'><strong>📧 Email:</strong> <code>{email}</code><br><strong>📞 Switchboard:</strong> {switch}<br><em style='font-size:12px;'>{notes}</em></div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # ==========================================
    # 🛒 TAB 3 – E‑COMMERCE GROWTH ENGINE (NEW)
    # ==========================================
    with tab_ecommerce:
        st.subheader("🛒 E‑commerce Growth Engine – CarryMe Operations")

        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        orders = st.session_state.ecommerce_orders
        products = st.session_state.ecommerce_products
        total_revenue = orders["Revenue (₹)"].sum() if not orders.empty else 0
        total_orders = len(orders)
        avg_order = total_revenue / total_orders if total_orders else 0
        unique_products = products["Product Name"].nunique() if not products.empty else 0
        with col1:
            st.metric("Total Revenue", f"₹{total_revenue:,.0f}")
        with col2:
            st.metric("Total Orders", total_orders)
        with col3:
            st.metric("Average Order Value", f"₹{avg_order:,.0f}")
        with col4:
            st.metric("Products Listed", unique_products)

        st.markdown("---")
        st.subheader("📦 Order Management")
        edited_orders = st.data_editor(
            orders,
            use_container_width=True,
            num_rows="dynamic",
            key="orders_editor",
            column_config={
                "Date": st.column_config.DateColumn("Date"),
                "Status": st.column_config.SelectboxColumn("Status", options=["Processing", "Shipped", "Delivered", "Cancelled"]),
                "Revenue (₹)": st.column_config.NumberColumn("Revenue (₹)", min_value=0, step=50)
            }
        )
        if st.button("💾 Save Orders", type="primary"):
            st.session_state.ecommerce_orders = edited_orders
            log_audit("EDIT", "E‑commerce orders updated.")
            st.success("Orders saved!")

        st.markdown("---")
        st.subheader("🏷️ Product Catalog")
        edited_products = st.data_editor(
            products,
            use_container_width=True,
            num_rows="dynamic",
            key="products_editor",
            column_config={
                "Price (₹)": st.column_config.NumberColumn("Price (₹)", min_value=0, step=10),
                "Stock": st.column_config.NumberColumn("Stock", min_value=0, step=1)
            }
        )
        if st.button("💾 Save Products"):
            st.session_state.ecommerce_products = edited_products
            log_audit("EDIT", "Product catalog updated.")
            st.success("Products saved!")

        st.markdown("---")
        st.subheader("📈 Revenue Analytics")
        if not orders.empty:
            # Daily revenue chart
            daily_rev = orders.groupby("Date")["Revenue (₹)"].sum().reset_index()
            fig = px.line(daily_rev, x="Date", y="Revenue (₹)", title="Daily Revenue Trend", markers=True)
            st.plotly_chart(fig, use_container_width=True)

            # Revenue by product
            prod_rev = orders.groupby("Product")["Revenue (₹)"].sum().reset_index()
            fig2 = px.bar(prod_rev, x="Product", y="Revenue (₹)", title="Revenue by Product")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No orders yet to display analytics.")

        # Growth recommendations from agent (e-commerce specific)
        st.markdown("---")
        st.subheader("🚀 E‑commerce Growth Recommendations")
        eco_insights = ecommerce_analyst(orders, products)
        for rec in eco_insights["recommendations"]:
            st.info(rec)

    # ==========================================
    # TAB 4 – MINISTRY CONSOLE (unchanged but with e‑commerce integration)
    # ==========================================
    with tab_ministry:
        st.subheader("🏛️ Investor Ministry Console – Goal: ₹1,00,000/month")
        # Show combined metrics
        total_rev = orders["Revenue (₹)"].sum() if not orders.empty else 0
        b2b_value = st.session_state.df["Estimated Contract Value (₹ Cr)"].sum() * 1e7  # convert Cr to ₹
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("B2B Pipeline Value (₹ Cr)", f"{st.session_state.df['Estimated Contract Value (₹ Cr)'].sum():.1f}")
        with col2:
            st.metric("E‑commerce Revenue (₹)", f"{total_rev:,.0f}")
        with col3:
            st.metric("Combined Potential", f"₹{total_rev + b2b_value:,.0f}")

        st.markdown("---")
        st.markdown("### 🕒 24‑Hour Schedule Matrix")
        schedule = pd.DataFrame([
            {"Time": "06:00 – 09:00", "Focus": "🧠 DEEP ASSET CREATION", "Tasks": "Build features, refine systems."},
            {"Time": "09:00 – 10:00", "Focus": "🥪 LOGISTICS CONTROL", "Tasks": "Fulfill orders, pack, label."},
            {"Time": "10:00 – 13:00", "Focus": "📈 CATALOG SCALE", "Tasks": "Bulk upload new products, optimise listings."},
            {"Time": "14:00 – 17:00", "Focus": "🎯 TRAFFIC FUNNEL", "Tasks": "Marketing, bio‑links, reels."},
            {"Time": "17:00 – 19:00", "Focus": "🤝 HIGH‑TICKET OUTREACH", "Tasks": "Pitch B2B and digital services."}
        ])
        st.dataframe(schedule, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### 📝 Daily Evening Report")
        with st.form("daily_report"):
            report_date = st.date_input("Date", datetime.now())
            fh_views = st.number_input("FutureHQ Views", min_value=0, step=100)
            fh_clicks = st.number_input("Bio‑Link Clicks", min_value=0, step=1)
            cm_catalogs = st.number_input("New Catalog Uploads", min_value=0, step=1)
            cm_orders = st.number_input("New Orders", min_value=0, step=1)
            revenue = st.number_input("Revenue Locked (₹)", min_value=0, step=50)
            bottleneck = st.text_area("Bottleneck today")
            submitted = st.form_submit_button("📊 Compile Report")

        if submitted:
            polished = auto_polish_text(bottleneck)
            report_text = f"""
### 📊 DAILY RESULTS – {report_date.strftime('%d-%m-%Y')}
#### 1. ASSET ENGINE
- Instagram Views: {fh_views}
- Bio‑Link Clicks: {fh_clicks}

#### 2. MARKETPLACE
- New Catalogs: {cm_catalogs}
- New Orders: {cm_orders}

#### 3. MONETIZATION
- Revenue Locked: ₹{revenue}

#### 4. BOTTLENECK
- Raw: {bottleneck if bottleneck.strip() else "None"}
- Polished: {polished}
            """
            st.success("✅ Report ready – copy for audit")
            st.code(report_text, language="text")
            st.session_state.daily_logs.append({"date": report_date, "report": report_text})
            log_audit("REPORT", f"Daily report for {report_date}")

        # Auto‑Polish standalone
        st.markdown("---")
        st.subheader("✨ Auto‑Polish Conductor")
        raw = st.text_area("Paste raw note", height=80)
        if st.button("Polish"):
            if raw.strip():
                st.code(auto_polish_text(raw), language="text")
            else:
                st.warning("Enter text.")

    # ==========================================
    # SIDEBAR – GOV SEARCH + CODE SHARING
    # ==========================================
    st.sidebar.markdown("---")
    st.sidebar.header("🌐 Govt Infrastructure Search")
    search = st.sidebar.text_input("Search term", placeholder="e.g., Delhi Metro")
    if search:
        try:
            url = f"https://html.duckduckgo.com/html/?q={search.replace(' ', '+')}+site:gov.in"
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
                    st.sidebar.warning("No results.")
            else:
                st.sidebar.warning("Search unavailable.")
        except Exception:
            st.sidebar.markdown(f"[🔍 Fallback Google Search](https://www.google.com/search?q={search.replace(' ', '+')}+site:gov.in)")

    st.sidebar.markdown("---")
    st.sidebar.header("📦 Code‑Sharing")
    if st.sidebar.button("📥 Download app.py"):
        try:
            with open(__file__, "r", encoding="utf-8") as f:
                code = f.read()
            st.sidebar.download_button("⬇️ Save app.py", data=code, file_name="orchestrator_app.py", mime="text/x-python", use_container_width=True)
            st.sidebar.success("Ready!")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

    if st.sidebar.button("🔐 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

    st.markdown("---")
    st.caption("🚀 Self Assist Core v5.0 | Billionaire Orchestrator | Berger · CarryMe · FutureHQ")
