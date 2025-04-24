# utils.py
import qrcode
import os
import streamlit as st

# Replace this with your actual Streamlit app base URL after deployment
APP_BASE_URL = "https://qr-menu-app-ngt9iyrw92m3rknxc85nqm.streamlit.app/"

def generate_qr(table_id):
    # Create the full URL for the QR code
    url = f"{APP_BASE_URL}/?table_id={table_id}"

    # Generate the QR code image
    qr = qrcode.make(url)

    # Save it locally (optional - helpful for printing or debugging)
    os.makedirs("qr_codes", exist_ok=True)
    path = f"qr_codes/{table_id}.png"
    qr.save(path)

    # Show in Streamlit
    st.image(qr, caption=f"Scan to Order at Table {table_id}", use_column_width=False)
    st.code(url, language="markdown")  # show the direct link too

    return path

def load_qr_code(table_id):
    return f"qr_codes/{table_id}.png"
