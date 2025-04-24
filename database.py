# database.py
import sqlite3
import datetime

DB_NAME = "menu.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def get_menu_items():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM menu WHERE status='Available'")
    rows = cur.fetchall()
    return [dict(row) for row in rows]

def place_order(table_id, items, instructions):
    conn = connect_db()
    cur = conn.cursor()
    items_str = ", ".join([item['name'] for item in items])
    cur.execute("INSERT INTO orders (table_id, items, instructions, status, timestamp) VALUES (?, ?, ?, ?, ?)",
                (table_id, items_str, instructions, "Received", datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_orders():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE status != 'Served'")
    rows = cur.fetchall()
    return [dict(row) for row in rows]

def update_order_status(order_id, status):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
    conn.commit()
    conn.close()

def add_menu_item(name, price, image_url, status):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO menu (name, price, image, status) VALUES (?, ?, ?, ?)", (name, price, image_url, status))
    conn.commit()
    conn.close()

def update_menu_item_status(item_id, status):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE menu SET status=? WHERE id=?", (status, item_id))
    conn.commit()
    conn.close()
