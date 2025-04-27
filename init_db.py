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
    status TEXT DEFAULT 'Received',
    timestamp TEXT
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'staff'))
);
"""

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Create tables
    cur.executescript(schema)

    # Clear old items
    cur.execute("DELETE FROM menu")

    # Insert new menu items
    cur.executemany("INSERT INTO menu (name, price, image, status) VALUES (?, ?, ?, ?)", menu_items)

    # Insert default admin if not exists
    cur.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('admin', '1234', 'admin'))

    conn.commit()
    conn.close()
    print("✅ Database initialized with sample data.")

def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Ensure the 'available' column exists in the 'menu' table
    c.execute('PRAGMA table_info(menu)')
    columns = [column[1] for column in c.fetchall()]
    if 'available' not in columns:
        c.execute('ALTER TABLE menu ADD COLUMN available INTEGER DEFAULT 1')
        print("✅ Added 'available' column to 'menu' table.")

    # Create orders table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_id TEXT,
        items TEXT,
        instructions TEXT,
        status TEXT DEFAULT 'Received',
        timestamp TEXT
    )''')

    # Create menu table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        name TEXT,
        description TEXT,
        price REAL,
        image_url TEXT,
        available INTEGER DEFAULT 1
    )''')

    conn.commit()
    conn.close()

# Run the function to ensure DB is initialized correctly
if __name__ == "__main__":
    initialize_db()

