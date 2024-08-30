import sqlite3
from datetime import datetime

# Initialize the database
def initialize_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Create products table
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        price REAL NOT NULL)''')
    
    # Create sales table
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY,
                        product_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        sale_date TEXT NOT NULL,
                        FOREIGN KEY(product_id) REFERENCES products(id))''')
    
    conn.commit()
    conn.close()

# Add a new product
def add_product(name, quantity, price):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)', 
                   (name, quantity, price))
    
    conn.commit()
    conn.close()

# Update product details
def update_product(product_id, name=None, quantity=None, price=None):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    if name:
        cursor.execute('UPDATE products SET name = ? WHERE id = ?', (name, product_id))
    if quantity is not None:
        cursor.execute('UPDATE products SET quantity = ? WHERE id = ?', (quantity, product_id))
    if price is not None:
        cursor.execute('UPDATE products SET price = ? WHERE id = ?', (price, product_id))
    
    conn.commit()
    conn.close()

# Delete a product
def delete_product(product_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    
    conn.commit()
    conn.close()

# Record a sale
def record_sale(product_id, quantity):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Check if enough inventory is available
    cursor.execute('SELECT quantity FROM products WHERE id = ?', (product_id,))
    current_quantity = cursor.fetchone()[0]
    
    if current_quantity >= quantity:
        # Update inventory
        new_quantity = current_quantity - quantity
        cursor.execute('UPDATE products SET quantity = ? WHERE id = ?', (new_quantity, product_id))
        
        # Record the sale
        sale_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO sales (product_id, quantity, sale_date) VALUES (?, ?, ?)', 
                       (product_id, quantity, sale_date))
        
        conn.commit()
        print("Sale recorded successfully.")
    else:
        print("Error: Insufficient inventory.")
    
    conn.close()

# Generate inventory report
def generate_inventory_report():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    
    print("\nInventory Report:")
    print("ID | Name | Quantity | Price")
    for product in products:
        print(f"{product[0]} | {product[1]} | {product[2]} | {product[3]}")
    
    conn.close()

# Generate sales report
def generate_sales_report():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('''SELECT sales.id, products.name, sales.quantity, sales.sale_date 
                      FROM sales 
                      JOIN products ON sales.product_id = products.id''')
    sales = cursor.fetchall()
    
    print("\nSales Report:")
    print("Sale ID | Product Name | Quantity Sold | Sale Date")
    for sale in sales:
        print(f"{sale[0]} | {sale[1]} | {sale[2]} | {sale[3]}")
    
    conn.close()

# Main function
def main():
    initialize_db()
    while True:
        print("\nInventory Management System")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. Record Sale")
        print("5. Generate Inventory Report")
        print("6. Generate Sales Report")
        print("7. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter product name: ")
            quantity = int(input("Enter product quantity: "))
            price = float(input("Enter product price: "))
            add_product(name, quantity, price)
        elif choice == '2':
            product_id = int(input("Enter product ID to update: "))
            name = input("Enter new name (leave blank to keep unchanged): ")
            quantity = input("Enter new quantity (leave blank to keep unchanged): ")
            price = input("Enter new price (leave blank to keep unchanged): ")
            update_product(product_id, name or None, int(quantity) if quantity else None, float(price) if price else None)
        elif choice == '3':
            product_id = int(input("Enter product ID to delete: "))
            delete_product(product_id)
        elif choice == '4':
            product_id = int(input("Enter product ID to sell: "))
            quantity = int(input("Enter quantity to sell: "))
            record_sale(product_id, quantity)
        elif choice == '5':
            generate_inventory_report()
        elif choice == '6':
            generate_sales_report()
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
