import json
import mysql.connector

# Function to connect to MySQL database
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="petlebi"
        )
        return conn
    except mysql.connector.Error as err:
        print("Error:", err)

def insert_data(conn, data):
    try:
        cursor = conn.cursor()
        # Check if product_id already exists in the table
        cursor.execute("SELECT * FROM petlebi WHERE product_id = %s", (data['product_id'],))
        existing_product = cursor.fetchone()

        # If the product_id already exists, do not insert
        if existing_product:
            print("Product already exists with the same product_id.")
            return

        # Insert the data into the petlebi table
        sql = """INSERT INTO petlebi (product_url, product_name, product_barcode, product_price, product_stock, description, product_id, brand, category, sku)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (data['product_url'], data['product_name'], data['product_barcode'], data['product_price'], data['product_stock'], data['description'], data['product_id'], data['brand'], data['category'], data['sku'])
        cursor.execute(sql, values)
        conn.commit()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()


# Main function
def main():
    # Load data from JSON file
    with open('petlebi_products.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Connect to MySQL database
    conn = connect_to_database()

    # Insert data into the petlebi table
    if conn:
        for item in data:
            insert_data(conn, item)
        conn.close()
    else:
        print("Connection to database failed.")

if __name__ == "__main__":
    main()
