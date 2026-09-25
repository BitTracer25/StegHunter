import streamlit as st
import os
import tempfile
from pathlib import Path
from stego.engine import StegHunter

st.set_page_config(page_title="StegHunter Lite", page_icon="🌐")
st.title("🌐 StegHunter Lite")
st.write("Quick statistical and LSB checks for hidden image data.")

uploaded_file = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    suffix = Path(uploaded_file.name).suffix.lower()
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_path = temp_file.name

        res = StegHunter(temp_path).run_full_analysis()
        if res:
            st.metric("Combined model score (mean)", f"{res['combined_score']*100:.2f}%")
            for model_name, score in res.get("model_scores", {}).items():
                st.metric(f"{model_name.replace('_', ' ').title()} score", f"{score*100:.2f}%")
            if res.get("model_errors"):
                st.warning(f"Some model scores are unavailable: {res.get('model_errors', {})}")
            st.text_area("LSB Extraction", value=res['lsb_data'] or "No message found.", height=100)
        else:
            st.error("Could not analyze this image.")
    except Exception as error:
        st.error(f"Analysis failed: {error}")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
