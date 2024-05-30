from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
firebase_url = "https://integracioncasoapis-default-rtdb.firebaseio.com/inventario"

@app.route('/get_product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    response = requests.get(f"{firebase_url}/{product_id}.json")
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route('/update_product', methods=['POST'])
def update_product():
    data = request.json
    product_id = data.get('id')
    update_quantity = data.get('cantidad')

    if product_id is None or update_quantity is None:
        return jsonify({"error": "Missing id or cantidad"}), 400

    # Get current product data
    response = requests.get(f"{firebase_url}/{product_id}.json")
    if response.status_code == 200:
        product_data = response.json()
        new_quantity = product_data['cantidad'] - update_quantity
        if new_quantity < 0:
            return jsonify({"error": "Insufficient quantity"}), 400
        
        product_data['cantidad'] = new_quantity

        # Update product data
        update_response = requests.put(f"{firebase_url}/{product_id}.json", json=product_data)
        if update_response.status_code == 200:
            return jsonify(product_data)
        else:
            return jsonify({"error": "Failed to update product"}), 500
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
