# eval_retrieval.py
import faiss
import pickle
import numpy as np
import os
import random
from pathlib import Path
from tqdm import tqdm  # Library untuk progress bar (pip install tqdm)

# Import logika penamaan kelas dari app.py (atau copy paste fungsi extract_class_name baru)
# Agar konsisten, kita tulis ulang fungsi cleaning-nya di sini
from data_metadata import BATIK_METADATA

# ==========================================
# KONFIGURASI
# ==========================================
INDEX_FILE = "batik_faiss.index"
PATHS_FILE = "image_paths.pkl"
K_VALUES = [1, 3, 5]  # Kita akan ukur P@1, P@3, dan P@5
SAMPLE_SIZE = 100     # Jumlah gambar yang akan dites (semakin banyak semakin akurat, tapi lama)

# ==========================================
# FUNGSI BANTU
# ==========================================
def extract_class_name_eval(image_path: str) -> str:
    """
    Logika ekstraksi nama kelas yang SAMA PERSIS dengan yang sudah diperbaiki.
    """
    path = Path(image_path)
    filename = path.stem.lower()
    
    for item in BATIK_METADATA:
        class_name_db = item['class_name']
        clean_db_name = class_name_db.lower()
        if clean_db_name in filename or clean_db_name.replace(" ", "_") in filename:
            return class_name_db
            
    clean_name = filename.replace("_", " ").replace("-", " ")
    import re
    clean_name = re.sub(r'\d+$', '', clean_name).strip()
    return clean_name.title()

def load_resources():
    print("📂 Memuat Index & Database...")
    index = faiss.read_index(INDEX_FILE)
    with open(PATHS_FILE, "rb") as f:
        image_paths = pickle.load(f)
    
    # Reconstruct embeddings (FAISS index IP menyimpan vektornya)
    # Note: Ini trik untuk mengambil vektor balik dari IndexFlatIP
    # Jika error, kita harus load model CLIP lagi (tapi itu lambat).
    # Untuk IndexFlatIP, kita bisa reconstruct.
    try:
        dataset_embeddings = index.reconstruct_n(0, index.ntotal)
        return index, image_paths, dataset_embeddings
    except:
        print("❌ Gagal merekonstruksi vektor dari Index. Pastikan index tipe IndexFlatIP.")
        exit()

# ==========================================
# LOGIKA EVALUASI UTAMA
# ==========================================
def evaluate():
    index, image_paths, embeddings = load_resources()
    total_images = len(image_paths)
    
    # Ambil sampel random untuk testing
    # (Atau gunakan semua data jika kuat menunggu)
    test_indices = random.sample(range(total_images), min(SAMPLE_SIZE, total_images))
    
    print(f"🚀 Memulai Evaluasi pada {len(test_indices)} sampel gambar...")
    print(f"Target Metrics: {['P@'+str(k) for k in K_VALUES]}")
    print("-" * 50)

    # Dictionary untuk menyimpan total score per K
    precision_scores = {k: [] for k in K_VALUES}

    for idx in tqdm(test_indices, desc="Evaluasi Berjalan"):
        # 1. Tentukan Ground Truth (Kelas Sebenarnya)
        query_path = image_paths[idx]
        true_class = extract_class_name_eval(query_path)
        
        # 2. Ambil Vektor Query (Kita pakai vektor yang sudah ada di index untuk hemat waktu)
        # Dalam skenario nyata, ini harusnya gambar baru yang di-encode CLIP.
        # Tapi untuk Self-Evaluation dataset, ini valid.
        query_vec = embeddings[idx].reshape(1, -1)
        
        # 3. Lakukan Pencarian (Retrieval)
        # Cari max K tertinggi (misal K=5) + 1 (karena hasil ke-1 pasti dirinya sendiri)
        max_k = max(K_VALUES) + 1 
        distances, indices = index.search(query_vec, max_k)
        
        # 4. Hitung Precision untuk setiap K
        retrieved_indices = indices[0]
        
        # Kita skip index ke-0 karena itu adalah gambar query itu sendiri (Self-Match)
        # Kita ingin tahu apakah gambar LAIN yang muncul relevan?
        retrieved_indices = retrieved_indices[1:] 
        
        for k in K_VALUES:
            # Ambil top-k hasil
            top_k_indices = retrieved_indices[:k]
            
            relevant_count = 0
            for res_idx in top_k_indices:
                res_path = image_paths[res_idx]
                pred_class = extract_class_name_eval(res_path)
                
                # Cek Relevansi: Apakah Kelas Hasil == Kelas Query?
                if pred_class == true_class:
                    relevant_count += 1
            
            # Hitung Score P@k
            score = relevant_count / k
            precision_scores[k].append(score)

    # ==========================================
    # LAPORAN HASIL
    # ==========================================
    print("\n" + "="*30)
    print("📊 LAPORAN EVALUASI RETRIEVAL")
    print("="*30)
    print(f"Total Sampel Uji: {len(test_indices)}")
    print("-" * 30)
    
    for k in K_VALUES:
        avg_precision = np.mean(precision_scores[k])
        print(f"✅ Average Precision@{k} (P@{k}) : {avg_precision:.2%}")
        
    print("="*30)
    print("Interpretasi:")
    print("- P@1 : Seberapa sering hasil teratas benar-benar tepat.")
    print("- P@3 : Seberapa banyak hasil benar dalam 3 rekomendasi.")

if __name__ == "__main__":
    evaluate()