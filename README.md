# DisasterCare API 🚑

DisasterCare adalah sistem backend berbasis **FastAPI** untuk memanajemen respons bencana alam. Platform ini memfasilitasi pendataan bencana, pendaftaran relawan, pembagian tugas lapangan, pengelolaan stok logistik, hingga laporan langsung dari lokasi kejadian.

## 🚀 Teknologi yang Digunakan
- **Framework:** FastAPI (Python 3.10+)
- **Database:** MySQL (via XAMPP)
- **ORM:** SQLAlchemy
- **Autentikasi:** JWT (JSON Web Tokens)
- **Validasi Data:** Pydantic

---

## 🛠️ Panduan Instalasi (Untuk Developer)

### 1. Persiapan Database (XAMPP)
Aplikasi ini membutuhkan database MySQL lokal untuk menyimpan data.
- Buka aplikasi **XAMPP Control Panel**.
- Klik tombol **Start** pada modul **Apache** dan **MySQL**.
- Buka browser dan pergi ke `http://localhost/phpmyadmin/`.
- Buat sebuah database baru dengan nama: **`disastercare`** (Biarkan kosong, tabel akan dibuat otomatis oleh program).

### 2. Clone Repositori
Clone proyek ini ke folder lokal komputer Anda:
```bash
git clone https://github.com/ferastoro/backend-disastercare.git
cd backend-disastercare
```

### 3. Buat Virtual Environment & Install Dependencies
Virtual Environment digunakan agar library Python proyek ini tidak bentrok dengan library di laptop Anda.
```bash
python -m venv venv

# Aktivasi Environment (Untuk Mac/Linux):
source venv/bin/activate  

# Aktivasi Environment (Untuk Windows):
venv\Scripts\activate

# Install semua library yang dibutuhkan
pip install -r requirements.txt
```

### 4. Konfigurasi Environment Variable (`.env`)
Aplikasi ini membutuhkan kredensial rahasia (seperti password database dan kunci JWT) untuk berjalan. 
- Di dalam folder proyek, *copy* file `.env.example` dan ubah namanya menjadi `.env`.
```bash
cp .env.example .env
```
- Buka file `.env` di text editor Anda. Isinya akan terlihat seperti ini:
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=disastercare
DB_USER=root
DB_PASSWORD=         # Kosongkan jika XAMPP Anda tidak pakai password
SECRET_KEY=kunci_rahasia_bebas_apa_saja
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
- Pastikan konfigurasi di atas sudah sesuai dengan setting XAMPP MySQL Anda.

### 5. Menjalankan Server Lokal & Seeder
Server sekarang siap dinyalakan! 
```bash
uvicorn main:app --reload
```
Aplikasi akan berjalan di `http://127.0.0.1:8000`.

**(Opsional: Membuat Dummy Data)**
Jika database Anda masih kosong dan ingin langsung ada datanya untuk keperluan tes UI, buka terminal baru (biarkan server uvicorn tetap menyala), pastikan berada di folder proyek dan *venv* sudah aktif, lalu jalankan skrip seeder:
```bash
python seed.py
```
Ini akan otomatis membuat 3 user (Admin, Koordinator, Relawan dengan password `password123`), bencana, tugas, dan logistik.

---

## 📚 Panduan Integrasi Frontend

Dokumentasi lengkap seluruh Endpoint (beserta tipe data, *request body*, dan *response*) dapat diakses langsung secara interaktif melalui Swagger UI:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

### 🔐 Alur Autentikasi (JWT)
1. Frontend mengirim `email` & `password` via `POST /auth/login`.
2. Backend mengembalikan `access_token` (JWT).
3. Frontend **wajib** menyisipkan token ini pada header HTTP untuk setiap *request* yang membutuhkan login:
   `Authorization: Bearer <access_token>`

### 🎭 Role-Based Access Control (RBAC)
PENTING! Frontend harus menyesuaikan antarmuka UI/UX (menyembunyikan/menampilkan tombol) berdasarkan *Role* user yang sedang login.

| Fitur / Endpoint | Role: Admin | Role: Koordinator | Role: Relawan |
|------------------|-------------|-------------------|---------------|
| **Manajemen Bencana** (`/disasters`) | CRUD Penuh | Hanya Lihat (GET) | Hanya Lihat (GET) |
| **Pendaftaran Bencana** (`/registrations`)| Approve/Reject | Approve/Reject, Daftar | Daftar Bencana |
| **Manajemen Tugas** (`/tasks`) | Buat & Edit Task | Buat & Edit Task, Assign | Ambil Tugas (Assign) |
| **Status Tugas** (`/tasks/assignments`) | Update Semua | Update Semua | Update Tugas Sendiri |
| **Manajemen Logistik** (`/supplies`) | CRUD Penuh | Edit & Alokasi Barang | Hanya Lihat Stok |
| **Laporan Lapangan** (`/reports`) | CRUD Penuh | Buat & Edit Laporan | Buat & Edit Laporan Sendiri |

### 🛑 Catatan Penting Validasi & Logika (Error 400)
Saat mendesain halaman Frontend, perhatikan respons *Error 400* (Bad Request) dari Backend pada kasus berikut agar Frontend bisa menampilkan notifikasi yang ramah pengguna:
- **Pendaftaran Bencana:** Akan gagal ditolak jika tanggal `end_date` bencana sudah terlewat.
- **Pengambilan Tugas:** Akan gagal jika kuota `max_volunteers` sudah penuh.
- **Alokasi Logistik:** Akan gagal jika nilai `quantity` melebihi stok yang ada di gudang (*Insufficient Stock*).

---

*Dibuat dengan ❤️ untuk Penanganan Bencana yang Lebih Cepat.*
