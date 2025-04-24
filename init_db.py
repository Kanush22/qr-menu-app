import sqlite3

DB_NAME = "menu.db"

menu_items = [
    ("Masala Dosa", 50, "https://i.imgur.com/z9b1ulR.jpg", "Available"),
    ("Idli Vada Sambar", 40, "https://i.imgur.com/xsOvSBZ.jpg", "Available"),
    ("Upma", 30, "https://i.imgur.com/DqOcHzo.jpg", "Available"),
    ("Medu Vada", 35, "https://i.imgur.com/YvRaEzV.jpg", "Available"),
    ("Pongal", 45, "https://i.imgur.com/j2CcoBt.jpg", "Available"),
    ("Rava Kesari", 25, "https://i.imgur.com/xK9HOVF.jpg", "Available"),
    ("Poori Kurma", 50, "https://i.imgur.com/PEQ5r5N.jpg", "Available"),
    ("Uttapam", 40, "https://i.imgur.com/MzN7cWS.jpg", "Available")
]

schema = """
CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    image TEXT,
    status TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_id TEXT NOT NULL,
    items TEXT NOT NULL,
    instructions TEXT,
    status TEXT,
    timestamp TEXT
);
"""

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Create tables first
    cur.executescript(schema)

    # Then ensure columns exist (redundant now, since we're recreating schema, but kept for safety)
    cur.execute("PRAGMA table_info(menu)")
    columns = [column[1] for column in cur.fetchall()]
    if 'status' not in columns:
        cur.execute("ALTER TABLE menu ADD COLUMN status TEXT")
        print("✅ Added missing 'status' column to 'menu' table.")
    if 'image' not in columns:
        cur.execute("ALTER TABLE menu ADD COLUMN image TEXT")
        print("✅ Added missing 'image' column to 'menu' table.")

    # Clear old items
    cur.execute("DELETE FROM menu")

    # Insert new menu items
    cur.executemany("INSERT INTO menu (name, price, image, status) VALUES (?, ?, ?, ?)", menu_items)

    conn.commit()
    conn.close()
    print("✅ South Indian menu added successfully.")

if __name__ == "__main__":
    init_db()




def initialize_db():
    conn = sqlite3.connect("menu.db")
    c = conn.cursor()

    # Create orders table
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_id TEXT,
            items TEXT,
            instructions TEXT,
            status TEXT DEFAULT 'Received',
            timestamp TEXT
        )
    ''')

    # Create menu table
    c.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            name TEXT,
            description TEXT,
            price REAL,
            image_url TEXT,
            available INTEGER DEFAULT 1
        )
    ''')

    conn.commit()
    conn.close()

# Optional: Run it directly to test
if __name__ == "__main__":
    initialize_db()
