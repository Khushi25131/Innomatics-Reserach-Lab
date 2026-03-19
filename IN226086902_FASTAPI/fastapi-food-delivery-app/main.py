from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

# -------------------------------
# Q1 — Home Route
# -------------------------------
@app.get("/")
def home():
    return {"message": "Welcome to QuickBite Food Delivery"}


# -------------------------------
# Q2 — Menu Data
# -------------------------------
menu = [
    {"id": 1, "name": "Pizza", "price": 200, "category": "Pizza", "is_available": True},
    {"id": 2, "name": "Burger", "price": 120, "category": "Burger", "is_available": True},
    {"id": 3, "name": "Pasta", "price": 180, "category": "Pizza", "is_available": False},
    {"id": 4, "name": "Coke", "price": 50, "category": "Drink", "is_available": True},
    {"id": 5, "name": "Ice Cream", "price": 90, "category": "Dessert", "is_available": True},
    {"id": 6, "name": "Fries", "price": 100, "category": "Burger", "is_available": True},
]


# -------------------------------
# Q4 — Orders Data
# -------------------------------
orders = []
order_counter = 1


# -------------------------------
# Q7 — Helper Functions
# -------------------------------
def find_menu_item(item_id):
    for item in menu:
        if item["id"] == item_id:
            return item
    return None


def calculate_bill(price, quantity, order_type):
    total = price * quantity
    if order_type == "delivery":
        total += 30
    return total


# -------------------------------
# Q6 — Pydantic Model
# -------------------------------
class OrderRequest(BaseModel):
    customer_name: str = Field(min_length=2)
    item_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=20)
    delivery_address: str = Field(min_length=10)
    order_type: str = "delivery"


# -------------------------------
# Q2 — GET All Menu
# -------------------------------
@app.get("/menu")
def get_menu():
    return {"items": menu, "total": len(menu)}


# -------------------------------
# Q5 — Summary (FIXED ROUTE FIRST)
# -------------------------------
@app.get("/menu/summary")
def menu_summary():
    available = [i for i in menu if i["is_available"]]
    categories = list(set([i["category"] for i in menu]))

    return {
        "total": len(menu),
        "available": len(available),
        "unavailable": len(menu) - len(available),
        "categories": categories
    }


# -------------------------------
# Q10 — Filter Menu
# -------------------------------
@app.get("/menu/filter")
def filter_menu(
    category: str = None,
    max_price: int = None,
    is_available: bool = None
):
    result = menu

    if category is not None:
        result = [i for i in result if i["category"] == category]

    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]

    if is_available is not None:
        result = [i for i in result if i["is_available"] == is_available]

    return {"items": result, "count": len(result)}


# -------------------------------
# Q3 — Get Item by ID (VARIABLE ROUTE LAST)
# -------------------------------
@app.get("/menu/{item_id}")
def get_item(item_id: int):
    item = find_menu_item(item_id)
    if item:
        return item
    return {"error": "Item not found"}


# -------------------------------
# Q4 — Get Orders
# -------------------------------
@app.get("/orders")
def get_orders():
    return {"orders": orders, "total_orders": len(orders)}


# -------------------------------
# Q8–Q9 — Create Order
# -------------------------------
@app.post("/orders")
def create_order(order: OrderRequest):
    global order_counter

    item = find_menu_item(order.item_id)

    if not item:
        return {"error": "Item not found"}

    if not item["is_available"]:
        return {"error": "Item not available"}

    total = calculate_bill(item["price"], order.quantity, order.order_type)

    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "item": item["name"],
        "quantity": order.quantity,
        "order_type": order.order_type,
        "total_price": total
    }

    orders.append(new_order)
    order_counter += 1

    return new_order
# -------------------------------
# Q11 — Add New Menu Item
# -------------------------------
from fastapi import Response

class NewMenuItem(BaseModel):
    name: str = Field(min_length=2)
    price: int = Field(gt=0)
    category: str = Field(min_length=2)
    is_available: bool = True


@app.post("/menu")
def add_menu_item(item: NewMenuItem, response: Response):
    for i in menu:
        if i["name"].lower() == item.name.lower():
            return {"error": "Item already exists"}

    new_id = len(menu) + 1

    new_item = {
        "id": new_id,
        "name": item.name,
        "price": item.price,
        "category": item.category,
        "is_available": item.is_available
    }

    menu.append(new_item)
    response.status_code = 201
    return new_item


