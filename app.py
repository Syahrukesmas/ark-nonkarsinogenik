import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman
st.set_page_config(page_title="ARKL Non-Karsinogenik", page_icon="🛡️", layout="wide")

# 2. CSS kustom
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 10px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e6e9ef;
    }
    /* Memaksa warna teks label dan nilai menjadi gelap */
    [data-testid="stMetricLabel"] { color: #555555 !important; }
    [data-testid="stMetricValue"] { color: #1f1f1f !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Analisis Risiko Kesehatan Lingkungan (ARKL)")
st.subheader("Kalkulator Risiko Non-Karsinogenik")

# 3. INPUT PARAMETER
with st.expander("📝 Masukkan Parameter Analisis", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        c_pollutant = st.number_input("Konsentrasi (C) - mg/m³ atau mg/L", format="%.4f", value=0.0100)
        r_rate = st.number_input("Laju Asupan (R)", value=0.83)
        rfd = st.number_input("Reference Dose (RfD)", format="%.5f", value=0.02000)
    with col2:
        te = st.number_input("Waktu Paparan (tE) - jam/hari", min_value=1, max_value=24, value=24)
        fe = st.number_input("Frekuensi (fE) - hari/tahun", min_value=1, max_value=366, value=350)
        dt = st.number_input("Durasi (Dt) - tahun", min_value=1, value=30)
    with col3:
        wb = st.number_input("Berat Badan (Wb) - kg", min_value=1.0, value=70.0)

# 4. LOGIKA PERHITUNGAN
avg_t = dt * 365
intake = (c_pollutant * r_rate * te * fe * dt) / (wb * avg_t) if (wb * avg_t) != 0 else 0
hq = intake / rfd if rfd != 0 else 0

# 5. TAMPILAN HASIL
st.divider()
res_col1, res_col2 = st.columns(2)
with res_col1:
    st.metric(label="Nilai Intake (Asupan)", value=f"{intake:.5f}")
with res_col2:
    if hq > 1:
        st.metric(label="Hazard Quotient (HQ)", value=f"{hq:.4f}", delta="TIDAK AMAN", delta_color="inverse")
        st.error("⚠️ Risiko tidak aman.")
    else:
        st.metric(label="Hazard Quotient (HQ)", value=f"{hq:.4f}", delta="AMAN")
        st.success("✅ Risiko aman.")
