import streamlit as st
import google.generativeai as genai
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
            radial-gradient(circle at 50% 10%, rgba(0, 255, 170, 0.06) 0%, transparent 60%),
            linear-gradient(rgba(0, 255, 170, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 170, 0.02) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
        color: #f1f5f9;
    }
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: rgba(5, 11, 20, 0.95); color: #94a3b8;
        text-align: center; padding: 8px; font-size: 12px;
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

@st.cache_data
def create_docx_file(content, title="Exported_Document"):
    doc = Document()
    doc.add_heading(title, 0)
    doc.add_paragraph(content)
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

def get_fast_ai_response(prompt, api_key):
    try:
        genai.configure(api_key=api_key)
        # Menggunakan gemini-1.5-pro yang stabil dan terhindar dari error kuota 3.7
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

with st.sidebar:
    st.markdown("### 🌴 English learning website")
    st.caption("Intelligence & Data Platform")
    st.markdown("---")
    api_key = st.text_input("Gemini API Key", type="password")
    menu = st.radio("Navigate:", ["12-Point Journal Evaluator", "Progress & Target Planner", "AI Video Prompt Gen"])
    st.markdown("---")
    st.markdown("👤 **Trisno Swandy Simanullang**")

st.title("🌴 Trisno's English learning website")
st.markdown("Platform Cerdas Pengembang Bahasa Inggris, Riset Perkebunan, & Analisis Pasar.")

if not api_key and menu != "Progress & Target Planner":
    st.warning("⚠️ Masukkan Gemini API Key Anda di sidebar.")

if menu == "12-Point Journal Evaluator":
    st.header("📝 12-Point Journal Evaluator")
    journal_input = st.text_area("Input Jurnal / Catatan Riset (ID/EN):", height=180)
    
    if st.button("🚀 INITIATE EVALUATION"):
        if not api_key:
            st.error("API Key belum dimasukkan!")
        elif not journal_input:
            st.warning("Mohon isi teks jurnal terlebih dahulu.")
        else:
            with st.spinner("⚡ AI sedang memproses data..."):
                prompt = f"Bertindaklah sebagai mentor Bahasa Inggris profesional. Evaluasi teks berikut secara komprehensif dalam 12 poin (Bahasa Indonesia & Inggris): \"{journal_input}\""
                result = get_fast_ai_response(prompt, api_key)
                st.success("✅ Evaluasi Selesai!")
                st.markdown(result)
                docx_data = create_docx_file(result, "Journal_Evaluation")
                st.download_button("📄 Export ke Word (.docx)", data=docx_data, file_name="Evaluasi_Jurnal.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

elif menu == "Progress & Target Planner":
    st.header("📈 Progress & Target Planner")
    st.text_area("Target & Fokus Belajar:", "1. Konsistensi Jurnal Harian\n2. Penguasaan Kosakata Perkebunan & Pasar\n3. Analisis Statistik", height=120)

elif menu == "AI Video Prompt Gen":
    st.header("🎬 AI Video Prompt Generator (Veo)")
    prompt_input = st.text_area("Deskripsi Visual / Ide Kreatif:", height=120)
    if st.button("✨ Generate Prompt"):
        if not api_key:
            st.error("API Key belum dimasukkan!")
        elif not prompt_input:
            st.warning("Masukkan deskripsi visual terlebih dahulu.")
        else:
            with st.spinner("🌀 Menyusun prompt video..."):
                result_prompt = get_fast_ai_response(f"Ubah ide ini menjadi prompt video AI sinematik: {prompt_input}", api_key)
                st.success("Prompt Berhasil Dibuat!")
                st.code(result_prompt, language="markdown")

st.markdown("<div class='footer'>Developed with ⚡ by <b>Trisno Swandy Simanullang</b></div>", unsafe_allow_html=True)
