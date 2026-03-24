import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Jaya Jaya Institut - Dropout Prediction",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data and models
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv", sep=";")
    return df

@st.cache_resource
def load_model_and_scaler():
    scaler = joblib.load("model/scaler.joblib")
    model = joblib.load("model/gradient_boosting_model.joblib")
    return scaler, model

df = load_data()
scaler, model = load_model_and_scaler()

# Definisi kolom fitur (sesuai tahap training)
numerical_cols = [
    'Previous_qualification_grade', 'Admission_grade', 'Age_at_enrollment',
    'Curricular_units_1st_sem_grade', 'Curricular_units_2nd_sem_grade',
    'Unemployment_rate', 'Inflation_rate', 'GDP'
]

nominal_cols = [
    'Marital_status', 'Application_mode', 'Course', 'Daytime_evening_attendance',
    'Nacionality', 'Mothers_occupation', 'Fathers_occupation', 'Displaced',
    'Educational_special_needs', 'Debtor', 'Tuition_fees_up_to_date',
    'Gender', 'Scholarship_holder', 'International'
]

ordinal_cols = [
    'Application_order', 'Previous_qualification',
    'Mothers_qualification', 'Fathers_qualification'
]

count_cols = [
    'Curricular_units_1st_sem_credited', 'Curricular_units_1st_sem_enrolled',
    'Curricular_units_1st_sem_evaluations', 'Curricular_units_1st_sem_approved',
    'Curricular_units_1st_sem_without_evaluations', 'Curricular_units_2nd_sem_credited',
    'Curricular_units_2nd_sem_enrolled', 'Curricular_units_2nd_sem_evaluations',
    'Curricular_units_2nd_sem_approved', 'Curricular_units_2nd_sem_without_evaluations'
]

# Mapping Dictionaries (Teks Manusia -> Kode Angka Dataset)
marital_map = {'Single': 1, 'Married': 2, 'Widower': 3, 'Divorced': 4, 'Facto union': 5, 'Legally separated': 6}

app_mode_map = {'1st phase - general contingent': 1, 'Ordinance No. 612/93': 2, '1st phase - special contingent (Azores Island)': 5, 'Holders of other higher courses': 7, 'Ordinance No. 854-B/99': 10, 'International student (bachelor)': 15, '1st phase - special contingent (Madeira Island)': 16, '2nd phase - general contingent': 17, '3rd phase - general contingent': 18, 'Ordinance No. 533-A/99, item b2) (Different Plan)': 26, 'Ordinance No. 533-A/99, item b3 (Other Institution)': 27, 'Over 23 years old': 39, 'Transfer': 42, 'Change of course': 43, 'Technological specialization diploma holders': 44, 'Change of institution/course': 51, 'Short cycle diploma holders': 53, 'Change of institution/course (International)': 57}

course_map = {'Biofuel Production Technologies': 33, 'Animation and Multimedia Design': 171, 'Social Service (evening attendance)': 8014, 'Agronomy': 9003, 'Communication Design': 9070, 'Veterinary Nursing': 9085, 'Informatics Engineering': 9119, 'Equinculture': 9130, 'Management': 9147, 'Social Service': 9238, 'Tourism': 9254, 'Nursing': 9500, 'Oral Hygiene': 9556, 'Advertising and Marketing Management': 9670, 'Journalism and Communication': 9773, 'Basic Education': 9853, 'Management (evening attendance)': 9991}

daytime_map = {'Daytime': 1, 'Evening': 0}

nacionality_map = {'Portuguese': 1, 'German': 2, 'Spanish': 6, 'Italian': 11, 'Dutch': 13, 'English': 14, 'Lithuanian': 17, 'Angolan': 21, 'Cape Verdean': 22, 'Guinean': 24, 'Mozambican': 25, 'Santomean': 26, 'Turkish': 32, 'Brazilian': 41, 'Romanian': 62, 'Moldova (Republic of)': 100, 'Mexican': 101, 'Ukrainian': 103, 'Russian': 105, 'Cuban': 108, 'Colombian': 109}

prev_qual_map = {'Secondary education': 1, "Higher education - bachelor's degree": 2, 'Higher education - degree': 3, "Higher education - master's": 4, 'Higher education - doctorate': 5, 'Frequency of higher education': 6, '12th year of schooling - not completed': 9, '11th year of schooling - not completed': 10, 'Other - 11th year of schooling': 12, '10th year of schooling': 14, '10th year of schooling - not completed': 15, 'Basic education 3rd cycle (9th/10th/11th year) or equiv.': 19, 'Basic education 2nd cycle (6th/7th/8th year) or equiv.': 38, 'Technological specialization course': 39, 'Higher education - degree (1st cycle)': 40, 'Professional higher technical course': 42, 'Higher education - master (2nd cycle)': 43}

binary_map = {'Yes': 1, 'No': 0}
gender_map = {'Male': 1, 'Female': 0}

st.title("🎓 Jaya Jaya Institut: Student Dropout Prediction")
st.markdown("Aplikasi ini dirancang untuk mendeteksi dini probabilitas **Mahasiswa Dropout** berdasarkan profil dan jejak akademik. Sistem menerjemahkan input label teks Anda kembali ke format numerik model secara otomatis.")

st.divider()
input_data = {}

def create_selectbox(col_name, mapping_dict):
    options = list(mapping_dict.keys())
    try:
        mode_val = int(df[col_name].mode()[0])
        reverse_dict = {v: k for k, v in mapping_dict.items()}
        default_index = options.index(reverse_dict[mode_val])
    except:
        default_index = 0
    selected_str = st.selectbox(col_name.replace('_', ' '), options, index=default_index)
    return mapping_dict[selected_str]

