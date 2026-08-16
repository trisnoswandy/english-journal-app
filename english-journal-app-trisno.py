import streamlit as st
from google import genai
from PIL import Image
import pandas as pd
import plotly.express as px
from docx import Document
from io import BytesIO

st.set_page_config(page_title="Trisno's AI Assistant & English Mentor", page_icon="🌴", layout="wide")

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

# Inisialisasi Session State untuk menyimpan hasil respons & evaluasi latihan
if "eval_result" not in st.session_state:
    st.session_state.eval_result = None
if "answer_feedback" not in st.session_state:
    st.session_state.answer_feedback = None

with st.sidebar:
    st.markdown("### 🌴 English & Intelligence Hub")
    st.caption("Data & AI Personal Platform")
    st.markdown("---")
    api_key = st.text_input("Gemini API Key", type="password", placeholder="api_key_anda")
    menu = st.radio("Navigate:", ["Smart Assistant & Journal Evaluator", "Progress & Target Planner", "AI Video Prompt Gen"])
    st.markdown("---")
    st.markdown("👤 **Trisno Swandy Simanullang**")

st.title("🌴 Trisno's AI Workspace")
st.markdown("Platform Cerdas Pengembang Bahasa Inggris, Analisis Pasar, & Riset Perkebunan.")

if not api_key:
    st.warning("⚠️ Masukkan Gemini API Key Anda di sidebar untuk mengaktifkan fitur AI.")

MODEL_NAME = 'gemini-2.5-flash'

if menu == "Smart Assistant & Journal Evaluator":
    st.header("💬 Smart Assistant & 12-Point Journal Evaluator")
    st.caption("Ketik pertanyaan umum (saham, riset, diskusi) untuk mengobrol biasa, atau masukkan draf jurnal/foto SS untuk evaluasi 12 Poin Bahasa Inggris.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        user_input = st.text_area("Input Pesan / Jurnal / Pertanyaan (ID/EN):", height=180, placeholder="Contoh 1: Analisis saham BBCA hari ini bagaimana?\nContoh 2: Today I studied soil biology in the campus...")
    with col2:
        uploaded_image = st.file_uploader("Upload Gambar / Screenshots (Opsional):", type=["png", "jpg", "jpeg"])
        if uploaded_image:
            image_preview = Image.open(uploaded_image)
            st.image(image_preview, caption="Preview Gambar SS", use_container_width=True)
    
    if st.button("🚀 KIRIM / ANALISIS"):
        if not api_key:
            st.error("API Key belum dimasukkan di sidebar!")
        elif not user_input and not uploaded_image:
            st.warning("Mohon masukkan teks atau upload gambar terlebih dahulu.")
        else:
            with st.spinner("Memproses respons AI..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    system_prompt = """
                    Kamu adalah asisten AI pribadi yang cerdas, fleksibel, dan komunikatif bernama Gemini. Tugasmu adalah merespons input dari pengguna (Trisno) sesuai dengan niat pengiriman pesan:

                    [INSTRUKSI LOGIKA RESPON]:
                    1. JIKA pengguna mengirimkan draf jurnal harian, tulisan latihan bahasa Inggris, atau secara eksplisit meminta evaluasi jurnal:
                       --> Berikan evaluasi lengkap dan mendalam yang terstruktur persis dalam 12 POIN EVALUASI JURNAL HARIAN berikut:
                          1. Transkripsi Teks & Versi Alami (Natural)
                          2. Kamus Kata-Kata (Siap Salin ke Notion, tanpa tabel)
                          3. Bedah Struktur & Pilihan Kata (Word-by-Word Analysis + Fonetik)
                          4. Before vs After Transformation
                          5. Top 3 Vocabulary Focus
                          6. Mastered Verb Tracker (V1, V2, V3)
                          7. Skor & Persentase Ketepatan Mandiri (Formula: Skor = (Kata Benar / Total Kata) * 100%)
                          8. Pronunciation Challenge
                          9. Native Phrase of the Day
                          10. Evaluasi Jurnal Harian
                          11. Daily Micro-Question
                          12. Sesi Belajar Singkat (Materi 6 Poin Fondasi & 3 Latihan Soal)

                    2. JIKA pengguna menanyakan pertanyaan umum, berita pasar/saham, riset perkebunan/pertanian, analisis data, atau mengobrol biasa:
                       --> Jawablah secara langsung, informatif, lugas, dan komunikatif seperti dalam obrolan biasa. JANGAN paksa menggunakan format 12 poin evaluasi jika pengguna hanya bertanya atau mengobrol umum.
                    """

                    contents_payload = [system_prompt]
                    if user_input:
                        contents_payload.append(f"\nInput Pengguna:\n{user_input}")
                    if uploaded_image:
                        image_obj = Image.open(uploaded_image)
                        contents_payload.append(image_obj)

                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=contents_payload
                    )
                    
                    st.session_state.eval_result = response.text
                    st.session_state.answer_feedback = None
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {str(e)}")

    if st.session_state.eval_result:
        st.markdown("### 🤖 Respons AI:")
        st.markdown(st.session_state.eval_result)
        
        st.markdown("---")
        st.subheader("✍️ Lembar Jawaban Interaktif (Khusus Evaluasi / Sesi Latihan)")
        st.caption("Gunakan kolom di bawah ini jika kamu sedang menjawab latihan soal atau pertanyaan dari sesi evaluasi di atas.")
        
        user_answers = st.text_area(
            "Tuliskan jawaban kamu di sini:",
            height=120,
            placeholder="Contoh:\nDaily Micro-Question: I usually read news in the morning...\nJawaban Soal 1: A\nJawaban Soal 2: learned"
        )
        
        if st.button("✔️ Periksa Jawaban Saya"):
            if not api_key:
                st.error("API Key belum dimasukkan!")
            elif not user_answers:
                st.warning("Silakan tuliskan jawaban kamu terlebih dahulu.")
            else:
                with st.spinner("Mengevaluasi jawaban kamu..."):
                    try:
                        client = genai.Client(api_key=api_key)
                        check_prompt = f"""
                        Berikut adalah konteks percakapan/soal sebelumnya:
                        {st.session_state.eval_result}

                        Berikut adalah jawaban dari pengguna (Trisno):
                        "{user_answers}"

                        Tugasmu:
                        1. Evaluasi apakah jawaban pengguna sudah benar dan tepat.
                        2. Jika ada kesalahan tata bahasa atau jawaban soal yang keliru, berikan koreksi ramah beserta penjelasannya.
                        3. Berikan apresiasi dan skor jika sesuai.
                        """
                        
                        feedback_res = client.models.generate_content(
                            model=MODEL_NAME,
                            contents=check_prompt
                        )
                        st.session_state.answer_feedback = feedback_res.text
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {str(e)}")
                        
        if st.session_state.answer_feedback:
            st.markdown("### 📊 Hasil Penilaian Jawaban Kamu")
            st.info(st.session_state.answer_feedback)

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
                        model=MODEL_NAME,
                        contents=f"Ubah ide ini menjadi prompt video AI yang sinematik: {prompt_input}"
                    )
                    st.success("Prompt Berhasil Dibuat!")
                    st.code(response.text, language="markdown")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {str(e)}")

st.markdown("<div class='footer'>Developed with ⚡ by <b>Trisno Swandy Simanullang</b></div>", unsafe_allow_html=True)
