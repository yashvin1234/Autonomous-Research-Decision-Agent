from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.sessions import get_db
from app.models.db_models import User
from app.core.security import hash_password, verify_password, create_access_token
from app.models.schemas import SignupRequest

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    email = data.email
    password = data.password
    print("RAW DATA:", data)
    print("PASSWORD TYPE:", type(data.password))
    print("PASSWORD LEN:", len(data.password))
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(400, "User already exists")

    new_user = User(
        email=email,
        name=email.split("@")[0],
        password_hash=hash_password(password)
    )
    db.add(new_user)
    db.commit()

    token = create_access_token(email)
    return {"access_token": token}


@router.post("/login")
def login(data: SignupRequest, db: Session = Depends(get_db)):
    email = data.email
    password = data.password

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token(user.email)
    return {"access_token": token}

