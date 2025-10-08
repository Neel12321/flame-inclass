from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flasgger import Swagger

# Initialize the app
app = Flask(__name__)
swagger = Swagger(app)
cart = []

# Dummy data: cafes and menus
cafes = {
    "Cafe One": ["Coffee", "Sandwich", "Muffin"],
    "Cafe Two": ["Tea", "Burger", "Fries"],
    "Cafe Three": ["Pizza", "Pasta", "Salad"]
}

@app.route("/cafes/list",methods=["GET"])
def list_cafes():
    """
    Show list of cafes
    ---
    responses:
      200:
        description: A list of cafes
        examples:
          application/json: {"Cafe One": ["Coffee", "Sandwich", "Muffin"], "Cafe Two": ["Tea", "Burger", "Fries"], "Cafe Three": ["Pizza", "Pasta", "Salad"]}
    """
    return jsonify(cafes)

@app.route("/cafe/<name>", methods=["GET"])
def show_cafe(name):
    """Show menu of a cafe"""
    menu = cafes.get(name, [])
    return jsonify(menu)

@app.route("/add_to_cart",methods=["POST"])
def add_to_cart():
    """
    Add an item to cart
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            cafe:
              type: string
            item:
              type: string
    responses:
      201:
        description: Details of cart
    """
    data = request.get_json()
    #I'm actually not checking if the item is present in the cafe!
    #This check has to be done. Skipping for now
    cart.append({"cafe": data["cafe"], "item": data["item"]})
    return jsonify(cart), 201

@app.route("/cart",methods=["GET"])
def view_cart():
    """
    View Items in Cart
    ---
    responses:
      200:
        description: Current Items in Cart
        examples:
          application/json: [{"cafe": "Cafe One", "item": "Coffee"},{"cafe": "Cafe Two", "item": "Burger"}]
    """
    return jsonify(cart)

@app.route("/delete_from_cart/<cafe>/<item>",methods=["DELETE"])
def delete_from_cart(cafe, item):
    """Add an item to the cart (stored in session)"""
    for item in cart:
        for c,i in item.items():
            if c==cafe and i==item:
                del cart[item][c]
                return jsonify(cart), 201
    return ("Item not found",404)
    

@app.route("/checkout",methods=["POST"])
def checkout():
    """Clear the cart (no real payment)"""
    cart.clear()
    return ("Thanks for ordering! Your cart is now empty.",201)
    
# if __name__ == "__main__":
#     app.run(debug=True)
