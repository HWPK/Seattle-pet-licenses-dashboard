import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Streamlit page config
st.set_page_config(page_title="Seattle Pet Licenses Dashboard", layout="wide")

# Loading data
df = pd.read_csv('Seattle_Pet_Licenses_Cleaned.csv')

# Clean key columns
df['Species'] = df['Species'].fillna('Unknown').str.strip().str.title()
df['Primary Breed'] = df['Primary Breed'].fillna('Unknown').str.strip().str.title()
df['ZIP Code'] = df['ZIP Code'].astype(str).str.strip()

# Filtering out 'Unknown' species
df = df[df['Species'] != 'Unknown']

# Sidebar — Dynamic filtering
st.sidebar.header("🔎 Filter the Data")

species_options = df['Species'].unique()
selected_species = st.sidebar.multiselect('Select Species', species_options, default=[])

# Dynamically narrow ZIP and Breed based on species filter
if selected_species:
    df_narrowed = df[df['Species'].isin(selected_species)]
else:
    df_narrowed = df

# Narrow options
zip_options = sorted(df_narrowed['ZIP Code'].dropna().unique())
selected_zips = st.sidebar.multiselect('Select ZIP Code', zip_options)

breed_options = df_narrowed['Primary Breed'].dropna().unique()
selected_breed = st.sidebar.selectbox('Select a Primary Breed (optional)', ['All'] + sorted(breed_options))

# Apply filters
filtered_df = df_narrowed.copy()

if selected_zips:
    filtered_df = filtered_df[filtered_df['ZIP Code'].isin(selected_zips)]

if selected_breed != 'All':
    filtered_df = filtered_df[filtered_df['Primary Breed'] == selected_breed]

if selected_species:
    filtered_df = filtered_df[filtered_df['Species'].isin(selected_species)]

# Title and KPIs
st.title("🐾 Seattle Pet Licenses Dashboard")
st.markdown("Analyze pet ownership trends across Seattle based on government licensing data.")

col1, col2, col3 = st.columns(3)
col1.metric("Total Pets", len(filtered_df))
col2.metric("Unique Breeds", filtered_df['Primary Breed'].nunique())
col3.metric("ZIP Codes Covered", filtered_df['ZIP Code'].nunique())

st.markdown("---")

# --- PIE CHART ---
st.header("📊 Visual Data Insights")
st.markdown("### 📘 What this shows:\nThis pie chart visualizes the proportion of each pet species across all licenses.")
species_count = filtered_df['Species'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(
    species_count,
    labels=species_count.index,
    autopct='%1.1f%%',
    startangle=90,
    textprops={'fontsize': 12}
)
ax1.axis('equal')
st.pyplot(fig1)

# --- TREEMAP ---
st.markdown("### 📘 What this shows:\nThis treemap displays the top 20 pet breeds and their relative proportions.")
st.subheader("🐕 Treemap of Top 20 Breeds by Pet Count")
top_breeds = filtered_df['Primary Breed'].value_counts().head(20).reset_index()
top_breeds.columns = ['Breed', 'Count']
fig_treemap = px.treemap(
    top_breeds,
    path=['Breed'],
    values='Count',
    color='Count',
    color_continuous_scale='Purples'
)
st.plotly_chart(fig_treemap, use_container_width=True)

# --- TOP BREEDS BAR CHART ---
st.markdown("### 📘 What this shows:\nThis bar chart highlights the most common breeds among registered pets.")
st.subheader("📊 Top 10 Primary Breeds")
top_breed_counts = filtered_df['Primary Breed'].value_counts().head(10)
fig2, ax2 = plt.subplots()
top_breed_counts.plot(kind='barh', ax=ax2, color='indigo')
ax2.invert_yaxis()
ax2.set_xlabel("Number of Pets")
ax2.set_ylabel("Breed")
st.pyplot(fig2)

# --- ZIP CODE BAR CHART ---
st.markdown("### 📘 What this shows:\nThis bar chart shows the top 25 ZIP codes by pet count.")
st.subheader("🏠 Top 25 ZIP Codes by Pet Count")
zip_counts = filtered_df['ZIP Code'].value_counts().head(25)
fig3, ax3 = plt.subplots(figsize=(12, 5))
zip_counts.plot(kind='bar', ax=ax3, color='darkred')
ax3.set_xlabel("ZIP Code")
ax3.set_ylabel("Number of Pets")
ax3.set_title("Top 25 ZIP Codes")
ax3.tick_params(axis='x', rotation=45)
st.pyplot(fig3)

# --- FILTERED DATA TABLE ---
st.markdown("---")
st.header("📄 View Filtered Data")
st.markdown("### 📘 What this shows:\nA full table showing all filtered pet license records.")
st.dataframe(filtered_df)

# Footer
st.markdown("---")
