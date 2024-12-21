from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    categories = conn.execute("SELECT category, COUNT(*) as cnt FROM products GROUP BY category").fetchall()
    # Fetch all products
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template('home.html', categories=categories, products=products)

@app.route('/search')
def search():
    query = request.args.get('q', '')

    conn = get_db_connection()
    # Search in all attributes: ad_no, description, price, city, category
    products = conn.execute("""
        SELECT * FROM products
        WHERE ad_no LIKE ? 
        OR description LIKE ?
        OR price LIKE ?
        OR city LIKE ?
        OR category LIKE ?
    """, (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%')).fetchall()
    conn.close()

    return render_template('search.html', products=products, query=query)

@app.route('/detail/<ad_no>')
def detail(ad_no):
    conn = get_db_connection()
    product = conn.execute("SELECT * FROM products WHERE ad_no = ?", (ad_no,)).fetchone()
    conn.close()

    if product is None:
        # Handle not found
        return "Product not found", 404

    return render_template('detail.html', product=product)


if __name__ == '__main__':
    app.run(debug=False) 