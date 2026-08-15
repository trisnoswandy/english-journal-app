import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px
from docx import Document
from io import BytesIO
import time
import datetime

# Pastikan Anda telah menginstal library berikut sebelum menjalankan aplikasi:
# pip install streamlit google-generativeai pandas plotly python-docx

st.set_page_config(
    page_title="Nexus AI | English & Video Prompter",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_custom_css():
    st.markdown("""
        <style>
        /* Base Theme */
        .stApp {
            background-color: #0a0e17;
            color: #e0e6ed;
            font-family: 'Inter', sans-serif;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #00f3ff !important;
            text-shadow: 0 0 15px rgba(0, 243, 255, 0.4);
            font-weight: 700 !important;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #111827 !important;
            border-right: 1px solid rgba(0, 243, 255, 0.2);
        }
        
        /* Buttons */
        .stButton>button {
            background-color: transparent !important;
            border: 2px solid #00f3ff !important;
            color: #00f3ff !important;
            border-radius: 8px !important;
            box-shadow: 0 0 10px rgba(0, 243, 255, 0.2) !important;
            transition: all 0.3s ease !important;
            font-weight: bold !important;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #00f3ff !important;
            color: #0a0e17 !important;
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.6) !important;
            transform: translateY(-2px);
        }
        
        /* Text Areas & Inputs */
        .stTextArea>div>div>textarea, .stTextInput>div>div>input {
            background-color: #1a2333 !important;
            color: #00f3ff !important;
            border: 1px solid rgba(0, 243, 255, 0.3) !important;
            border-radius: 8px !important;
        }
        .stTextArea>div>div>textarea:focus, .stTextInput>div>div>input:focus {
            border-color: #00f3ff !important;
            box-shadow: 0 0 10px rgba(0, 243, 255, 0.5) !important;
        }

        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: transparent;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #1a2333;
            border: 1px solid rgba(0, 243, 255, 0.3);
            border-radius: 8px;
            padding: 10px 20px;
            color: #a0aec0;
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(0, 243, 255, 0.1);
            color: #00f3ff !important;
            border: 1px solid #00f3ff;
            box-shadow: 0 0 15px rgba(0, 243, 255, 0.4);
        }
        
        /* Metric Cards */
        [data-testid="stMetricValue"] {
            color: #00f3ff !important;
            text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
        }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

def show_futuristic_loader():
    loader_html = """
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px;">
        <div style="border: 3px solid rgba(0, 243, 255, 0.1); border-top-color: #00f3ff; border-radius: 50%; width: 60px; height: 60px; animation: spin 1s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite; box-shadow: 0 0 20px rgba(0,243,255,0.4);"></div>
        <p style="color: #00f3ff; margin-top: 20px; font-family: monospace; font-size: 16px; letter-spacing: 2px; text-shadow: 0 0 8px #00f3ff; animation: pulse 1.5s infinite;">NEURAL NETWORK PROCESSING...</p>
        <style>
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            @keyframes pulse { 0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; } }
        </style>
    </div>
    """
    return st.markdown(loader_html, unsafe_allow_html=True)

def generate_word_doc(content, title="Document"):
    doc = Document()
    # Mengatur heading
    heading = doc.add_heading(title, 0)
    # Memasukkan teks
    for line in content.split('\n'):
        doc.add_paragraph(line)
    
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>💠 NEXUS CORE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    api_key = st.text_input("🔑 Google Gemini API Key", type="password", help="Dapatkan API Key di Google AI Studio")
    if api_key:
        genai.configure(api_key=api_key)
        st.success("API Terhubung!")
    else:
        st.warning("Masukkan API Key untuk memulai.")
        
    st.markdown("---")
    st.markdown("### 🧑‍🚀 User Profile")
    st.write("Status: **Active**")
    st.write(f"Date: **{datetime.date.today().strftime('%B %d, %Y')}**")
    st.write("Streak: 🔥 **14 Days**")
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.caption("Nexus AI Engine v1.0 | Cyberpunk UI Edition")

st.markdown("<h1>🌐 Nexus Learning System</h1>", unsafe_allow_html=True)
st.write("Sistem Pendamping Belajar Bahasa Inggris Harian & Generator Visual AI.")

tab_journal, tab_tracker, tab_veo = st.tabs([
    "📝 AI Journal Evaluator", 
    "📊 Progress & Planner", 
    "🎥 Google Veo Prompter"
])

with tab_journal:
    st.markdown("### 📝 Draf Jurnal Harian")
    
    col_input, col_settings = st.columns([2, 1])
    
    with col_input:
        journal_draft = st.text_area("Tulis jurnalmu di sini (Bahasa Indonesia atau Inggris):", height=250, 
                                     placeholder="Today I feel very happy because I can finish my task earlier...")
    
    with col_settings:
        st.markdown("### ⚙️ Pengaturan Output")
        var_options = st.selectbox("Variasi Perbaikan", ["1 Versi", "2 Versi", "3 Versi"], index=0)
        tone_options = st.selectbox("Gaya Bahasa", ["Casual / Daily", "Professional / Formal", "Native Conversational", "Slang / Street English"], index=2)
        length_options = st.selectbox("Panjang Umpan Balik", ["Ringkas / Compact", "Sedang", "Detail / Komprehensif"], index=1)
        
    generate_btn = st.button("🚀 Inisiasi Evaluasi Neural (Generate)")

    if generate_btn:
        if not api_key:
            st.error("⚠️ Harap masukkan API Key di Sidebar terlebih dahulu.")
        elif not journal_draft:
            st.warning("⚠️ Jurnal tidak boleh kosong.")
        else:
            loader_placeholder = st.empty()
            with loader_placeholder:
                show_futuristic_loader()
                
            try:
                # Setup model
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Desain Prompt
                prompt = f"""
                Bertindaklah sebagai Tutor Bahasa Inggris AI level Master. Evaluasi draf jurnal berikut:
                "{journal_draft}"
                
                Pengaturan yang diminta user:
                - Jumlah opsi perbaikan: {var_options}
                - Gaya bahasa: {tone_options}
                - Detail umpan balik: {length_options}
                
                Keluarkan output MENGGUNAKAN MARKDOWN dengan TEPAT 12 Poin terstruktur berikut:
                1. Transkripsi Teks & Versi Alami (Natural)
                2. Kamus Kata-Kata (Siap Salin ke Notion)
                3. Bedah Struktur & Pilihan Kata (Word-by-Word Analysis)
                4. Before vs After Transformation
                5. Top 3 Vocabulary Focus
                6. Mastered Verb Tracker
                7. Skor & Persentase Ketepatan Mandiri (0-100%)
                8. Pronunciation Challenge (Tantangan Pengucapan & Panduan Fonetik)
                9. Native Phrase of the Day
                10. Evaluasi Jurnal Harian (Komentar penyemangat)
                11. Daily Micro-Question (Pertanyaan pemantik untuk dijawab besok)
                12. Sesi Belajar Singkat (Materi Fondasi & 3 Latihan Soal)
                """
                
                response = model.generate_content(prompt)
                
                loader_placeholder.empty() # Hapus animasi loading
                
                st.markdown("### ✨ Hasil Evaluasi Jurnal")
                st.markdown(response.text)
                
                # Fitur Download / Export to Word
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    # Menampilkan teks di code block memudahkan fitur "Copy" bawaan Streamlit
                    st.success("Gunakan icon copy di pojok kanan atas kotak ini untuk menyalin ke Notion.")
                    st.code(response.text, language="markdown")
                
                with col_btn2:
                    docx_data = generate_word_doc(response.text, "AI Journal Evaluation")
                    st.download_button(
                        label="📄 Export ke Word (.docx)",
                        data=docx_data,
                        file_name=f"Journal_Evaluation_{datetime.date.today()}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            
            except Exception as e:
                loader_placeholder.empty()
                st.error(f"Terjadi kesalahan pada koneksi AI: {e}")

with tab_tracker:
    st.markdown("### 📊 Dashboard Metrik Pembelajaran")
    
    col_met1, col_met2, col_met3 = st.columns(3)
    col_met1.metric(label="Total Kosakata Dikuasai", value="342", delta="+12 minggu ini")
    col_met2.metric(label="Rata-rata Akurasi Jurnal", value="84%", delta="3% naik")
    col_met3.metric(label="Jam Latihan Bulan Ini", value="18.5 Jam", delta="+2.5 Jam")
    
    st.markdown("---")
    st.markdown("### 📈 Grafik Kemajuan Akurasi Jurnal (30 Hari Terakhir)")
    
    # Mock data untuk grafik
    dates = pd.date_range(end=datetime.date.today(), periods=30)
    # Generate dummy scores trending upwards
    scores = [65, 66, 64, 68, 70, 71, 70, 72, 75, 74, 76, 78, 77, 80, 81, 80, 82, 84, 85, 83, 86, 88, 87, 89, 90, 89, 91, 92, 91, 94]
    
    df_progress = pd.DataFrame({'Date': dates, 'Accuracy Score (%)': scores})
    
    fig = px.line(df_progress, x='Date', y='Accuracy Score (%)', template='plotly_dark')
    fig.update_traces(line_color='#00f3ff', line_width=4, fill='tozeroy', fillcolor='rgba(0, 243, 255, 0.1)')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 🎯 Papan Rencana Belajar (Planner)")
    target_plan = st.text_area("Tulis fokus mingguan/bulanan Anda:", height=150, 
                               value="- Minggu ini fokus: Past Tense & Phrasal Verbs\n- Target: 30 kosakata baru\n- Jadwal: 20 menit jurnal tiap malam")
    st.button("💾 Simpan Rencana")

with tab_veo:
    st.markdown("### 🎥 Veo 3 Cinematic Prompt Generator")
    st.write("Visualisasikan cerita jurnal Anda menjadi video beresolusi tinggi dengan Google Veo 3.")
    
    col_veo_main, col_veo_opt = st.columns([2, 1])
    
    with col_veo_main:
        veo_concept = st.text_area("Ide / Deskripsi Subjek Visualisasi:", height=200,
                                   placeholder="Contoh: Seorang astronot berjalan di hutan bercahaya neon, menemukan sebuah artefak bercahaya biru...")
        
    with col_veo_opt:
        st.markdown("#### 🎬 Parameter Visual")
        veo_camera = st.selectbox("Pergerakan Kamera (Camera Motion)", 
                                  ["Slow Panning", "Cinematic Drone Flythrough", "Handheld / Shaky", "Static / Fixed", "Zoom In Slowly", "Orbiting Dolly"], index=1)
        veo_lighting = st.selectbox("Pencahayaan (Lighting)", 
                                    ["Cinematic / Moody", "Cyberpunk Neon", "Natural Golden Hour", "Harsh Studio Lighting", "Bioluminescent Glow"], index=1)
        veo_style = st.selectbox("Gaya Visual (Visual Style)", 
                                 ["Hyper-realistic / 8k", "Anime Makoto Shinkai style", "3D Pixar Render", "Retro Sci-fi / Synthwave", "Watercolor Dream"], index=0)
    
    generate_veo_btn = st.button("🪄 Sintesis Prompt Veo 3")
    
    if generate_veo_btn:
        if not api_key:
            st.error("⚠️ Harap masukkan API Key di Sidebar terlebih dahulu.")
        elif not veo_concept:
            st.warning("⚠️ Deskripsi subjek tidak boleh kosong.")
        else:
            loader_veo = st.empty()
            with loader_veo:
                show_futuristic_loader()
                
            try:
                model_veo = genai.GenerativeModel('gemini-1.5-flash')
                veo_prompt_instruction = f"""
                Bertindaklah sebagai AI Video Prompt Engineer profesional.
                Buatkan prompt Bahasa Inggris yang sangat detail dan konsisten untuk AI Video Generator (Google Veo 3).
                
                Ide Dasar: "{veo_concept}"
                Kamera: {veo_camera}
                Lighting: {veo_lighting}
                Style: {veo_style}
                
                Buatkan dalam 1 paragraf panjang berbahasa Inggris yang sangat deskriptif (memuat subject, action, environment, lighting, camera movement, style, texture, frame rate/lens detail).
                Prompt harus langsung siap di-copy-paste ke platform Veo tanpa teks pengantar.
                """
                
                veo_resp = model_veo.generate_content(veo_prompt_instruction)
                loader_veo.empty()
                
                st.markdown("#### 🎞️ Final Video Prompt (Ready to Copy)")
                # Tampilkan dalam code block untuk fitur satu-klik copy
                st.code(veo_resp.text, language="text")
                
                docx_veo = generate_word_doc(veo_resp.text, "Google Veo 3 Video Prompt")
                st.download_button(
                    label="📄 Export Prompt ke Word",
                    data=docx_veo,
                    file_name="Veo3_Prompt.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key="veo_download"
                )
                
            except Exception as e:
                loader_veo.empty()
                st.error(f"Terjadi kesalahan saat memproses prompt: {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #4b5563; font-size: 14px;'>Nexus AI Engine © 2026. Powered by Google Gemini & Streamlit.</p>", unsafe_allow_html=True)
