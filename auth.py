import sqlite3
import streamlit as st

def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("kanush")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        conn = sqlite3.connect("menu.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        conn.close()
        if user:
            st.session_state['user'] = username
            st.session_state['role'] = user[2]
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")



def login_admin():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "1234":
            return True
        else:
            st.error("Invalid credentials")
    return False
