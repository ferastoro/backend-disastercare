from app.database import SessionLocal, engine, Base
import app.models
from app.models.user import User
from app.core.security import hash_password


def upsert_user(db, name, email, password, role, phone):
    user = db.query(User).filter(User.email == email).first()

    if user:
        user.name = name
        user.password_hash = hash_password(password)
        user.role = role
        user.phone = phone
        print(f"Updated: {email}")
    else:
        user = User(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role=role,
            phone=phone,
        )
        db.add(user)
        print(f"Created: {email}")


def main():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        upsert_user(
            db,
            name="Admin",
            email="admin@disastercare.com",
            password="password123",
            role="admin",
            phone="081234567890",
        )

        upsert_user(
            db,
            name="Koordinator 1",
            email="koor@disastercare.com",
            password="password123",
            role="koordinator",
            phone="081234567891",
        )

        upsert_user(
            db,
            name="Relawan 1",
            email="relawan@disastercare.com",
            password="password123",
            role="relawan",
            phone="081234567892",
        )

        db.commit()
        print("Akun demo berhasil dibuat / diperbarui.")
        print("Admin      : admin@disastercare.com / password123")
        print("Koordinator: koor@disastercare.com / password123")
        print("Relawan    : relawan@disastercare.com / password123")

    except Exception as error:
        db.rollback()
        print(f"Gagal membuat akun demo: {error}")

    finally:
        db.close()


if __name__ == "__main__":
    main()