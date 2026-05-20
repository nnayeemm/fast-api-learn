from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session


# -----------------------------
# DATABASE CONFIGURATION
# -----------------------------

DATABASE_URL = "mysql+pymysql://root:password123@127.0.0.1:3307/fastapi_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# -----------------------------
# SQLALCHEMY MODEL
# -----------------------------

class UserDB(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    age = Column(Integer)


Base.metadata.create_all(bind=engine)


# -----------------------------
# PYDANTIC SCHEMAS
# -----------------------------

class UserCreate(BaseModel):
    name: str
    email: str
    age: int


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int

    class Config:
        from_attributes = True


# -----------------------------
# FASTAPI APP
# -----------------------------

app = FastAPI()


# -----------------------------
# DATABASE DEPENDENCY
# -----------------------------

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# -----------------------------
# GET USERS
# -----------------------------

@app.get(
    "/view_users",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK
)
def get_users(db: Session = Depends(get_db)):

    users = db.query(UserDB).all()

    return users


# -----------------------------
# ADD USER
# -----------------------------

@app.post(
    "/add_user",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def add_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    new_user = UserDB(
        name=user.name,
        email=user.email,
        age=user.age
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


# -----------------------------
# UPDATE USER
# -----------------------------

@app.put(
    "/update_user/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
def update_user(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(UserDB).filter(
        UserDB.id == user_id
    ).first()

    if not existing_user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing_user.name = user.name
    existing_user.email = user.email
    existing_user.age = user.age

    db.commit()

    db.refresh(existing_user)

    return existing_user


# -----------------------------
# DELETE USER
# -----------------------------

@app.delete(
    "/delete_user/{user_id}",
    status_code=status.HTTP_200_OK
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    existing_user = db.query(UserDB).filter(
        UserDB.id == user_id
    ).first()

    if not existing_user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(existing_user)

    db.commit()

    return {
        "message": "User deleted successfully"
    }                 