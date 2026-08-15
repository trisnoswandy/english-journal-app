import streamlit as st
from google import genai
from PIL import Image
import pandas as pd
import plotly.express as px
from docx import Document
from io import BytesIO

st.set_page_config(page_title="English Learning Website", page_icon="🌴", layout="wide")

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

# Inisialisasi Session State untuk menyimpan hasil evaluasi & latihan
if "eval_result" not in st.session_state:
    st.session_state.eval_result = None
if "answer_feedback" not in st.session_state:
    st.session_state.answer_feedback = None

with st.sidebar:
    st.markdown("### 🌴 English Learning Website")
    st.caption("Intelligence & Data Platform")
    st.markdown("---")
    api_key = st.text_input("Gemini API Key", type="password", placeholder="api_key_anda")
    menu = st.radio("Navigate:", ["12-Point Journal Evaluator", "Progress & Target Planner", "AI Video Prompt Gen"])
    st.markdown("---")
    st.markdown("👤 **Trisno Swandy Simanullang**")

st.title("🌴 Trisno's English Learning Website")
st.markdown("Platform Cerdas Pengembang Bahasa Inggris, Riset Perkebunan, & Analisis Pasar.")

if not api_key:
    st.warning("⚠️ Masukkan Gemini API Key Anda di sidebar untuk mengaktifkan fitur AI.")

MODEL_NAME = 'gemini-3.6-flash'

