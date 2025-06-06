from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.utils.security import get_password_hash


def get_user_by_id(db: Session, user_id: int) -> Optional[UserModel]:
    """
    Fetch a user by their ID.
    """
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[UserModel]:
    """
    Fetch a user by their username.
    """
    return db.query(UserModel).filter(UserModel.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
    """
    Fetch a user by their email.
    """
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[UserModel]:
    """
    Get a list of users with optional pagination.
    """
    return db.query(UserModel).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> UserResponse:
    """
    Create a new user in the database.
    Hashes the password before saving.
    """
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role="user"  # default role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponse.model_validate(db_user)


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[UserResponse]:
    """
    Update an existing user.
    Only non-None fields are updated.
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return UserResponse.model_validate(db_user)


def delete_user(db: Session, user_id: int) -> bool:
    """
    Delete a user from the database.
    Returns True if deletion was successful.
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True