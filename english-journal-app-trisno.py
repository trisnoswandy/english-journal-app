import streamlit as st
from google import genai
from PIL import Image
import pandas as pd
import plotly.express as px
from docx import Document
from io import BytesIO

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Trisno's Intelligence Hub",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS & Styling (Tema Cyber-Neon Pro)
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background-color: #030712;
        background-image: 
            radial-gradient(circle at 50% 0%, rgba(0, 255, 170, 0.12) 0%, transparent 50%),
            linear-gradient(rgba(0, 255, 170, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 170, 0.03) 1px, transparent 1px);
        background-size: 100% 100%, 30px 30px, 30px 30px;
        color: #f1f5f9;
    }

    /* Container Card bergaya Glassmorphism */
    .pro-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 170, 0.2);
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(7, 12, 22, 0.95) !important;
        border-right: 1px solid rgba(0, 255, 170, 0.15);
    }

    /* Text & Headings */
    h1, h2, h3 {
        color: #00ffaa !important;
        font-family: 'JetBrains Mono', monospace !important;
        letter-spacing: -0.5px;
    }

    .brand-title {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00ffaa 0%, #00b8d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }

    .brand-subtitle {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 20px;
    }

    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(135deg, rgba(0, 255, 170, 0.1) 0%, rgba(0, 184, 212, 0.1) 100%) !important;
        color: #00ffaa !important;
        border: 1px solid #00ffaa !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }

    .stButton>button:hover {
        background: #00ffaa !important;
        color: #030712 !important;
        box-shadow: 0 0 15px rgba(0, 255, 170, 0.4);
        transform: translateY(-2px);
    }

    /* Input Fields Styling */
    .stTextArea textarea, .stTextInput input {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid #1e293b !important;
        color: #f8fafc !important;
        border-radius: 10px !important;
    }

    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #00ffaa !important;
        box-shadow: 0 0 8px rgba(0, 255, 170, 0.3) !important;
    }

    /* Footer */
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: rgba(3, 7, 18, 0.95);
        color: #64748b; text-align: center;
        padding: 12px; font-size: 12px;
        border-top: 1px solid rgba(0, 255, 170, 0.15);
        z-index: 100; backdrop-filter: blur(8px);
    }

    /* Custom Badge */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(0, 255, 170, 0.1);
        color: #00ffaa;
        border: 1px solid rgba(0, 255, 170, 0.3);
        margin-bottom: 12px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Session State Management
if "eval_result" not in st.session_state:
    st.session_state.eval_result = None
if "answer_feedback" not in st.session_state:
    st.session_state.answer_feedback = None

