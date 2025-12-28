# indexer.py
import os
import torch
import faiss
import numpy as np
import pickle
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# Konfigurasi
DATASET_PATH = r"C:\Semester 7\Kelompok TKC\Project-RAG-Nitik-Batik-960-main\Batik Nitik 960 Images" # sesuaikan dengan konfigurasi file
INDEX_FILE = "batik_faiss.index"
PATHS_FILE = "image_paths.pkl"
MODEL_ID = "openai/clip-vit-base-patch32"

def create_index():
    print("Memuat Model CLIP...")
    model = CLIPModel.from_pretrained(MODEL_ID)
    processor = CLIPProcessor.from_pretrained(MODEL_ID)
    
    image_paths = []
    embeddings = []
    
    print(f"Mulai scanning folder: {DATASET_PATH}")
    # Scanning dataset
    for root, dirs, files in os.walk(DATASET_PATH):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                path = os.path.join(root, file)
                image_paths.append(path)

    if not image_paths:
        print("Error: Tidak ada gambar ditemukan. Cek DATASET_PATH.")
        return

    print(f"Ditemukan {len(image_paths)} gambar. Mulai ekstraksi fitur...")
    
    batch_size = 32
    for i in range(0, len(image_paths), batch_size):
        batch_paths = image_paths[i:i+batch_size]
        images = [Image.open(p).convert("RGB") for p in batch_paths]
        
        # Preprocessing & Inference
        inputs = processor(images=images, return_tensors="pt", padding=True)
        with torch.no_grad():
            image_features = model.get_image_features(**inputs)
        
        # Normalisasi vektor (Penting untuk Cosine Similarity)
        image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
        embeddings.append(image_features.numpy())
        
        print(f"Processed {min(i+batch_size, len(image_paths))}/{len(image_paths)}")

    # Gabungkan semua embedding
    embeddings = np.vstack(embeddings).astype('float32')
    
    # Buat Index FAISS 
    d = embeddings.shape[1]
    index = faiss.IndexFlatIP(d) 
    index.add(embeddings)
    
    # Simpan ke disk
    faiss.write_index(index, INDEX_FILE)
    with open(PATHS_FILE, "wb") as f:
        pickle.dump(image_paths, f)
        
    print("Indexing selesai! File tersimpan.")

if __name__ == "__main__":
    create_index()
