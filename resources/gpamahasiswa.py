import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import os

def load_custom_css():
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Set konfigurasi halaman
st.set_page_config(
    page_title="Dashboard IPK Mahasiswa",
    layout="wide"
)

load_custom_css()

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

# Baca data
csv_file = "resources/datavisdat.csv"
try:
    df = pd.read_csv(csv_file)
    df = df.rename(columns={
        'ID No': 'Mahasiswa',
        'Prog Code': 'Prodi',
        'YoG': 'Tahun',
        'CGPA': 'IPK'
    })

    # Mapping nama prodi
    program_studi_dict = {
        'BCH': 'Biochemistry', 'BLD': 'Building Technology', 'CEN': 'Computer Engineering',
        'CHE': 'Chemical Engineering', 'CHM': 'Industrial Chemistry', 'CIS': 'Computer Science',
        'CVE': 'Civil Engineering', 'EEE': 'Electrical and Electronics Engineering',
        'ICE': 'Information and Communication Engineering', 'MAT': 'Mathematics',
        'MCB': 'Microbiology', 'MCE': 'Mechanical Engineering', 'MIS': 'Management and Information System',
        'PET': 'Petroleum Engineering', 'PHYE': 'Industrial Physics-Electronics and IT Applications',
        'PHYG': 'Industrial Physics-Applied Geophysics', 'PHYR': 'Industrial Physics-Renewable Energy'
    }

    # Sidebar Navigasi
    menu = st.sidebar.radio("Navigasi", ["Beranda", "Visualisasi Data", "Tentang"])

    if menu == "Beranda":
        st.markdown('<h1 class="main-title">Dashboard IPK Mahasiswa</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Analisis Data IPK dari Berbagai Program Studi</p>', unsafe_allow_html=True)

        with st.expander("Daftar Kode Program Studi"):
            col1, col2 = st.columns(2)
            prodi_items = list(program_studi_dict.items())
            mid_point = len(prodi_items) // 2

            with col1:
                for code, name in prodi_items[:mid_point]:
                    st.write(f"**{code}**: {name}")
            with col2:
                for code, name in prodi_items[mid_point:]:
                    st.write(f"**{code}**: {name}")

        st.markdown("### Statistik Dasar (semua tahun dan prodi)")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Mahasiswa", df['Mahasiswa'].nunique())
        with col2:
            st.metric("Jumlah Prodi", df['Prodi'].nunique())
        with col3:
            st.metric("Rata-rata IPK", f"{df['IPK'].mean():.2f}")
        with col4:
            st.metric("IPK Tertinggi", f"{df['IPK'].max():.2f}")

    elif menu == "Visualisasi Data":
        st.markdown('<h1 class="main-title">Visualisasi Data</h1>', unsafe_allow_html=True)

        tahun_terpilih = st.sidebar.selectbox("Pilih Tahun:", sorted(df['Tahun'].unique()))
        prodi_terpilih = st.sidebar.multiselect(
            "Pilih Program Studi:",
            sorted(df['Prodi'].unique()),
            default=df['Prodi'].unique()
        )

        df_filtered = df[(df['Tahun'] == tahun_terpilih) & (df['Prodi'].isin(prodi_terpilih))]

        # Pie Chart Kategori IPK
        st.subheader("Distribusi Kategori IPK")
        df_filtered_copy = df_filtered.copy()
        df_filtered_copy['Kategori IPK'] = df_filtered_copy['IPK'].apply(kategori_ipk)
        kategori_data = df_filtered_copy['Kategori IPK'].value_counts()

        if not kategori_data.empty:
            fig_pie = px.pie(values=kategori_data.values, names=kategori_data.index)
            st.plotly_chart(fig_pie, use_container_width=True)

        # Bar Chart Rata-rata IPK per Prodi
        st.subheader("Rata-rata IPK per Prodi")
        if not df_filtered.empty:
            avg_ipk = df_filtered.groupby('Prodi')['IPK'].mean().reset_index()
            fig_bar = px.bar(avg_ipk, x='Prodi', y='IPK', color='IPK', color_continuous_scale='Blues')
            fig_bar.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_bar, use_container_width=True)

        # Line Chart Tren IPK
        st.subheader("Tren IPK dari Waktu ke Waktu")
        trend_data = df[df['Prodi'].isin(prodi_terpilih)].groupby(['Tahun', 'Prodi'])['IPK'].mean().reset_index()
        fig_line = px.line(trend_data, x='Tahun', y='IPK', color='Prodi', markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

        # Histogram Distribusi IPK per Prodi
        st.subheader("Distribusi IPK per Program Studi")
        num_prodi = len(prodi_terpilih)

        if num_prodi > 0:
            cols_per_row = min(3, num_prodi)
            rows_needed = (num_prodi + cols_per_row - 1) // cols_per_row

            prodi_list = sorted(prodi_terpilih)
            prodi_index = 0

            for row in range(rows_needed):
                cols = st.columns(cols_per_row)

                for col_idx in range(cols_per_row):
                    if prodi_index < num_prodi:
                        prodi = prodi_list[prodi_index]
                        prodi_data = df_filtered[df_filtered['Prodi'] == prodi]['IPK']

                        with cols[col_idx]:
                            st.subheader(f"{prodi}")

                            if len(prodi_data) > 0:
                                fig, ax = plt.subplots(figsize=(6, 4))
                                ax.hist(prodi_data, bins=10, color='skyblue', alpha=0.7, edgecolor='black')
                                ax.set_title(f"Distribusi IPK - {prodi}")
                                ax.set_xlabel("IPK")
                                ax.set_ylabel("Frekuensi")
                                ax.grid(True, alpha=0.3)

                                mean_ipk = prodi_data.mean()
                                ax.axvline(mean_ipk, color='red', linestyle='--', 
                                          label=f'Rata-rata: {mean_ipk:.2f}')

                                st.pyplot(fig)
                                plt.close()

                                st.write(f"**Jumlah Mahasiswa:** {len(prodi_data)}")
                                st.write(f"**Rata-rata IPK:** {prodi_data.mean():.2f}")
                                st.write(f"**IPK Tertinggi:** {prodi_data.max():.2f}")
                                st.write(f"**IPK Terendah:** {prodi_data.min():.2f}")
                            else:
                                st.write("Tidak ada data untuk program studi ini.")

                        prodi_index += 1
        else:
            st.info("Silakan pilih program studi untuk melihat distribusi IPK")

    elif menu == "Tentang":
        st.markdown('<h1 class="main-title">Tentang Dashboard</h1>', unsafe_allow_html=True)
        st.write("""
            Dashboard ini dikembangkan untuk menganalisis distribusi dan tren IPK mahasiswa berdasarkan program studi.

            **Fitur utama:**
            - Statistik dasar IPK
            - Visualisasi distribusi IPK per prodi
            - Tren IPK dari waktu ke waktu
            - Filter tahun dan program studi

            Dibuat menggunakan Streamlit, Plotly, dan Pandas.
        """)

except FileNotFoundError:
    st.error(f"❌ File '{csv_file}' tidak ditemukan")
    st.info("💡 Pastikan file CSV ada di folder yang sesuai dengan script")
except Exception as e:
    st.error(f"❌ Error: {e}")
