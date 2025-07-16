import streamlit as st
from PIL import Image
import math

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Flex Analysis Report",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
        body, .main {
            background-color: #e6e6e6;
        }
        h1 {
            color: #003366;
            font-weight: 500;
            text-align: center;
            font-size: 48px;
            font-family: 'Arial Narrow', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: -40px;
        }
        label, .stTextInput label, .stSelectbox label, .stNumberInput label {
            color: #003366 !important;
            font-weight: 500;
            font-family: 'Arial Narrow', sans-serif;
            text-transform: uppercase;
        }
    </style>
""", unsafe_allow_html=True)

# --- LOGOS ---
col_logo1, col_logo2, col_logo3 = st.columns([1, 6, 1])
with col_logo1:
    st.image("flexlogo.png", width=160)
with col_logo2:
    st.markdown("<h1>Flex Analysis Report</h1>", unsafe_allow_html=True)
with col_logo3:
    st.image("fluitec_logo.png", width=140)

# --- MODEL OPTIONS ---
model_options = {
    "Siemens Energy": {
        "Gas Turbine": ["SGT-100", "SGT-200", "SGT-300", "SGT-400", "SGT-500", "SGT-600", "SGT-700", "SGT-750", "SGT-800", "SGT-900"],
        "Steam Turbine": ["SST-100", "SST-200", "SST-300", "SST-400", "SST-500", "SST-600", "SST-800", "SST-900", "SST-5000"]
    },
    "Mitsubishi": {
        "Gas Turbine": ["H-25", "H-50", "M501D", "M501F", "M501G", "M501J", "M501JAC (air-cooled)"],
        "Steam Turbine": ["TC-series", "MF-series", "Tandem-compound axial-flow (various)", "Nuclear TC4F"]
    },
    "General Electric": {
        "Gas Turbine": ["Frame 5 (5E)", "Frame 6 (6B/6F)", "Frame 7E", "rame 7F", "Frame 7HA.01", "Frame 7HA.02", "Frame 9F", "Frame 9HA"],
        "Steam Turbine": ["D-series", "E-series", "A-series", "Tandem-compound axial flow"]
    },
    "Solar Turbines": {
        "Gas Turbine": ["Saturn 20", "Centaur 40", "Centaur 50", "Taurus 60", "Taurus 70", "Mars 90", "Mars 100", "Titan 130", "Titan 250"],
        "Steam Turbine": []
    }
}

# --- FORMULAS ---

rpvot_funcs = {
    "Castrol SN 46": lambda h: 91.2239183452624 - 30,
    "Castrol XEP 46": lambda h: max(87.88136 * math.exp(-0.00075575 * h), 0),
    "Chevron GST 32": lambda h: 89.390543491572 - 40,
    "Chevron GST Advantage EP 32": lambda h: max(102.73982 * math.exp(-0.0002572 * h), 0),
    "Chevron GST Premium XL32 (2)": lambda h: max(102.98036 * math.exp(-0.00034336 * h), 0),
    "Fuchs Eterna 46": lambda h: max(93.06849 * math.exp(-0.00054818 * h), 0),
    "Infinity TO32": lambda h: max(107.27841 * math.exp(-0.00039224 * h), 0),
    "Jentram Syn 46": lambda h: max(102.00911 * math.exp(-0.00080471 * h), 0),
    "Kluber Summit SH 32": lambda h: max(90.81009 * math.exp(-0.00044569 * h), 0),
    "Mobil DTE 732": lambda h: max(108.81924 * math.exp(-0.00037696 * h), 0),
    "Mobil DTE 732 Geared": lambda h: max(105.82153 * math.exp(-0.00024602 * h), 0),
    "Mobil DTE 832": lambda h: 6.32217964186245 + 25,
    "Mobil DTE 932 GT": lambda h: max(90.54567 * math.exp(-0.00014641 * h), 0),
    "Mobil SHC 824": lambda h: max(95.89441 * math.exp(-0.00009471 * h), 0),
    "Mobil SHC 832 Ultra": lambda h: max(101.24346 * math.exp(-0.00016257 * h), 0),
    "Petromin Turbo 46": lambda h: max(97.69654 * math.exp(-0.00064843 * h), 0),
    "Repsol Turbo Aries Plus": lambda h: max(96.25161 * math.exp(-0.00040146 * h), 0),
    "Shell Turbo S4 GX 32": lambda h: max(91.33195 * math.exp(-0.00025352 * h), 0),
    "Shell Turbo S4X32": lambda h: max(91.06849 * math.exp(-0.0002014 * h), 0),
    "Shell Turbo T 32": lambda h: max(104.55415 * math.exp(-0.00049444 * h), 0),
    "Total Preslia EVO 32": lambda h: 13.7425815554628 + 50,
    "Total Preslia GT": lambda h: 96.33903 - 40,
    "Turboflo HTS": lambda h: max(101.64971 * math.exp(-0.00028872 * h), 0),
    "Turboflo LV": lambda h: max(100.67579 * math.exp(-0.00067692 * h), 0),
    "Turboflo R&O": lambda h: max(91.84005 * math.exp(-0.00106696 * h), 0),
    "Turboflo XL": lambda h: max(109.69558 * math.exp(-0.00017808 * h), 0),
}

aminic_funcs = {
    "Castrol SN 46": lambda h: max(105.08543 * math.exp(-0.0003269 * h), 0),
    "Castrol XEP 46": lambda h: max(97.02338 * math.exp(-0.00078991 * h), 0),
    "Chevron GST Advantage EP 32": lambda h: max(108.42032 * math.exp(-0.00037097 * h), 0),
    "Chevron GST Premium XL32 (2)": lambda h: max(94.28367 * math.exp(-0.00072707 * h), 0),
    "Fuchs Eterna 46": lambda h: max(105.8678 * math.exp(-0.00048179 * h), 0),
    "Infinity TO32": lambda h: max(104.32032 * math.exp(-0.00027361 * h), 0),
    "Jentram Syn 46": lambda h: max(106.62101 * math.exp(-0.00047731 * h), 0),
    "Kluber Summit SH 32": lambda h: max(102.31298 * math.exp(-0.0002616 * h), 0),
    "Mobil DTE 732": lambda h: max(107.40819 * math.exp(-0.00091084 * h), 0),
    "Mobil DTE 732 Geared": lambda h: max(107.72234 * math.exp(-0.0004424 * h), 0),
    "Mobil DTE 832": lambda h: max(102.39014 * math.exp(-0.00025732 * h), 0),
    "Mobil DTE 932 GT": lambda h: max(108.19652 * math.exp(-0.000536 * h), 0),
    "Mobil SHC 824": lambda h: max(99.96255 * math.exp(-0.00009784 * h), 0),
    "Mobil SHC 832 Ultra": lambda h: max(99.76654 * math.exp(-0.00021702 * h), 0),
    "Petromin Turbo 46": lambda h: max(102.68657 * math.exp(-0.00043107 * h), 0),
    "Repsol Turbo Aries Plus": lambda h: max(103.23661 * math.exp(-0.00025331 * h), 0),
    "Shell Turbo S4 GX 32": lambda h: max(108.37683 * math.exp(-0.00048742 * h), 0),
    "Shell Turbo S4X32": lambda h: max(95.59583 * math.exp(-0.00056219 * h), 0),
    "Shell Turbo T 32": lambda h: max(111.29316 * math.exp(-0.00062519 * h), 0),
    "Total Preslia EVO 32": lambda h: max(98.24761 * math.exp(-0.0000581 * h), 0),
    "Total Preslia GT": lambda h: 101.12 - 20,
    "Turboflo HTS": lambda h: max(104.32293 * math.exp(-0.00067565 * h), 0),
    "Turboflo LV": lambda h: max(106.73885 * math.exp(-0.00108233 * h), 0),
    "Turboflo R&O": lambda h: max(91.93054 * math.exp(-0.00058039 * h), 0),
    "Turboflo XL": lambda h: max(99.41411 * math.exp(-0.00017067 * h), 0),
}

# --- INPUT COLUMNS ---
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    rpvot = st.number_input("RPVOT (%)", min_value=0.0, max_value=200.0)
    aminic = st.number_input("% Aminic", min_value=0.0, max_value=100.0)
    phenolic = st.number_input("% Phenolic", min_value=0.0, max_value=100.0)
    delta_e = st.number_input("MPC ΔE", min_value=0.0, max_value=100.0)

with col2:
    selected_oil = st.selectbox("Oil Type", sorted(rpvot_funcs.keys()))

with col3:
    decon_added = st.selectbox("DECON Added", ["Yes", "No"])

with col4:
    hours_in_use = st.number_input("Hours in Use", min_value=0)

with col5:
    app_type = st.selectbox("Application Type", ["Gas Turbine", "Steam Turbine"])
    model_brand = st.selectbox("Model Brand", list(model_options.keys()))
    model_name = st.selectbox("Model", model_options[model_brand][app_type])

# --- REMAINING LIFE FUNCTION ---
def find_remaining_life(h0, r_fn, a_fn):
    def avg_pct(h):
        r = r_fn(h)
        a = a_fn(h) if a_fn else r
        return (r + a) / 2

    if avg_pct(h0) <= 25:
        return 0

    low, high = h0, h0 + 1
    while avg_pct(high) > 25:
        high *= 2
        if high > 1e6:
            return None

    for _ in range(50):
        mid = (low + high) / 2
        if avg_pct(mid) > 25:
            low = mid
        else:
            high = mid
    return high - h0

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

    st.markdown(f"""
        <div style="width:100%;height:20px;background:linear-gradient(to right, green, yellow, red);border-radius:10px;position:relative;">
            <div style="position:absolute;left:0;width:{usage_pct:.2f}%;height:20px;background:rgba(0,0,0,0.3);border-radius:10px;"></div>
            <div style="position:absolute;left:100%;width:2px;height:20px;background:red;"></div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"This oil has **{remaining:.0f} hours** left of useful life.")
