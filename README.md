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
| **Accuracy** | 0.89 |
| **Precision** | 0.86 |
| **Recall (Dropout Detection)** | 0.79 |
| **F1-Score** | 0.82 |
| **ROC-AUC** | 0.94 |

> Model ini sangat handal dalam membedakan antara mahasiswa yang berisiko keluar (*Dropout*) dan yang tidak, dengan skor ROC-AUC mencapai 0.94.

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
[https://bpds-submission-2-dicoding.streamlit.app/](https://bpds-submission-2-dicoding.streamlit.app/)

## Conclusion
Berdasarkan analisis data, penyebab utama *dropout* di Jaya Jaya Institut adalah **ketidakstabilan finansial** dan **kegagalan akademik pada tahun pertama**. Terdapat korelasi yang sangat kuat antara mahasiswa yang berhutang (*debtor*) dengan kegagalan dalam meluluskan jumlah SKS minimum pada semester 1 dan 2. Model Machine Learning kami berhasil menangkap pola ini dengan akurasi 89%, menjadikannya alat yang valid untuk sistem deteksi dini.

### Rekomendasi Action Items
Untuk menurunkan angka *dropout*, Jaya Jaya Institut disarankan untuk:
1.  **Implementasi Early Warning System (EWS):** Mengintegrasikan model ini ke dalam sistem manajemen mahasiswa untuk menandai secara otomatis mahasiswa berisiko tinggi segera setelah nilai Semester 1 keluar.
2.  **Intervensi Finansial Proaktif:** Memberikan bantuan khusus bagi mahasiswa berstatus *Debtor* melalui skema cicilan yang lebih fleksibel atau menghubungkan mereka dengan program beasiswa tambahan.
3.  **Pendampingan Akademik Semester 1:** Memfungsikan dosen pembimbing akademik untuk melakukan bimbingan intensif bagi mahasiswa yang gagal meluluskan lebih dari 30% SKS di semester pertama.
4.  **Dukungan Khusus Mahasiswa Dewasa:** Menyediakan fleksibilitas jadwal atau layanan dukungan konseling bagi mahasiswa berusia dewasa yang seringkali memiliki hambatan waktu antara pekerjaan dan studi.
