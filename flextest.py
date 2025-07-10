import streamlit as st
from PIL import Image

# Page config
st.set_page_config(
    page_title="FLEX REPORT",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS: darker background, dark-blue text, larger logos, title moved up
st.markdown("""
    <style>
        /* Darker page background and text color override */
        [data-testid="stAppViewContainer"],
        [data-testid="stBlock"],
        [data-testid="stSidebar"],
        [data-testid="stHeader"],
        [data-testid="stToolbar"] {
            background-color: #e8e8e8 !important;
            color: #003366 !important;
        }
        /* Ensure body text is dark blue */
        body, .main, .css-1d391kg, .css-1dp5vir, .css-1v3fvcr {
            color: #003366 !important;
        }
        /* Tweak headings */
        h1 {
            color: #003366 !important;
            margin-top: -20px !important;
            margin-bottom: 10px !important;
            font-family: 'Arial Narrow', sans-serif !important;
        }
        /* Style input labels */
        label, .stTextInput label, .stSelectbox label, .stNumberInput label {
            color: #003366 !important;
            font-weight: 500 !important;
            font-family: 'Arial Narrow', sans-serif !important;
            text-transform: uppercase !important;
        }
        /* Green accent on input boxes */
        .stSelectbox > div, .stTextInput > div, .stNumberInput > div {
            border-color: #00A651 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Load logos
fluitec_logo = Image.open("fluitec_logo.png")
flex_logo   = Image.open("flexlogo.png")

# Display logos larger and title moved up
logo_col1, logo_col2, logo_col3 = st.columns([1, 6, 1])
with logo_col1:
    st.image(fluitec_logo, width=300)
with logo_col3:
    st.image(flex_logo, width=300)

# Page title
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

# Analyze button and results
if st.button("Analyze"):
    st.markdown("---")
    st.subheader("Results")

    # Placeholder model output
    estimated_total_life = 20000
    remaining_life = max(estimated_total_life - hours_in_use, 0)

    # Percentages for rendering
    usage_pct     = (hours_in_use / estimated_total_life) * 100
    threshold_pct = 75  # 75% marker
    deposit_pct   = min(delta_e, 100)

    # Two hot-dog bars side by side
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
