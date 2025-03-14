import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Load dataset dari GitHub
url_day = "https://raw.githubusercontent.com/AAmmar01/ProjectDataAnalysis-CodingCampDBS2025/main/day.csv"
url_hour = "https://raw.githubusercontent.com/AAmmar01/ProjectDataAnalysis-CodingCampDBS2025/main/hour.csv"
day_df = pd.read_csv(url_day, parse_dates=["dteday"])
hour_df = pd.read_csv(url_hour, parse_dates=["dteday"])

# Konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("🚲 Bike Sharing Dashboard")

# Sidebar: Filter rentang tanggal
st.sidebar.header("🔍 Filter")
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

# Filter data berdasarkan tanggal
filtered_day = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) & (day_df["dteday"] <= pd.to_datetime(end_date))]
filtered_hour = hour_df[(hour_df["dteday"] >= pd.to_datetime(start_date)) & (hour_df["dteday"] <= pd.to_datetime(end_date))]

# Metrik utama
total_rentals = filtered_day["cnt"].sum()
avg_rentals = filtered_day["cnt"].mean()
max_rentals = filtered_day["cnt"].max()

# Layout untuk metrik
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Rentals", f"{total_rentals:,.0f}")
with col2:
    st.metric("Average Rentals", f"{avg_rentals:,.2f}")
with col3:
    st.metric("Max Rentals in a Day", f"{max_rentals:,.0f}")

# Pola Peminjaman Sepeda Berdasarkan Jam dalam Sehari
st.subheader("⏰ Pola Peminjaman Sepeda Berdasarkan Jam dalam Sehari")
# Menghitung rata-rata peminjaman sepeda per jam
hourly_trend = filtered_hour.groupby("hr")["cnt"].mean().reset_index()
# Gunakan plotly untuk membuat line chart
fig_hourly = px.line(hourly_trend, x="hr", y="cnt", markers=True,
                      labels={"hr": "Jam dalam Sehari", "cnt": "Rata-rata Peminjaman"},
                      title="Pola Peminjaman Sepeda Berdasarkan Jam dalam Sehari")
# Tampilkan di Streamlit
st.plotly_chart(fig_hourly, use_container_width=True)

# Pola Peminjaman Sepeda Berdasarkan Hari dalam Seminggu
st.subheader("📆 Pola Peminjaman Sepeda Berdasarkan Hari dalam Seminggu")
# Menghitung rata-rata peminjaman sepeda per hari dalam seminggu
weekday_trend = hour_df.groupby("weekday")["cnt"].mean().reset_index()
# Gunakan Plotly untuk visualisasi
fig_day_of_week = px.bar(
    weekday_trend,
    x="weekday",
    y="cnt",
    labels={"weekday": "Hari dalam Seminggu", "cnt": "Rata-rata Peminjaman"},
    title="Rata-rata Peminjaman Sepeda Berdasarkan Hari dalam Seminggu"
)
# Ubah angka weekday ke label hari
fig_day_of_week.update_xaxes(
    tickmode="array",
    tickvals=list(range(7)),
    ticktext=["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
)
# Tampilkan di Streamlit
st.plotly_chart(fig_day_of_week, use_container_width=True)

# Pengaruh Suhu terhadap Peminjaman Sepeda
st.subheader("🌡️ Pengaruh Suhu terhadap Peminjaman Sepeda")
fig_temp = px.scatter(filtered_hour, x="temp", y="cnt",
                      labels={"temp": "Suhu", "cnt": "Jumlah Peminjaman"},
                      title="Hubungan Suhu dengan Peminjaman Sepeda")
st.plotly_chart(fig_temp, use_container_width=True)

# Pengaruh Kelembaban terhadap Peminjaman Sepeda
st.subheader("💧 Pengaruh Kelembaban terhadap Peminjaman Sepeda")
fig_hum = px.scatter(filtered_hour, x="hum", y="cnt",
                     labels={"hum": "Kelembaban", "cnt": "Jumlah Peminjaman"},
                     title="Hubungan Kelembaban dengan Peminjaman Sepeda")
st.plotly_chart(fig_hum, use_container_width=True)

# Pengaruh Kecepatan Angin terhadap Peminjaman Sepeda
st.subheader("💨 Pengaruh Kecepatan Angin terhadap Peminjaman Sepeda")
fig_wind = px.scatter(filtered_hour, x="windspeed", y="cnt",
                      labels={"windspeed": "Kecepatan Angin", "cnt": "Jumlah Peminjaman"},
                      title="Hubungan Kecepatan Angin dengan Peminjaman Sepeda")
st.plotly_chart(fig_wind, use_container_width=True)

# Sewa Berdasarkan Waktu dalam Sehari
def categorize_hour(hour):
    if 0 <= hour < 6:
        return 'Malam'
    elif 6 <= hour < 12:
        return 'Pagi'
    elif 12 <= hour < 18:
        return 'Siang'
    else:
        return 'Malam'

filtered_hour = filtered_hour.copy()
filtered_hour['time_of_day'] = filtered_hour['hr'].apply(categorize_hour)
st.subheader("🕒 Sewa Sepeda Berdasarkan Waktu dalam Sehari")
time_trend = filtered_hour.groupby("time_of_day")["cnt"].mean().reset_index()
fig_time = px.bar(time_trend, x="time_of_day", y="cnt", color="time_of_day",
                  labels={"time_of_day": "Waktu dalam Sehari", "cnt": "Rata-rata Peminjaman"},
                  title="Rata-rata Peminjaman Sepeda Berdasarkan Waktu dalam Sehari")
st.plotly_chart(fig_time, use_container_width=True)

# Tambahkan subheader untuk clustering peminjaman sepeda
st.subheader("📊 Distribusi Cluster Permintaan Sepeda")
# Clustering permintaan sepeda dengan binning
bins = [0, 100, 300, hour_df['cnt'].max()]
labels = ['Rendah', 'Sedang', 'Tinggi']
hour_df['demand_cluster'] = pd.cut(hour_df['cnt'], bins=bins, labels=labels)
# Hitung jumlah observasi untuk setiap kategori
demand_counts = hour_df['demand_cluster'].value_counts().reset_index()
demand_counts.columns = ['Kategori Permintaan', 'Jumlah Observasi']
# Buat bar chart menggunakan Plotly
fig_demand = px.bar(
    demand_counts, x="Kategori Permintaan", y="Jumlah Observasi", color="Kategori Permintaan",
    title="Distribusi Cluster Permintaan Sepeda", labels={"Kategori Permintaan": "Kategori Permintaan"}
)
# Tampilkan di Streamlit
st.plotly_chart(fig_demand, use_container_width=True)

st.write("Dashboard ini dibuat untuk menganalisis tren peminjaman sepeda berdasarkan faktor-faktor seperti jam, hari, suhu, kelembaban, kecepatan angin, dan waktu dalam sehari.")