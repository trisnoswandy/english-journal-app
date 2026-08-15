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
        # Daftar nama model resmi yang didukung Google AI Studio
        models_to_try = [
            "gemini-1.5-flash",
            "gemini-2.0-flash",
            "gemini-1.5-pro"
        ]
        
        success = False
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": f"Evaluasi jurnal berikut dalam 12 poin:\n\n{journal_text}"}]
            }]
        }
        
        for model_name in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key.strip()}"
            try:
                response = requests.post(url, headers=headers, json=payload)
                res_data = response.json()
                
                if response.status_code == 200 and 'candidates' in res_data:
                    output = res_data['candidates'][0]['content']['parts'][0]['text']
                    st.success(f"Evaluasi Selesai (Menggunakan model: {model_name})!")
                    st.write(output)
                    success = True
                    break
            except Exception:
                continue

        if not success:
            st.error("Gagal memproses jurnal. Pastikan API Key yang dimasukkan benar dan aktif.")
                continue

        if not success:
            st.error("Gagal memproses jurnal. Pastikan API Key yang dimasukkan benar dan aktif.")
