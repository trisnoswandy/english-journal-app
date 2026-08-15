import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px
from docx import Document
from io import BytesIO
import time
from datetime import datetime, timedelta

# ==========================================
# 1. KONFIGURASI HALAMAN & BACKGROUND BERPOLA
# ==========================================
st.set_page_config(page_title="Trisno's Neo-Analytics Hub", page_icon="🌴", layout="wide")

# CSS Custom: Latar belakang dengan pola grid / garis-garis futuristik & neon
custom_css = """
<style>
    /* Latar Belakang Utama dengan Efek Pola Grid Cyber / Garis Abstrak */
    .stApp {
        background-color: #050b14;
        background-image: 
            radial-gradient(circle at 50% 10%, rgba(0, 255, 170, 0.08) 0%, transparent 60%),
            linear-gradient(rgba(0, 255, 170, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 170, 0.03) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
        color: #f1f5f9;
    }
    
    /* Footer Identitas Pembuat */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(5, 11, 20, 0.95);
        color: #94a3b8;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        border-top: 1px solid #1e293b;
        z-index: 100;
        backdrop-filter: blur(5px);
    }

    /* Heading dengan Efek Neon Hijau */
    h1, h2, h3 { 
        color: #00ffaa !important; 
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 0 0 10px rgba(0, 255, 170, 0.3);
    }
    
    /* Tombol Interaktif */
    .stButton>button {
        background-color: rgba(0, 255, 170, 0.05) !important;
        color: #00ffaa !important;
        border: 1px solid #00ffaa !important;
        border-radius: 8px;
        transition: 0.3s;
        box-shadow: 0 0 10px rgba(0, 255, 170, 0.2);
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #00ffaa !important;
        color: #050b14 !important;
        box-shadow: 0 0 20px rgba(0, 255, 170, 0.6);
    }

    /* Kotak Input & Text Area */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #38bdf8 !important;
        border: 1px solid #334155 !important;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #00ffaa !important;
        box-shadow: 0 0 10px rgba(0, 255, 170, 0.4) !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 2. SIDEBAR & MENU NAVIGASI
# ==========================================
with st.sidebar:
    st.markdown("### 🌴 English learning website")
    st.caption("Intelligence & Data Platform")
    st.markdown("---")
    
    api_key = st.text_input("Gemini API Key", type="password", placeholder="api_key_anda")
    menu = st.radio("Navigate:", ["12-Point Journal Evaluator", "Progress & Target Planner", "AI Video Prompt Gen"])
    st.markdown("---")
    st.markdown("👨‍💻 **Trisno Swandy Simanullang**")

# ==========================================
# HEADER UTAMA
# ==========================================
st.title("🌴 Trisno's English learning website")
st.markdown("Platform Cerdas Pengembang Bahasa Inggris, Riset Perkebunan, & Analisis Pasar.")

if not api_key:
    st.warning("⚠️ Masukkan Gemini API Key Anda di sidebar untuk mengaktifkan fitur AI.")

# ==========================================
# MODULE 1: 12-POINT JOURNAL EVALUATOR
# ==========================================
if menu == "12-Point Journal Evaluator":
    st.header("📝 12-Point Journal Evaluator")
    journal_input = st.text_area("Input Jurnal / Catatan Riset (ID/EN):", height=200, placeholder="Tuliskan jurnal harian, analisis pasar, atau catatan perkebunan Anda di sini...")
    
    if st.button("🚀 INITIATE EVALUATION"):
        if not api_key:
            st.error("API Key belum dimasukkan!")
        elif not journal_input:
            st.warning("Mohon isi teks terlebih dahulu.")
        else:
            with st.spinner("Menganalisis teks dengan kecerdasan buatan..."):
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-3.7-flash')
                response = model.generate_content(f"Bertindaklah sebagai mentor tingkat lanjut. Evaluasi dan perbaiki teks berikut secara komprehensif dalam bahasa Inggris dan Indonesia: {journal_input}")
                st.success("Evaluasi Selesai!")
                st.markdown(response.text)

# ==========================================
# MODULE 2: PROGRESS PLANNER
# ==========================================
elif menu == "Progress & Target Planner":
    st.header("📈 Progress & Target Planner")
    st.info("Kelola target harian, kosakata, serta parameter riset Anda.")
    st.text_area("Target & Fokus Belajar:", "1. Analisis fundamental & teknikal (P/E Ratios)\n2. Patologi tanaman & biologi tanah\n3. Statistik & pengujian hipotesis", height=120)

# ==========================================
# MODULE 3: AI VIDEO PROMPT GEN
# ==========================================
elif menu == "AI Video Prompt Gen":
    st.header("🎬 AI Video Prompt Generator (Veo)")
    st.text_area("Deskripsi Visual / Ide Kreatif:", placeholder="Visualisasi grafik tren pasar atau ekosistem perkebunan futuristik...", height=120)
    if st.button("✨ Generate Prompt"):
        st.info("Modul video prompt siap digunakan.")

# ==========================================
# FOOTER / NAMA PEMBUAT
# ==========================================
st.markdown("""
    <div class='footer'>
        Developed with ⚡ by <b>Trisno Swandy Simanullang</b>
    </div>
    """, unsafe_allow_html=True)
