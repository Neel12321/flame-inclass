from flask import Flask, jsonify, request

# Initialize the app
app = Flask(__name__)

# In-memory cart for demo purposes
cart = []

# Dummy data: cafes and menus
cafes = {
    "Cafe One": ["Coffee", "Sandwich", "Muffin"],
    "Cafe Two": ["Tea", "Burger", "Fries"],
    "Cafe Three": ["Pizza", "Pasta", "Salad"]
}


@app.route("/cafes/list", methods=["GET"])
def list_cafes():
    """Return the available cafes as JSON"""
    return jsonify(cafes)


@app.route("/cafe/<name>", methods=["GET"])
def show_cafe(name):
    """Return menu for a given cafe or 404 if not found"""
    menu = cafes.get(name)
    if menu is None:
        return jsonify({"error": "Cafe not found"}), 404
    return jsonify(menu)


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    """Add an item to the cart.

    Expects JSON body: {"cafe": "Cafe One", "item": "Coffee"}
    """
    data = request.get_json() or {}
    cafe = data.get("cafe")
    item = data.get("item")

    if not cafe or not item:
        return jsonify({"error": "Both 'cafe' and 'item' are required"}), 400

    if cafe not in cafes or item not in cafes[cafe]:
        return jsonify({"error": "Invalid cafe or item"}), 400

    entry = {"cafe": cafe, "item": item}
    cart.append(entry)
    return jsonify(cart), 201


@app.route("/cart", methods=["GET"])
def view_cart():
    """Return current cart contents"""
    return jsonify(cart)


@app.route("/delete_from_cart/<cafe>/<item>", methods=["DELETE"])
def delete_from_cart(cafe, item):
    """Remove the first matching item from the cart"""
    for entry in cart[:]:
        if entry.get("cafe") == cafe and entry.get("item") == item:
            cart.remove(entry)
            return jsonify(cart), 200
    return jsonify({"error": "Item not found"}), 404


@app.route("/checkout", methods=["POST"])
def checkout():
    """Clear the cart (no real payment)"""
    cart.clear()
    return jsonify({"message": "Thanks for ordering! Your cart is now empty."}), 200


if __name__ == "__main__":
    app.run(debug=True)
