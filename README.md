freemir TikTok Pre-Sales Calculation App

Aplikasi web sederhana untuk menghitung total kebutuhan SKU dari file laporan "To Ship" TikTok Shop, diperkaya dengan nama produk (Inggris & Mandarin) dari database TAT.

Cara Menggunakan (Untuk User)

Buka link aplikasi.

Upload file Excel "TT To Ship".

Tunggu proses selesai.

Download hasil dalam format Excel yang rapi.

🚀 Cara Setup di GitHub & Streamlit Cloud

Agar aplikasi ini bisa berjalan online dan membaca file TAT.xlsx (Database Produk), ikuti langkah ini:

Langkah 1: Siapkan File

Pastikan Anda memiliki 3 file ini di dalam satu folder di komputer Anda:

streamlit_app.py (Kode Python utama)

requirements.txt (Daftar library)

TAT.xlsx (File Excel Database Produk Anda)

Langkah 2: Upload ke GitHub

Buat Repository baru di GitHub (misal: freemir-sku-calc).

Upload ketiga file di atas (streamlit_app.py, requirements.txt, dan TAT.xlsx) secara bersamaan ke dalam repository tersebut.

PENTING: File TAT.xlsx harus berada di folder "root" (folder paling luar), sejajar dengan streamlit_app.py. Jangan masukkan ke dalam folder lain.

Commit changes (Simpan).

Langkah 3: Deploy ke Streamlit Cloud

Buka share.streamlit.io.

Login dengan GitHub.

Klik "New App".

Pilih repository freemir-sku-calc yang baru dibuat.

Pastikan "Main file path" adalah streamlit_app.py.

Klik Deploy.

Bagaimana cara update TAT.xlsx?

Jika ada produk baru, Anda cukup update file TAT.xlsx di komputer Anda, lalu upload ulang (replace) file tersebut ke GitHub Repository yang sama. Aplikasi akan otomatis menggunakan data terbaru setelah Anda me-refresh halaman webnya.
