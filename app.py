import streamlit as st
from utils import generate_qr  # Only import generate_qr here
from database import get_menu_items, place_order, get_orders, update_order_status, add_menu_item, update_menu_item_status
from auth import login_admin
from init_db import initialize_db

# Initialize database
initialize_db()

# Streamlit page config
st.set_page_config(page_title="QR Menu App", layout="wide")

# Parse table_id from URL
query_params = st.query_params
table_id_param = query_params.get("table_id", [None])[0]

# Navigation menu
menu = ["Customer View", "Restaurant Dashboard", "Admin Panel"]
choice = st.sidebar.selectbox("Navigate", menu)

# ---------------- CUSTOMER VIEW ----------------
if choice == "Customer View":
    st.header("📱 Customer Menu")

    table_id = table_id_param or st.text_input("Enter Table ID (from QR):")

    if table_id:
        items = get_menu_items()
        selected_items = []

        for item in items:
            st.image(item['image_url'], width=100)
            if st.checkbox(f"{item['name']} - ₹{item['price']}", key=f"{item['id']}_{table_id}"):
                selected_items.append(item)

        special_instructions = st.text_area("Special Instructions")

        if st.button("Place Order"):
            if selected_items:
                place_order(table_id, selected_items, special_instructions)
                st.success("✅ Order placed!")
            else:
                st.warning("Please select at least one item to order.")

# ---------------- RESTAURANT DASHBOARD ----------------
elif choice == "Restaurant Dashboard":
    st.header("🧾 Incoming Orders")
    
    # Only fetch orders with status "Pending" or "Received"
    orders = get_orders(status="Pending")  # Modify get_orders to accept status filter

    if not orders:
        st.info("No orders yet.")
    else:
        for order in orders:
            with st.expander(f"Order #{order['id']} | Table {order['table_id']}"):
                st.markdown(f"**Items**: {order['items']}")
                st.markdown(f"**Instructions**: {order['instructions']}")
                st.markdown(f"**Status**: {order['status']}")
                st.markdown(f"**Time**: {order['timestamp']}")

                if st.button("Mark as Served", key=f"serve_{order['id']}"):
                    update_order_status(order['id'], "Served")
                    st.success(f"✅ Order #{order['id']} marked as Served")

    # Fetch and display served orders (optional)
    served_orders = get_orders(status="Served")  # Fetch orders that are already served
    if served_orders:
        with st.expander("🔒 Served Orders"):
            for order in served_orders:
                st.markdown(f"**Order #{order['id']} | Table {order['table_id']}**")
                st.markdown(f"**Items**: {order['items']}")
                st.markdown(f"**Status**: {order['status']}")
                st.markdown(f"**Time**: {order['timestamp']}")

# ---------------- ADMIN PANEL ----------------
elif choice == "Admin Panel":
    if login_admin():
        st.success("✅ Logged in as Admin")

        # Add Menu Item
        st.subheader("➕ Add Menu Item")
        name = st.text_input("Item Name")
        price = st.number_input("Price (₹)", min_value=0.0)
        image_url = st.text_input("Image URL")
        status = st.selectbox("Status", ["Available", "Out of Stock"])

        if st.button("Add Menu Item"):
            if name and image_url:
                add_menu_item(name, price, image_url, status)
                st.success(f"✅ '{name}' added to menu.")
            else:
                st.error("Please provide name and image URL.")

        # Update Item Status
        st.subheader("🔄 Update Menu Item Status")
        item_id = st.number_input("Item ID", min_value=1, step=1)
        new_status = st.selectbox("New Status", ["Available", "Out of Stock"])

        if st.button("Update Status"):
            update_menu_item_status(item_id, new_status)
            st.success(f"✅ Item #{item_id} status updated to {new_status}.")

        # Generate QR Code
        st.subheader("📎 Generate QR Code for Table")
        qr_table_id = st.text_input("Enter Table ID to generate QR Code")
        if st.button("Generate QR Code"):
            if qr_table_id.strip():
                qr_image_path = generate_qr(qr_table_id, show_in_streamlit=False)
                st.image(qr_image_path, caption=f"QR Code for Table {qr_table_id}")
                st.success("✅ QR Code generated successfully!")
            else:
                st.error("Please enter a valid Table ID.")