if menu == "12-Point Journal Evaluator":
    st.header("📝 12-Point Journal Evaluator ")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        journal_input = st.text_area("Input Teks Jurnal / Catatan Riset (ID/EN):", height=180)
    with col2:
        uploaded_image = st.file_uploader("Upload Foto / Screenshots Jurnal (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])
        if uploaded_image:
            image_preview = Image.open(uploaded_image)
            st.image(image_preview, caption="Preview Foto SS Jurnal", use_container_width=True)
    
    if st.button("🚀 INITIATE EVALUATION"):
        if not api_key:
            st.error("API Key belum dimasukkan di sidebar!")
        elif not journal_input and not uploaded_image:
            st.warning("Mohon masukkan teks jurnal atau upload foto screenshot terlebih dahulu.")
        else:
            with st.spinner("Menganalisis 12 Poin Evaluasi Jurnal Harian..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    system_prompt = """
                    Bertindaklah sebagai Mentor Bahasa Inggris Pribadi. Evaluasi draf jurnal pengguna dan berikan umpan balik yang terstruktur persis mengikuti 12 Poin Evaluasi Jurnal Harian berikut:

                    1. **Transkripsi Teks & Versi Alami (Natural)**
                       Menampilkan draf tulisan asli pengguna dan versi perbaikan Bahasa Inggris yang alami (natural English) dalam bentuk paragraf rapi.

                    2. **Kamus Kata-Kata (Siap Salin)**
                       Daftar kosakata baru dari draf pengguna dalam format rapat (tanpa tabel) beserta arti dan contoh kalimatnya, siap ditempel ke Notion.

                    3. **Bedah Struktur & Pilihan Kata (Word-by-Word Analysis)**
                       Analisis mendalam mengenai kesalahan tata bahasa (grammar), ejaan, tata kata, serta dilengkapi panduan cara baca fonetiknya.

                    4. **Before vs After Transformation (Transformasi Kalimat)**
                       Perbandingan langsung antara kalimat kurang tepat pada draf asli dengan versi perbaikannya beserta pelajaran utamanya.

                    5. **Top 3 Vocabulary Focus (3 Kata Kunci Utama)**
                       Tiga kosakata atau idiom paling penting dari jurnal hari itu yang wajib dihafalkan.

                    6. **Mastered Verb Tracker (Lacak Kata Kerja yang Dikuasai)**
                       Pelacakan penggunaan perubahan kata kerja (V1, V2, V3) untuk melihat mana yang sudah berhasil dikuasai dan mana yang perlu diperbaiki.

                    7. **Skor & Persentase Ketepatan Mandiri**
                       Perhitungan akurasi tulisan secara transparan menggunakan formula matematika:
                       $$\\text{Skor} = \\left( \\frac{\\text{Kata Benar}}{\\text{Total Kata}} \\right) \\times 100\\%$$

                    8. **Pronunciation Challenge (Tantangan Pengucapan)**
                       Kalimat terpilih dari jurnal untuk dilatih secara lisan, lengkap dengan panduan pengucapan suara alami (natural phonetic guide).

                    9. **Native Phrase of the Day (Ungkapan Gaul Penutur Asli)**
                       Satu frasa, phrasal verb, atau idiom khas penutur asli beserta contoh penggunaannya dalam kalimat.

                    10. **Evaluasi Jurnal Harian**
                        Umpan balik ringkas, catatan perkembangan, dan apresiation atas alur cerita jurnal pengguna.

                    11. **Daily Micro-Question (Pertanyaan Tematik Hari Ini)**
                        Satu pertanyaan singkat berbahasa Inggris yang relevan dengan topik jurnal untuk melatih kemampuan merespons cepat.

                    12. **Sesi Belajar Singkat (Materi & Latihan Soal)**
                        Pembahasan materi dasar secara berurutan (6 Poin Fondasi) menggunakan siklus 3 hari pengulangan per materi, diakhiri dengan 3 latihan soal singkat (Soal 1, Soal 2, Soal 3).
                    """

                    contents_payload = [system_prompt]
                    if journal_input:
                        contents_payload.append(f"\nTeks Jurnal Input:\n{journal_input}")
                    if uploaded_image:
                        image_obj = Image.open(uploaded_image)
                        contents_payload.append(image_obj)

                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=contents_payload
                    )
                    
                    st.session_state.eval_result = response.text
                    st.session_state.answer_feedback = None  # Reset jawaban lama
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {str(e)}")

    # Menampilkan hasil evaluasi jika sudah di-generate
    if st.session_state.eval_result:
        st.success("Evaluasi 12 Poin Selesai!")
        st.markdown(st.session_state.eval_result)
        
        st.markdown("---")
        st.subheader("✍️ Lembar Jawaban Latihan Soal & Daily Micro-Question")
        st.caption("Jawablah pertanyaan dari poin 11 dan 12 di atas untuk diperiksa langsung oleh AI.")
        
        user_answers = st.text_area(
            "Tuliskan jawaban Anda di sini (misal: Jawaban Micro-Question, Jawaban Soal 1, 2, dan 3):",
            height=150,
            placeholder="Contoh:\nDaily Micro-Question: I usually study in the evening...\nSoal 1: B\nSoal 2: went\nSoal 3: because"
        )
        
        if st.button("️ Periksa Jawaban Saya"):
            if not api_key:
                st.error("API Key belum dimasukkan!")
            elif not user_answers:
                st.warning("Silakan tuliskan jawaban Anda terlebih dahulu.")
            else:
                with st.spinner("Mengevaluasi jawaban Anda..."):
                    try:
                        client = genai.Client(api_key=api_key)
                        check_prompt = f"""
                        Berikut adalah konteks soal dan hasil evaluasi sebelumnya:
                        {st.session_state.eval_result}

                        Berikut adalah jawaban dari pengguna:
                        "{user_answers}"

                        Tugasmu:
                        1. Berikan koreksi dan penilaian apakah jawaban pengguna untuk Daily Micro-Question dan 3 Latihan Soal sudah benar.
                        2. Jika ada yang salah, jelaskan letak kesalahannya dan berikan jawaban yang benar beserta penjelasannya dalam bahasa Indonesia & Inggris.
                        3. Berikan nilai/skor akhir untuk sesi latihan ini.
                        """
                        
                        feedback_res = client.models.generate_content(
                            model=MODEL_NAME,
                            contents=check_prompt
                        )
                        st.session_state.answer_feedback = feedback_res.text
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {str(e)}")
                        
        if st.session_state.answer_feedback:
            st.markdown("### 📊 Hasil Penilaian Jawaban Anda")
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
