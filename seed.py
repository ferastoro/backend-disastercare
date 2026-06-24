from datetime import date

from app.database import SessionLocal, engine, Base
from app.core.security import hash_password

from app.models.user import User
from app.models.disaster import Disaster
from app.models.supply import Supply
from app.models.task import Task
from app.models.registration import Registration
from app.models.task_assignment import TaskAssignment
from app.models.allocation import Allocation
from app.models.report import Report

from app.models.shelter import Shelter
from app.models.shelter_need import ShelterNeed
from app.models.volunteer_skill import VolunteerSkill
from app.models.activity_log import ActivityLog


def seed_data():
    # Pastikan tabel sudah terbuat
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Cek apakah data admin sudah ada. Jika sudah, hentikan seeder.
        admin_exists = (
            db.query(User)
            .filter(User.email == "admin@disastercare.com")
            .first()
        )

        if admin_exists:
            print("Data sudah ada di database. Seeder dibatalkan untuk menghindari duplikasi.")
            return

        print("Menjalankan seeder: Memasukkan data awal DisasterCare...")

        # =========================================================
        # 1. USER DEMO
        # Semua password: password123
        # =========================================================

        admin = User(
            name="Admin DisasterCare",
            email="admin@disastercare.com",
            password_hash=hash_password("password123"),
            role="admin",
            phone="081234567890",
            region="Makassar, Sulawesi Selatan",
            readiness="aktif",
            availability="Full time",
            transport="Mobil operasional",
            area="Sulawesi Selatan",
            emergency_contact="BPBD Pusat - 112",
        )

        coordinator = User(
            name="Koordinator Lapangan",
            email="koor@disastercare.com",
            password_hash=hash_password("password123"),
            role="koordinator",
            phone="081234567891",
            region="Cianjur, Jawa Barat",
            readiness="aktif",
            availability="Siaga harian",
            transport="Mobil lapangan",
            area="Cianjur dan sekitarnya",
            emergency_contact="Admin DisasterCare - 081234567890",
        )

        volunteer = User(
            name="Relawan 1",
            email="relawan@disastercare.com",
            password_hash=hash_password("password123"),
            role="relawan",
            phone="081234567892",
            region="Makassar, Sulawesi Selatan",
            readiness="aktif",
            availability="Siaga akhir pekan",
            transport="Motor pribadi",
            area="Makassar, Gowa, Maros",
            emergency_contact="Mima - 081290001122",
        )

        volunteer_2 = User(
            name="Ishmah Nurwasilah",
            email="ishmah@disastercare.com",
            password_hash=hash_password("password123"),
            role="relawan",
            phone="081234567893",
            region="Makassar, Sulawesi Selatan",
            readiness="siaga",
            availability="Siaga sore dan akhir pekan",
            transport="Motor pribadi",
            area="Makassar dan Maros",
            emergency_contact="Keluarga - 081233334444",
        )

        users = [admin, coordinator, volunteer, volunteer_2]
        db.add_all(users)
        db.commit()

        db.refresh(admin)
        db.refresh(coordinator)
        db.refresh(volunteer)
        db.refresh(volunteer_2)

        # =========================================================
        # 2. DATA BENCANA
        # =========================================================

        disasters = [
            Disaster(
                title="Gempa Bumi Cianjur",
                location="Cianjur, Jawa Barat",
                type="gempa",
                emergency_level="tinggi",
                start_date=date(2026, 5, 10),
                description="Gempa tektonik 5.6 SR dengan kerusakan berat di area pedesaan.",
            ),
            Disaster(
                title="Banjir Bandang Demak",
                location="Demak, Jawa Tengah",
                type="banjir",
                emergency_level="sedang",
                start_date=date(2026, 6, 1),
                description="Banjir akibat tanggul jebol yang merendam ribuan rumah.",
            ),
            Disaster(
                title="Longsor Serasan Natuna",
                location="Serasan, Natuna",
                type="longsor",
                emergency_level="kritis",
                start_date=date(2026, 6, 5),
                description="Longsor besar menutup akses jalan utama dan membutuhkan evakuasi cepat.",
            ),
            Disaster(
                title="Kebakaran Permukiman Makassar",
                location="Makassar, Sulawesi Selatan",
                type="kebakaran",
                emergency_level="tinggi",
                start_date=date(2026, 6, 8),
                description="Kebakaran permukiman padat penduduk dengan kebutuhan posko darurat.",
            ),
        ]

        db.add_all(disasters)
        db.commit()

        gempa = db.query(Disaster).filter(Disaster.title == "Gempa Bumi Cianjur").first()
        banjir = db.query(Disaster).filter(Disaster.title == "Banjir Bandang Demak").first()
        longsor = db.query(Disaster).filter(Disaster.title == "Longsor Serasan Natuna").first()
        kebakaran = db.query(Disaster).filter(Disaster.title == "Kebakaran Permukiman Makassar").first()

        # =========================================================
        # 3. TASK / TUGAS LAPANGAN
        # =========================================================

        tasks = [
            Task(
                disaster_id=gempa.id,
                title="Evakuasi Lansia",
                category="evakuasi",
                status="open",
                max_volunteers=10,
                location="Desa Cugenang",
            ),
            Task(
                disaster_id=gempa.id,
                title="Distribusi Makanan",
                category="logistik",
                status="ongoing",
                max_volunteers=8,
                location="Posko Utama Cugenang",
            ),
            Task(
                disaster_id=banjir.id,
                title="Distribusi Air Bersih",
                category="logistik",
                status="open",
                max_volunteers=12,
                location="Posko Demak Barat",
            ),
            Task(
                disaster_id=longsor.id,
                title="Pendataan Korban Terdampak",
                category="komunikasi",
                status="ongoing",
                max_volunteers=6,
                location="Balai Desa Serasan",
            ),
            Task(
                disaster_id=kebakaran.id,
                title="Pelayanan Medis Darurat",
                category="medis",
                status="open",
                max_volunteers=5,
                location="Pos Kesehatan Antang",
            ),
        ]

        db.add_all(tasks)
        db.commit()

        task_evakuasi = db.query(Task).filter(Task.title == "Evakuasi Lansia").first()
        task_makanan = db.query(Task).filter(Task.title == "Distribusi Makanan").first()

        # =========================================================
        # 4. REGISTRATION / PENDAFTARAN RELAWAN
        # =========================================================

        registrations = [
            Registration(
                user_id=volunteer.id,
                disaster_id=gempa.id,
                status="approved",
                notes="Relawan siap membantu distribusi logistik dan pendataan pengungsi.",
            ),
            Registration(
                user_id=volunteer_2.id,
                disaster_id=banjir.id,
                status="pending",
                notes="Siap membantu distribusi air bersih dan dapur umum.",
            ),
            Registration(
                user_id=coordinator.id,
                disaster_id=gempa.id,
                status="approved",
                notes="Koordinator bertugas mengelola wilayah Cianjur.",
            ),
        ]

        db.add_all(registrations)
        db.commit()

        # =========================================================
        # 5. TASK ASSIGNMENTS / PENUGASAN RELAWAN
        # =========================================================

        assignments = [
            TaskAssignment(
                task_id=task_evakuasi.id,
                user_id=volunteer.id,
                status="ongoing",
                notes="Relawan sudah berada di titik evakuasi.",
            ),
            TaskAssignment(
                task_id=task_makanan.id,
                user_id=volunteer_2.id,
                status="assigned",
                notes="Relawan dijadwalkan membantu distribusi makanan siang.",
            ),
        ]

        db.add_all(assignments)
        db.commit()

        # =========================================================
        # 6. SUPPLIES / STOK LOGISTIK
        # =========================================================

        supplies = [
            Supply(
                name="Beras 5kg",
                category="makanan",
                unit="karung",
                quantity_available=100,
                description="Beras putih premium untuk dapur umum dan distribusi keluarga.",
            ),
            Supply(
                name="Obat P3K",
                category="obat",
                unit="kotak",
                quantity_available=50,
                description="Peralatan P3K standar dan obat flu/demam.",
            ),
            Supply(
                name="Tenda Pengungsi",
                category="tenda",
                unit="unit",
                quantity_available=10,
                description="Tenda pleton kapasitas 10 orang.",
            ),
            Supply(
                name="Air Mineral Dus",
                category="makanan",
                unit="dus",
                quantity_available=260,
                description="Air mineral dus untuk kebutuhan posko dan relawan.",
            ),
            Supply(
                name="Selimut",
                category="pakaian",
                unit="lembar",
                quantity_available=180,
                description="Selimut untuk pengungsi lansia, anak-anak, dan keluarga terdampak.",
            ),
        ]

        db.add_all(supplies)
        db.commit()

        beras = db.query(Supply).filter(Supply.name == "Beras 5kg").first()
        air = db.query(Supply).filter(Supply.name == "Air Mineral Dus").first()
        obat = db.query(Supply).filter(Supply.name == "Obat P3K").first()

        # =========================================================
        # 7. ALLOCATION / ALOKASI LOGISTIK
        # =========================================================

        allocations = [
            Allocation(
                supply_id=beras.id,
                disaster_id=gempa.id,
                quantity=25,
                allocated_by=admin.name,
            ),
            Allocation(
                supply_id=air.id,
                disaster_id=banjir.id,
                quantity=40,
                allocated_by=coordinator.name,
            ),
            Allocation(
                supply_id=obat.id,
                disaster_id=kebakaran.id,
                quantity=8,
                allocated_by=admin.name,
            ),
        ]

        # Karena model route allocation mengurangi stok saat request,
        # di seed ini kita kurangi manual supaya data stok tetap masuk akal.
        beras.quantity_available -= 25
        air.quantity_available -= 40
        obat.quantity_available -= 8

        db.add_all(allocations)
        db.commit()

        # =========================================================
        # 8. SHELTERS / POSKO
        # =========================================================

        shelters = [
            Shelter(
                disaster_id=gempa.id,
                name="Posko Utama Cugenang",
                location="Lapangan Desa Cugenang",
                capacity=250,
                current_occupancy=180,
                status="aktif",
                coordinator_name=coordinator.name,
                contact_phone=coordinator.phone,
                description="Posko utama untuk pengungsi terdampak gempa Cianjur.",
            ),
            Shelter(
                disaster_id=banjir.id,
                name="Posko Demak Barat",
                location="Balai Kecamatan Demak Barat",
                capacity=180,
                current_occupancy=142,
                status="hampir_penuh",
                coordinator_name=coordinator.name,
                contact_phone=coordinator.phone,
                description="Posko banjir dengan kebutuhan air bersih dan makanan siap saji.",
            ),
            Shelter(
                disaster_id=longsor.id,
                name="Posko Serasan Aman",
                location="Balai Desa Serasan",
                capacity=120,
                current_occupancy=110,
                status="hampir_penuh",
                coordinator_name=coordinator.name,
                contact_phone=coordinator.phone,
                description="Posko sementara untuk warga terdampak longsor.",
            ),
            Shelter(
                disaster_id=kebakaran.id,
                name="Posko Antang Makassar",
                location="Lapangan Antang",
                capacity=90,
                current_occupancy=58,
                status="aktif",
                coordinator_name=coordinator.name,
                contact_phone=coordinator.phone,
                description="Posko darurat bagi warga terdampak kebakaran permukiman.",
            ),
        ]

        db.add_all(shelters)
        db.commit()

        posko_cugenang = (
            db.query(Shelter)
            .filter(Shelter.name == "Posko Utama Cugenang")
            .first()
        )
        posko_demak = (
            db.query(Shelter)
            .filter(Shelter.name == "Posko Demak Barat")
            .first()
        )
        posko_serasan = (
            db.query(Shelter)
            .filter(Shelter.name == "Posko Serasan Aman")
            .first()
        )
        posko_antang = (
            db.query(Shelter)
            .filter(Shelter.name == "Posko Antang Makassar")
            .first()
        )

        # =========================================================
        # 9. SHELTER NEEDS / KEBUTUHAN POSKO
        # =========================================================

        shelter_needs = [
            ShelterNeed(
                shelter_id=posko_cugenang.id,
                item_name="Air Bersih",
                category="air",
                quantity=80,
                unit="dus",
                priority="kritis",
                status="diajukan",
                notes="Stok air bersih hanya cukup sampai malam ini.",
            ),
            ShelterNeed(
                shelter_id=posko_cugenang.id,
                item_name="Makanan Siap Saji",
                category="makanan",
                quantity=120,
                unit="paket",
                priority="tinggi",
                status="diproses",
                notes="Dibutuhkan untuk dapur umum dan pengungsi anak-anak.",
            ),
            ShelterNeed(
                shelter_id=posko_demak.id,
                item_name="Obat Gatal dan Demam",
                category="obat",
                quantity=45,
                unit="paket",
                priority="tinggi",
                status="diajukan",
                notes="Banyak pengungsi mengalami gatal dan demam ringan.",
            ),
            ShelterNeed(
                shelter_id=posko_serasan.id,
                item_name="Selimut",
                category="pakaian",
                quantity=90,
                unit="lembar",
                priority="sedang",
                status="diproses",
                notes="Dibutuhkan untuk lansia dan anak-anak.",
            ),
            ShelterNeed(
                shelter_id=posko_antang.id,
                item_name="Tenda Tambahan",
                category="tenda",
                quantity=6,
                unit="unit",
                priority="kritis",
                status="diajukan",
                notes="Area pengungsian belum cukup menampung seluruh warga terdampak.",
            ),
        ]

        db.add_all(shelter_needs)
        db.commit()

        # =========================================================
        # 10. REPORTS / LAPORAN
        # =========================================================

        reports = [
            Report(
                disaster_id=gempa.id,
                reported_by=volunteer.id,
                report_date=date(2026, 6, 12),
                content="Evakuasi lansia di Desa Cugenang berjalan. Beberapa warga membutuhkan obat-obatan dan selimut tambahan.",
                attachments="uploads/demo-evakuasi-cugenang.jpg",
                status="submitted",
                priority="tinggi",
            ),
            Report(
                disaster_id=banjir.id,
                reported_by=volunteer_2.id,
                report_date=date(2026, 6, 13),
                content="Distribusi air bersih di Posko Demak Barat belum mencukupi. Warga membutuhkan tambahan 80 dus air mineral.",
                attachments="uploads/demo-banjir-demak.jpg",
                status="reviewed",
                priority="kritis",
                review_notes="Segera koordinasikan dengan tim logistik.",
                reviewed_by=admin.id,
            ),
            Report(
                disaster_id=kebakaran.id,
                reported_by=coordinator.id,
                report_date=date(2026, 6, 14),
                content="Posko Antang membutuhkan tenda tambahan dan dukungan medis untuk warga yang mengalami sesak napas ringan.",
                attachments="uploads/demo-posko-antang.jpg",
                status="revision",
                priority="tinggi",
                review_notes="Lengkapi detail jumlah keluarga terdampak.",
                reviewed_by=admin.id,
            ),
        ]

        db.add_all(reports)
        db.commit()

        # =========================================================
        # 11. VOLUNTEER SKILLS
        # =========================================================

        skills = [
            VolunteerSkill(
                user_id=volunteer.id,
                skill_name="Distribusi Logistik",
            ),
            VolunteerSkill(
                user_id=volunteer.id,
                skill_name="Pendataan Pengungsi",
            ),
            VolunteerSkill(
                user_id=volunteer.id,
                skill_name="Dokumentasi Laporan",
            ),
            VolunteerSkill(
                user_id=volunteer_2.id,
                skill_name="Dapur Umum",
            ),
            VolunteerSkill(
                user_id=volunteer_2.id,
                skill_name="Komunikasi Lapangan",
            ),
        ]

        db.add_all(skills)
        db.commit()

        # =========================================================
        # 12. ACTIVITY LOG / NOTIFIKASI
        # =========================================================

        logs = [
            ActivityLog(
                user_id=None,
                role_target="admin",
                title="Seeder berhasil membuat data demo",
                description="Data awal bencana, posko, kebutuhan, logistik, laporan, dan relawan tersedia.",
                type="system",
            ),
            ActivityLog(
                user_id=None,
                role_target="koordinator",
                title="Kebutuhan posko kritis masuk",
                description="Posko Utama Cugenang membutuhkan air bersih dengan prioritas kritis.",
                type="priority",
            ),
            ActivityLog(
                user_id=volunteer.id,
                role_target="relawan",
                title="Profil relawan aktif",
                description="Relawan demo siap menerima tugas lapangan.",
                type="info",
            ),
            ActivityLog(
                user_id=volunteer_2.id,
                role_target="relawan",
                title="Pendaftaran menunggu review",
                description="Pendaftaran relawan untuk Banjir Bandang Demak sedang menunggu keputusan koordinator.",
                type="review",
            ),
        ]

        db.add_all(logs)
        db.commit()

        print("Seeder sukses! Data demo DisasterCare berhasil dimasukkan.")
        print("")
        print("Akun demo:")
        print("Admin       : admin@disastercare.com / password123")
        print("Koordinator : koor@disastercare.com / password123")
        print("Relawan     : relawan@disastercare.com / password123")
        print("Relawan 2   : ishmah@disastercare.com / password123")

    except Exception as e:
        db.rollback()
        print(f"Terjadi kesalahan saat menjalankan seeder: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()