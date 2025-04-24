import qrcode
import os
import streamlit as st
from PIL import Image

APP_BASE_URL = "https://qr-menu-app-ngt9iyrw92m3rknxc85nqm.streamlit.app"

def generate_qr(table_id, show_in_streamlit=True):
    url = f"{APP_BASE_URL}/?table_id={table_id}"
    qr_img = qrcode.make(url)

    # Save locally
    os.makedirs("qr_codes", exist_ok=True)
    path = f"qr_codes/{table_id}.png"
    qr_img.save(path)

    # Only display if Streamlit is running
    if show_in_streamlit:
        st.image(Image.open(path), caption=f"Scan to Order at Table {table_id}", use_container_width=False)
        st.code(url, language="markdown")

    return path
