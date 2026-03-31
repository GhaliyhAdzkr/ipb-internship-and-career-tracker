import os
import sys
import uuid
import uuid
from sqlalchemy.orm import Session
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app_backend.models.users import Users
from app_backend.shared.database import SessionLocal
from app_backend.shared.security import hash_password

def seed_admin():
    db: Session = SessionLocal()
    try:
        # Check if admin already exists
        admin = db.query(Users).filter(Users.email == "admin@example.com").first()
        if not admin:
            print("Creating initial Admin...")
            admin = Users(
                id=uuid.uuid4(),
                email="admin@example.com",
                password_hash=hash_password("Password123!"),
                role="ADMIN",
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("Created admin@example.com / Password123!")
        else:
            print("Admin admin@example.com already exists. Updating password...")
            admin.password_hash=hash_password("Password123!")
            admin.role="ADMIN"
            admin.is_active=True
            db.commit()
            print("Updated admin@example.com / Password123!")
    except Exception as e:
        print(f"Error seeding admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
