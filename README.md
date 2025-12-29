# Batik-Nitik-960-RAG
# 🏛️ Batik Nitik 960 RAG: Multimodal AI Heritage Preservation

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![AI Models](https://img.shields.io/badge/AI-CLIP%20%7C%20BLIP%20%7C%20Llama3-green)

Proyek ini adalah sistem **Retrieval-Augmented Generation (RAG) Multimodal** yang dirancang untuk mengidentifikasi, menganalisis, dan menceritakan filosofi motif **Batik Nitik**. Sistem ini menggabungkan kemampuan visi komputer (*Computer Vision*) dan pemrosesan bahasa alami (*NLP*) untuk melestarikan warisan budaya digital.

## 🌟 Fitur Utama

1.  **Identifikasi Motif Akurat (Retrieval):** Menggunakan **CLIP (Contrastive Language-Image Pre-training)** dan **FAISS** untuk mencari kemiripan visual antara gambar input dengan database 960 citra Batik Nitik.
2.  **Analisis Visual Cerdas (Vision):** Menggunakan **BLIP (Bootstrapping Language-Image Pre-training)** untuk menjadi "mata" AI yang mendeskripsikan elemen visual (warna, bentuk, pola) secara real-time.
3.  **Generasi Narasi Budaya (Synthesis):** Menggunakan **Llama 3 (via Groq API)** untuk menyusun narasi filosofis yang mendalam, menggabungkan data historis dengan pengamatan visual langsung.
4.  **Evaluasi Sistem Real-time:** Dashboard terintegrasi untuk memantau *Latency* (waktu respons) dan stabilitas sistem.

## 🛠️ Arsitektur Sistem

Sistem ini bekerja dengan alur kerja (pipeline) sebagai berikut:

1.  **Input:** Pengguna mengunggah citra batik.
2.  **Indexing & Retrieval:**
    * Model **CLIP** mengekstrak fitur visual (embedding).
    * **FAISS** mencari vektor tetangga terdekat (Top-K) dari database.
3.  **Visual Captioning:** Model **BLIP** menghasilkan deskripsi teks dari gambar input.
4.  **Augmented Generation:**
    * Metadata motif (Nama, Makna) diambil berdasarkan hasil retrieval.
    * Prompt disusun: *Metadata + Deskripsi BLIP + Instruksi Kurator*.
5.  **Output:** **Llama 3** menghasilkan narasi JSON yang berisi Filosofi dan Analisis Struktur Visual.

## 📦 Struktur Proyek

```text
├── Batik Nitik 960 Images/  # Dataset gambar sumber
├── app.py                   # Aplikasi Utama (Streamlit Dashboard)
├── indexer.py               # Skrip untuk membuat Vector Database (FAISS)
├── eval_retrieval.py        # Skrip Evaluasi Metrik (Precision@K)
├── data_metadata.py         # Database statis berisi filosofi motif
├── batik_faiss.index        # File Index FAISS (Generated)
├── image_paths.pkl          # File path mapping (Generated)
└── requirements.txt         # Daftar library python
```
## 🚀 Cara Instalasi & Menjalankan

Ikuti langkah-langkah berikut untuk menyiapkan lingkungan pengembangan dan menjalankan aplikasi di komputer lokal Anda.

### 1. Prasyarat
Pastikan Anda telah menginstal:
* **Python 3.8** atau versi yang lebih baru.
* **Git** (opsional, untuk clone repository).
* Koneksi internet stabil (diperlukan untuk mengunduh model AI dari Hugging Face saat pertama kali dijalankan).

### 2. Clone Repository & Setup Environment
Buka terminal atau command prompt, lalu jalankan perintah berikut:

```bash
# 1. Clone repository (jika menggunakan git)
git clone [https://github.com/username-anda/Project-RAG-Nitik-Batik-960.git](https://github.com/username-anda/Project-RAG-Nitik-Batik-960.git)
cd Project-RAG-Nitik-Batik-960

# 2. Buat Virtual Environment (Sangat Disarankan)
# Untuk Windows:
python -m venv venv
.\venv\Scripts\activate

# Untuk Mac/Linux:
python3 -m venv venv
source venv/bin/activate

# 3. Install Dependensi
pip install -r requirements.txt

# 4. Membuat Index Database (hanya perlu dijalankan sekali)
python indexer.py

# 5. Menjalankan Aplikasi
python indexer.py
```
## 📊 Evaluasi Kinerja
Proyek ini dilengkapi dengan instrumen evaluasi untuk mengukur performa sistem dari sisi kecepatan (latency) dan akurasi (precision).
Setiap kali Anda mengunggah gambar di dashboard aplikasi (app.py), Panel Evaluasi Sistem akan muncul di bagian bawah hasil untuk menampilkan:

* **Total Latency**: Waktu total dari upload hingga narasi muncul.
* **Vision Process Time**: Durasi pemrosesan CLIP & BLIP.
* **Generation Time**: Durasi pembuatan narasi oleh Llama 3.
* **Integrasi Status**: Indikator stabilitas sistem (Success/Fail).
