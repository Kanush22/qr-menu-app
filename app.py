# app.py
import streamlit as st
from utils import generate_qr
from database import get_menu_items, place_order, get_orders, update_order_status, add_menu_item, update_menu_item_status
from auth import login_admin

st.set_page_config(page_title="QR Menu App", layout="wide")

menu = ["Customer View", "Restaurant Dashboard", "Admin Panel"]
choice = st.sidebar.selectbox("Navigate", menu)

if choice == "Customer View":
    st.header("📱 Customer Menu")
    table_id = st.text_input("Enter Table ID (from QR):")
    if table_id:
        items = get_menu_items()
        selected_items = []
        for item in items:
            st.image(item['image'], width=100)
            if st.checkbox(f"{item['name']} - ₹{item['price']}", key=item['id']):
                selected_items.append(item)
        special_instructions = st.text_area("Special Instructions")
        if st.button("Place Order"):
            place_order(table_id, selected_items, special_instructions)
            st.success("Order placed!")

elif choice == "Restaurant Dashboard":
    st.header("🧾 Incoming Orders")
    orders = get_orders()
    for order in orders:
        st.write(f"Order #{order['id']} | Table: {order['table_id']} | Items: {order['items']} | Instructions: {order['instructions']} | Status: {order['status']} | Time: {order['timestamp']}")
        if st.button("Mark as Served", key=order['id']):
            update_order_status(order['id'], "Served")
            st.success(f"Order #{order['id']} marked as Served")

elif choice == "Admin Panel":
    if login_admin():
        st.success("Logged in as Admin")
        st.subheader("Manage Menu")
        name = st.text_input("Item Name")
        price = st.number_input("Price", min_value=0.0)
        image_url = st.text_input("Image URL")
        status = st.selectbox("Status", ["Available", "Out of Stock"])
        if st.button("Add Menu Item"):
            add_menu_item(name, price, image_url, status)
            st.success("Item added!")

        st.subheader("Update Item Status")
        item_id = st.number_input("Item ID", min_value=1)
        new_status = st.selectbox("New Status", ["Available", "Out of Stock"])
        if st.button("Update Status"):
            update_menu_item_status(item_id, new_status)
            st.success("Item status updated!")