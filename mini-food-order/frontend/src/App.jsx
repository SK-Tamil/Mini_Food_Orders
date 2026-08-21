import { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "/api";

function App() {
  const [foods, setFoods] = useState([]);
  const [orders, setOrders] = useState([]);

  const [customerName, setCustomerName] = useState("");
  const [selectedFood, setSelectedFood] = useState(null);
  const [quantity, setQuantity] = useState(1);

  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    loadFoods();
    loadOrders();
  }, []);

  async function loadFoods() {
    try {
      const response = await axios.get(`${API_URL}/foods`);
      setFoods(response.data);
    } catch (error) {
      console.error("Failed to load foods:", error);
      setMessage("Unable to load food items.");
    } finally {
      setLoading(false);
    }
  }

  async function loadOrders() {
    try {
      const response = await axios.get(`${API_URL}/orders`);
      setOrders(response.data);
    } catch (error) {
      console.error("Failed to load orders:", error);
    }
  }

  function selectFood(food) {
    setSelectedFood(food);
    setQuantity(1);
    setMessage("");
  }

  async function placeOrder(event) {
    event.preventDefault();

    if (!selectedFood) {
      setMessage("Please select a food item.");
      return;
    }

    if (!customerName.trim()) {
      setMessage("Please enter your name.");
      return;
    }

    try {
      const response = await axios.post(`${API_URL}/orders`, {
        food_id: selectedFood.id,
        customer_name: customerName,
        quantity: quantity
      });

      setMessage(
        `Order #${response.data.order_id} placed successfully!`
      );

      setCustomerName("");
      setSelectedFood(null);
      setQuantity(1);

      loadOrders();
    } catch (error) {
      console.error("Order failed:", error);
      setMessage(
        error.response?.data?.message || "Unable to place order."
      );
    }
  }

  async function cancelOrder(id) {
    try {
      await axios.delete(`${API_URL}/orders/${id}`);
      setMessage("Order cancelled.");
      loadOrders();
    } catch (error) {
      console.error("Cancel failed:", error);
      setMessage("Unable to cancel order.");
    }
  }

  return (
    <div className="app">

      <header className="header">
        <div>
          <h1>🍔 Mini Food Order</h1>
          <p>Fresh food. Simple ordering.</p>
        </div>
      </header>

      <main className="container">

        {message && (
          <div className="message">
            {message}
          </div>
        )}

        <section>
          <h2>Our Menu</h2>

          {loading ? (
            <p>Loading food...</p>
          ) : (
            <div className="food-grid">

              {foods.map((food) => (
                <div className="food-card" key={food.id}>

                  <img
                    src={`/images/${food.image}`}
                    alt={food.name}
                    className="food-image"
                  />

                  <div className="food-content">

                    <span className="category">
                      {food.category}
                    </span>

                    <h3>{food.name}</h3>

                    <p className="price">
                      ₹{Number(food.price).toFixed(2)}
                    </p>

                    <p>
                      {food.available
                        ? "Available"
                        : "Not Available"}
                    </p>

                    <button
                      disabled={!food.available}
                      onClick={() => selectFood(food)}
                    >
                      {food.available
                        ? "Order Now"
                        : "Unavailable"}
                    </button>

                  </div>
                </div>
              ))}

            </div>
          )}
        </section>

        {selectedFood && (
          <section className="order-section">

            <h2>Place Order</h2>

            <div className="selected-food">
              <img
                src={`/images/${selectedFood.image}`}
                alt={selectedFood.name}
              />

              <div>
                <h3>{selectedFood.name}</h3>
                <p>
                  ₹{Number(selectedFood.price).toFixed(2)}
                </p>
              </div>
            </div>

            <form onSubmit={placeOrder}>

              <input
                type="text"
                placeholder="Customer name"
                value={customerName}
                onChange={(e) =>
                  setCustomerName(e.target.value)
                }
              />

              <input
                type="number"
                min="1"
                value={quantity}
                onChange={(e) =>
                  setQuantity(Number(e.target.value))
                }
              />

              <div className="form-buttons">
                <button type="submit">
                  Place Order
                </button>

                <button
                  type="button"
                  className="cancel-button"
                  onClick={() => setSelectedFood(null)}
                >
                  Cancel
                </button>
              </div>

            </form>

          </section>
        )}

        <section className="orders-section">

          <h2>Recent Orders</h2>

          {orders.length === 0 ? (
            <p>No orders yet.</p>
          ) : (
            <div className="orders">

              {orders.map((order) => (
                <div className="order-card" key={order.id}>

                  <div>
                    <h3>
                      Order #{order.id}
                    </h3>

                    <p>
                      {order.food_name}
                    </p>

                    <p>
                      Customer: {order.customer_name}
                    </p>

                    <p>
                      Quantity: {order.quantity}
                    </p>

                    <strong>
                      ₹{Number(order.total_price).toFixed(2)}
                    </strong>
                  </div>

                  <div className="order-right">

                    <span className="status">
                      {order.status}
                    </span>

                    <button
                      className="cancel-button"
                      onClick={() =>
                        cancelOrder(order.id)
                      }
                    >
                      Cancel
                    </button>

                  </div>

                </div>
              ))}

            </div>
          )}

        </section>

      </main>

      <footer>
        <p>Mini Food Order System</p>
      </footer>

    </div>
  );
}

export default App;
