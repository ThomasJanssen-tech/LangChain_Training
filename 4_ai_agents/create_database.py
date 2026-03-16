import sqlite3

# Databse initieren
db_file = "restaurant.db"

# Verbinding maken met SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Tabel aanmaken als die nog niet bestaat
cursor.execute("""
CREATE TABLE IF NOT EXISTS pizza_menu (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL
)
""")


# Tabel pizzas vullen
cursor.execute("""
INSERT INTO pizza_menu (name, description, price) VALUES
('Margherita', 'Classic pizza with tomato sauce, mozzarella and fresh basil', 8.50),
('Pepperoni', 'Tomato sauce, mozzarella and spicy pepperoni slices', 9.75),
('Hawaiian', 'Tomato sauce, mozzarella, ham and pineapple', 10.00),
('Quattro Formaggi', 'Four cheese pizza with mozzarella, gorgonzola, parmesan and goat cheese', 11.50),
('Vegetarian', 'Tomato sauce, mozzarella, bell peppers, mushrooms, onions and olives', 9.25),
('BBQ Chicken', 'BBQ sauce, mozzarella, grilled chicken, red onion and cilantro', 11.75),
('Diavola', 'Tomato sauce, mozzarella, spicy salami and chili flakes', 10.50),
('Prosciutto Funghi', 'Tomato sauce, mozzarella, ham and mushrooms', 10.25),
('Capricciosa', 'Tomato sauce, mozzarella, ham, artichokes, olives and mushrooms', 11.00),
('Truffle Deluxe', 'Mozzarella, mushrooms and truffle oil', 13.50);
""")



# Tabel aanmaken als die nog niet bestaat
cursor.execute("""
CREATE TABLE IF NOT EXISTS restaurant_details (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    opening_hours TEXT
)
""")

# restaurant details invullen
cursor.execute("""
INSERT INTO restaurant_details (name, address, opening_hours)
VALUES
('Luigi''s Pizza Palace', 'Via Roma 12, Amsterdam, Netherlands', 'Mon-Sun: 11:00 - 23:00')
""")

# Tabel aanmaken als die nog niet bestaat
cursor.execute("""
CREATE TABLE IF NOT EXISTS restaurant_orders (
    id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    order_time TEXT
)
""")

# Tabel aanmaken als die nog niet bestaat
cursor.execute("""
CREATE TABLE IF NOT EXISTS restaurant_orders_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    pizza_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES restaurant_orders(id),
    FOREIGN KEY (pizza_id) REFERENCES pizza_menu(id)
)
""")

conn.commit()
conn.close()