from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# In-memory product storage
products = []


# -------------------------------
# Q1 - Add Product
# -------------------------------
@app.post("/products")
def add_product(product: dict):
    products.append(product)
    return {"message": "Product added successfully", "product": product}


# -------------------------------
# Q2 - Get All Products
# -------------------------------
@app.get("/products")
def get_products():
    return {
        "total_products": len(products),
        "products": products
    }


# -------------------------------
# Q5 - Audit API
# IMPORTANT: Keep this ABOVE product_id route
# -------------------------------
@app.get("/products/audit")
def audit_products():

    total_products = len(products)

    in_stock_count = sum(1 for p in products if p["in_stock"])

    out_of_stock_names = [p["name"] for p in products if not p["in_stock"]]

    total_stock_value = sum(p["price"] for p in products if p["in_stock"])

    most_expensive = None
    if products:
        most_expensive = max(products, key=lambda x: x["price"])

    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_names": out_of_stock_names,
        "total_stock_value": total_stock_value,
        "most_expensive": most_expensive
    }


# -------------------------------
# Q4 - Get Product By ID
# -------------------------------
@app.get("/products/{product_id}")
def get_product(product_id: int):

    if product_id < 0 or product_id >= len(products):
        return {"error": "Product not found"}

    return products[product_id]


# -------------------------------
# Q2 - Update Product
# -------------------------------
@app.put("/products/{product_id}")
def update_product(
        product_id: int,
        price: Optional[int] = None,
        in_stock: Optional[bool] = None):

    if product_id < 0 or product_id >= len(products):
        return {"error": "Product not found"}

    if price is not None:
        products[product_id]["price"] = price

    if in_stock is not None:
        products[product_id]["in_stock"] = in_stock

    return {
        "message": "Product updated successfully",
        "product": products[product_id]
    }


# -------------------------------
# Q3 - Delete Product
# -------------------------------
@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    if product_id < 0 or product_id >= len(products):
        return {"error": "Product not found"}

    deleted_product = products.pop(product_id)

    return {
        "message": f"Product '{deleted_product['name']}' deleted successfully"
    }