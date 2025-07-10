import streamlit as st
from PIL import Image

# Page config
st.set_page_config(
    page_title="Flex Analysis Report",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
        body {
            background-color: #f5f5f5;
        }
        .main {
            background-color: #f5f5f5;
        }
        h1 {
            color: #003366;
            font-weight: 500;
            text-align: center;
            font-size: 48px;
            font-family: 'Arial Narrow', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        label, .stTextInput label, .stSelectbox label, .stNumberInput label {
            color: #003366 !important;
            font-weight: 500;
            font-family: 'Arial Narrow', sans-serif;
            text-transform: uppercase;
        }
        .stSelectbox > div, .stTextInput > div, .stNumberInput > div {
            border-color: #006B5F;
        }
    </style>
""", unsafe_allow_html=True)

# Load and display Fluitec logo
logo = Image.open("fluitec_logo.png")
st.image(logo, width=200)

# Title
st.markdown("<h1>Flex Analysis Report</h1>", unsafe_allow_html=True)

# Oil dropdown (unique names only)
oil_names = sorted(list(set([
    "Kluber Summit SH 32", "Castrol SN 46", "Total Preslia EVO 32", "Chevron GST Premium XL32 (2)",
    "Total Preslia GT", "Chevron GST 32", "Chevron GST Advantage EP 32", "Mobil DTE 732",
    "Mobil SHC 824", "Mobil DTE 932 GT", "Mobil SHC 832 Ultra", "Shell Turbo S4X32",
    "Shell Turbo T 32", "Infinity TO32", "Mobil DTE 732 Geared", "Castrol XEP 46",
    "Petromin Turbo 46", "Jentram Syn 46", "Shell Turbo S4 GX 32", "Turboflo XL",
    "Turboflo R&O", "Turboflo LV", "Turboflo HTS", "Fuchs Eterna 46", "Mobil DTE 832",
    "Repsol Turbo Aries Plus"
])))

# Input fields
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    rpvot = st.number_input("RPVOT (%)", min_value=0.0, max_value=200.0)
    aminic = st.number_input("% Aminic", min_value=0.0, max_value=100.0)
    phenolic = st.number_input("% Phenolic", min_value=0.0, max_value=100.0)
    delta_e = st.number_input("MPC ΔE", min_value=0.0, max_value=100.0)

with col2:
    selected_oil = st.selectbox("Oil Type", oil_names)

with col3:
    decon_added = st.selectbox("DECON Added", ["Yes", "No"])

with col4:
    hours_in_use = st.number_input("Hours in Use", min_value=0)

with col5:
    application = st.selectbox("Application", [
        "Large Gas Turbine", "Small Gas Turbine",
        "Large Steam Turbine", "Small Steam Turbine"
    ])

# Placeholder for future results section
st.markdown("""
---
*Results section coming soon.*
""")

# Analyze button
if st.button("Analyze"):
    st.markdown("---")
    st.subheader("Results")

    # Placeholder for total estimated life – this will be replaced by actual model later
    estimated_total_life = 20000  # You can replace this later with your prediction

    remaining_life = max(estimated_total_life - hours_in_use, 0)
    threshold_pct = 0.75  # 75% point in red
    usage_pct = (hours_in_use / estimated_total_life) * 100
    threshold_pos = threshold_pct * 100

    # For deposits, using ΔE as a placeholder level
    deposit_level = delta_e
    deposit_pct = min(deposit_level, 100)

    # Layout two “hot-dog” bars side by side
    life_col, dep_col = st.columns(2)

    with life_col:
        st.markdown(f"""
            <div style="
                width: 100%; height: 20px;
                background: linear-gradient(to right, green 0%, yellow 50%, red 100%);
                border-radius: 10px; position: relative;
                margin-bottom: 4px;
            ">
                <div style="
                    position: absolute; left: 0;
                    width: {usage_pct}%; height: 20px;
                    background: rgba(0,0,0,0.3);
                    border-radius: 10px;
                "></div>
                <div style="
                    position: absolute; left: {threshold_pos}%;
                    width: 2px; height: 20px;
                    background: red;
                "></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"This oil has **{remaining_life:,} hours** left of useful life.")

    with dep_col:
        st.markdown(f"""
            <div style="
                width: 100%; height: 20px;
                background: linear-gradient(to right, green 0%, yellow 50%, red 100%);
                border-radius: 10px; position: relative;
                margin-bottom: 4px;
            ">
                <div style="
                    position: absolute; left: 0;
                    width: {deposit_pct}%; height: 20px;
                    background: rgba(0,0,0,0.3);
                    border-radius: 10px;
                "></div>
                <div style="
                    position: absolute; left: {threshold_pos}%;
                    width: 2px; height: 20px;
                    background: red;
                "></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"This oil has a **{deposit_level}%** level of deposits.")
