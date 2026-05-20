from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import mysql.connector

app = FastAPI()


# Database connection
db = mysql.connector.connect(
    host="127.0.0.1",
    port=3307,
    user="root",
    password="password123",
    database="fastapi_db"
)

cursor = db.cursor(dictionary=True)


# Pydantic model
class User(BaseModel):
    name: str
    email: str
    age: int


# Get all users
@app.get("/view_users", status_code=status.HTTP_200_OK)
def get_users():

    try:
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()

        return {
            "users": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Add user
@app.post("/add_user", status_code=status.HTTP_201_CREATED)
def add_user(user: User):

    try:

        query = """
        INSERT INTO users (name, email, age)
        VALUES (%s, %s, %s)
        """

        values = (user.name, user.email, user.age)

        cursor.execute(query, values)

        db.commit()

        return {
            "message": "User added successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

#Update user
@app.put("/update_user/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: User):
    try:

        query = """
        UPDATE users
        SET name = %s, email = %s, age = %s
        WHERE id = %s
        """

        values = (user.name, user.email, user.age, user_id)

        cursor.execute(query, values)

        db.commit()

        return {
            "message": "User updated successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )        
    

#DELETE user
@app.delete("/delete_user/{user_id}", status_code=status.HTTP_200_OK)    
def delete_user(user_id: int):
    try:

        query = """
        DELETE FROM users
        WHERE id = %s
        """

        cursor.execute(query, (user_id,))

        db.commit()

        return {
            "message": "User deleted successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )