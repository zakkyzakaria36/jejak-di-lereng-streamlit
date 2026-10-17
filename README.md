# 🏔️ Jejak di Lereng - Streamlit Dashboard

Analisis Spasio-Temporal Tanah Longsor DIY (2016-2026)

## 📊 Dataset

- **112 kejadian longsor** tervalidasi
- **5 wilayah DIY**: Kulon Progo, Sleman, Gunungkidul, Bantul, Kota Yogyakarta
- **10 tahun data**: Februari 2016 – Februari 2026

## 🎯 Fitur

✅ **Dashboard Interaktif** - 5 tabs dengan visualisasi lengkap  
✅ **Antigravity Design** - Dark theme dengan gradient modern  
✅ **Interactive Charts** - Plotly untuk exploration data  
✅ **Data Download** - Export CSV untuk analisis lanjutan  
✅ **Responsive** - Optimized untuk mobile & desktop  

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run App
```bash
streamlit run app.py
```

### 3. Open Browser
```
http://localhost:8501
```

## 📁 Struktur

```
jejak-streamlit/
├── app.py                    # Main Streamlit app
├── requirements.txt          # Dependencies
├── .streamlit/
│   └── config.toml          # Streamlit config
└── README.md                # Documentation
```

## 📊 Tabs

1. **Dashboard Utama** - Key metrics & overview
2. **Analisis Spasial** - Distribusi per wilayah
3. **Analisis Temporal** - Trend waktu & musiman
4. **Dampak & Mitigasi** - Breakdown dampak & program
5. **Data & Download** - Export & explore data

## 🎨 Design

- **Theme**: Antigravity Dark
- **Primary Color**: #FF6B6B (Red)
- **Secondary**: #A855F7 (Purple)
- **Background**: #0A0E1A (Almost Black)

## 📈 Key Findings

- **Kulon Progo Hotspot**: 41 kejadian (36.6%)
- **Musim Hujan Pattern**: 96 kejadian (86%) pada Okt-Mar
- **Puncak 2021**: 24 kejadian (tertinggi)
- **Mitigasi Efektif**: 0% fatality rate post-2020 (vs 45.5% pre-2020)

## 🔗 Deploy

### Streamlit Cloud
1. Push ke GitHub
2. Buka https://share.streamlit.io
3. New app → Select repo → `app.py`
4. Deploy!

## 📌 Data Sources

- DIBI BNPB (Database Bencana Alam)
- BPBD DIY (Badan Penanggulangan Bencana)
- BMKG Yogyakarta (Curah Hujan)
- Peta Rawan Bencana DIY

---

**Instagram**: @zkyzakariaa  
**Project**: Jejak di Lereng - Analisis Longsor DIY 2016-2026
