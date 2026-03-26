# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding
Jaya Jaya Institut merupakan salah satu institusi pendidikan perguruan yang telah berdiri sejak tahun 2000. Hingga saat ini ia telah mencetak banyak lulusan dengan reputasi yang sangat baik. Akan tetapi, terdapat banyak juga siswa yang tidak menyelesaikan pendidikannya alias dropout.

Jumlah dropout yang tinggi ini tentunya menjadi salah satu masalah yang besar untuk sebuah institusi pendidikan. Oleh karena itu, Jaya Jaya Institut ingin mendeteksi secepat mungkin siswa yang mungkin akan melakukan dropout sehingga dapat diberi bimbingan khusus.

Dalam proyek ini, pendekatan data science digunakan untuk menganalisis faktor-faktor yang memengaruhi dropout serta membangun model machine learning yang dapat memprediksi kemungkinan seorang mahasiswa mengalami dropout.

### Permasalahan Bisnis
Berikut adalah permasalahan bisnis yang ingin diselesaikan:

- Tingginya angka mahasiswa dropout di Jaya Jaya Institut
- Kesulitan dalam mengidentifikasi mahasiswa yang berisiko dropout secara dini
- Belum adanya sistem berbasis data untuk mendukung pengambilan keputusan terkait intervensi akademik
- Kurangnya pemahaman mengenai faktor-faktor utama yang memengaruhi keberhasilan atau kegagalan studi mahasiswa

### Cakupan Proyek
Cakupan dari proyek ini meliputi:

- Melakukan eksplorasi dan analisis data mahasiswa untuk memahami karakteristik dan pola yang berkaitan dengan dropout
- Mengidentifikasi faktor-faktor utama yang memengaruhi kemungkinan mahasiswa mengalami dropout
- Mengembangkan model machine learning untuk memprediksi risiko dropout mahasiswa
- Mengubah permasalahan menjadi klasifikasi biner (dropout vs tidak dropout) untuk mendukung sistem early warning
- Membuat dashboard interaktif untuk membantu pihak institusi dalam memonitor performa mahasiswa
- Mengembangkan prototype sistem prediksi berbasis Streamlit yang dapat digunakan oleh pengguna non-teknis
- Memberikan rekomendasi berbasis data (action items) untuk membantu institusi dalam menurunkan angka dropout

## Data Understanding
Dataset yang digunakan berasal dari "Students' Performance" yang mencakup informasi demografis, sosial-ekonomi, dan akademik. Tahap pemahaman data melibatkan audit kualitas untuk memastikan keandalan model:
- **Missing Values**: Tidak terdeteksi adanya nilai yang hilang (*null values*).
- **Duplicate Data**: Tidak ditemukan baris data ganda (*0 duplicate rows*).
- **Invalid Values**: Seluruh fitur numerik kunci (seperti *Curricular units* dan *Age*) divalidasi memiliki nilai dalam rentang yang logis.

#### Persiapan

