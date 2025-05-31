import time
import os
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)

# Ambil data dari GitHub dan cache hasilnya
dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"

@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

# Load data
df = get_data()

# Judul Dashboard
st.title("Real-Time / Live Data Science Dashboard")

# Filter utama: pilih jenis pekerjaan
job_filter = st.selectbox("Select the Job", pd.unique(df["job"]))

# Filter DataFrame berdasarkan pilihan
df_filtered = df[df["job"] == job_filter].copy()

# Placeholder untuk update dinamis
placeholder = st.empty()

# Simulasi update data real-time
for seconds in range(200):
    # Buat data baru secara acak untuk simulasi
    df_filtered["age_new"] = df_filtered["age"] * np.random.choice(range(1, 5), size=len(df_filtered))
    df_filtered["balance_new"] = df_filtered["balance"] * np.random.choice(range(1, 5), size=len(df_filtered))

    # Hitung KPI
    avg_age = np.mean(df_filtered["age_new"])
    count_married = int(df_filtered[df_filtered["marital"] == "married"].shape[0] + np.random.choice(range(1, 30)))
    balance = np.mean(df_filtered["balance_new"])

    with placeholder.container():
        # Tiga kolom KPI
        kpi1, kpi2, kpi3 = st.columns(3)

        kpi1.metric(
            label="Age ⏳",
            value=round(avg_age),
            delta=round(avg_age) - 10,
        )

        kpi2.metric(
            label="Married Count 💍",
            value=int(count_married),
            delta=-10 + count_married,
        )

        kpi3.metric(
            label="A/C Balance ＄",
            value=f"$ {round(balance, 2)}",
            delta=-round(balance / (count_married or 1)) * 100,  # Hindari pembagian nol
        )

        # Dua grafik interaktif
        fig_col1, fig_col2 = st.columns(2)

        with fig_col1:
            st.markdown("### Age vs Marital Heatmap")
            fig = px.density_heatmap(
                data_frame=df_filtered, y="age_new", x="marital", nbinsy=20, color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig, use_container_width=True)

        with fig_col2:
            st.markdown("### Age Distribution Histogram")
            fig2 = px.histogram(data_frame=df_filtered, x="age_new", nbins=20, color_discrete_sequence=["#58a6ff"])
            st.plotly_chart(fig2, use_container_width=True)

        # Tabel detail
        st.markdown("### Detailed Data View")
        st.dataframe(df_filtered, use_container_width=True)

    # Delay 1 detik (simulasi real-time)
    time.sleep(1)
