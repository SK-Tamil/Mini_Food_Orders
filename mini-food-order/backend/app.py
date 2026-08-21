from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# =====================================================
# DATABASE CONFIGURATION
# =====================================================

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://"
    f"{os.getenv('DB_USER', 'fooduser')}:"
    f"{os.getenv('DB_PASSWORD', 'foodpassword')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '3306')}/"
    f"{os.getenv('DB_NAME', 'fooddb')}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =====================================================
# FOOD MODEL
# =====================================================

class Food(db.Model):
    __tablename__ = "foods"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    available = db.Column(db.Boolean, default=True)


# =====================================================
# ORDER MODEL
# =====================================================

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    food_id = db.Column(
        db.Integer,
        db.ForeignKey("foods.id"),
        nullable=False
    )

    customer_name = db.Column(
        db.String(100),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    total_price = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


# =====================================================
# HEALTH CHECK
# =====================================================

@app.route("/api", methods=["GET"])
def health():

    return jsonify({
        "message": "Mini Food Order API",
        "status": "healthy"
    })


# =====================================================
# HOME
# =====================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Mini Food Order API is running"
    })


# =====================================================
# FOOD APIs
# =====================================================

# GET ALL FOODS

@app.route("/api/foods", methods=["GET"])
def get_foods():

    foods = Food.query.all()

    result = []

    for food in foods:

        result.append({
            "id": food.id,
            "name": food.name,
            "category": food.category,
            "price": food.price,
            "image": food.image,
            "available": food.available
        })

    return jsonify(result)


# GET SINGLE FOOD

@app.route("/api/foods/<int:id>", methods=["GET"])
def get_food(id):

    food = Food.query.get(id)

    if not food:
        return jsonify({
            "message": "Food not found"
        }), 404

    return jsonify({
        "id": food.id,
        "name": food.name,
        "category": food.category,
        "price": food.price,
        "image": food.image,
        "available": food.available
    })


# ADD FOOD

@app.route("/api/foods", methods=["POST"])
def add_food():

    data = request.get_json()

    food = Food(
        name=data["name"],
        category=data["category"],
        price=data["price"],
        image=data.get("image"),
        available=data.get("available", True)
    )

    db.session.add(food)
    db.session.commit()

    return jsonify({
        "message": "Food added successfully",
        "id": food.id
    }), 201


# UPDATE FOOD

@app.route("/api/foods/<int:id>", methods=["PUT"])
def update_food(id):

    food = Food.query.get(id)

    if not food:
        return jsonify({
            "message": "Food not found"
        }), 404

    data = request.get_json()

    food.name = data["name"]
    food.category = data["category"]
    food.price = data["price"]
    food.image = data.get("image", food.image)
    food.available = data.get(
        "available",
        food.available
    )

    db.session.commit()

    return jsonify({
        "message": "Food updated successfully"
    })


# DELETE FOOD

@app.route("/api/foods/<int:id>", methods=["DELETE"])
def delete_food(id):

    food = Food.query.get(id)

    if not food:
        return jsonify({
            "message": "Food not found"
        }), 404

    db.session.delete(food)
    db.session.commit()

    return jsonify({
        "message": "Food deleted successfully"
    })


# =====================================================
# ORDER APIs
# =====================================================

# GET ALL ORDERS

@app.route("/api/orders", methods=["GET"])
def get_orders():

    orders = Order.query.all()

    result = []

    for order in orders:

        food = Food.query.get(order.food_id)

        result.append({
            "id": order.id,
            "food_id": order.food_id,
            "food_name": food.name if food else None,
            "food_image": food.image if food else None,
            "customer_name": order.customer_name,
            "quantity": order.quantity,
            "total_price": order.total_price,
            "status": order.status,
            "created_at": order.created_at
        })

    return jsonify(result)


# GET SINGLE ORDER

@app.route("/api/orders/<int:id>", methods=["GET"])
def get_order(id):

    order = Order.query.get(id)

    if not order:
        return jsonify({
            "message": "Order not found"
        }), 404

    food = Food.query.get(order.food_id)

    return jsonify({
        "id": order.id,
        "food_id": order.food_id,
        "food_name": food.name if food else None,
        "customer_name": order.customer_name,
        "quantity": order.quantity,
        "total_price": order.total_price,
        "status": order.status,
        "created_at": order.created_at
    })


# PLACE ORDER

@app.route("/api/orders", methods=["POST"])
def add_order():

    data = request.get_json()

    food = Food.query.get(data["food_id"])

    if not food:
        return jsonify({
            "message": "Food not found"
        }), 404

    if not food.available:

        return jsonify({
            "message": "Food is not available"
        }), 400

    try:
        quantity = int(data["quantity"])
    except (TypeError, ValueError):

        return jsonify({
            "message": "Quantity must be a valid number"
        }), 400

    if quantity <= 0:

        return jsonify({
            "message": "Quantity must be greater than zero"
        }), 400

    total_price = food.price * quantity

    order = Order(
        food_id=food.id,
        customer_name=data["customer_name"],
        quantity=quantity,
        total_price=total_price,
        status="Pending"
    )

    db.session.add(order)
    db.session.commit()

    return jsonify({
        "message": "Order placed successfully",
        "order_id": order.id,
        "total_price": total_price
    }), 201


# UPDATE ORDER STATUS

@app.route("/api/orders/<int:id>", methods=["PUT"])
def update_order(id):

    order = Order.query.get(id)

    if not order:

        return jsonify({
            "message": "Order not found"
        }), 404

    data = request.get_json()

    allowed_statuses = [
        "Pending",
        "Preparing",
        "Ready",
        "Completed",
        "Cancelled"
    ]

    status = data.get("status")

    if status not in allowed_statuses:

        return jsonify({
            "message": "Invalid order status"
        }), 400

    order.status = status

    db.session.commit()

    return jsonify({
        "message": "Order status updated successfully"
    })


# CANCEL / DELETE ORDER

@app.route("/api/orders/<int:id>", methods=["DELETE"])
def delete_order(id):

    order = Order.query.get(id)

    if not order:

        return jsonify({
            "message": "Order not found"
        }), 404

    db.session.delete(order)
    db.session.commit()

    return jsonify({
        "message": "Order cancelled successfully"
    })


# =====================================================
# CREATE DATABASE TABLES
# =====================================================

with app.app_context():
    db.create_all()


# =====================================================
# LOCAL DEVELOPMENT
# =====================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
