import streamlit as st
from PIL import Image

# Page config
st.set_page_config(
    page_title="FLEX REPORT",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to match Fluitec branding and force white background
st.markdown("""
    <style>
        /* Override Streamlit dark mode background */
        [data-testid="stAppViewContainer"],
        [data-testid="stBlock"],
        [data-testid="stSidebar"],
        [data-testid="stHeader"],
        [data-testid="stToolbar"] {
            background-color: #ffffff !important;
        }
        /* Page text and controls */
        body, .main {
            background-color: #ffffff !important;
        }
        h1 {
            color: #003366 !important;
            font-weight: 500 !important;
            text-align: center !important;
            font-size: 48px !important;
            font-family: 'Arial Narrow', sans-serif !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
        }
        label, .stTextInput label, .stSelectbox label, .stNumberInput label {
            color: #003366 !important;
            font-weight: 500 !important;
            font-family: 'Arial Narrow', sans-serif !important;
            text-transform: uppercase !important;
        }
        .stSelectbox > div, .stTextInput > div, .stNumberInput > div {
            border-color: #00A651 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Load and display logos (made a bit larger)
fluitec_logo = Image.open("fluitec_logo.png")
flex_logo   = Image.open("flexlogo.png")

logo_col1, logo_col2, logo_col3 = st.columns([1, 8, 1])
with logo_col1:
    st.image(fluitec_logo, width=250)
with logo_col3:
    st.image(flex_logo, width=250)

# Title
st.markdown("<h1>FLEX REPORT</h1>", unsafe_allow_html=True)

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
    rpvot       = st.number_input("RPVOT (%)",     min_value=0.0, max_value=200.0)
    aminic      = st.number_input("% Aminic",      min_value=0.0, max_value=100.0)
    phenolic    = st.number_input("% Phenolic",    min_value=0.0, max_value=100.0)
    delta_e     = st.number_input("MPC ΔE",        min_value=0.0, max_value=100.0)
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
st.markdown("""---
*Results section coming soon.*
""")

# Analyze button
if st.button("Analyze"):
    st.markdown("---")
    st.subheader("Results")

    # Placeholder for model output
    estimated_total_life = 20000  # replace with your actual model output
    remaining_life = max(estimated_total_life - hours_in_use, 0)

    # Percentages for rendering
    usage_pct     = (hours_in_use / estimated_total_life) * 100
    threshold_pct = 75  # marker at 75%
    deposit_pct   = min(delta_e, 100)

    # Draw two side-by-side "hot-dog" bars
    life_col, dep_col = st.columns(2)

    with life_col:
        st.markdown(f"""
            <div style="
                width: 100%; height: 20px;
                background: linear-gradient(to right, green 0%, yellow 50%, red 100%);
                border-radius: 10px; position: relative; margin-bottom: 4px;
            ">
                <div style="
                    position: absolute; left: 0;
                    width: {usage_pct}%; height: 20px;
                    background: rgba(0,0,0,0.3);
                    border-radius: 10px;
                "></div>
                <div style="
                    position: absolute; left: {threshold_pct}%;
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
                border-radius: 10px; position: relative; margin-bottom: 4px;
            ">
                <div style="
                    position: absolute; left: 0;
                    width: {deposit_pct}%; height: 20px;
                    background: rgba(0,0,0,0.3);
                    border-radius: 10px;
                "></div>
                <div style="
                    position: absolute; left: {threshold_pct}%;
                    width: 2px; height: 20px;
                    background: red;
                "></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"This oil has a **{delta_e}%** level of deposits.")
