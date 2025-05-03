import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set Streamlit page config
st.set_page_config(page_title="Seattle Pet Licenses Dashboard", layout="wide")

# Load data
df = pd.read_csv('Seattle_Pet_Licenses_Cleaned.csv')

# Clean up columns
df['Species'] = df['Species'].fillna('Unknown').str.strip().str.title()
df['Primary Breed'] = df['Primary Breed'].fillna('Unknown').str.strip().str.title()
df['ZIP Code'] = df['ZIP Code'].astype(str).str.strip()

# Optional: remove 'Unknown' from species
df = df[df['Species'] != 'Unknown']

# Sidebar
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

# Main page
st.title("🐾 Seattle Pet Licenses Dashboard")
st.markdown("Analyze pet ownership trends across Seattle based on government licensing data.")

col1, col2, col3 = st.columns(3)
col1.metric("Total Pets", len(filtered_df))
col2.metric("Unique Breeds", filtered_df['Primary Breed'].nunique())
col3.metric("ZIP Codes Covered", filtered_df['ZIP Code'].nunique())

st.markdown("---")

# Visual Data Insights
st.header("📊 Visual Data Insights")

# Pie Chart: Pet Species
st.subheader("Distribution of Pet Species")
species_count = filtered_df['Species'].value_counts()
# Remove slices with 0 values to avoid clutter
species_count = species_count[species_count > 0]

fig1, ax1 = plt.subplots()
ax1.pie(
    species_count,
    labels=species_count.index,
    autopct=lambda p: f'{p:.1f}%' if p > 0 else '',
    startangle=90,
    textprops={'fontsize': 12}
)
ax1.axis('equal')
st.pyplot(fig1)

# Top 10 Primary Breeds
st.subheader("Top 10 Primary Breeds")
top_breeds = filtered_df['Primary Breed'].value_counts().head(10)
fig2, ax2 = plt.subplots()
top_breeds.plot(kind='barh', ax=ax2, color='skyblue')
ax2.invert_yaxis()
ax2.set_xlabel("Number of Pets")
ax2.set_ylabel("Breed")
st.pyplot(fig2)

# ZIP Code Bar Chart — Top 25
st.subheader("Top 25 ZIP Codes by Pet Count")
zip_counts = filtered_df['ZIP Code'].value_counts().head(25)
fig3, ax3 = plt.subplots(figsize=(12, 5))
zip_counts.plot(kind='bar', ax=ax3, color='lightgreen')
ax3.set_xlabel("ZIP Code")
ax3.set_ylabel("Number of Pets")
ax3.set_title("Top 25 ZIP Codes")
ax3.tick_params(axis='x', rotation=45)
st.pyplot(fig3)

# Map (if coordinates exist)
if 'Latitude' in df.columns and 'Longitude' in df.columns:
    st.subheader("🗺️ Map of Pet Licenses by Location")
    map_df = filtered_df[['Latitude', 'Longitude']].dropna()
    st.map(map_df)

# Show filtered data
st.markdown("---")
st.header("📄 View Filtered Data")
st.dataframe(filtered_df)

# Footer
st.markdown("---")
