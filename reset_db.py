from app.database import engine, Base
import app.models


def reset_database():
    print("Menghapus semua tabel DisasterCare...")
    Base.metadata.drop_all(bind=engine)

    print("Membuat ulang semua tabel sesuai model terbaru...")
    Base.metadata.create_all(bind=engine)

    print("Reset database selesai.")


if __name__ == "__main__":
    reset_database()