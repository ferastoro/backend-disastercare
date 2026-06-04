# DisasterCare API 🚑

DisasterCare adalah sistem backend berbasis **FastAPI** untuk memanajemen respons bencana alam. Platform ini memfasilitasi pendataan bencana, pendaftaran relawan, pembagian tugas lapangan, pengelolaan stok logistik, hingga laporan langsung dari lokasi kejadian.

## 🚀 Teknologi yang Digunakan
- **Framework:** FastAPI (Python 3.10+)
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Autentikasi:** JWT (JSON Web Tokens)
- **Validasi Data:** Pydantic

---

## 🛠️ Panduan Instalasi (Untuk Developer)

1. **Clone Repositori**
   ```bash
   git clone https://github.com/username/fastapi-disaster-care.git
   cd fastapi-disaster-care
   ```

2. **Buat Virtual Environment & Install Dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Konfigurasi Environment**
   - Copy file `.env.example` menjadi `.env`.
   - Sesuaikan konfigurasi koneksi MySQL Anda di dalam `.env`.
   ```bash
   cp .env.example .env
   ```

4. **Jalankan Seeder (Opsional: Untuk Dummy Data)**
   Aplikasi membutuhkan data dasar. Anda bisa menjalankan skrip berikut untuk membuat database otomatis beserta data dummy:
   ```bash
   python seed.py
   ```

5. **Jalankan Server Lokal**
   ```bash
   uvicorn main:app --reload
   ```
   Aplikasi akan berjalan di `http://127.0.0.1:8000`.

---

## 📚 Panduan Integrasi Frontend

Dokumentasi lengkap seluruh Endpoint (beserta tipe data, *request body*, dan *response*) dapat diakses langsung secara interaktif melalui Swagger UI:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

### 🔐 Alur Autentikasi (JWT)
1. Frontend mengirim `email` & `password` via `POST /auth/login`.
2. Backend mengembalikan `access_token` (JWT).
3. Frontend **wajib** menyisipkan token ini pada header untuk *request* berikutnya:
   `Authorization: Bearer <access_token>`

### 🎭 Role-Based Access Control (RBAC)
PENTING! Frontend harus menyesuaikan UI/UX berdasarkan *Role* user yang sedang login.

| Fitur / Endpoint | Role: Admin | Role: Koordinator | Role: Relawan |
|------------------|-------------|-------------------|---------------|
| **Manajemen Bencana** (`/disasters`) | CRUD Penuh | Hanya Lihat (GET) | Hanya Lihat (GET) |
| **Pendaftaran Bencana** (`/registrations`)| Approve/Reject | Approve/Reject, Daftar | Daftar Bencana |
| **Manajemen Tugas** (`/tasks`) | Buat & Edit Task | Buat & Edit Task | Ambil Tugas (Assign) |
| **Status Tugas** (`/tasks/assignments`) | Update Semua | Update Semua | Update Tugas Sendiri |
| **Manajemen Logistik** (`/supplies`) | CRUD Penuh | Edit & Alokasi Barang | Hanya Lihat Stok |
| **Laporan Lapangan** (`/reports`) | CRUD Penuh | Buat & Edit Laporan | Buat & Edit Laporan Sendiri |

### 🛑 Catatan Penting Validasi & Logika
Saat mendesain halaman Frontend, perhatikan respons *Error 400* (Bad Request) dari Backend pada kasus berikut:
- **Pendaftaran:** Akan gagal jika tanggal `end_date` bencana sudah terlewat.
- **Tugas:** Pengambilan tugas akan gagal jika kuota `max_volunteers` sudah penuh.
- **Logistik:** Alokasi barang akan gagal jika nilai `quantity` melebihi stok yang ada di gudang.

---

*Dibuat dengan ❤️ untuk Penanganan Bencana yang Lebih Cepat.*
