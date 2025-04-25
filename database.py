import sqlite3
from datetime import datetime

DB_NAME = "menu.db"

# Helper function to execute SELECT queries
def fetch_all(query, params=()):
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute(query, params)]

# ---------------- MENU ----------------
def get_menu_items():
    """Fetches all available menu items"""
    query = "SELECT * FROM menu WHERE available = 1"
    menu_items = fetch_all(query)
    
    # Ensure the image_url is valid, otherwise use a placeholder
    for item in menu_items:
        if not item.get('image_url'):
            item['image_url'] = "https://via.placeholder.com/100"  # Fallback image if not available
    return menu_items

def add_menu_item(name, price, image_url, status):
    """Adds a new menu item to the database"""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO menu (category, name, description, price, image_url, available) VALUES (?, ?, ?, ?, ?, ?)",
            ('Default', name, '', price, image_url, 1 if status == "Available" else 0),
        )
        conn.commit()

def update_menu_item_status(item_id, new_status):
    """Updates the status of a menu item"""
    available = 1 if new_status == 'Available' else 0
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "UPDATE menu SET available = ? WHERE id = ?",
            (available, item_id),
        )
        conn.commit()

# ---------------- ORDERS ----------------
def place_order(table_id, items, instructions):
    """Places a new order in the orders table"""
    item_names = ", ".join([item['name'] for item in items])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Inserting the order into the orders table
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO orders (table_id, items, instructions, status, timestamp) VALUES (?, ?, ?, ?, ?)",
            (table_id, item_names, instructions, "Pending", timestamp),
        )
        conn.commit()
        
def get_orders(status=None):
    """Fetch orders based on their status"""
    if status:
        query = "SELECT * FROM orders WHERE status = ? ORDER BY timestamp DESC"
        return fetch_all(query, (status,))
    else:
        query = "SELECT * FROM orders ORDER BY timestamp DESC"
        return fetch_all(query)

def update_order_status(order_id, new_status):
    """Updates the status of an order"""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "UPDATE orders SET status = ? WHERE id = ?",
            (new_status, order_id),
        )
        conn.commit()
