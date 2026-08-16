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

# 2. Custom CSS (Pembersihan Kotak Kosong & Desain Tampilan Veo Generator)
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

    /* Pembasmi Kontainer Kosong Bawaan Streamlit */
    div[data-testid="stVerticalBlock"] > div:empty,
    div[data-baseweb="notification"],
    .element-container:empty {
        display: none !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Styling Form Bawaan Streamlit */
    div[data-testid="stForm"] {
        background: rgba(15, 23, 42, 0.65) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(0, 255, 170, 0.2) !important;
        border-radius: 14px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(7, 12, 22, 0.95) !important;
        border-right: 1px solid rgba(0, 255, 170, 0.15);
    }

    h1, h2, h3 {
        color: #00ffaa !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Text Header */
    .brand-title {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00ffaa 0%, #00b8d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 4px 0 !important;
        font-family: 'JetBrains Mono', monospace;
    }

    .brand-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        margin: 0 0 20px 0 !important;
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

    /* Form Input */
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

    .api-warn-badge {
        padding: 10px 16px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        background: rgba(239, 68, 68, 0.12);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
        margin-bottom: 20px;
    }

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

    .response-card {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 170, 0.25);
        border-radius: 14px;
        padding: 24px;
        margin: 20px 0;
    }

    .footer {
        position: relative;
        margin-top: 40px;
        width: 100%;
        background-color: rgba(3, 7, 18, 0.95);
        color: #64748b; 
        text-align: center;
        padding: 16px; 
        font-size: 12px;
        border-top: 1px solid rgba(0, 255, 170, 0.15);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Session State Management
if "eval_result" not in st.session_state:
    st.session_state.eval_result = None
if "answer_feedback" not in st.session_state:
    st.session_state.answer_feedback = None
if "video_prompt_result" not in st.session_state:
    st.session_state.video_prompt_result = None

# 4. Sidebar UI
with st.sidebar:
    st.markdown("<div class='brand-title' style='font-size:1.5rem;'>🌴 Trisno's Hub</div>", unsafe_allow_html=True)
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
st.markdown("<div class='brand-subtitle'>Platform Cerdas Pengembang Bahasa Inggris, Analisis Pasar, & Riset Perkebunan.</div>", unsafe_allow_html=True)

if not api_key:
    st.markdown("<div class='api-warn-badge'>⚠️ Masukkan Gemini API Key di sidebar sebelah kiri untuk mengaktifkan fitur AI.</div>", unsafe_allow_html=True)

MODEL_NAME = 'gemini-3.6-flash'

# 6. Fitur 1: Smart Assistant & Evaluator
if menu == "💬 Smart Assistant & Evaluator":
    st.subheader("💬 Smart Assistant & 12-Point Journal Evaluator")
    st.caption("Ketik pertanyaan (saham, berita, riset) lalu tekan Enter untuk respon langsung.")
    
    with st.form(key="chat_form", clear_on_submit=False):
        col1, col2 = st.columns([1, 1])
        with col1:
            user_input = st.text_input(
                "📝 Pesan / Pertanyaan (Tekan Enter untuk Kirim):",
                placeholder="Misal: Apa kejadian penting kemarin? / Analisis saham BBCA... (tekan Enter)"
            )
        with col2:
            uploaded_image = st.file_uploader("📷 Upload Foto / Screenshot (Opsional):", type=["png", "jpg", "jpeg"])
        
        submitted = st.form_submit_button("🚀 Kirim / Analisis Data")
    
    if uploaded_image:
        image_preview = Image.open(uploaded_image)
        st.image(image_preview, caption="Preview Gambar SS", use_container_width=True)

    if submitted:
        if not api_key:
            st.error("⚠️ Silakan masukkan Gemini API Key di sidebar terlebih dahulu!")
        elif not user_input and not uploaded_image:
            st.warning("⚠️ Mohon masukkan pesan teks atau upload foto screenshot terlebih dahulu.")
        else:
            with st.spinner("⚡ Memproses respons dengan Gemini 3.6 Flash..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    system_prompt = """
                    Kamu adalah asisten AI pribadi bernama Gemini. 

                    [INSTRUKSI UTAMA]:
                    1. DILARANG BERTANYA BALIK ATAU MEMBERIKAN OPSI PILIHAN.
                    2. JAWAB LANGSUNG, CEPAT, RINGKAS, DAN AKURAT saat menerima pertanyaan. 
                    3. Jika pengguna bertanya hal umum (seperti "apa yang terjadi kemarin?"), LANGSUNG berikan rangkuman poin-poin peristiwa penting utama (Berita Nasional/Global & Pasar Finansial) tanpa meminta konfirmasi.
                    4. Lakukan kroscek data dan logika secara mandiri sebelum memberikan jawaban akhir.
                    5. Gunakan poin-poin terstruktur agar mudah dibaca di HP maupun PC.

                    [INSTRUKSI KONTEN]:
                    - JIKA pertanyaan berisi obrolan biasa / berita / pasar saham / riset pertanian: Jawab secara langsung dalam bentuk rangkuman poin-poin berita atau analisis teknis tanpa bertanya kembali.
                    - JIKA draf berupa tulisan latihan bahasa Inggris atau evaluasi jurnal harian: Berikan evaluasi lengkap 12 POIN EVALUASI JURNAL HARIAN.
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
        st.markdown("<div class='response-card'>", unsafe_allow_html=True)
        st.markdown("### 🤖 Respons AI / Hasil Evaluasi")
        st.markdown(st.session_state.eval_result)
        st.markdown("</div>", unsafe_allow_html=True)
        
        with st.form(key="answer_form", clear_on_submit=False):
            st.subheader("✍️ Lembar Jawaban Interaktif")
            st.caption("Gunakan bagian ini untuk menjawab latihan soal atau Micro-Question dari hasil evaluasi di atas.")
            user_answers = st.text_input(
                "Tuliskan jawaban Anda di sini (Tekan Enter untuk Kirim):",
                placeholder="Misal: Jawaban soal 1: A... (lalu tekan Enter)"
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
                        1. Kroscek dan evaluasi apakah jawaban pengguna meenuhi kriteria.
                        2. Berikan penjelasan ringkas beserta koreksi tata bahasa jika ada.
                        """
                        
                        feedback_res = client.models.generate_content(
                            model=MODEL_NAME,
                            contents=check_prompt
                        )
                        st.session_state.answer_feedback = feedback_res.text
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {str(e)}")
                        
        if st.session_state.answer_feedback:
            st.markdown("<div class='response-card'>", unsafe_allow_html=True)
            st.markdown("### 📊 Hasil Penilaian & FeedBack")
            st.write(st.session_state.answer_feedback)
            st.markdown("</div>", unsafe_allow_html=True)

# 7. Fitur 2: Target Planner
elif menu == "📈 Target & Learning Planner":
    st.subheader("📈 Target & Learning Planner")
    st.text_area(
        "Fokus & Target Belajar Utama:",
        "1. Analisis Pasar & Keuangan: Fundamental, Teknikal, P/E Ratios\n2. Riset Perkebunan: Patologi Tanaman & Biologi Tanah\n3. Statistik: Pengujian Hipotesis & Distribution Models",
        height=140
    )

# 8. Fitur 3: AI Video Prompt Generator (Veo Optimized)
elif menu == "🎬 AI Video Prompt Gen":
    st.subheader("🎬 AI Video Prompt Generator (Google Veo / Sora)")
    st.caption("Ubah ide sederhana atau konsep adegan Anda menjadi prompt sinematik profesional yang siap di-copy ke Google Veo, Runway, atau Sora.")

    with st.form(key="video_form", clear_on_submit=False):
        prompt_input = st.text_input(
            "Deskripsi Visual / Ide Kreatif (Tekan Enter untuk Kirim):",
            placeholder="Misal: Drone memperlihatkan kebun kelapa sawit saat matahari terbit..."
        )
        prompt_submitted = st.form_submit_button("✨ Generate Cinematic Video Prompt")

    if prompt_submitted:
        if not api_key:
            st.error("⚠️ Silakan masukkan Gemini API Key di sidebar terlebih dahulu!")
        elif not prompt_input:
            st.warning("⚠️ Masukkan ide visual atau deskripsi adegan terlebih dahulu.")
        else:
            with st.spinner("⚡ Menyusun prompt sinematik untuk Google Veo..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    veo_system_prompt = """
                    Kamu adalah seorang Prompt Engineer & Director of Photography (DoP) spesialis AI Generator Video seperti Google Veo, OpenAI Sora, dan Runway Gen-3.

                    [TUGAS UTAMA]:
                    Ubah input atau pertanyaan pengguna langsung menjadi Prompt Video AI Sinematik yang sangat detail dalam Bahasa Inggris (standar industri AI Video). 
                    Jangan memberikan penjelasan teori/definisi tentang apa itu Veo kecuali diminta secara khusus!

                    [FORMAT OUTPUT YANG WAJIB DIGUNAKAN]:
                    1. **English Prompt (Ready-to-Copy for Veo/Sora)**:
                       Prompt lengkap dalam 1 paragraf bahasa Inggris yang mencakup: Subject, Action, Environment, Camera Movement (contoh: Panning, Drone FP, Orbit), Lighting (contoh: Golden Hour, Cinematic Neon), Style (contoh: Photorealistic, 8k resolution, IMAX 35mm lens, 60fps).
                    
                    2. **Breakdown Elemen Sinematik**:
                       - 🎥 **Camera Angle/Movement**: ...
                       - 💡 **Lighting & Color Palette**: ...
                       - 🎞️ **Visual Style & Lens**: ...
                       - 🔊 **Suggested Audio/Atmosphere**: ...

                    Jawab langsung sesuai format tanpa intro bertele-tele.
                    """
                    
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=f"{veo_system_prompt}\n\nInput Ide Pengguna: {prompt_input}"
                    )
                    st.session_state.video_prompt_result = response.text
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {str(e)}")

    if st.session_state.video_prompt_result:
        st.markdown("<div class='response-card'>", unsafe_allow_html=True)
        st.markdown("### 🎬 Prompt Video Sinematik Siap Pakai")
        st.markdown(st.session_state.video_prompt_result)
        st.markdown("</div>", unsafe_allow_html=True)

# 9. Footer
st.markdown("<div class='footer'>Developed with ⚡ by <b>Trisno Swandy Simanullang</b> | Powered by Gemini 3.6 Flash</div>", unsafe_allow_html=True)