# 📝 SEKSI 1: Profil Demografis & Ekonomi
st.header("📝 1. Profil Demografis & Ekonomi")
st.markdown("*Referensi kode angka kualifikasi/pekerjaan: [10.24432/C5MC89](https://doi.org/10.24432/C5MC89)*")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Data Diri")
    input_data['Marital_status'] = create_selectbox('Marital_status', marital_map)
    input_data['Application_mode'] = create_selectbox('Application_mode', app_mode_map)
    input_data['Course'] = create_selectbox('Course', course_map)
    input_data['Daytime_evening_attendance'] = create_selectbox('Daytime_evening_attendance', daytime_map)
    input_data['Nacionality'] = create_selectbox('Nacionality', nacionality_map)
    input_data['Gender'] = create_selectbox('Gender', gender_map)
    
    # Pekerjaan orang tua (kode angka sesuai referensi eksternal)
    input_data['Mothers_occupation'] = st.selectbox("Mother's occupation (Code)", sorted(df['Mothers_occupation'].unique().tolist()))
    input_data['Fathers_occupation'] = st.selectbox("Father's occupation (Code)", sorted(df['Fathers_occupation'].unique().tolist()))
    
    input_data['Application_order'] = st.number_input("Application order", int(df['Application_order'].min()), int(df['Application_order'].max()), int(df['Application_order'].median()))
    input_data['Age_at_enrollment'] = st.number_input("Age at enrollment", value=int(df['Age_at_enrollment'].median()), step=1)
        
with col2:
    st.subheader("Pendidikan & Ekonomi")
    input_data['Previous_qualification'] = create_selectbox('Previous_qualification', prev_qual_map)
    
    input_data['Mothers_qualification'] = st.selectbox("Mother's qualification (Code)", sorted(df['Mothers_qualification'].unique().tolist()))
    input_data['Fathers_qualification'] = st.selectbox("Father's qualification (Code)", sorted(df['Fathers_qualification'].unique().tolist()))
    
    input_data['Displaced'] = create_selectbox('Displaced', binary_map)
    input_data['Educational_special_needs'] = create_selectbox('Educational_special_needs', binary_map)
    input_data['Debtor'] = create_selectbox('Debtor', binary_map)
    input_data['Tuition_fees_up_to_date'] = create_selectbox('Tuition_fees_up_to_date', binary_map)
    input_data['Scholarship_holder'] = create_selectbox('Scholarship_holder', binary_map)
    input_data['International'] = create_selectbox('International', binary_map)
        
    for col in ['Unemployment_rate', 'Inflation_rate', 'GDP']:
        input_data[col] = st.number_input(col.replace('_', ' '), value=float(df[col].mean()))

st.divider()

# 📚 SEKSI 2: Akademik Semester 1
st.header("📚 2. Performa Akademik Semester 1")
col3, col4 = st.columns(2)

with col3:
    input_data['Previous_qualification_grade'] = st.number_input("Previous qualification grade", value=float(df['Previous_qualification_grade'].mean()))
    input_data['Admission_grade'] = st.number_input("Admission grade", value=float(df['Admission_grade'].mean()))
    input_data['Curricular_units_1st_sem_grade'] = st.number_input("1st sem grade", value=float(df['Curricular_units_1st_sem_grade'].mean()))
    
with col4:
    for col in count_cols[:5]:
        input_data[col] = st.number_input(col.replace('_', ' '), value=int(df[col].median()), step=1)

st.divider()

# 📈 SEKSI 3: Akademik Semester 2
st.header("📈 3. Performa Akademik Semester 2")
col5, col6 = st.columns(2)

with col5:
    input_data['Curricular_units_2nd_sem_grade'] = st.number_input("2nd sem grade", value=float(df['Curricular_units_2nd_sem_grade'].mean()))
    
with col6:
    for col in count_cols[5:]:
        input_data[col] = st.number_input(col.replace('_', ' '), value=int(df[col].median()), step=1)

st.divider()

if st.button("🚀 Prediksi Status Mahasiswa", use_container_width=True):
    with st.spinner("Menganalisis data..."):
        input_df = pd.DataFrame([input_data])
        
        # Load encoding info
        encoding_info = joblib.load("model/encoding_info.joblib")
        
        # Apply Label Encoding for High Cardinality nominal features
        for col in encoding_info['high_card_cols']:
            le = encoding_info['le_dict'][col]
            input_df[col] = le.transform(input_df[col])
            
        # Apply One-Hot Encoding for Low Cardinality nominal features
        X_new = pd.get_dummies(input_df, columns=encoding_info['low_card_cols'], drop_first=True)
        
        # Align features with the model training columns
        X_new = X_new.reindex(columns=encoding_info['X_columns'], fill_value=0)
        
        # Scale the numerical and count features
        X_new[numerical_cols + count_cols] = scaler.transform(X_new[numerical_cols + count_cols])
        
        # Eksekusi Prediksi
        pred = model.predict(X_new)[0]
        prob = model.predict_proba(X_new)[0][1] # Asumsi kelas '1' pada model adalah Dropout
        
        st.subheader("Hasil Analisis & Keputusan:")
        if pred == 1:
            st.error(f"⚠️ **Peringatan!** Probabilitas mahasiswa berujung **Dropout** sangat fatal di angka **{prob:.1%}**.")
            st.info("💡 **Catatan:** Prioritaskan intervensi finansial dan jadwalkan evaluasi prestasi akademik secara berkala.")
        else:
            st.success(f"✅ **Aman!** Probabilitas prediksi Dropout pada kriteria mahasiswa ini hanyalah **{prob:.1%}**.")
            st.info("💡 **Catatan:** Mahasiswa ini cenderung akan lulus (*Graduate*). Tetap pastikan pendampingan rutin berjalan normal.")