# -------------------------------
# Q12 — Update Menu Item
# -------------------------------
@app.put("/menu/{item_id}")
def update_menu(item_id: int, price: int = None, is_available: bool = None):
    item = find_menu_item(item_id)

    if not item:
        return {"error": "Item not found"}

    if price is not None:
        item["price"] = price

    if is_available is not None:
        item["is_available"] = is_available

    return item


# -------------------------------
# Q13 — Delete Menu Item
# -------------------------------
@app.delete("/menu/{item_id}")
def delete_item(item_id: int):
    item = find_menu_item(item_id)

    if not item:
        return {"error": "Item not found"}

    menu.remove(item)
    return {"message": f"{item['name']} deleted successfully"}


# -------------------------------
# Q14 — Cart System
# -------------------------------
cart = []

@app.post("/cart/add")
def add_to_cart(item_id: int, quantity: int = 1):
    item = find_menu_item(item_id)

    if not item:
        return {"error": "Item not found"}

    if not item["is_available"]:
        return {"error": "Item not available"}

    for c in cart:
        if c["item_id"] == item_id:
            c["quantity"] += quantity
            return {"message": "Quantity updated", "cart": cart}

    cart.append({
        "item_id": item_id,
        "name": item["name"],
        "price": item["price"],
        "quantity": quantity
    })

    return {"message": "Item added to cart", "cart": cart}


@app.get("/cart")
def view_cart():
    total = sum(i["price"] * i["quantity"] for i in cart)
    return {"cart": cart, "grand_total": total}


# -------------------------------
# Q15 — Remove from Cart + Checkout
# -------------------------------
class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str


@app.delete("/cart/{item_id}")
def remove_from_cart(item_id: int):
    for item in cart:
        if item["item_id"] == item_id:
            cart.remove(item)
            return {"message": "Item removed"}
    return {"error": "Item not in cart"}


@app.post("/cart/checkout")
def checkout(data: CheckoutRequest):
    global order_counter

    if not cart:
        return {"error": "Cart is empty"}

    new_orders = []
    grand_total = 0

    for c in cart:
        total = c["price"] * c["quantity"]

        order = {
            "order_id": order_counter,
            "customer_name": data.customer_name,
            "item": c["name"],
            "quantity": c["quantity"],
            "total_price": total
        }

        orders.append(order)
        new_orders.append(order)

        grand_total += total
        order_counter += 1

    cart.clear()

    return {
        "message": "Order placed",
        "orders": new_orders,
        "grand_total": grand_total
    }


# -------------------------------
# Q16 — Search Menu
# -------------------------------
@app.get("/menu/search")
def search_menu(keyword: str):
    result = [
        i for i in menu
        if keyword.lower() in i["name"].lower()
        or keyword.lower() in i["category"].lower()
    ]

    if not result:
        return {"message": "No items found"}

    return {"results": result, "total_found": len(result)}


# -------------------------------
# Q17 — Sort Menu
# -------------------------------
@app.get("/menu/sort")
def sort_menu(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name", "category"]:
        return {"error": "Invalid sort field"}

    if order not in ["asc", "desc"]:
        return {"error": "Invalid order"}

    sorted_menu = sorted(menu, key=lambda x: x[sort_by])

    if order == "desc":
        sorted_menu.reverse()

    return {"sorted": sorted_menu}


# -------------------------------
# Q18 — Pagination
# -------------------------------
import math

@app.get("/menu/page")
def paginate_menu(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    end = start + limit

    total = len(menu)
    total_pages = math.ceil(total / limit)

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "items": menu[start:end]
    }


# -------------------------------
# Q19 — Order Search + Sort
# -------------------------------
@app.get("/orders/search")
def search_orders(customer_name: str):
    result = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]
    return {"results": result}


@app.get("/orders/sort")
def sort_orders(order: str = "asc"):
    sorted_orders = sorted(orders, key=lambda x: x["total_price"])

    if order == "desc":
        sorted_orders.reverse()

    return {"orders": sorted_orders}


# -------------------------------
# Q20 — Combined Browse
# -------------------------------
@app.get("/menu/browse")
def browse_menu(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = menu

    if keyword:
        result = [
            i for i in result
            if keyword.lower() in i["name"].lower()
            or keyword.lower() in i["category"].lower()
        ]

    result = sorted(result, key=lambda x: x[sort_by])

    if order == "desc":
        result.reverse()

    start = (page - 1) * limit
    end = start + limit

    return {
        "total": len(result),
        "page": page,
        "items": result[start:end]
    }    