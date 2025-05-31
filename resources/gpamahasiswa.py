import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import os

def load_custom_css():
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard IPK Mahasiswa", 
    layout="wide"
)

# Terapkan CSS kustom
load_custom_css()

# Header utama
st.markdown('<h1 class="main-title">📊 Dashboard IPK Mahasiswa</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Analisis Data IPK dari Berbagai Program Studi</p>', unsafe_allow_html=True)

# Dictionary untuk mapping kode program studi
program_studi_dict = {
    'BCH': 'Biochemistry',
    'BLD': 'Building Technology', 
    'CEN': 'Computer Engineering',
    'CHE': 'Chemical Engineering',
    'CHM': 'Industrial Chemistry',
    'CIS': 'Computer Science',
    'CVE': 'Civil Engineering',
    'EEE': 'Electrical and Electronics Engineering',
    'ICE': 'Information and Communication Engineering',
    'MAT': 'Mathematics',
    'MCB': 'Microbiology',
    'MCE': 'Mechanical Engineering',
    'MIS': 'Management and Information System',
    'PET': 'Petroleum Engineering',
    'PHYE': 'Industrial Physics-Electronics and IT Applications',
    'PHYG': 'Industrial Physics-Applied Geophysics',
    'PHYR': 'Industrial Physics-Renewable Energy'
}

# Informasi Program Studi
with st.expander("📚 Daftar Kode Program Studi"):
    col1, col2 = st.columns(2)
    
    prodi_items = list(program_studi_dict.items())
    mid_point = len(prodi_items) // 2
    
    with col1:
        for code, name in prodi_items[:mid_point]:
            st.write(f"**{code}**: {name}")
    
    with col2:
        for code, name in prodi_items[mid_point:]:
            st.write(f"**{code}**: {name}")

# Ganti dengan nama file CSV Anda
csv_file = "resources/datavisdat.csv"

