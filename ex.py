from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
print(__name__)
app = FastAPI(
    title="My API",
    description="This is a sample API built with FastAPI",
    version="6.7"
)

# GET Home Route
@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {"msg": "Hello"}


# GET Products
@app.get("/products", status_code=status.HTTP_200_OK)
def products():
    return {"products": ["laptop", "mobile", "tablet"]}


# Dynamic Route
@app.get("/services/{data}", status_code=status.HTTP_200_OK)
def services(data: str):
    return {"services": data}


# f-string example
@app.get("/contact/{data}", status_code=status.HTTP_200_OK)
def contact(data: str):
    return {"contact": f"Hi {data}"}


# Integer path parameter
@app.get("/help/{id}", status_code=status.HTTP_200_OK)
def help(id: int):
    return {"help": id}


# Multiple parameters
@app.get("/number/{amount}/{name}", status_code=status.HTTP_200_OK)
def number(amount: int, name: str):
    return {
        "amount": amount,
        "name": name
    }


# Pydantic Model
class Items(BaseModel):
    name: str
    price: float
    quantity: int


# POST Method Example
@app.post("/items", status_code=status.HTTP_201_CREATED)
def class_post(item: Items):
    return {
        "name": f"Hello {item.name}",
        "price": f"Price is {item.price}",
        "quantity": f"Quantity is {item.quantity}"
    }


# In-memory list
items = []


# Create Order
@app.post("/order", status_code=status.HTTP_201_CREATED)
def show_items(item: Items):

    # Check duplicate item
    for existing_item in items:
        if existing_item.name == item.name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Item already exists"
            )

    items.append(item)

    return {
        "message": "Item added successfully",
        "data": items
    }


# Get All Orders
@app.get("/order", status_code=status.HTTP_200_OK)
def get_items():

    if not items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No items found"
        )

    return items


# Get Single Item
@app.get("/order/{name}", status_code=status.HTTP_200_OK)
def get_item_by_name(name: str):

    for item in items:
        if item.name == name:
            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found"
    )


# Update Item
@app.put("/order/{name}", status_code=status.HTTP_200_OK)
def update_item(name: str, updated_item: Items):

    for item in items:
        if item.name == name:

            item.price = updated_item.price
            item.quantity = updated_item.quantity

            return {
                "message": "Item updated successfully",
                "updated_item": item
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found"
    )


# Delete Item
@app.delete("/order/{name}", status_code=status.HTTP_200_OK)
def delete_item(name: str):

    for item in items:
        if item.name == name:

            items.remove(item)

            return {
                "message": "Item deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found"
    )