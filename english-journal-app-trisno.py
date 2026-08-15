import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="English Journal Evaluator", page_icon="📝")

st.title("📝 AI English Journal Evaluator")
st.write("Masukkan jurnal harianmu untuk mendapatkan evaluasi otomatis 12 Poin!")

# Ambil API Key dari Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    api_key = st.text_input("Masukkan Gemini API Key kamu:", type="password")

journal_text = st.text_area("Tulis draf jurnalmu di sini (Bahasa Indonesia & Inggris):", height=150)

if st.button("Evaluasi Jurnal 🚀"):
    if not api_key:
        st.error("Silakan masukkan Gemini API Key terlebih dahulu!")
    elif not journal_text:
        st.warning("Tuliskan jurnalmu sebelum mengeklik tombol evaluasi.")
    else:
        with st.spinner("Sedang menganalisis jurnalmu..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash-latest")
                
                prompt = f"""
                Bertindaklah sebagai mentor Bahasa Inggris yang ramah dan suportif. 
                Evaluasi jurnal berikut menggunakan struktur 12 Poin (Transkripsi & Versi Alami, Kamus Kata Siap Salin, Bedah Struktur, Before vs After, Top 3 Vocab, Mastered Verb Tracker, Skor Ketepatan, Pronunciation Challenge, Native Phrase, Evaluasi Jurnal, Micro-Question, dan Sesi Belajar Singkat).

                Draf Jurnal:
                {journal_text}
                """
                
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
