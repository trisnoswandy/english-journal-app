import streamlit as st
from google import genai

st.title("📄 Evaluator Jurnal Bahasa Inggris AI")
st.write("Masukkan jurnal harianmu untuk mendapatkan evaluasi otomatis 12 Poin!")

api_key = st.text_input("Masukkan Kunci API Gemini kamu:", type="password")
journal_text = st.text_area("Tulis draf jurnalmu di sini (Bahasa Indonesia & Inggris):")

if st.button("Evaluasi Jurnal 🚀"):
    if not api_key or not journal_text:
        st.warning("Mohon isi API Key dan draf jurnal kamu.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"Evaluasi jurnal berikut dalam 12 poin:\n\n{journal_text}",
            )
            
            st.success("Evaluasi Selesai!")
            st.write(response.text)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
