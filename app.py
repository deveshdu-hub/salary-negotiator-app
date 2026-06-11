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
