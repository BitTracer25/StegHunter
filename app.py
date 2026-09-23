import streamlit as st
import os
from stego.engine import StegHunter
from PIL import Image

st.set_page_config(page_title="StegHunter Lite", page_icon="🌐")
st.title("🌐 StegHunter Lite")
st.write("Quick AI check for hidden data.")

uploaded_file = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    temp_path = "temp_lite.png"
    with open(temp_path, "wb") as f: f.write(uploaded_file.getbuffer())
    
    hunter = StegHunter(temp_path)
    res = hunter.run_full_analysis()
    
    if res:
        st.metric("Stego Probability", f"{res['probability']*100:.2f}%")
        st.text_area("LSB Extraction", value=res['lsb_data'], height=100)
    
    os.remove(temp_path)
