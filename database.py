import sqlite3
from datetime import datetime, time

DB_NAME = "menu.db"

# ---------------- HELPER FUNCTIONS ----------------
def fetch_all(query, params=()):
    """Execute SELECT query and return list of dict rows"""
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute(query, params)]

# ---------------- TIME-BASED CATEGORY DETERMINATION ----------------
def get_current_meal_category():
    """Determine the current meal category based on time of day"""
    current_time = datetime.now().time()
    
    # Get restaurant timings
    restaurant_timings = get_restaurant_timings()
    
    # Parse restaurant hours
    try:
        open_time = datetime.strptime(restaurant_timings['open_time'], '%I:%M %p').time()
        close_time = datetime.strptime(restaurant_timings['close_time'], '%I:%M %p').time()
    except (KeyError, ValueError):
        # Default times if parsing fails
        open_time = time(8, 0)  # 8:00 AM
        close_time = time(22, 0)  # 10:00 PM
    
    # Define meal time boundaries
    breakfast_end = time(11, 30)  # 11:30 AM
    lunch_end = time(16, 0)  # 4:00 PM
    
    # Check if restaurant is closed
    if current_time < open_time or current_time > close_time:
        return None
    
    # Determine meal category
    if current_time < breakfast_end:
        return "Breakfast"
    elif current_time < lunch_end:
        return "Lunch"
    else:
        return "Dinner"

# ---------------- MENU ----------------
def get_menu_items(category=None, respect_time=True):
    """
    Fetches menu items based on category (Breakfast, Lunch, Dinner)
    If respect_time is True, only returns items for the current time period
    """
    if respect_time and category is None:
        # Determine current meal category based on time
        category = get_current_meal_category()
        
        # If restaurant is closed
        if category is None:
            print("Restaurant is currently closed.")
            return []
    
    if category:
        query = "SELECT * FROM menu WHERE category = ? AND available = 1"
        menu_items = fetch_all(query, (category,))
    else:
        query = "SELECT * FROM menu WHERE available = 1"
        menu_items = fetch_all(query)

    print(f"Fetched {len(menu_items)} menu items for {'current time period' if respect_time else 'all categories'}.")
    
    # Ensure the image_url is valid
    for item in menu_items:
        if not item.get('image_url'):
            item['image_url'] = "https://via.placeholder.com/100"
    return menu_items

def add_menu_item(name, price, image_url, category, status):
    """Adds a new menu item to the database"""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO menu (category, name, description, price, image_url, available) VALUES (?, ?, ?, ?, ?, ?)",
            (category, name, '', price, image_url, 1 if status == "Available" else 0),
        )
        conn.commit()

def update_menu_item_status(item_id, new_status):
    """Updates the availability status of a menu item"""
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

# ---------------- RESTAURANT TIMINGS ----------------
def get_restaurant_timings():
    """Fetch the restaurant timings"""
    query = "SELECT * FROM timings WHERE id = 1"
    timings = fetch_all(query)
    return timings[0] if timings else {}

def update_restaurant_timings(open_time, close_time):
    """Update the restaurant timings"""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "UPDATE timings SET open_time = ?, close_time = ? WHERE id = 1",
            (open_time, close_time),
        )
        conn.commit()

# ---------------- MEAL TIMINGS ----------------
def get_meal_timings():
    """Fetch the meal serving timings"""
    query = "SELECT * FROM meal_timings WHERE id = 1"
    timings = fetch_all(query)
    return timings[0] if timings else {}

def update_meal_timings(breakfast_start, breakfast_end, lunch_start, lunch_end, dinner_start, dinner_end):
    """Update the meal serving timings"""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            """UPDATE meal_timings SET 
               breakfast_start = ?, breakfast_end = ?, 
               lunch_start = ?, lunch_end = ?,
               dinner_start = ?, dinner_end = ? 
               WHERE id = 1""",
            (breakfast_start, breakfast_end, lunch_start, lunch_end, dinner_start, dinner_end),
        )
        conn.commit()

