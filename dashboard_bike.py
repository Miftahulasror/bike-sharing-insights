import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_sum_casual_df(df):
    sum_casual_df = df.groupby('casual').agg({
        'id_rec': 'nunique',
        'casual': sum
    })
    return sum_casual_df

def create_sum_registered_df(df):
    sum_registered_df = df.groupby('registered').agg({
        'id_rec': 'nunique',
        'registered': sum
    })
    return sum_registered_df

def create_sum_total_count_df(df):
    sum_total_count_df = df.groupby('total_count').agg({
        'id_rec': 'nunique',
        'total_count': sum
    })
    return sum_total_count_df


day_df = pd.read_csv('day_bike.csv')

day_df.info()

day_df.sort_values(by='datetime', inplace=True)
day_df.reset_index(inplace=True)
day_df['datetime'] = pd.to_datetime(day_df['datetime'])

min_date = day_df['datetime'].min()
max_date = day_df['datetime'].max()

with st.sidebar:
    # menambahkan logo
    st.image('logo.png')
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]  # Use a single date for the value parameter
    )

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

main_df = day_df[(day_df['datetime'] >= start_date) & 
                 (day_df['datetime'] <= end_date)]

casual_df = create_sum_casual_df(main_df)
registered_df = create_sum_registered_df(main_df)
total_count_df = create_sum_total_count_df(main_df)


st.header('Bike Dashboard')

st.subheader('Grafik peminjaman sepeda')

# Use individual columns instead of st.columns(1)
col1, col2, col3 = st.columns(3)

with col1:
    casual_count = casual_df['casual'].sum()
    st.metric("Casual bike", value=casual_count)


with col2:
    registered_count = registered_df['registered'].sum()
    st.metric("Registered bike", value=registered_count)
    
with col3:
    total_count = total_count_df['total_count'].sum()
    st.metric("Total count bike", value=total_count)

# Plot 1
st.subheader("Grafik peminjaman sepeda")
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(x='datetime', y='total_count', data=main_df)
plt.xlabel('Tanggal')
plt.ylabel('Jumlah Peminjaman')
plt.title('Tren jumlah peminjaman dan registrasi sepeda')
st.pyplot(fig)

# Plot 2
st.subheader("Grafik perbandingan musim dan cuaca")

col1, col2 = st.columns(2)

sorted_df = main_df.sort_values(by='total_count', ascending=False)


with col1:
    fig, ax = plt.subplots(figsize=(8,4))
    
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
    sns.barplot(x='season', y='total_count', data=sorted_df, palette=colors)
    plt.title('Jumlah peminjaman sepeda berdasarkan musim')
    plt.xlabel('Musim')
    plt.ylabel('Jumlah peminjaman')
    st.pyplot(fig)
    
with col2:
    fig, ax = plt.subplots(figsize=(8,4))
    
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3"]
    
    sns.barplot(x='weather_condition', y='total_count', data=sorted_df, palette=colors)
    plt.title('Jumlah peminjaman sepeda berdasarkan cuaca')
    plt.xlabel('Cuaca')
    plt.ylabel('Jumlah peminjaman')
    st.pyplot(fig)

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x='season', y='total_count', hue='weather_condition', data=main_df)
plt.xlabel('Musim')
plt.ylabel('Jumlah Peminjaman')
plt.title('Pengaruh musim dan cuaca terhadap jumlah peminjaman')
st.pyplot(fig)

# Plot 3
st.subheader("Korelasi")
fig, ax = plt.subplots(figsize=(16, 8))
sns.scatterplot(x='temp', y='total_count', hue='season', style='weather_condition', data=main_df, s=100)
plt.title('Korelasi antara total peminjaman sepeda dan suhu temperature')
plt.xlabel('Temperature')
plt.ylabel('Jumlah peminjaman')
plt.legend(title='Legend', bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig)

# Plot 4
st.subheader("Cluster")
fig, ax = plt.subplots(figsize=(16, 8))
plt.scatter(
    day_df['temp'],
    day_df['humidity'],
    c=day_df['total_count'],
    cmap='viridis',
    s=100,
    alpha=0.8
)
plt.xlabel('Temperature')
plt.ylabel('Humidity')
plt.title('Clustering berdasarkan temperature, humidity, and total peminjaman')
plt.colorbar(label='Total peminjaman')
st.pyplot(fig)
