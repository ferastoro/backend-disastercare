import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.disaster import Disaster
from app.models.supply import Supply
from app.models.task import Task
from app.core.security import hash_password
from datetime import date

def seed_data():
    # Pastikan tabel sudah terbuat
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Cek apakah data admin sudah ada. Jika sudah, hentikan seeder.
        admin_exists = db.query(User).filter(User.email == "admin@disastercare.com").first()
        if admin_exists:
            print("Data sudah ada di database. Seeder dibatalkan untuk menghindari duplikasi.")
            return

        print("Menjalankan seeder: Memasukkan data awal (dummy)...")

        # 1. Buat Data User (Admin, Koordinator, Relawan)
        # Semua passwordnya adalah: password123
        users = [
            User(name="Admin", email="admin@disastercare.com", password_hash=hash_password("password123"), role="admin", phone="081234567890"),
            User(name="Koordinator 1", email="koor@disastercare.com", password_hash=hash_password("password123"), role="koordinator", phone="081234567891"),
            User(name="Relawan 1", email="relawan@disastercare.com", password_hash=hash_password("password123"), role="relawan", phone="081234567892")
        ]
        db.add_all(users)
        db.commit()

        # 2. Buat Data Bencana (Disasters)
        disasters = [
            Disaster(title="Gempa Bumi Cianjur", location="Cianjur, Jawa Barat", type="gempa", emergency_level="tinggi", start_date=date(2026, 5, 10), description="Gempa tektonik 5.6 SR dengan kerusakan berat di pedesaan."),
            Disaster(title="Banjir Bandang Demak", location="Demak, Jawa Tengah", type="banjir", emergency_level="sedang", start_date=date(2026, 6, 1), description="Banjir akibat tanggul jebol yang merendam ribuan rumah.")
        ]
        db.add_all(disasters)
        db.commit()

        # Ambil ID Bencana pertama (Cianjur) untuk dihubungkan dengan Task
        gempa = db.query(Disaster).filter(Disaster.title == "Gempa Bumi Cianjur").first()

        # 3. Buat Data Tugas di Lapangan (Tasks)
        tasks = [
            Task(disaster_id=gempa.id, title="Evakuasi Lansia", category="evakuasi", status="open", max_volunteers=10, location="Desa Cugenang"),
            Task(disaster_id=gempa.id, title="Distribusi Makanan", category="logistik", status="open", max_volunteers=5, location="Posko Utama Cugenang")
        ]
        db.add_all(tasks)

        # 4. Buat Data Stok Logistik (Supplies)
        supplies = [
            Supply(name="Beras 5kg", category="makanan", unit="karung", quantity_available=100, description="Beras putih premium"),
            Supply(name="Obat P3K", category="obat", unit="kotak", quantity_available=50, description="Peralatan P3K standar dan obat flu/demam"),
            Supply(name="Tenda Pengungsi", category="tenda", unit="unit", quantity_available=10, description="Tenda pleton kapasitas 10 orang")
        ]
        db.add_all(supplies)

        db.commit()
        print("Seeder sukses! Dummy data berhasil dimasukkan ke dalam database.")

    except Exception as e:
        db.rollback()
        print(f"Terjadi kesalahan saat menjalankan seeder: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
