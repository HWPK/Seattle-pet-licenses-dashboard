import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set Streamlit page config
st.set_page_config(page_title="Seattle Pet Licenses Dashboard", layout="wide")

# Load data
df = pd.read_csv('Seattle_Pet_Licenses_Cleaned.csv')

# Sidebar
st.sidebar.header("🔎 Filter the Data")

# Species filter
species_options = df['Species'].unique()
selected_species = st.sidebar.multiselect('Select Species', species_options, default=species_options)

# ZIP Code filter
zip_options = sorted(df['ZIP Code'].unique())
selected_zips = st.sidebar.multiselect('Select ZIP Code', zip_options)

# Breed search
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

# Key metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Pets", len(filtered_df))
col2.metric("Unique Breeds", filtered_df['Primary Breed'].nunique())
col3.metric("ZIP Codes Covered", filtered_df['ZIP Code'].nunique())

st.markdown("---")

# Visualizations
st.header("📊 Visual Data Insights")

# Distribution of Pet Species
st.subheader("Distribution of Pet Species")
species_count = filtered_df['Species'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(species_count, labels=species_count.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio makes the pie chart round
st.pyplot(fig1)

# Top 10 Primary Breeds
st.subheader("Top 10 Primary Breeds")
top_breeds = filtered_df['Primary Breed'].value_counts().head(10)
fig2, ax2 = plt.subplots()
top_breeds.plot(kind='barh', ax=ax2)
ax2.invert_yaxis()
ax2.set_xlabel("Number of Pets")
ax2.set_ylabel("Breed")
st.pyplot(fig2)

# Pets per ZIP Code
st.subheader("Number of Pets by ZIP Code")
pets_zip = filtered_df['ZIP Code'].value_counts().sort_index()
fig3, ax3 = plt.subplots(figsize=(10, 5))
pets_zip.plot(kind='bar', ax=ax3)
ax3.set_xlabel("ZIP Code")
ax3.set_ylabel("Number of Pets")
ax3.set_title("Pets Registered per ZIP Code")
st.pyplot(fig3)

# Show filtered data
st.markdown("---")
st.header("📄 View Filtered Data")
st.dataframe(filtered_df)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit.")
