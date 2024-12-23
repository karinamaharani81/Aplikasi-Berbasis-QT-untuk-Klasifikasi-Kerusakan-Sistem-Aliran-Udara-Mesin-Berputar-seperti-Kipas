(Aplikasi Qt yang belum diupload)

# Aplikasi Berbasis QT untuk Klasifikasi Kerusakan Sistem Aliran Udara Mesin Berputar seperti Kipas

Proyek ini adalah aplikasi GUI Python berbasis PySide6 untuk merekam, memvisualisasikan, dan menganalisis sinyal audio secara real-time. Aplikasi mendukung perekaman audio hingga 40.000 Hz selama 15 detik, visualisasi FFT, dan penyimpanan dalam format WAV. Terintegrasi dengan Edge Impulse, memungkinkan unggah audio untuk pelatihan ML dan inferensi langsung.

## Authors
1. Galuh Pandu Satrio (2042231019)
2. Karina Lailatul Maghfiroh Maharani (2042231035)
3. Syahira Arliya Putri Subekti (2042231051)
4. Ahmad Radhy (Penguji)

Teknik Instrumentasi - Institut Teknologi Sepuluh Nopember

## Features 

1. **Voice Recording**: Rekam audio dari mikrofon menggunakan GUI yang intuitif dengan kecepatan sampling hingga 40.000 Hz.  
2. **Real-Time Visualization**: Tampilkan gelombang audio dan spektrum frekuensi secara langsung menggunakan grafik interaktif.  
3. **Audio Saving**: Simpan hasil rekaman dalam format WAV dengan nama file yang dapat disesuaikan.  
4. **Edge Impulse Integration**: Unggah file audio ke Edge Impulse untuk melatih model pembelajaran mesin.  
5. **Inference Processing**: Jalankan inferensi pada file audio menggunakan model yang sudah dilatih dan tampilkan hasilnya.  

## Requirements

### Software
- **Python 3.8+**
- **PySide6** (untuk GUI)
- **SoundDevice** (untuk perekaman audio)
- **SciPy** (untuk analisis FFT)
- **Matplotlib** (untuk visualisasi grafik)
- **Requests** (untuk komunikasi dengan API Edge Impulse)
- **Edge Impulse API** (untuk pengunggahan data dan inferensi model)


### Hardware
- Microphone (Input Audio) 
- Edge Impulse Platform 
- Computer (for GUI): Komputer atau laptop dengan sistem operasi yang mendukung PySide6 dan dependensi terkait untuk menjalankan aplikasi GUI ini.

## Instalasi

### 1. Clone the Repository
```bash
git clone https://github.com/karinamaharani81/Aplikasi-Berbasis-QT-untuk-Klasifikasi-Kerusakan-Sistem-Aliran-Udara-Mesin-Berputar-seperti-Kipas
```

### 2. Instal Dependensi Python 
```bash
pip install PySide6 sounddevice scipy matplotlib requests
```

### 3. Siapkan Platform Edge Impulse
```bash
npm install -g edge-impulse-cli
edge-impulse-login
```

### 4. Siapkan Hardware
- Mikrofon untuk merekam audio.
- Komputer atau laptop dengan sistem operasi yang mendukung PySide6 untuk menjalankan aplikasi GUI.

## Penggunaan

### 1. Run Aplikasi PySide6
Mulai aplikasi GUI:
```bash
python main.py
```

### 2. Merekam dan Visualisasi Audio
- Gunakan GUI untuk merekam audio.
- Visualisasikan gelombang audio dan spektrum frekuensi secara real-time

### 3. Simpan Rekaman Audio
- Rekaman audio dapat disimpan dalam format WAV dengan nama yang dapat disesuaikan.

### 4. Upload ke Edge Impulse
- Unggah rekaman audio ke Edge Impulse menggunakan GUI atau command line untuk keperluan pelatihan model:
```bash
edge-impulse-uploader recordings/yourfile.wav
```

### 5. Train Model
- Latih model di Edge Impulse menggunakan data yang telah diunggah.

### 6. Jalankan Inferensi
- Gunakan model yang telah dilatih untuk melakukan inferensi terhadap rekaman audio yang baru diunggah.
## Struktur Proyek
```
repository-name/
├── main.py              # Aplikasi GUI PySide6
├── recorder.py          # Logika perekaman suara
├── edge_impulse.py      # Integrasi dengan Edge Impulse
├── recordings/          # File audio yang disimpan
└── README.md            # Dokumentasi proyek
```

## Peningkatan Fitur Masa Mendatang
- Menambahkan fitur untuk mendukung lebih banyak format audio.
- Mengoptimalkan inferensi untuk penggunaan real-time.
- Menambahkan dukungan untuk integrasi dengan perangkat keras lainnya, seperti ESP32.
