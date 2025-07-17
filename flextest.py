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
st.markdown("""
    <style>
        .custom-title {
            color: #002f5f !important;  /* dark blue override */
            font-size: 20px;
            font-weight: 200;
            text-align: center;
            font-family: 'Arial Narrow', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: -30px;
        }
    </style>
""", unsafe_allow_html=True)

from PIL import Image

# --- Open and upscale manually ---
logo1 = Image.open("flexlogo.png")
logo1 = logo1.resize((400, int(logo1.height * (400 / logo1.width))))  # Resize proportionally

logo2 = Image.open("fluitec_logo.png")
logo2 = logo2.resize((240, int(logo2.height * (240 / logo2.width))))

# --- Layout ---
col_logo1, col_logo2, col_logo3 = st.columns([1, 6, 1])

with col_logo1:
    st.image(logo1)

with col_logo2:
    st.markdown('<h1 class="custom-title">Flex Analysis Report</h1>', unsafe_allow_html=True)

with col_logo3:
    st.image(logo2)


# --- MODEL OPTIONS + TSI VALUES ---
model_options = {
    "Siemens Energy": {
        "Gas Turbine": {"SGT-100": 0.60, "SGT-200": 0.67, "SGT-300": 0.74, "SGT-400": 0.82, "SGT-500": 1.00,
                        "SGT-600": 1.23, "SGT-700": 1.50, "SGT-750": 1.83, "SGT-800": 2.22, "SGT-900": 2.69},
        "Steam Turbine": {"SST-100": 0.35, "SST-200": 0.44, "SST-300": 0.54, "SST-400": 0.67,
                          "SST-500": 0.35, "SST-600": 0.39, "SST-800": 0.35, "SST-900": 0.35, "SST-5000": 0.35}
    },
    "Mitsubishi": {
        "Gas Turbine": {"H-25": 1.00, "H-50": 1.11, "M501D": 1.00, "M501F": 1.23, "M501G": 1.50,
                        "M501J": 1.83, "M501JAC (air-cooled)": 2.22},
        "Steam Turbine": {"TC-series": 0.35, "MF-series": 0.44,
                          "Tandem-compound axial-flow (various)": 0.35, "Nuclear TC4F": 0.44}
    },
    "General Electric": {
        "Gas Turbine": {"Frame 5 (5E)": 1.00, "Frame 6 (6B/6F)": 1.23, "Frame 7E": 1.50, "rame 7F": 1.00,
                        "Frame 7HA.01": 1.23, "Frame 7HA.02": 1.50, "Frame 9F": 1.83, "Frame 9HA": 2.22},
        "Steam Turbine": {"D-series": 0.35, "E-series": 0.44, "A-series": 0.54, "Tandem-compound axial flow": 0.60}
    },
    "Solar Turbines": {
        "Gas Turbine": {"Saturn 20": 1.00, "Centaur 40": 1.23, "Centaur 50": 1.50, "Taurus 60": 1.83,
                        "Taurus 70": 2.22, "Mars 90": 2.69, "Mars 100": 3.26, "Titan 130": 3.93, "Titan 250": 4.73},
        "Steam Turbine": {}
    }
}