Sumber data: [Students' Performance](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance)

Setup environment:
```
pip install -r requirements.txt
```

## Business Dashboard
Dashboard interaktif telah dibuat menggunakan Tableau Public untuk memberikan visibilitas terhadap pendorong utama *dropout*. Anda dapat mengakses dashboard tersebut melalui tautan berikut:

**[Jaya Jaya Institut - Business Dashboard (Tableau Public)](https://public.tableau.com/views/BusinessDashboardEduTech/Home?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)**

Wawasan utama dari dashboard meliputi:
*   **Akar Masalah Ekonomi:** Mahasiswa yang memiliki status *Debtor* (berhutang) atau menunggak biaya kuliah (*Tuition fees not up to date*) memiliki tingkat *dropout* yang sangat tinggi. Sebaliknya, penerima beasiswa memiliki tingkat kelulusan yang hampir sempurna.
*   **Sinyal Akademik Dini:** Penurunan performa akademik (IPK mendekati 0) dan rendahnya jumlah SKS yang lulus pada Semester 1 merupakan prediktor terkuat kegagalan studi.
*   **Faktor Demografis:** Mahasiswa laki-laki dan mereka yang mendaftar pada usia yang lebih dewasa (*mature students*) cenderung memiliki risiko dropout yang lebih tinggi dibandingkan mahasiswi perempuan atau siswa lulusan SMA baru.

### Data Preprocessing
Untuk mengoptimalkan performa model, sistem menggunakan strategi **Hybrid Encoding**:
*   **One-Hot Encoding**: Diterapkan pada fitur kategorikal dengan jumlah kategori rendah (≤ 2), seperti *Gender* dan status beasiswa.
*   **Label Encoding**: Diterapkan pada fitur kategorikal dengan jumlah kategori yang lebih banyak (> 2), seperti *Course* dan *Nationality*. Hal ini bertujuan untuk mencegah ledakan dimensi fitur (*feature explosion*) namun tetap mempertahankan informasi kategori yang kaya.
*   **Standard Scaling**: Dilakukan normalisasi pada seluruh fitur numerik dan fitur hitung (*count*) untuk memastikan model konvergen lebih cepat.

## Modelling & Evaluation
Model terbaik yang dikembangkan menggunakan algoritma **Gradient Boosting** dengan optimasi hiperparameter melalui *Optuna*. Model ini dirancang untuk memaksimalkan deteksi risiko dini.

Berikut adalah performa model pada data uji:
| Metric | Score |
| :--- | :--- |
| **Accuracy** | 0.91 |
| **Precision** | 0.90 |
| **Recall (Dropout Detection)** | 0.87 |
| **F1-Score** | 0.88 |
| **ROC-AUC** | 0.96 |

> Model ini sangat handal dalam membedakan antara mahasiswa yang berisiko keluar (*Dropout*) dan yang lulus (*Graduate*), dengan skor ROC-AUC mencapai 0.96.

### Feature Importance
Berdasarkan analisis model Gradient Boosting, faktor-faktor utama yang paling memengaruhi kemungkinan mahasiswa *dropout* adalah:
1.  **Curricular units 2nd sem approved**: Jumlah mata kuliah yang approved di semester 2 (Faktor terkuat).
2.  **Curricular units 1st sem approved**: Jumlah mata kuliah yang approved di semester 1.
3.  **Tuition fees up to date**: Kedisiplinan pembayaran uang kuliah.
4.  **Curricular units 2nd sem grade**: Rata-rata nilai pada semester 2.
5.  **Age at enrollment**: Usia saat mendaftar (Mahasiswa yang lebih tua memiliki risiko dropout lebih tinggi).

## Menjalankan Sistem Machine Learning
Prototype aplikasi prediksi dikembangkan menggunakan **Streamlit**. Aplikasi ini memungkinkan staf akademik untuk memasukkan profil mahasiswa dan mendapatkan prediksi risiko secara instan.

**Cara Menjalankan secara Lokal:**
1. Pastikan Anda berada di direktori proyek.
2. Jalankan perintah:
```
streamlit run app.py
```
3. Buka URL yang muncul di terminal (biasanya `http://localhost:8501`).

**Link Deployment:**
[https://bpds-submission-2-drtaufiqh.streamlit.app/](https://bpds-submission-2-drtaufiqh.streamlit.app/)

## Conclusion

Proyek ini berhasil mengembangkan solusi berbasis data untuk memitigasi risiko *dropout* di Jaya Jaya Institut. Melalui pendekatan data science, kita dapat memahami pola kegagalan studi dan mengidentifikasi mahasiswa yang membutuhkan dukungan secara proaktif.

### Pemilihan Model Terbaik
Dari seluruh eksperimen pemodelan yang dilakukan (termasuk *Logistic Regression* dan *Random Forest*), model **Gradient Boosting** dipilih sebagai model final. Berikut adalah alasannya:
- **Performa Unggul**: Model ini mencapai skor **ROC-AUC 0.96**, yang menunjukkan kemampuan luar biasa dalam membedakan antara mahasiswa yang akan *dropout* dan yang akan lulus.
- **Deteksi Risiko Maksimal**: Dengan nilai **Recall sebesar 0.87**, model ini mampu menangkap sebagian besar kasus *dropout* potensial, meminimalkan jumlah mahasiswa berisiko yang tidak terdeteksi.
- **Stabilitas**: Metrik **F1-Score (0.88)** menunjukkan keseimbangan yang baik antara presisi dan recall, menjadikannya handal untuk digunakan dalam operasional institusi.

### Insight Utama
Hasil analisis dan pemodelan memberikan beberapa temuan kunci:
1.  **Prediktor Akademik Terkuat**: Keberhasilan meluluskan mata kuliah pada tahun pertama (khususnya **Curricular units 2nd sem approved**) adalah faktor tunggal paling berpengaruh. Mahasiswa yang gagal mendapatkan *approval* pada beban SKS di semester 2 memiliki peluang *dropout* yang sangat signifikan.
2.  **Hambatan Finansial**: Status pembayaran biaya kuliah (*Tuition fees up to date*) dan status hutang (*Debtor*) menjadi pendorong utama kedua. Hal ini menunjukkan bahwa banyak kasus *dropout* tidak hanya disebabkan oleh masalah kemampuan akademik, tetapi juga kendala ekonomi.
3.  **Risiko Demografis**: Mahasiswa laki-laki dan mereka yang mendaftar pada usia yang lebih dewasa (*mature students*) terdeteksi memiliki kerentanan lebih tinggi, kemungkinan karena tantangan penyesuaian sosial atau pembagian waktu antara beban kerja dan studi.

### Implikasi dan Rekomendasi Action Items
Implementasi model ini bukan hanya sekadar angka, melainkan alat pengambilan keputusan strategis. Berdasarkan temuan di atas, berikut adalah rekomendasi yang dapat ditindaklanjuti:

1.  **Implementasi Early Warning System (EWS):** Mengintegrasikan model Gradient Boosting ke dalam sistem informasi akademik untuk memberikan alert otomatis kepada dosen pembimbing jika performa akademik semester 1 mahasiswa berada di bawah ambang batas (threshold).
2.  **Optimasi Beasiswa dan Skema Pembayaran:** Fokuskan bantuan finansial atau diskon UKT pada mahasiswa yang memiliki record akademik baik namun terkendala status *debtor*. Hal ini memastikan potensi akademik tidak terbuang karena alasan biaya.
3.  **Program Mentoring Khusus:** Memberikan pendampingan akademik intensif bagi mahasiswa di transisi semester 1 ke semester 2, karena periode ini merupakan fase kritis yang paling menentukan kelangsungan studi mereka.
4.  **Kebijakan Inklusif untuk Mahasiswa Pendewasa:** Menyediakan fleksibilitas administratif bagi mahasiswa yang masuk di usia dewasa untuk membantu mereka menyeimbangkan tanggung jawab pribadi dengan target akademik.
