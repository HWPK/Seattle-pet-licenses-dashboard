import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Streamlit settings
st.set_page_config(page_title="Seattle Pet Licenses Dashboard", layout="wide")

# Load data
df = pd.read_csv('Seattle_Pet_Licenses_Cleaned.csv')

# Clean columns
df['Species'] = df['Species'].fillna('Unknown').str.strip().str.title()
df['Primary Breed'] = df['Primary Breed'].fillna('Unknown').str.strip().str.title()
df['ZIP Code'] = df['ZIP Code'].astype(str).str.strip()

# Filter out 'Unknown' species
df = df[df['Species'] != 'Unknown']

# Sidebar filters
st.sidebar.header("🔎 Filter the Data")

species_options = df['Species'].unique()
selected_species = st.sidebar.multiselect('Select Species', species_options, default=species_options)

zip_options = sorted(df['ZIP Code'].dropna().unique())
selected_zips = st.sidebar.multiselect('Select ZIP Code', zip_options)

breed_options = df['Primary Breed'].unique()
selected_breed = st.sidebar.selectbox('Select a Primary Breed (optional)', ['All'] + list(breed_options))

# Apply filters
filtered_df = df.copy()

if selected_species:
    filtered_df = filtered_df[filtered_df['Species'].isin(selected_species)]

if selected_zips:
    filtered_df = filtered_df[filtered_df['ZIP Code'].isin(selected_zips)]

if selected_breed != 'All':
    filtered_df = filtered_df[filtered_df['Primary Breed'] == selected_breed]

# Main Title
st.title("🐾 Seattle Pet Licenses Dashboard")
st.markdown("Analyze pet ownership trends across Seattle based on government licensing data.")

# Key Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Pets", len(filtered_df))
col2.metric("Unique Breeds", filtered_df['Primary Breed'].nunique())
col3.metric("ZIP Codes Covered", filtered_df['ZIP Code'].nunique())

st.markdown("---")

# --- Donut Chart ---
st.header("📊 Visual Data Insights")

st.markdown("### 📘 What this shows:\nThis donut chart visualizes the proportion of pet species registered in Seattle. It replaces the pie chart for better clarity and spacing.")
species_count = filtered_df['Species'].value_counts()
species_count = species_count[species_count > 0]
fig1, ax1 = plt.subplots()
wedges, texts, autotexts = ax1.pie(
    species_count,
    labels=species_count.index,
    autopct='%1.1f%%',
    startangle=90,
    textprops={'fontsize': 12},
    wedgeprops=dict(width=0.4)
)
ax1.axis('equal')
plt.setp(autotexts, color='white')
st.pyplot(fig1)

# --- Treemap ---
st.markdown("### 📘 What this shows:\nThis treemap highlights the top 20 primary breeds by pet count. Larger boxes represent more popular breeds.")
st.subheader("🐕 Treemap of Top 20 Breeds by Pet Count")
top_breeds = filtered_df['Primary Breed'].value_counts().head(20).reset_index()
top_breeds.columns = ['Breed', 'Count']
fig_treemap = px.treemap(
    top_breeds,
    path=['Breed'],
    values='Count',
    color='Count',
    color_continuous_scale='RdPu'  # Red-Purple scale
)
st.plotly_chart(fig_treemap, use_container_width=True)

# --- Bubble Chart ---
st.markdown("### 📘 What this shows:\nThis bubble chart shows the spread of pet species by ZIP Code. Larger circles represent higher counts.")
st.subheader("📍 Bubble Chart: Pets by ZIP Code and Species")
bubble_data = filtered_df.groupby(['ZIP Code', 'Species']).size().reset_index(name='Count')
fig_bubble = px.scatter(
    bubble_data,
    x="ZIP Code",
    y="Species",
    size="Count",
    color="Species",
    size_max=50,
    color_discrete_sequence=px.colors.qualitative.Dark24
)
fig_bubble.update_layout(height=500)
st.plotly_chart(fig_bubble, use_container_width=True)

# --- ZIP Code Bar Chart ---
st.markdown("### 📘 What this shows:\nThis chart shows the top 25 ZIP codes by number of registered pets. It reveals areas with the most pet ownership activity.")
st.subheader("Top 25 ZIP Codes by Pet Count")
zip_counts = filtered_df['ZIP Code'].value_counts().head(25)
fig_zip, ax_zip = plt.subplots(figsize=(12, 5))
zip_counts.plot(kind='bar', ax=ax_zip, color='#6A0DAD')  # Deep purple
ax_zip.set_xlabel("ZIP Code")
ax_zip.set_ylabel("Number of Pets")
ax_zip.set_title("Top 25 ZIP Codes")
ax_zip.tick_params(axis='x', rotation=45)
st.pyplot(fig_zip)

# --- Map ---
if 'Latitude' in df.columns and 'Longitude' in df.columns:
    st.markdown("### 📘 What this shows:\nThis map displays pet license locations based on latitude/longitude. Clusters show dense regions of pet ownership.")
    st.subheader("🗺️ Map of Pet Licenses by Location")
    map_df = filtered_df[['Latitude', 'Longitude']].dropna()
    st.map(map_df)

# --- Filtered Table ---
st.markdown("---")
st.header("📄 View Filtered Data")
st.markdown("### 📘 What this shows:\nA detailed table of all filtered data entries, useful for individual lookups and deeper exploration.")
st.dataframe(filtered_df)

# Footer
st.markdown("---")
