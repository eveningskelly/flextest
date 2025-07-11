import streamlit as st
from PIL import Image
import math

# Page config
st.set_page_config(
    page_title="FLEX REPORT",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS: darker background, dark-blue text, green accents
st.markdown("""
    <style>
        /* Background and text */
        [data-testid="stAppViewContainer"],
        [data-testid="stBlock"],
        [data-testid="stSidebar"],
        [data-testid="stHeader"],
        [data-testid="stToolbar"] {
            background-color: #e8e8e8 !important;
            color: #003366 !important;
        }
        body, .main {
            background-color: #e8e8e8 !important;
            color: #003366 !important;
        }
        h1 {
            color: #003366 !important;
            margin-top: -20px !important;
            margin-bottom: 10px !important;
            font-family: 'Arial Narrow', sans-serif !important;
            text-align: center !important;
            font-size: 48px !important;
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

# Load logos
fluitec_logo = Image.open("fluitec_logo.png")
flex_logo    = Image.open("flexlogo.png")

# Display logos larger and centered
logo_col1, logo_col2, logo_col3 = st.columns([1, 6, 1])
with logo_col1:
    st.image(fluitec_logo, width=300)
with logo_col3:
    st.image(flex_logo, width=300)

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

# Per-oil formula dictionaries
rpvot_funcs = {
    "Castrol SN 46": lambda h: max(100.79786 * math.exp(-0.00001996 * h), 0),
    "Castrol XEP 46": lambda h: max(87.88136 * math.exp(-0.00075575 * h), 0),
    "Chevron GST 32": lambda h: max(93.31351 * math.exp(-0.00000859 * h), 0),
    "Chevron GST Advantage EP 32": lambda h: max(102.73982 * math.exp(-0.0002572 * h), 0),
    "Chevron GST Premium XL32 (2)": lambda h: max(102.98036 * math.exp(-0.00034336 * h), 0),
    "Fuchs Eterna 46": lambda h: max(93.06849 * math.exp(-0.00054818 * h), 0),
    "Infinity TO32": lambda h: max(107.27841 * math.exp(-0.00039224 * h), 0),
    "Jentram Syn 46": lambda h: max(102.00911 * math.exp(-0.00080471 * h), 0),
    "Kluber Summit SH 32": lambda h: max(90.81009 * math.exp(-0.00044569 * h), 0),
    "Mobil DTE 732": lambda h: max(108.81924 * math.exp(-0.00037696 * h), 0),
    "Mobil DTE 732 Geared": lambda h: max(105.82153 * math.exp(-0.00024602 * h), 0),
    "Mobil DTE 832": lambda h: max(97.47189 * math.exp(-0.0005471 * h), 0),
    "Mobil DTE 932 GT": lambda h: max(90.54567 * math.exp(-0.00014641 * h), 0),
    "Mobil SHC 824": lambda h: max(95.89441 * math.exp(-0.00009471 * h), 0),
    "Mobil SHC 832 Ultra": lambda h: max(101.24346 * math.exp(-0.00016257 * h), 0),
    "Petromin Turbo 46": lambda h: max(97.69654 * math.exp(-0.00064843 * h), 0),
    "Repsol Turbo Aries Plus": lambda h: max(96.25161 * math.exp(-0.00040146 * h), 0),
    "Shell Turbo S4 GX 32": lambda h: max(91.33195 * math.exp(-0.00025352 * h), 0),
    "Shell Turbo S4X32": lambda h: max(91.06849 * math.exp(-0.0002014 * h), 0),
    "Shell Turbo T 32": lambda h: max(104.55415 * math.exp(-0.00049444 * h), 0),
    "Total Preslia EVO 32": lambda h: max(107.82388 * math.exp(-0.000412 * h), 0),
    "Total Preslia GT": lambda h: max(96.33903, 0),
    "Turboflo HTS": lambda h: max(101.64971 * math.exp(-0.00028872 * h), 0),
    "Turboflo LV": lambda h: max(100.67579 * math.exp(-0.00067692 * h), 0),
    "Turboflo R&O": lambda h: max(91.84005 * math.exp(-0.00106696 * h), 0),
    "Turboflo XL": lambda h: max(109.69558 * math.exp(-0.00017808 * h), 0)
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
    "Total Preslia GT": lambda h: max(101.12, 0),
    "Turboflo HTS": lambda h: max(104.32293 * math.exp(-0.00067565 * h), 0),
    "Turboflo LV": lambda h: max(106.73885 * math.exp(-0.00108233 * h), 0),
    "Turboflo R&O": lambda h: max(91.93054 * math.exp(-0.00058039 * h), 0),
    "Turboflo XL": lambda h: max(99.41411 * math.exp(-0.00017067 * h), 0)
}

# Helper to find remaining life until avg(RPVOT%, Aminic%) reaches 25%
def find_remaining_life(h0, r_fn, a_fn):
    def avg_pct(h):
        r = r_fn(h)
        a = a_fn(h) if a_fn else r
        return (r + a) / 2

    if avg_pct(h0) <= 25:
        return 0

    low, high = h0, h0 * 2 + 1
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

# Inputs
oil_col, hours_col = st.columns(2)
with oil_col:
    selected_oil = st.selectbox("Oil Type", oil_names)
with hours_col:
    hours_in_use = st.number_input("Hours in Use", min_value=0)

# Analyze button
if st.button("Analyze"):
    st.markdown("---")
    st.subheader("Results")

    # Compute current RPVOT% and Aminic%
    r_val = rpvot_funcs[selected_oil](hours_in_use)
    a_val = aminic_funcs.get(selected_oil, lambda h: r_val)(hours_in_use)

    # Compute remaining life
    extra_hours = find_remaining_life(hours_in_use, rpvot_funcs[selected_oil], aminic_funcs.get(selected_oil))
    rem_life = extra_hours if extra_hours is not None else 0
    total_life = hours_in_use + rem_life

    # Slider percentages
    used_pct = (hours_in_use / total_life) * 100 if total_life else 100
    deposit_pct = min(100, rem_life / total_life * 100 if total_life else 100)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div style="width:100%;height:20px;background:linear-gradient(to right,green, yellow, red);border-radius:10px;position:relative;">
                <div style="position:absolute;left:0;width:{used_pct}%;height:20px;background:rgba(0,0,0,0.3);border-radius:10px;"></div>
                <div style="position:absolute;left:100%;width:2px;height:20px;background:red;"></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"This oil has **{rem_life:.0f} hours** left of useful life.")
    with col2:
        st.markdown(f"""
            <div style="width:100%;height:20px;background:linear-gradient(to right,green, yellow, red);border-radius:10px;position:relative;">
                <div style="position:absolute;left:0;width:{deposit_pct}%;height:20px;background:rgba(0,0,0,0.3);border-radius:10px;"></div>
                <div style="position:absolute;left:100%;width:2px;height:20px;background:red;"></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"This oil has RPVOT: **{r_val:.1f}%**, Aminic: **{a_val:.1f}%**.")
