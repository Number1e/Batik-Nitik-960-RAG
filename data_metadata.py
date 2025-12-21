import pandas as pd

BATIK_METADATA = [
    {
        "class_name": "Sekar Kemuning",
        "meaning": "Keseimbangan antara cipta (pemikiran), rasa, dan karsa. Melambangkan konsentrasi penuh dan kesucian.",
        "description": "Diambil dari tanaman Kemuning (Murraya paniculata). Bunganya harum di malam hari, daunnya sering dipakai untuk alas jenazah."
    },
    {
        "class_name": "Ceplok Liring",
        "meaning": "Peringatan agar tidak memandang remeh (liring/melirik) orang lain. Sikap hati-hati dan saling menghargai.",
        "description": "Motif ceplok (beraturan) yang terinspirasi dari pandangan sudut mata."
    },
    {
        "class_name": "Sekar Duren",
        "meaning": "Peringatan agar tidak 'dlongop' (melamun/tidak kritis). Mendorong masyarakat untuk berpikir kritis demi inovasi.",
        "description": "Terinspirasi dari bunga durian (Durio)."
    },
    {
        "class_name": "Sekar Gayam",
        "meaning": "Melambangkan 'gayuh' (mencapai cita-cita) dan 'ayem' (tentram). Harapan agar hidup menentramkan bagi diri dan lingkungan.",
        "description": "Pohon Gayam (Inocarpus fagifer) adalah peneduh dan penyerap air yang baik."
    },
    {
        "class_name": "Sekar Pacar",
        "meaning": "Manusia harus 'migunani' (bermanfaat) bagi sesama, seperti bunga pacar yang harum dan berguna untuk upacara.",
        "description": "Bunga pacar air (Impatiens balsamina L.), kecil namun harum."
    },
    {
        "class_name": "Arumdalu",
        "meaning": "Manusia hendaknya berbuat kebaikan yang berguna bagi sekitar tanpa memandang perbedaan, ibarat wangi di kegelapan malam.",
        "description": "Bunga Cestrum nocturnum yang mekar dan harum pada malam hari."
    },
    {
        "class_name": "Sekar Srigading",
        "meaning": "Simbol kerukunan, ketenangan, dan kedamaian dalam rumah tangga atau masyarakat.",
        "description": "Tanaman Sri Gading (Nyctanthes arbor-tristis), bunga putih bertangkai merah yang harum."
    },
    {
        "class_name": "Kemukus",
        "meaning": "Peringatan untuk selalu waspada (eling lan waspada) menghadapi segala kemungkinan marabahaya.",
        "description": "Lintang kemukus adalah sebutan Jawa untuk komet atau bintang berekor."
    },
    {
        "class_name": "Sekar Gudhe",
        "meaning": "Simbol agar hidup manusia bermanfaat (migunani) bagi sesama, sumber protein dan penyubur tanah.",
        "description": "Kembang Gudhe (Cajanus cajan) atau kacang gude."
    },
    {
        "class_name": "Sekar Ketongkeng",
        "meaning": "Keindahan yang unik dari bentuk alami.",
        "description": "Sejenis anggrek (Scorpions orhide) yang bunganya menyerupai kalajengking."
    },
    {
        "class_name": "Brendi",
        "meaning": "Mengambil ide dari simbol dagang minuman keras era kolonial (tiga koin berjajar), diadaptasi menjadi seni.",
        "description": "Brendi adalah minuman keras impor zaman Hindia Belanda."
    },
    {
        "class_name": "Cakar Ayam",
        "meaning": "Simbol semangat mencari rejeki (seperti ayam mengais tanah pagi hari). Biasa dipakai saat acara 'mitoni' atau pernikahan.",
        "description": "Motif menyerupai jejak kaki ayam yang saling terkait."
    },
    {
        "class_name": "Sekar Menur",
        "meaning": "Melambangkan kesucian dan kebaikan hati yang melimpah tanpa pamrih (putih bersih menumpuk).",
        "description": "Bunga Menur (Clerodendrum chinense) berwarna putih bersih dan bersusun."
    },
    {
        "class_name": "Sekar Tebu",
        "meaning": "Nasihat agar tidak berlebihan dalam menilai sesuatu. Hati-hati dan penuh perhitungan.",
        "description": "Bunga tebu (Saccharum officinarum) atau 'gleges' (tertawa)."
    },
    {
        "class_name": "Sekar Manggis",
        "meaning": "Harapan agar pemakainya menjadi manusia terbaik lahir batin (seperti manggis yang jujur, isi sesuai kulit).",
        "description": "Manggis (Garcinia mangostana), ratu buah."
    },
    {
        "class_name": "Sekar Randu",
        "meaning": "Memberi kenikmatan/manfaat kepada sesama dan selalu menjaga nama baik (kehormatan).",
        "description": "Bunga pohon kapuk randu (Ceiba pentandra)."
    },
    {
        "class_name": "Worawari Rumpuk",
        "meaning": "Simbol cinta, gairah, dan semangat yang menyala (warna merah).",
        "description": "Bunga sepatu tumpuk (Hibiscus) yang berwarna merah."
    },
    {
        "class_name": "Sekar Duku",
        "meaning": "Ide artistik dari alam sekitar tempat tinggal.",
        "description": "Bentuk bunga duku dilihat dari atas."
    },
    {
        "class_name": "Sekar Jagung",
        "meaning": "Pesan untuk menghormati sesama manusia, terutama orang yang lebih tua (Sinuwun/ditinggikan).",
        "description": "Bunga jagung (Zea mays)."
    },
    {
        "class_name": "Jayakirana",
        "meaning": "Simbol kepahlawanan, tanpa pamrih, dan rela berkorban untuk nusa bangsa.",
        "description": "Nama lain Wijanarka, senapati kerajaan Malwapati dalam pewayangan."
    },
    {
        "class_name": "Mawur",
        "meaning": "Menggambarkan sesuatu yang tersebar atau berserakan.",
        "description": "Mawur dalam bahasa Jawa artinya tidak menyatu."
    },
    {
        "class_name": "Sekar Tanjung",
        "meaning": "Harapan agar selalu menjunjung tinggi ('tansah njunjung') perbuatan baik yang mengharumkan nama keluarga.",
        "description": "Bunga Tanjung (Mimusops elengi) yang harum."
    },
    {
        "class_name": "Sekar Keben",
        "meaning": "Harapan untuk mencari ketentraman dan pengayoman. Simbol perlindungan yang indah.",
        "description": "Pohon Keben (Barringtonia asiatica) yang biasa tumbuh di keraton."
    },
    {
        "class_name": "Sekar Srengenge",
        "meaning": "Simbol konsistensi, ketegaran menghadapi hidup, dan selalu mencari 'cahaya' kebenaran.",
        "description": "Bunga Matahari (Helianthus annuus)."
    },
    {
        "class_name": "Sekar Soka",
        "meaning": "Ketabahan menjalani suka duka kehidupan (seperti Dewi Shinta di taman Arga Soka) hingga kebahagiaan sejati tiba.",
        "description": "Bunga Asoka (Ixora coccinea)."
    },
    {
        "class_name": "Sekar Nangka",
        "meaning": "Jangan menilai orang hanya dari luar (seperti nangka berduri tapi isinya manis).",
        "description": "Bunga/buah Nangka (Artocarpus heterophyllus) atau 'angkup'."
    },
    {
        "class_name": "Kawung Nitik",
        "meaning": "Pengendalian 4 hawa nafsu (Sedulur Papat Limo Pancer) untuk menyatu dengan Tuhan. Harapan masa depan berkembang.",
        "description": "Empat lingkaran yang saling bersinggungan dengan isen-isen nitik."
    },
    {
        "class_name": "Sekar Kentang",
        "meaning": "Harapan agar pemakai selalu memberikan manfaat (migunani) bagi sesama, seperti kentang sebagai pangan.",
        "description": "Bunga tanaman kentang (Solanum tuberosum)."
    },
    {
        "class_name": "Sekar Pudak",
        "meaning": "Harapan mampu menjaga kehormatan dan status sosial yang terhormat.",
        "description": "Bunga Pandan Duri (Pandanus tectorius) yang harum."
    },
    {
        "class_name": "Sekar Dlima",
        "meaning": "Ide artistik dari keindahan alam.",
        "description": "Bunga Delima (Punica granatum)."
    },
    {
        "class_name": "Karawitan",
        "meaning": "Hidup bermasyarakat harus bekerjasama secara harmonis (seperti orkestra gamelan) untuk menghasilkan kebaikan.",
        "description": "Terinspirasi dari bunga karawitan atau seni musik Jawa."
    },
    {
        "class_name": "Cinde Wilis",
        "meaning": "Simbol kesuburan dan kemakmuran (warna hijau).",
        "description": "Sutra hijau bermotif bunga, sering dipakai pengantin gaya Yogyakarta."
    },
    {
        "class_name": "Sekar Mlati",
        "meaning": "Simbol kesucian, menciptakan suasana menyenangkan dan menyehatkan bagi orang banyak.",
        "description": "Bunga Melati (Jasmine)."
    },
    {
        "class_name": "Kuncup Kanthil",
        "meaning": "Simbol 'kemanthil' (selalu teringat/lekat). Harapan agar kebaikan selalu dikenang dan diteladani.",
        "description": "Bunga Cempaka/Kanthil (Magnolia x alba)."
    },
    {
        "class_name": "Sekar Dangan",
        "meaning": "Harapan untuk kesembuhan atau masa depan yang lebih baik ('dangan' = sembuh).",
        "description": "Motif berbentuk bunga geometris."
    },
    {
        "class_name": "Sekar Sawo",
        "meaning": "Peringatan agar 'rikuh' (segan/sopan), memperhatikan etika pergaulan, dan menghormati orang lain.",
        "description": "Bunga Sawo (Manilkara zapota)."
    },
    {
        "class_name": "Manggar",
        "meaning": "Simbol kesetiaan antara satu dengan yang lainnya.",
        "description": "Bunga kelapa (Cocos nucifera) yang berbentuk mayang."
    },
    {
        "class_name": "Sekar Cengkeh",
        "meaning": "Menerima pemberian Tuhan dengan hati lega/puas ('plong').",
        "description": "Bunga Cengkeh (Syzygium aromaticum) atau 'polong'."
    },
    {
        "class_name": "Sritaman",
        "meaning": "Harapan agar pemakainya selalu bersikap bijaksana (seperti raja di taman sari).",
        "description": "Taman di dalam istana raja."
    },
    {
        "class_name": "Sekar Mundu",
        "meaning": "Menyatu dengan lingkungan, membangun kebersamaan, dan berbagi.",
        "description": "Bunga Mundu (Garcinia dulcis)."
    },
    {
        "class_name": "Sekar Andong",
        "meaning": "Menangkap keindahan di antara perbedaan (bunga putih di antara daun merah).",
        "description": "Tanaman Andong (Cordyline fruticosa)."
    },
    {
        "class_name": "Gedhangan",
        "meaning": "Simbol kemampuan menjaga rahasia (seperti tabung penyimpan azimat).",
        "description": "Bentuk tabung (gedhang/pisang-pisangan)."
    },
    {
        "class_name": "Sekar Pala",
        "meaning": "Harapan hidup tenang dan tentram, namun tetap waspada.",
        "description": "Bunga Pala (Myristica fragrans) yang bijinya menenangkan."
    },
    {
        "class_name": "Klampok Arum",
        "meaning": "Harapan mendapatkan nama baik (harum) dan kebahagiaan.",
        "description": "Varietas jambu air (Syzygium jambos) yang manis dan wangi."
    },
    {
        "class_name": "Sekar Jali",
        "meaning": "Simbol kehidupan yang memberikan manfaat dan mengenyangkan.",
        "description": "Tanaman Jali (Coix lacryma-jobi L), sejenis rumput biji-bijian."
    },
    {
        "class_name": "Sekar Lintang",
        "meaning": "Jadilah manusia besar yang bersinar layaknya bintang dan bermanfaat bagi orang lain.",
        "description": "Bintang (Star)."
    },
    {
        "class_name": "Sekar Kenanga",
        "meaning": "Menghormati leluhur dengan cara berbuat kebaikan (kenang-a).",
        "description": "Bunga Kenanga (Cananga odorata), khas untuk upacara adat."
    },
    {
        "class_name": "Sekar Jeruk",
        "meaning": "Hidup hendaknya 'alon' (pelan tapi pasti), hati-hati, tidak grusa-grusu (terburu-buru).",
        "description": "Bunga Jeruk (Citrus)."
    },
    {
        "class_name": "Sekar Mindi",
        "meaning": "Harapan agar selalu berbuat yang bermanfaat bagi sesama (seperti batang mindi yang berguna).",
        "description": "Pohon Mindi (Melia azedarach)."
    },
    {
        "class_name": "Tanjung Gunung",
        "meaning": "Harapan mendapatkan kebahagiaan, kehormatan, dan nama baik.",
        "description": "Variasi motif Tanjung."
    },
    {
        "class_name": "Sekar Kenikir",
        "meaning": "Simbol kegiatan bermanfaat dan kesehatan (penawar penyakit).",
        "description": "Tanaman Kenikir (Cosmos caudatus)."
    },
    {
        "class_name": "Sekar Blimbing",
        "meaning": "Filosofi untuk memancarkan kebaikan (seperti bentuk bintang buah belimbing).",
        "description": "Bunga Belimbing (Averrhoa carambola)."
    },
    {
        "class_name": "Sekar Pijetan",
        "meaning": "Harapan memelihara keseimbangan hidup untuk mencapai ketenangan dan kebahagiaan.",
        "description": "Buah Pijetan (Krendang) yang rasanya asam manis."
    },
    {
        "class_name": "Sarimulat",
        "meaning": "Menjadi manusia yang selalu mawas diri (introspeksi).",
        "description": "Sari (inti) dan Mulat (melihat ke dalam diri)."
    },
    {
        "class_name": "Sekar Mrica",
        "meaning": "Kesiapan menghadapi segala pengalaman hidup, baik manis maupun pedas/pahit, demi kedewasaan.",
        "description": "Merica (Piper nigrum) yang pedas."
    },
    {
        "class_name": "Sekar Kepel",
        "meaning": "Semangat kebersamaan, persatuan, dan gotong royong (mengepal/bersatu).",
        "description": "Buah Kepel (Stelechocarpus burahol) yang menempel di batang."
    },
    {
        "class_name": "Truntum",
        "meaning": "Cahaya terang kehidupan mulia yang diturunkan ke generasi berikutnya. Biasa dipakai orang tua pengantin.",
        "description": "Tumaruntum (tumbuh/turun temurun) dan gambaran sinar bintang."
    },
    {
        "class_name": "Jayakusuma",
        "meaning": "Simbol ketaatan, kepatuhan pada orang tua/pimpinan, dan jiwa ksatria muda.",
        "description": "Nama salah satu putra Arjuna dalam pewayangan."
    },
    {
        "class_name": "Rengganis",
        "meaning": "Simbol langkah baik dalam membela kebenaran dan kecantikan budi.",
        "description": "Dewi Rengganis, putri cantik dari kerajaan Mukadam dalam cerita Menak."
    },
    {
        "class_name": "Sekar Gambir",
        "meaning": "Kesucian hati yang menebarkan keharuman (perilaku mulia) bagi lingkungannya.",
        "description": "Bunga Melati Gambir (Jasminum officinale)."
    }
]

def get_metadata_df():
    """Mengembalikan dataframe pandas dari metadata."""
    return pd.DataFrame(BATIK_METADATA)

# Opsional: Fungsi bantu untuk testing
if __name__ == "__main__":
    df = get_metadata_df()
    print(f"Total Motif Terdaftar: {len(df)}")
    print(df.head())