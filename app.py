import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Kalkulator ARKL Lengkap", page_icon="🧬", layout="wide")

# 2. CSS kustom untuk Kontras Tinggi
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
    [data-testid="stMetricLabel"] { color: #555555 !important; }
    [data-testid="stMetricValue"] { color: #1f1f1f !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧬 Aplikasi ARKL Terintegrasi")
st.write("Pilih jenis analisis risiko pada tab di bawah ini:")

# --- MEMBUAT TAB ---
tab1, tab2 = st.tabs(["🟢 Non-Karsinogenik (HQ)", "🔴 Karsinogenik (ECR)"])

# ==========================================
# TAB 1: NON-KARSINOGENIK
# ==========================================
with tab1:
    st.header("Analisis Risiko Non-Karsinogenik")
    with st.expander("📝 Input Parameter Non-Karsinogenik", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            c_non = st.number_input("Konsentrasi (C)", format="%.4f", value=0.0100, key="c_non")
            r_non = st.number_input("Laju Asupan (R)", value=0.83, key="r_non")
            rfd_non = st.number_input("Reference Dose (RfD)", format="%.5f", value=0.02000, key="rfd_non")
        with c2:
            te_non = st.number_input("Waktu Paparan (tE)", value=24, key="te_non")
            fe_non = st.number_input("Frekuensi (fE)", value=350, key="fe_non")
            dt_non = st.number_input("Durasi (Dt)", value=30, key="dt_non")
        with c3:
            wb_non = st.number_input("Berat Badan (Wb)", value=70.0, key="wb_non")

    # Hitung HQ
    intake_non = (c_non * r_non * te_non * fe_non * dt_non) / (wb_non * (dt_non * 365))
    hq = intake_non / rfd_non
    
    st.divider()
    res1, res2 = st.columns(2)
    res1.metric("Intake Non-Karsinogenik", f"{intake_non:.5f}")
    if hq > 1:
        res2.metric("Hazard Quotient (HQ)", f"{hq:.4f}", delta="TIDAK AMAN", delta_color="inverse")
    else:
        res2.metric("Hazard Quotient (HQ)", f"{hq:.4f}", delta="AMAN")

# ==========================================
# TAB 2: KARSINOGENIK
# ==========================================
with tab2:
    st.header("Analisis Risiko Karsinogenik")
    with st.expander("📝 Input Parameter Karsinogenik", expanded=True):
        ck1, ck2, ck3 = st.columns(3)
        with ck1:
            c_kar = st.number_input("Konsentrasi (C)", format="%.4f", value=0.0100, key="c_kar")
            r_kar = st.number_input("Laju Asupan (R)", value=0.83, key="r_kar")
            sf_kar = st.number_input("Slope Factor (SF)", format="%.5f", value=0.00100, key="sf_kar")
        with ck2:
            te_kar = st.number_input("Waktu Paparan (tE)", value=24, key="te_kar")
            fe_kar = st.number_input("Frekuensi (fE)", value=350, key="fe_kar")
            dt_kar = st.number_input("Durasi (Dt)", value=30, key="dt_kar")
        with ck3:
            wb_kar = st.number_input("Berat Badan (Wb)", value=70.0, key="wb_kar")
            life_time = st.number_input("Life Time (Tavg)", value=25550, key="lt_kar")

    # Hitung ECR
    intake_kar = (c_kar * r_kar * te_kar * fe_kar * dt_kar) / (wb_kar * life_time)
    ecr = intake_kar * sf_kar
    
    st.divider()
    rk1, rk2 = st.columns(2)
    rk1.metric("Intake Karsinogenik", f"{intake_kar:.7f}")
    if ecr > 0.0001:
        rk2.metric("Excess Cancer Risk (ECR)", f"{ecr:.7f}", delta="TIDAK AMAN", delta_color="inverse")
    else:
        rk2.metric("Excess Cancer Risk (ECR)", f"{ecr:.7f}", delta="AMAN")
#MASIH DALAM TAHAP PENGEMBANGAN, JIKA ADA YANG SALAH SILAHKAN HUBUNGI EMAIL:muhamaddoni689@gmail.com
