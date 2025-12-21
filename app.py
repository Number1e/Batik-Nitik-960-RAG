# app.py
import streamlit as st
import torch
import faiss
import pickle
import numpy as np
import json
import os
import time
from PIL import Image
from pathlib import Path

# --- BACKEND IMPORTS (TETAP SAMA) ---
from transformers import CLIPProcessor, CLIPModel, BlipProcessor, BlipForConditionalGeneration
from groq import Groq 
from data_metadata import BATIK_METADATA

# =============================================================================
# KONFIGURASI UTAMA
# =============================================================================
INDEX_FILE = "batik_faiss.index"
PATHS_FILE = "image_paths.pkl"
CLIP_MODEL_ID = "openai/clip-vit-base-patch32"
BLIP_MODEL_ID = "Salesforce/blip-image-captioning-base" 
TOP_K = 3 
# Ganti dengan API Key Anda yang aman
GROQ_API_KEY = "fill it by yourself" 

# =============================================================================
# FUNGSI BACKEND & AI (TIDAK DIUBAH - COPY DARI KODE LAMA ANDA)
# =============================================================================

@st.cache_resource
def load_models():
    # ... (Isi sama persis dengan kode Anda) ...
    print("Loading CLIP...")
    clip_model = CLIPModel.from_pretrained(CLIP_MODEL_ID)
    clip_processor = CLIPProcessor.from_pretrained(CLIP_MODEL_ID)
    print("Loading BLIP v1...")
    blip_processor = BlipProcessor.from_pretrained(BLIP_MODEL_ID)
    blip_model = BlipForConditionalGeneration.from_pretrained(BLIP_MODEL_ID)
    return clip_model, clip_processor, blip_model, blip_processor

@st.cache_resource
def load_faiss_index():
    if not os.path.exists(INDEX_FILE) or not os.path.exists(PATHS_FILE):
        return None, None
    index = faiss.read_index(INDEX_FILE)
    with open(PATHS_FILE, "rb") as f:
        image_paths = pickle.load(f)
    return index, image_paths

def get_image_embedding(image: Image.Image, model, processor):
    width, height = image.size
    new_size = min(width, height)
    left = (width - new_size)/2
    top = (height - new_size)/2
    right = (width + new_size)/2
    bottom = (height + new_size)/2
    image_crop = image.crop((left, top, right, bottom))
    inputs = processor(images=image_crop, return_tensors="pt", padding=True)
    with torch.no_grad():
        features = model.get_image_features(**inputs)
    features = features / features.norm(p=2, dim=-1, keepdim=True)
    return features.numpy().astype('float32')

def generate_blip_caption(image: Image.Image, model, processor):
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs, max_new_tokens=50, min_length=20)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

def search_similar_images(query_embedding, index, image_paths, top_k=TOP_K):
    distances, indices = index.search(query_embedding, top_k)
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(image_paths):
            results.append({
                "path": image_paths[idx],
                "score": float(distances[0][i]),
                "class_name": extract_class_name(image_paths[idx])
            })
    return results

def extract_class_name(image_path: str) -> str:
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

def get_metadata_by_class(class_name: str) -> dict:
    for item in BATIK_METADATA:
        if item["class_name"].lower() == class_name.lower():
            return item
    for item in BATIK_METADATA:
        if item["class_name"].lower() in class_name.lower():
            return item
    return None

