import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px
from docx import Document
from io import BytesIO

# ==========================================
# 1. KONFIGURASI HALAMAN & TEMA CEPAT
# ==========================================
st.set_page_config(page_title="English learning website", page_icon="🌴", layout="wide")

# CSS Custom: Tema Neon Hijau, Latarmotif Grid Halus, dan Performa Optimal
custom_css = """
<style>
    .stApp {
        background-color: #050b14;
        background-image: 
            radial-gradient(circle at 50% 10%, rgba(0, 255, 170, 0.06) 0%, transparent 60%),
            linear-gradient(rgba(0, 255, 170, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 170, 0.02) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
        color: #f1f5f9;
    }
    
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(5, 11, 20, 0.95);
        color: #94a3b8;
        text-align: center;
        padding: 8px;
        font-size: 12px;
        border-top: 1px solid #1e293b;
        z-index: 100;
        backdrop-filter: blur(5px);
    }

    h1, h2, h3 { 
        color: #00ffaa !important; 
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 0 0 10px rgba(0, 255, 170, 0.3);
    }
    
    .stButton>button {
        background-color: rgba(0, 255, 170, 0.05) !important;
        color: #00ffaa !important;
        border: 1px solid #00ffaa !important;
        border-radius: 8px;
        transition: 0.2s;
        box-shadow: 0 0 10px rgba(0, 255, 170, 0.2);
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #00ffaa !important;
        color: #050b14 !important;
        box-shadow: 0 0 20px rgba(0, 255, 170, 0.6);
    }

    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #38bdf8 !important;
        border: 1px solid #334155 !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 2. FUNGSI OPTIMASI (CACHED & FAST API)
# ==========================================
@st.cache_data
def create_docx_file(content, title="Exported_Document"):
    doc = Document()
    doc.add_heading(title, 0)
    doc.add_paragraph(content)
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

# Fungsi pemanggilan AI menggunakan model 'gemini-2.5-flash' terbaru
def get_fast_ai_response(prompt, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# ==========================================
# 3. SIDEBAR & NAVIGASI
# ==========================================
with st.sidebar:
    st.markdown("### 🌴 English learning website")
    st.caption("Intelligence & Data Platform")
    st.markdown("---")
    
    api_key = st.text_input("Gemini API Key", type="password")
    menu = st.radio("Navigate:", ["12-Point Journal Evaluator", "Progress & Target Planner", "AI Video Prompt Gen"])
    st.markdown("---")
    st.markdown("👤 **Trisno Swandy Simanullang**")

# ==========================================
# HEADER UTAMA
# ==========================================
st.title("🌴 Trisno's English learning website")
st.markdown("Platform Cerdas Pengembang Bahasa Inggris, Riset Perkebunan, & Analisis Pasar.")

if not api_key and menu != "Progress & Target Planner":
    st.warning("⚠️ Masukkan Gemini API Key Anda di sidebar untuk mengaktifkan modul AI.")

# ==========================================
# MODULE 1: 12-POINT JOURNAL EVALUATOR
# ==========================================
if menu == "12-Point Journal Evaluator":
    st.header("📝 12-Point Journal Evaluator")
    journal_input = st.text_area("Input Jurnal / Catatan Riset (ID/EN):", height=180, placeholder="Tuliskan catatan harian atau jurnal Anda di sini...")
    
    if st.button("🚀 INITIATE EVALUATION"):
        if not api_key:
            st.error("API Key belum dimasukkan!")
        elif not journal_input:
            st.warning("Mohon isi teks jurnal terlebih dahulu.")
        else:
            with st.spinner("⚡ AI sedang memproses data dengan cepat..."):
                prompt = f"""
                Bertindaklah sebagai mentor Bahasa Inggris profesional. Evaluasi teks berikut secara komprehensif dalam 12 poin (Bahasa Indonesia & Inggris):
                Teks: "{journal_input}"
                """
                result = get_fast_ai_response(prompt, api_key)
                st.success("✅ Evaluasi Selesai!")
                st.markdown(result)
                
                # Tombol Export Word instan
                docx_data = create_docx_file(result, "Journal_Evaluation")
                st.download_button("📄 Export ke Word (.docx)", data=docx_data, file_name="Evaluasi_Jurnal.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

# ==========================================
# MODULE 2: PROGRESS PLANNER
# ==========================================
elif menu == "Progress & Target Planner":
    st.header("📈 Progress & Target Planner")
    st.info("Pantau target harian dan kosakata Anda secara real-time.")
    st.text_area("Target & Fokus Belajar:", "1. Konsistensi Jurnal Harian\n2. Penguasaan Kosakata Perkebunan & Pasar\n3. Analisis Statistik", height=120)

# ==========================================
# MODULE 3: AI VIDEO PROMPT GEN
# ==========================================
elif menu == "AI Video Prompt Gen":
    st.header("🎬 AI Video Prompt Generator (Veo)")
    prompt_input = st.text_area("Deskripsi Visual / Ide Kreatif:", placeholder="Contoh: Perkebunan sawit modern dengan latar belakang teknologi futuristik...", height=120)
    if st.button("✨ Generate Prompt"):
        if not api_key:
            st.error("API Key belum dimasukkan!")
        elif not prompt_input:
            st.warning("Masukkan deskripsi visual terlebih dahulu.")
        else:
            with st.spinner("🌀 Menyusun prompt video..."):
                ai_prompt = f"Ubah ide ini menjadi prompt video AI yang sinematik: {prompt_input}"
                result_prompt = get_fast_ai_response(ai_prompt, api_key)
                st.success("Prompt Berhasil Dibuat!")
                st.code(result_prompt, language="markdown")

# ==========================================
# FOOTER
# ==========================================
st.markdown("""
    <div class='footer'>
        Developed with ⚡ by <b>Trisno Swandy Simanullang</b>
    </div>
    """, unsafe_allow_html=True)
