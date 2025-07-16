import streamlit as st
from PIL import Image
import math

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Flex Analysis Report",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS ---
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
        .logo-container {
            position: absolute;
            top: 10px;
            right: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- LOAD LOGOS ---
st.markdown('<div class="logo-container"><img src="data:image/png;base64,' + 
            Image.open("flexlogo.png").resize((150, 150))._repr_png_().decode("utf-8") + 
            '" width="120"></div>', unsafe_allow_html=True)

# --- TITLE ---
st.markdown("<h1>Flex Analysis Report</h1>", unsafe_allow_html=True)

# --- MODEL OPTIONS ---
model_options = {
    "Siemens Energy": {
        "Gas Turbine": [
            "SGT-100", "SGT-200", "SGT-300", "SGT-400", "SGT-500", "SGT-600",
            "SGT-700", "SGT-750", "SGT-800", "SGT-900"
        ],
        "Steam Turbine": [
            "SST-100", "SST-200", "SST-300", "SST-400", "SST-500", "SST-600",
            "SST-800", "SST-900", "SST-5000"
        ]
    },
    "Mitsubishi": {
        "Gas Turbine": [
            "H-25", "H-50", "M501D", "M501F", "M501G", "M501J", "M501JAC (air-cooled)"
        ],
        "Steam Turbine": [
            "TC-series", "MF-series", "Tandem-compound axial-flow (various)", "Nuclear TC4F"
        ]
    },
    "General Electric": {
        "Gas Turbine": [
            "Frame 5 (5E)", "Frame 6 (6B/6F)", "Frame 7E", "rame 7F", "Frame 7HA.01",
            "Frame 7HA.02", "Frame 9F", "Frame 9HA"
        ],
        "Steam Turbine": [
            "D-series", "E-series", "A-series", "Tandem-compound axial flow"
        ]
    },
    "Solar Turbines": {
        "Gas Turbine": [
            "Saturn 20", "Centaur 40", "Centaur 50", "Taurus 60", "Taurus 70",
            "Mars 90", "Mars 100", "Titan 130", "Titan 250"
        ],
        "Steam Turbine": []
    }
}

# --- OIL NAMES ---
oil_names = sorted([
    "Kluber Summit SH 32", "Castrol SN 46", "Total Preslia EVO 32", "Chevron GST Premium XL32 (2)",
    "Total Preslia GT", "Chevron GST 32", "Chevron GST Advantage EP 32", "Mobil DTE 732",
    "Mobil SHC 824", "Mobil DTE 932 GT", "Mobil SHC 832 Ultra", "Shell Turbo S4X32",
    "Shell Turbo T 32", "Infinity TO32", "Mobil DTE 732 Geared", "Castrol XEP 46",
    "Petromin Turbo 46", "Jentram Syn 46", "Shell Turbo S4 GX 32", "Turboflo XL",
    "Turboflo R&O", "Turboflo LV", "Turboflo HTS", "Fuchs Eterna 46", "Mobil DTE 832",
    "Repsol Turbo Aries Plus"
])

# --- INPUT COLUMNS ---
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
    selected_oem = st.selectbox("OEM", list(model_options.keys()))
    selected_app = st.selectbox("Application", list(model_options[selected_oem].keys()))
    model_list = model_options[selected_oem][selected_app]
    selected_model = st.selectbox("Model", model_list if model_list else ["N/A"])

# --- FORMULAS ---
# (Include rpvot_funcs, aminic_funcs, and find_remaining_life function exactly as you have it.)

# --- ANALYZE BUTTON ---
if st.button("Analyze"):
    st.markdown("---")
    st.subheader("Results")

    r_fn = rpvot_funcs[selected_oil]
    a_fn = aminic_funcs.get(selected_oil, None)

    r_val = r_fn(hours_in_use)
    a_val = a_fn(hours_in_use) if a_fn else r_val

    remaining = find_remaining_life(hours_in_use, r_fn, a_fn)
    remaining = remaining if remaining is not None else 0
    total = hours_in_use + remaining
    usage_pct = (hours_in_use / total) * 100 if total else 100

    # --- HOT DOG BAR ---
    st.markdown(f"""
        <div style="width:100%;height:20px;background:linear-gradient(to right, green, yellow, red);border-radius:10px;position:relative;">
            <div style="position:absolute;left:0;width:{usage_pct:.2f}%;height:20px;background:rgba(0,0,0,0.3);border-radius:10px;"></div>
            <div style="position:absolute;left:100%;width:2px;height:20px;background:red;"></div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"This oil has **{remaining:.0f} hours** left of useful life.")
