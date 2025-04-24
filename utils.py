# utils.py
import qrcode
import os

def generate_qr(table_id):
    url = f"https://qrmenuapp.com/?table={table_id}"
    qr = qrcode.make(url)
    os.makedirs("qr_codes", exist_ok=True)
    path = f"qr_codes/{table_id}.png"
    qr.save(path)
    return path

def load_qr_code(table_id):
    return f"qr_codes/{table_id}.png"


# auth.py
import streamlit as st

def login_admin():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "1234":
            return True
        else:
            st.error("Invalid credentials")
    return False