# 4. Sidebar UI
with st.sidebar:
    st.markdown("<div class='brand-title'>🌴 Trisno's Hub</div>", unsafe_allow_html=True)
    st.markdown("<div class='brand-subtitle'>Intelligence & Data Platform</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    api_key = st.text_input("🔑 Gemini API Key", type="password", placeholder="Masukkan API Key Anda...")
    st.caption("API Key aman & tidak disimpan permanen.")
    
    st.markdown("---")
    menu = st.radio("🧭 Navigasi Fitur:", [
        "💬 Smart Assistant & Evaluator", 
        "📈 Target & Learning Planner", 
        "🎬 AI Video Prompt Gen"
    ])
    
    st.markdown("---")
    st.markdown("👤 **Trisno Swandy Simanullang**")
    st.markdown("<span class='status-badge'>PRO PLATFORM ACTIVE</span>", unsafe_allow_html=True)

# 5. Header Utama
st.markdown("<div class='brand-title'>🌴 Trisno's Intelligence Workspace</div>", unsafe_allow_html=True)
st.markdown("Platform Cerdas Pengembang Bahasa Inggris, Analisis Pasar, & Riset Perkebunan.")

if not api_key:
    st.info("💡 **Petunjuk:** Masukkan Gemini API Key Anda di sidebar sebelah kiri untuk mulai menggunakan fitur AI.")

MODEL_NAME = 'gemini-2.5-flash'

# 6. Fitur 1: Smart Assistant & Evaluator
if menu == "💬 Smart Assistant & Evaluator":
    st.markdown("<div class='pro-card'>", unsafe_allow_html=True)
    st.subheader("💬 Smart Assistant & 12-Point Journal Evaluator")
    st.write("Ketik pertanyaan bebas (saham, riset, diskusi) untuk obrolan biasa, atau masukkan draf jurnal/foto SS untuk evaluasi 12 Poin Bahasa Inggris.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Menggunakan st.form agar tekan Enter langsung mengirimkan pesan
        with st.form(key="chat_form", clear_on_submit=False):
            user_input = st.text_input(
                "📝 Pesan / Jurnal / Pertanyaan (Tekan Enter untuk Kirim):",
                placeholder="Misal: Analisis saham BBCA hari ini... (lalu tekan Enter)"
            )
            submitted = st.form_submit_button("🚀 Kirim / Analisis Data")
            
    with col2:
        uploaded_image = st.file_uploader("📷 Upload Foto / Screenshot (Opsional):", type=["png", "jpg", "jpeg"])
        if uploaded_image:
            image_preview = Image.open(uploaded_image)
            st.image(image_preview, caption="Preview Gambar SS", use_container_width=True)
    
    # Eksekusi saat Form disubmit (baik via Enter maupun klik tombol)
    if submitted:
        if not api_key:
            st.error("⚠️ Silakan masukkan Gemini API Key di sidebar terlebih dahulu!")
        elif not user_input and not uploaded_image:
            st.warning("⚠️ Mohon masukkan pesan teks atau upload foto screenshot terlebih dahulu.")
        else:
            with st.spinner("⚡ Memproses respons dengan Gemini 2.5 Flash..."):
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
    st.markdown("</div>", unsafe_allow_html=True)

    # Tampilan Hasil Respons AI
    if st.session_state.eval_result:
        st.markdown("<div class='pro-card'>", unsafe_allow_html=True)
        st.markdown("### 🤖 Respons AI / Hasil Evaluasi")
        st.markdown(st.session_state.eval_result)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Lembar Jawaban Interaktif
        st.markdown("<div class='pro-card'>", unsafe_allow_html=True)
        st.subheader("✍️ Lembar Jawaban Interaktif")
        st.caption("Gunakan bagian ini untuk menjawab latihan soal atau Micro-Question dari hasil evaluasi di atas.")
        
        with st.form(key="answer_form", clear_on_submit=False):
            user_answers = st.text_input(
                "Tuliskan jawaban Anda di sini (Tekan Enter untuk Kirim):",
                placeholder="Misal: Daily Micro-Question: I usually analyze stock trends... (lalu tekan Enter)"
            )
            answer_submitted = st.form_submit_button("✔️ Periksa Jawaban Saya")
        
        if answer_submitted:
            if not api_key:
                st.error("⚠️ Masukkan Gemini API Key terlebih dahulu!")
            elif not user_answers:
                st.warning("⚠️ Tuliskan jawaban Anda pada kolom di atas terlebih dahulu.")
            else:
                with st.spinner("⚡ AI sedang mengevaluasi jawaban Anda..."):
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
            st.markdown("---")
            st.markdown("### 📊 Hasil Penilaian & FeedBack")
            st.info(st.session_state.answer_feedback)
        st.markdown("</div>", unsafe_allow_html=True)

# 7. Fitur 2: Target Planner
elif menu == "📈 Target & Learning Planner":
    st.markdown("<div class='pro-card'>", unsafe_allow_html=True)
    st.subheader("📈 Target & Learning Planner")
    st.text_area(
        "Fokus & Target Belajar Utama:",
        "1. Analisis Pasar & Keuangan: Fundamental, Teknikal, P/E Ratios\n2. Riset Perkebunan: Patologi Tanaman & Biologi Tanah\n3. Statistik: Pengujian Hipotesis & Distribution Models",
        height=140
    )
    st.markdown("</div>", unsafe_allow_html=True)

# 8. Fitur 3: AI Video Prompt Gen
elif menu == "🎬 AI Video Prompt Gen":
    st.markdown("<div class='pro-card'>", unsafe_allow_html=True)
    st.subheader("🎬 AI Video Prompt Generator (Veo)")
    with st.form(key="video_form", clear_on_submit=False):
        prompt_input = st.text_input("Deskripsi Visual / Ide Kreatif (Tekan Enter untuk Kirim):", placeholder="Misal: Cinematic drone shot of oil palm plantation...")
        prompt_submitted = st.form_submit_button("✨ Generate Prompt")
    
    if prompt_submitted:
        if not api_key:
            st.error("⚠️ Masukkan API Key di sidebar!")
        elif not prompt_input:
            st.warning("⚠️ Masukkan deskripsi visual terlebih dahulu.")
        else:
            with st.spinner("⚡ Menyusun prompt sinematik..."):
                try:
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=f"Ubah ide ini menjadi prompt video AI sinematik berkualitas tinggi: {prompt_input}"
                    )
                    st.success("Prompt Berhasil Dibuat!")
                    st.code(response.text, language="markdown")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {str(e)}")
    st.markdown("</div>", unsafe_allow_html=True)

# 9. Footer
st.markdown("<div class='footer'>Developed with ⚡ by <b>Trisno Swandy Simanullang</b> | Powered by Gemini 2.5 Flash</div>", unsafe_allow_html=True)
