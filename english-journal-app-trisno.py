import streamlit as st
import requests

st.title("📄 Evaluator Jurnal Bahasa Inggris AI")
st.write("Masukkan jurnal harianmu untuk mendapatkan evaluasi otomatis 12 Poin!")

api_key = st.text_input("Masukkan Kunci API Gemini kamu:", type="password")
journal_text = st.text_area("Tulis draf jurnalmu di sini (Bahasa Indonesia & Inggris):")

if st.button("Evaluasi Jurnal 🚀"):
    if not api_key or not journal_text:
        st.warning("Mohon isi API Key dan draf jurnal kamu.")
    else:
        clean_key = api_key.strip()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={clean_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": f"Evaluasi jurnal berikut dalam 12 poin:\n\n{journal_text}"}]
            }]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            res_data = response.json()
            
            if response.status_code == 200 and 'candidates' in res_data:
                output = res_data['candidates'][0]['content']['parts'][0]['text']
                st.success("Evaluasi Selesai!")
                st.write(output)
            else:
                err_msg = res_data.get('error', {}).get('message', 'Terjadi kesalahan pada respon API.')
                st.error(f"Gagal memproses jurnal: {err_msg}")
        except Exception as e:
            st.error(f"Koneksi gagal: {e}")
