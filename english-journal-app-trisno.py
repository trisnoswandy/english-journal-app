import streamlit as st
from google import genai

st.title("📄 AI English Journal Evaluator")
st.write("Masukkan jurnal harianmu untuk mendapatkan evaluasi otomatis 12 Poin!")

api_key = st.text_input("Masukkan Gemini API Key kamu:", type="password")
journal_text = st.text_area("Tulis draf jurnalmu di sini (Bahasa Indonesia & Inggris):")

if st.button("Evaluasi Jurnal 🚀"):
    if not api_key or not journal_text:
        st.warning("Mohon isi API Key dan draf jurnal kamu.")
    else:
        try:
            # Menginisialisasi client dengan SDK google-genai terbaru
            client = genai.Client(api_key=api_key)
            
            # Memanggil model gemini-2.0-flash
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=f"Evaluasi jurnal berikut dalam 12 poin:\n\n{journal_text}",
            )
            
            st.success("Evaluasi Selesai!")
            st.write(response.text)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
