import streamlit as st
from google import genai
import pandas as pd
import plotly.express as px
from docx import Document
from io import BytesIO

st.set_page_config(page_title="English learning website", page_icon="🌴", layout="wide")

custom_css = """
<style>
    .stApp {
        background-color: #050b14;
        background-image: 
            radial-gradient(circle at 50% 10%, rgba(0, 255, 170, 0.08) 0%, transparent 60%),
            linear-gradient(rgba(0, 255, 170, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 170, 0.03) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
        color: #f1f5f9;
    }
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: rgba(5, 11, 20, 0.95); color: #94a3b8;
        text-align: center; padding: 10px; font-size: 12px;
        border-top: 1px solid #1e293b; z-index: 100; backdrop-filter: blur(5px);
    }
    h1, h2, h3 { color: #00ffaa !important; font-family: 'Courier New', Courier, monospace; }
    .stButton>button {
        background-color: rgba(0, 255, 170, 0.05) !important;
        color: #00ffaa !important; border: 1px solid #00ffaa !important;
        border-radius: 8px; font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #00ffaa !important; color: #050b14 !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🌴 English learning website")
    st.caption("Intelligence & Data Platform")
    st.markdown("---")
    api_key = st.text_input("Gemini API Key", type="password", placeholder="api_key_anda")
    menu = st.radio("Navigate:", ["12-Point Journal Evaluator", "Progress & Target Planner", "AI Video Prompt Gen"])
    st.markdown("---")
    st.markdown("👤 **Trisno Swandy Simanullang**")

st.title("🌴 Trisno's English learning website")
st.markdown("Platform Cerdas Pengembang Bahasa Inggris, Riset Perkebunan, & Analisis Pasar.")

if not api_key:
    st.warning("⚠️ Masukkan Gemini API Key Anda di sidebar untuk mengaktifkan fitur AI.")

if menu == "12-Point Journal Evaluator":
    st.header("📝 12-Point Journal Evaluator")
    journal_input = st.text_area("Input Jurnal / Catatan Riset (ID/EN):", height=200)
    
    if st.button("🚀 INITIATE EVALUATION"):
        if not api_key:
            st.error("API Key belum dimasukkan!")
        elif not journal_input:
            st.warning("Mohon isi teks terlebih dahulu.")
        else:
            with st.spinner("Menganalisis teks..."):
                try:
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=f"Bertindaklah sebagai mentor tingkat lanjut. Evaluasi dan perbaiki teks berikut secara komprehensif dalam bahasa Inggris dan Indonesia: {journal_input}"
                    )
                    st.success("Evaluasi Selesai!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {str(e)}")

elif menu == "Progress & Target Planner":
    st.header("📈 Progress & Target Planner")
    st.text_area("Target & Fokus Belajar:", "1. Analisis fundamental & teknikal (P/E Ratios)\n2. Patologi tanaman & biologi tanah\n3. Statistik & pengujian hipotesis", height=120)

elif menu == "AI Video Prompt Gen":
    st.header("🎬 AI Video Prompt Generator (Veo)")
    prompt_input = st.text_area("Deskripsi Visual / Ide Kreatif:", height=120)
    if st.button("✨ Generate Prompt"):
        if not api_key:
            st.error("API Key belum dimasukkan!")
        elif not prompt_input:
            st.warning("Masukkan deskripsi visual terlebih dahulu.")
        else:
            with st.spinner("Menyusun prompt video..."):
                try:
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model='gemini-3.7-flash',
                        contents=f"Ubah ide ini menjadi prompt video AI yang sinematik: {prompt_input}"
                    )
                    st.success("Prompt Berhasil Dibuat!")
                    st.code(response.text, language="markdown")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {str(e)}")

st.markdown("<div class='footer'>Developed with ⚡ by <b>Trisno Swandy Simanullang</b></div>", unsafe_allow_html=True)
