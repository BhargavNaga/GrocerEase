from flask import Flask, request, jsonify,render_template
import json

# Importing the necessary modules for database access
from sql_connection import get_sql_connection
import products_dao
import orders_dao
import uom_dao

app = Flask(__name__, static_folder='../ui/static', template_folder='../ui/templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/manage_product')
def manage_product():
    return render_template('manage_product.html')


@app.route('/order')
def order():
    return render_template('order.html')


# Establishing the connection to the database
connection = get_sql_connection()

# Route to get all units of measure (UOM)
@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Route to get all products
@app.route('/getProducts', methods=['GET'])
def get_products():
    response = products_dao.get_all_products(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Route to insert a new product
@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Route to get all orders
@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Route to insert a new order
@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Route to delete a product by its ID
@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server for Grocery Store Management System")
    app.run(port=5000)
