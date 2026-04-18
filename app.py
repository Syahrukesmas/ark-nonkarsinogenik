import streamlit as st
st.title("Kalkulator ARKL Non-Karsinogenik")
st.write("Aplikasi siap digunakan.")
cat > app.py <<EOF
import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="ARKL Non-Karsinogenik", page_icon="🛡️", layout="wide")

# CSS kustom untuk tampilan lebih profesional
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_index=True)

st.title("🛡️ Analisis Risiko Kesehatan Lingkungan (ARKL)")
st.subheader("Kalkulator Risiko Non-Karsinogenik")
st.info("Aplikasi ini menghitung tingkat risiko berdasarkan durasi paparan spesifik (Non-Karsinogenik).")

# --- INPUT PARAMETER ---
with st.expander("📝 Masukkan Parameter Analisis", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Variabel Polutan**")
        c_pollutant = st.number_input("Konsentrasi (C) - mg/m³ atau mg/L", format="%.4f", value=0.0100)
        r_rate = st.number_input("Laju Asupan (R)", value=0.83, help="Default udara: 0.83 m³/jam")
        rfd = st.number_input("Reference Dose (RfD) - mg/kg-hari", format="%.5f", value=0.02000)

    with col2:
        st.markdown("**Waktu & Frekuensi**")
        te = st.number_input("Waktu Paparan (tE) - jam/hari", min_value=1, max_value=24, value=24)
        fe = st.number_input("Frekuensi (fE) - hari/tahun", min_value=1, max_value=366, value=350)
        dt = st.number_input("Durasi (Dt) - tahun", min_value=1, value=30)

    with col3:
        st.markdown("**Profil Responden**")
        wb = st.number_input("Berat Badan (Wb) - kg", min_value=1.0, value=70.0)

# --- LOGIKA PERHITUNGAN ---
# AvgT untuk Non-Karsinogenik adalah Dt * 365 hari
avg_t = dt * 365
intake = (c_pollutant * r_rate * te * fe * dt) / (wb * avg_t)
hq = intake / rfd

# --- TAMPILAN HASIL ---
st.divider()
res_col1, res_col2 = st.columns(2)

with res_col1:
    st.metric(label="Nilai Intake (Asupan)", value=f"{intake:.5f} mg/kg-hari")
    
with res_col2:
    if hq > 1:
        st.metric(label="Hazard Quotient (HQ)", value=f"{hq:.4f}", delta="TIDAK AMAN", delta_color="inverse")
        st.error("⚠️ Kesimpulan: Konsentrasi polutan melampaui batas aman bagi kesehatan.")
    else:
        st.metric(label="Hazard Quotient (HQ)", value=f"{hq:.4f}", delta="AMAN")
        st.success("✅ Kesimpulan: Risiko kesehatan masih berada dalam batas yang dapat diterima.")

# --- DOKUMENTASI ---
st.divider()
with st.expander("📚 Referensi Perhitungan"):
    st.latex(r'''Intake = \frac{C \times R \times tE \times fE \times Dt}{Wb \times avgT}''')
    st.write("Di mana untuk Non-Karsinogenik, $avgT = Dt \\times 365$ hari.")
    st.caption("Sumber: Pedoman Analisis Risiko Kesehatan Lingkungan (ARKL) Kemenkes RI.")

EOF
