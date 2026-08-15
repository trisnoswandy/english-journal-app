import streamlit as st
import requests

st.title("📄 AI English Journal Evaluator")
st.write("Masukkan jurnal harianmu untuk mendapatkan evaluasi otomatis 12 Poin!")

api_key = st.text_input("Masukkan Gemini API Key kamu:", type="password")
journal_text = st.text_area("Tulis draf jurnalmu di sini (Bahasa Indonesia & Inggris):")

if st.button("Evaluasi Jurnal 🚀"):
    if not api_key or not journal_text:
        st.warning("Mohon isi API Key dan draf jurnal kamu.")
    else:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": f"Evaluasi jurnal berikut dalam 12 poin:\n\n{journal_text}"}]
            }]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            try:
                output = result['candidates'][0]['content']['parts'][0]['text']
                st.success("Evaluasi Selesai!")
                st.write(output)
            except Key:
                st.error("Gagal membaca respon dari API.")
        else:
            st.error(f"Terjadi kesalahan: {response.status_code} - {response.text}")
