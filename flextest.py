
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

    st.markdown("**Remaining Useful Life**")

    st.slider(
        label="",
        min_value=0,
        max_value=int(estimated_total_life),
        value=int(hours_in_use),
        step=1,
        disabled=True,
        help=f"{remaining_life} hours remaining out of {estimated_total_life} total"
    )

    st.caption(f"{remaining_life} hours remaining out of {estimated_total_life}")