try:
    # Membaca data CSV
    df = pd.read_csv(csv_file)
    
    # Rename kolom untuk konsistensi
    df = df.rename(columns={
        'ID No': 'Mahasiswa',
        'Prog Code': 'Prodi',
        'YoG': 'Tahun',
        'CGPA': 'IPK'
    })
    
    # Fungsi kategori IPK
    def kategori_ipk(ipk):
        if ipk >= 3.5:
            return "Sangat Baik"
        elif ipk >= 3.0:
            return "Baik"
        elif ipk >= 2.5:
            return "Cukup"
        else:
            return "Kurang"
    
    # Cek apakah kolom yang diperlukan ada
    required_columns = {'Tahun', 'IPK', 'Prodi', 'Mahasiswa'}
    if required_columns.issubset(df.columns):
        
        # Sidebar untuk filter
        st.sidebar.header("🔍 Filter Data")
        tahun_terpilih = st.sidebar.selectbox("Pilih Tahun:", sorted(df['Tahun'].unique()))
        prodi_terpilih = st.sidebar.multiselect(
            "Pilih Program Studi:", 
            sorted(df['Prodi'].unique()), 
            default=df['Prodi'].unique()
        )
        
        # Filter data berdasarkan pilihan
        df_filtered = df[(df['Tahun'] == tahun_terpilih) & (df['Prodi'].isin(prodi_terpilih))]
        
        # Statistik Dasar
        st.markdown('<h2 class="section-title">📈 Statistik Dasar</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
            st.metric("Total Mahasiswa", df['Mahasiswa'].nunique())
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
            st.metric("Jumlah Prodi", df['Prodi'].nunique())
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
            st.metric("Rata-rata IPK", f"{df_filtered['IPK'].mean():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
            st.metric("IPK Tertinggi", f"{df_filtered['IPK'].max():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Visualisasi dalam 2 kolom
        st.markdown('<h2 class="section-title">📊 Visualisasi Data</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        # Pie Chart Kategori IPK
        with col1:
            st.subheader("Kategori IPK")
            # Buat kategori IPK untuk data yang sudah difilter
            df_filtered_copy = df_filtered.copy()
            df_filtered_copy['Kategori IPK'] = df_filtered_copy['IPK'].apply(kategori_ipk)
            kategori_data = df_filtered_copy['Kategori IPK'].value_counts()
            
            if len(kategori_data) > 0:
                fig_pie = px.pie(
                    values=kategori_data.values,
                    names=kategori_data.index,
                    title=f"Distribusi Kategori IPK - Tahun {tahun_terpilih}"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.warning("Tidak ada data untuk ditampilkan")
        
        # Bar Chart IPK per Prodi
        with col2:
            st.subheader("IPK per Program Studi")
            if len(df_filtered) > 0:
                avg_ipk = df_filtered.groupby('Prodi')['IPK'].mean().reset_index()
                
                fig_bar = px.bar(
                    avg_ipk, 
                    x='Prodi', 
                    y='IPK',
                    title=f"Rata-rata IPK per Prodi - Tahun {tahun_terpilih}",
                    color='IPK',
                    color_continuous_scale='Blues'
                )
                fig_bar.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.warning("Tidak ada data untuk ditampilkan")
        
        # Grafik Tren
        st.markdown('<h2 class="section-title">📈 Tren IPK dari Waktu ke Waktu</h2>', unsafe_allow_html=True)
        
        trend_data = df[df['Prodi'].isin(prodi_terpilih)].groupby(['Tahun', 'Prodi'])['IPK'].mean().reset_index()
        
        fig_line = px.line(
            trend_data,
            x='Tahun',
            y='IPK',
            color='Prodi',
            markers=True,
            title="Tren Rata-rata IPK per Tahun"
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
         # Distribusi IPK
        st.markdown('<h2 class="section-title">📊 Distribusi IPK per Program Studi</h2>', unsafe_allow_html=True)
        
        # Hitung jumlah kolom berdasarkan jumlah prodi
        num_prodi = len(prodi_terpilih)
        
        if num_prodi > 0:
            # Tentukan jumlah kolom (maksimal 3 kolom per baris)
            cols_per_row = min(3, num_prodi)
            
            # Buat baris-baris sesuai kebutuhan
            rows_needed = (num_prodi + cols_per_row - 1) // cols_per_row
            
            prodi_list = sorted(prodi_terpilih)
            prodi_index = 0
            
            for row in range(rows_needed):
                # Buat kolom untuk baris ini
                cols = st.columns(cols_per_row)
                
                for col_idx in range(cols_per_row):
                    if prodi_index < num_prodi:
                        prodi = prodi_list[prodi_index]
                        prodi_data = df_filtered[df_filtered['Prodi'] == prodi]['IPK']
                        
                        with cols[col_idx]:
                            st.subheader(f"{prodi}")
                            
                            if len(prodi_data) > 0:
                                # Buat histogram menggunakan matplotlib
                                fig, ax = plt.subplots(figsize=(6, 4))
                                ax.hist(prodi_data, bins=10, color='skyblue', alpha=0.7, edgecolor='black')
                                ax.set_title(f"Distribusi IPK - {prodi}")
                                ax.set_xlabel("IPK")
                                ax.set_ylabel("Frekuensi")
                                ax.grid(True, alpha=0.3)
                                
                                # Tambahkan garis rata-rata
                                mean_ipk = prodi_data.mean()
                                ax.axvline(mean_ipk, color='red', linestyle='--', 
                                          label=f'Rata-rata: {mean_ipk:.2f}')
                                
                                st.pyplot(fig)
                                plt.close()
                                
                                # Tampilkan statistik singkat
                                st.write(f"**Jumlah Mahasiswa:** {len(prodi_data)}")
                                st.write(f"**Rata-rata IPK:** {prodi_data.mean():.2f}")
                                st.write(f"**IPK Tertinggi:** {prodi_data.max():.2f}")
                                st.write(f"**IPK Terendah:** {prodi_data.min():.2f}")
                            else:
                                st.write("Tidak ada data untuk program studi ini.")
                        
                        prodi_index += 1
        else:
            st.info("Silakan pilih program studi untuk melihat distribusi IPK")
        
        # Tabel Ringkasan
        st.markdown('<h2 class="section-title">📋 Ringkasan Statistik</h2>', unsafe_allow_html=True)
        
        summary_stats = df[df['Prodi'].isin(prodi_terpilih)].groupby('Prodi')['IPK'].agg([
            'count', 'mean', 'std', 'min', 'max'
        ]).round(2)
        summary_stats.columns = ['Jumlah', 'Rata-rata', 'Std Dev', 'Min', 'Max']
        
        st.dataframe(summary_stats, use_container_width=True)
    
    else:
        st.error("❌ File CSV tidak memiliki kolom yang diperlukan")
        st.write("Kolom yang diperlukan: Tahun, IPK, Prodi, Mahasiswa")

except FileNotFoundError:
    st.error(f"❌ File '{csv_file}' tidak ditemukan")
    st.info("💡 Pastikan file CSV ada di folder yang sama dengan script ini")
except Exception as e:
    st.error(f"❌ Error: {e}")