# --- OIL DEGRADATION CONSTANTS ---
oil_constants = {
    "Castrol SN 46": (0.0012, 0.00038),
    "Castrol XEP 46": (0.00075575, 0.00078991),
    "Chevron GST 32": (0.0, 0.0005),
    "Chevron GST Advantage EP 32": (0.0002572, 0.00037097),
    "Chevron GST Premium XL32 (2)": (0.00034336, 0.00072707),
    "Fuchs Eterna 46": (0.00054818, 0.00048179),
    "Infinity TO32": (0.00039224, 0.00027361),
    "Jentram Syn 46": (0.00080471, 0.00047731),
    "Kluber Summit SH 32": (0.00044569, 0.0002616),
    "Mobil DTE 732": (0.00037696, 0.00091084),
    "Mobil DTE 732 Geared": (0.00024602, 0.0004424),
    "Mobil DTE 832": (0.0, 0.00025732),
    "Mobil DTE 932 GT": (0.00014641, 0.000536),
    "Mobil SHC 824": (0.00009471, 0.00009784),
    "Mobil SHC 832 Ultra": (0.00016257, 0.00021702),
    "Petromin Turbo 46": (0.00064843, 0.00043107),
    "Repsol Turbo Aries Plus": (0.00040146, 0.00025331),
    "Shell Turbo S4 GX 32": (0.00025352, 0.00048742),
    "Shell Turbo S4X32": (0.0002014, 0.00056219),
    "Shell Turbo T 32": (0.00049444, 0.00062519),
    "Total Preslia EVO 32": (0.0, 0.0000581),
    "Total Preslia GT": (0.0, 0.0),
    "Turboflo HTS": (0.00028872, 0.00067565),
    "Turboflo LV": (0.00067692, 0.00108233),
    "Turboflo R&O": (0.00106696, 0.00058039),
    "Turboflo XL": (0.00017808, 0.00017067)
}

# --- USER INPUT ---
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    rpvot_input = st.number_input("RPVOT (%)", min_value=0.0, max_value=200.0)
    aminic_input = st.number_input("% Aminic", min_value=0.0, max_value=100.0)
    phenolic = st.number_input("% Phenolic", min_value=0.0, max_value=100.0)
    delta_e = st.number_input("MPC ΔE", min_value=0.0, max_value=100.0)

with col2:
    selected_oil = st.selectbox("Oil Type", sorted(oil_constants.keys()))

with col3:
    decon_added = st.selectbox("DECON Added", ["Yes", "No"])

with col4:
    hours_in_use = st.number_input("Hours in Use", min_value=0)

with col5:
    app_type = st.selectbox("Application Type", ["Gas Turbine", "Steam Turbine"])
    model_brand = st.selectbox("OEM", list(model_options.keys()))
    model_name = st.selectbox("Model", list(model_options[model_brand][app_type].keys()))
    tsi = model_options[model_brand][app_type][model_name]

# --- CALCULATE RUL ---
if st.button("Analyze"):
    st.markdown("---")
    st.subheader("Results")

    k_r, k_a = oil_constants[selected_oil]

    # Adjust constants
    factor = math.exp((90000 / 8.314) * (1 / (273.15 + 55) - 1 / (273.15 + 120)))
    adjusted_k_r = k_r * tsi / factor
    adjusted_k_a = k_a * tsi / factor

    try:
        t_total_r = -math.log(25 / rpvot_input) / adjusted_k_r if adjusted_k_r > 0 else 0
    except:
        t_total_r = 0
    rul_rpvot = t_total_r - hours_in_use

    try:
        t_total_a = -math.log(25 / aminic_input) / adjusted_k_a if adjusted_k_a > 0 else 0
    except:
        t_total_a = 0
    rul_aminic = t_total_a - hours_in_use

    rul_avg = max((rul_rpvot + rul_aminic) / 2, 0)
    total_hours = hours_in_use + rul_avg
    usage_pct = (hours_in_use / total_hours) * 100 if total_hours > 0 else 100

        # --- RESULT BAR ---
    st.markdown(f"""
        <div style="width:100%;height:20px;background:linear-gradient(to right, green, yellow, red);border-radius:10px;position:relative;">
            <div style="position:absolute;left:0;width:{usage_pct:.2f}%;height:20px;background:rgba(0,0,0,0.3);border-radius:10px;"></div>
            <div style="position:absolute;left:100%;width:2px;height:20px;background:red;"></div>
        </div>
    """, unsafe_allow_html=True)

    # --- NEW OUTPUT TEXT ---
    st.markdown(f"**Your turbine model, oil type, and present oil condition have been analyzed to estimate the remaining useful oil life: {rul_avg:.0f} hours.**")

    