# ---------------- DATABASE INITIALIZATION ----------------
def initialize_db():
    """Ensure database tables are created and initialized"""
    schema = """
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        image_url TEXT,
        available INTEGER DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_id TEXT NOT NULL,
        items TEXT NOT NULL,
        instructions TEXT,
        status TEXT DEFAULT 'Received',
        timestamp TEXT
    );

    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin', 'staff'))
    );

    CREATE TABLE IF NOT EXISTS timings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        open_time TEXT NOT NULL,
        close_time TEXT NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS meal_timings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        breakfast_start TEXT NOT NULL,
        breakfast_end TEXT NOT NULL,
        lunch_start TEXT NOT NULL,
        lunch_end TEXT NOT NULL,
        dinner_start TEXT NOT NULL,
        dinner_end TEXT NOT NULL
    );
    """

    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.executescript(schema)

        # Initialize restaurant timings
        c.execute("SELECT COUNT(*) FROM timings WHERE id = 1")
        if c.fetchone()[0] == 0:
            c.execute("INSERT INTO timings (open_time, close_time) VALUES (?, ?)", ('08:00 AM', '10:00 PM'))
            
        # Initialize meal timings
        c.execute("SELECT COUNT(*) FROM meal_timings WHERE id = 1")
        if c.fetchone()[0] == 0:
            c.execute("""
                INSERT INTO meal_timings 
                (breakfast_start, breakfast_end, lunch_start, lunch_end, dinner_start, dinner_end) 
                VALUES (?, ?, ?, ?, ?, ?)
                """, 
                ('08:00 AM', '11:30 AM', '11:30 AM', '04:00 PM', '04:00 PM', '10:00 PM'))

        # Initialize default admin user
        c.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        if c.fetchone()[0] == 0:
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('admin', '1234', 'admin'))

        # Insert default menu items if not present
        sample_items = [
            ("Breakfast", "Masala Dosa", 50, "https://i.imgur.com/z9b1ulR.jpg", 1),
            ("Breakfast", "Idli Vada Sambar", 40, "https://i.imgur.com/xsOvSBZ.jpg", 1),
            ("Breakfast", "Upma", 35, "https://i.imgur.com/dT9jU3k.jpg", 1),
            ("Breakfast", "Pongal", 45, "https://i.imgur.com/A4FQhRf.jpg", 1),
            ("Lunch", "Vegetable Biryani", 80, "https://i.imgur.com/ufbG5LT.jpg", 1),
            ("Lunch", "Paneer Butter Masala", 100, "https://i.imgur.com/RyRlmG3.jpg", 1),
            ("Lunch", "Chole Bhature", 75, "https://i.imgur.com/FLHADNW.jpg", 1),
            ("Dinner", "Paneer Tikka", 90, "https://i.imgur.com/BqX0nz3.jpg", 1),
            ("Dinner", "Butter Naan", 25, "https://i.imgur.com/tTY6Ryr.jpg", 1),
            ("Dinner", "Pasta Alfredo", 95, "https://i.imgur.com/TJeAQnY.jpg", 1),
        ]

        for category, name, price, image_url, available in sample_items:
            c.execute("SELECT COUNT(*) FROM menu WHERE name = ? AND category = ?", (name, category))
            if c.fetchone()[0] == 0:
                c.execute(
                    "INSERT INTO menu (category, name, description, price, image_url, available) VALUES (?, ?, ?, ?, ?, ?)",
                    (category, name, '', price, image_url, available)
                )

        conn.commit()

    print("✅ Database initialized successfully")

# ---------------- RUN INITIALIZATION ----------------
if __name__ == "__main__":
    initialize_db()

    # Optional: print available items for testing
    print("\n-- Available Menu Items --")
    current_category = get_current_meal_category()
    print(f"\nCurrent time category: {current_category}")
    if current_category:
        items = get_menu_items(current_category)
        for item in items:
            print(f"- {item['name']} | ₹{item['price']} | Available: {bool(item['available'])}")
    else:
        print("Restaurant is currently closed.")