def generate_narration(class_name: str, metadata: dict, blip_caption: str) -> dict:
    try:
        client = Groq(api_key=GROQ_API_KEY)
    except Exception:
        return _fallback_narration(metadata, class_name, "API Key error")

    meaning = metadata['meaning'] if metadata else "Data tidak ditemukan."
    desc_db = metadata['description'] if metadata else "Pola batik tradisional."
    
    prompt = f"""
    Kamu adalah Kurator Museum Batik Profesional.
    
    [DATA]
    - Motif: {class_name}
    - Filosofi Baku: {meaning}
    - Deskripsi Baku: {desc_db}
    - PENGAMATAN VISUAL (BLIP): "{blip_caption}"
    
    [TUGAS]
    Buatlah narasi JSON dengan format persis seperti ini:
    {{
        "philosophy": "Tuliskan esai filosofi lengkap dalam 3 paragraf pendek di sini. Gunakan bahasa Indonesia yang puitis dan mendalam.",
        "structure": "Tuliskan analisis visual lengkap dalam 2 paragraf di sini. Gabungkan data baku dan pengamatan visual."
    }}
    Output JSON Only.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant that outputs clean JSON."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile", 
            temperature=0.5, 
            response_format={"type": "json_object"}
        )
        result_json = chat_completion.choices[0].message.content
        parsed_result = json.loads(result_json)
        
        philosophy_content = parsed_result.get("philosophy", meaning)
        structure_content = parsed_result.get("structure", desc_db)

        if isinstance(philosophy_content, dict):
            philosophy_content = "\n\n".join([str(v) for v in philosophy_content.values()])
        if isinstance(structure_content, dict):
            structure_content = "\n\n".join([str(v) for v in structure_content.values()])
        if isinstance(philosophy_content, list):
            philosophy_content = "\n\n".join([str(v) for v in philosophy_content])
        if isinstance(structure_content, list):
            structure_content = "\n\n".join([str(v) for v in structure_content.values()])
            
        return {"philosophy": str(philosophy_content), "structure": str(structure_content)}

    except Exception as e:
        return _fallback_narration(metadata, class_name, str(e))

def _fallback_narration(metadata, class_name, error_msg=""):
    meaning = metadata['meaning'] if metadata else "Tidak ada data."
    desc = metadata['description'] if metadata else "Tidak ada deskripsi."
    return {
        "philosophy": f"**[Mode Offline]** {meaning}. (Error: {error_msg})",
        "structure": f"**[Mode Offline]** {desc}"
    }

# =============================================================================
# NEW MODERN UI/UX IMPLEMENTATION
# =============================================================================

def inject_custom_css():
    st.markdown("""
    <style>
    /* IMPORT FONTS: Playfair Display (Serif) & Plus Jakarta Sans (Sans) */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');

    /* BACKGROUND TEXTURE: Subtle Nitik/Dot Pattern */
    .stApp {
        background-color: #0E1117;
        background-image: radial-gradient(#262730 1px, transparent 1px), radial-gradient(#262730 1px, transparent 1px);
        background-size: 20px 20px;
        background-position: 0 0, 10px 10px;
    }

    /* TYPOGRAPHY */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #E0E0E0;
    }
    
    p, div, span {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* HERO HEADER */
    .hero-container {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(180deg, rgba(212,175,55,0.15) 0%, rgba(14,17,23,0) 100%);
        border-bottom: 1px solid rgba(212,175,55,0.3);
        margin-bottom: 30px;
        border-radius: 0 0 20px 20px;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #D4AF37; /* Gold */
        margin-bottom: 0px;
        text-shadow: 0px 0px 10px rgba(212,175,55,0.3);
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #aaa;
        font-style: italic;
        font-family: 'Playfair Display', serif;
    }

    /* GLASSMORPHISM CARD FOR RESULTS */
    .result-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }

    /* IMAGE FRAME (MUSEUM STYLE) */
    .museum-frame img {
        border: 8px solid #1a1a1a;
        outline: 2px solid #D4AF37;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
        border-radius: 4px;
    }

    /* NARRATIVE BOX */
    .philosophy-text {
        font-family: 'Playfair Display', serif;
        font-size: 1.15rem;
        line-height: 1.8;
        color: #f0f0f0;
        text-align: justify;
        padding: 15px;
        border-left: 4px solid #D4AF37;
        background: rgba(212,175,55, 0.05);
        border-radius: 0 10px 10px 0;
    }

    /* TABS CUSTOMIZATION */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0 0;
        color: #aaa;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(212,175,55,0.1);
        color: #D4AF37;
        border-bottom: 2px solid #D4AF37;
    }

    /* BUTTONS */
    .stButton>button {
        background-color: transparent;
        border: 1px solid #D4AF37;
        color: #D4AF37;
        border-radius: 20px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #D4AF37;
        color: #000;
        box-shadow: 0 0 10px rgba(212,175,55,0.5);
    }
    
    /* HIDE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Batik Nitik 960: Digital Museum", page_icon="🏛️", layout="wide")
    inject_custom_css()

    # --- HERO SECTION ---
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">BATIK NITIK 960</h1>
        </div>
    """, unsafe_allow_html=True)

    # --- LOAD MODELS ---
    # Menggunakan placeholder agar tidak merusak layout saat loading awal
    with st.container():
        try:
            clip_model, clip_processor, blip_model, blip_processor = load_models()
            index, image_paths = load_faiss_index()
            if index is None:
                st.error("⚠️ Database Index belum tersedia. Jalankan indexing dulu.")
                st.stop()
        except Exception as e:
            st.error(f"Gagal inisialisasi sistem: {e}")
            st.stop()

    # --- INPUT SECTION (DUAL MODE: UPLOAD & CAMERA) ---
    st.markdown("### Identifikasi Koleksi")
    
    input_tabs = st.tabs(["Upload File", "Kamera Langsung"])
    
    query_image = None
    source_type = None

    with input_tabs[0]:
        uploaded_file = st.file_uploader("Pilih gambar motif batik", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            query_image = Image.open(uploaded_file).convert("RGB")
            source_type = "upload"

    with input_tabs[1]:
        camera_file = st.camera_input("Ambil foto motif secara tegak lurus")
        if camera_file:
            query_image = Image.open(camera_file).convert("RGB")
            source_type = "camera"

    # --- PROCESSING PIPELINE ---
    if query_image:
        # Layout Utama: 2 Kolom (Visual vs Narasi)
        st.divider()
        col_visual, col_narrative = st.columns([1, 1.3], gap="large")

        # Inisialisasi Timer
        start_total = time.time()
        vision_time = 0
        gen_time = 0
        is_success = False

        try:
            # 1. VISUAL COLUMN
            with col_visual:
                st.markdown('<div class="museum-frame">', unsafe_allow_html=True)
                st.image(query_image, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Visual Processing Progress
                progress_text = "Menganalisis pola visual..."
                my_bar = st.progress(0, text=progress_text)

                # VISION PROCESS
                start_vision = time.time()
                query_embedding = get_image_embedding(query_image, clip_model, clip_processor)
                my_bar.progress(30, text="Mencocokkan dengan 960 motif database...")
                
                results = search_similar_images(query_embedding, index, image_paths, TOP_K)
                top_result = results[0]
                
                my_bar.progress(60, text="Membuat deskripsi optik...")
                blip_caption = generate_blip_caption(query_image, blip_model, blip_processor)
                my_bar.progress(100, text="Selesai.")
                time.sleep(0.5)
                my_bar.empty()
                
                vision_time = time.time() - start_vision

                # Tampilkan Hasil Identifikasi (Card Style)
                st.markdown(f"""
                <div class="result-card">
                    <h3 style="margin:0; color:#D4AF37;">{top_result['class_name']}</h3>
                    <p style="margin:0; font-size:0.9em; color:#aaa;">Confidence Score: {top_result['score']:.1%}</p>
                    <hr style="border-color:rgba(255,255,255,0.1);">
                    <p style="font-style:italic; font-size:0.9em;">"{blip_caption}"</p>
                </div>
                """, unsafe_allow_html=True)

            # 2. NARRATIVE COLUMN
            with col_narrative:
                st.subheader("Kurasi Budaya")
                
                # NARRATIVE GENERATION
                start_gen = time.time()
                with st.spinner("Kurator AI sedang menulis narasi..."):
                    metadata = get_metadata_by_class(top_result["class_name"])
                    narration = generate_narration(top_result["class_name"], metadata, blip_caption)
                gen_time = time.time() - start_gen

                # Display Tabs
                tab_phil, tab_vis, tab_ref = st.tabs(["FILOSOFI", "ANALISIS VISUAL", "REFERENSI"])
                
                with tab_phil:
                    st.markdown(f'<div class="philosophy-text">{narration["philosophy"]}</div>', unsafe_allow_html=True)
                
                with tab_vis:
                    st.markdown(f'<div class="philosophy-text">{narration["structure"]}</div>', unsafe_allow_html=True)
                
                with tab_ref:
                    st.caption("Motif serupa dalam database:")
                    cols_ref = st.columns(3)
                    for i, res in enumerate(results):
                        with cols_ref[i]:
                            try:
                                st.image(Image.open(res['path']), use_container_width=True)
                                st.caption(f"{res['class_name']}\n({res['score']:.2f})")
                            except: pass

            is_success = True
            st.toast(f"Analisis Selesai: {top_result['class_name']}", icon="✅")

        except Exception as e:
            st.error(f"Terjadi kesalahan: {str(e)}")
            is_success = False

        # --- FOOTER: EVALUATION PANEL (COLLAPSIBLE) ---
        end_total = time.time()
        total_latency = end_total - start_total
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        with st.expander("Panel Data Teknis & Latency"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Latency", f"{total_latency:.2f}s")
            c2.metric("Vision Process", f"{vision_time:.2f}s")
            c3.metric("LLM Generation", f"{gen_time:.2f}s")
            
            st.json({
                "model_clip": CLIP_MODEL_ID,
                "model_blip": BLIP_MODEL_ID,
                "top_k": TOP_K,
                "detected_class": top_result['class_name'] if is_success else "N/A"
            })

    else:
        # EMPTY STATE / WELCOME
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 50px;">
            <p>Silakan unggah atau ambil foto kain batik untuk memulai eksplorasi.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
