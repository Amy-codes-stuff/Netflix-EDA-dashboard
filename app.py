import pandas as pd
import streamlit as st
import plotly.express as px

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv('netflix_cleaned.csv')

    # Clean and convert date
    df['date_added'] = df['date_added'].astype(str).str.strip()
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce', infer_datetime_format=True)

    # Feature engineering
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    df['num_genres'] = df['listed_in'].apply(lambda x: len(str(x).split(', ')))
    
    return df

# Load the dataset
df = load_data()

# Streamlit page setup
st.set_page_config(page_title="Netflix EDA Dashboard", layout="wide")
st.title("Netflix EDA Dashboard")
st.markdown("Interactive analysis of the Netflix dataset.")

# Dataset overview
with st.expander("View Raw Dataset"):
    st.dataframe(df)

# Sidebar filters
st.sidebar.header("Filters")
selected_type = st.sidebar.multiselect("Select Type", options=df['type'].unique(), default=df['type'].unique())
selected_country = st.sidebar.multiselect("Select Country", options=df['country'].dropna().unique(), default=None)

filtered_df = df.copy()
if selected_type:
    filtered_df = filtered_df[filtered_df['type'].isin(selected_type)]
if selected_country:
    filtered_df = filtered_df[filtered_df['country'].isin(selected_country)]

# Plot 1: Content count by type
st.subheader("Content Count by Type")
type_count = filtered_df['type'].value_counts().reset_index()
type_count.columns = ['Type', 'Count']
fig1 = px.bar(type_count, x='Type', y='Count', color='Type', title="Movies vs TV Shows")
st.plotly_chart(fig1, use_container_width=True)

# Plot 2: Number of releases over years
st.subheader("Releases Over the Years")
year_count = filtered_df['release_year'].value_counts().reset_index()
year_count.columns = ['Release Year', 'Count']
year_count = year_count.sort_values(by='Release Year')
fig2 = px.line(year_count, x='Release Year', y='Count', title="Content Releases by Year")
st.plotly_chart(fig2, use_container_width=True)

# Plot 3: Top genres
st.subheader("Top Genres")
genre_list = []
for genres in filtered_df['listed_in'].dropna():
    genre_list.extend([g.strip() for g in genres.split(',')])
genre_df = pd.DataFrame(genre_list, columns=['Genre'])
genre_count = genre_df['Genre'].value_counts().reset_index().head(10)
genre_count.columns = ['Genre', 'Count']
fig3 = px.bar(genre_count, x='Genre', y='Count', title="Top 10 Genres")
st.plotly_chart(fig3, use_container_width=True)

# Plot 4: Content added per year
st.subheader("Content Added to Netflix Per Year")
added_year = filtered_df['year_added'].value_counts().reset_index()
added_year.columns = ['Year Added', 'Count']
added_year = added_year.sort_values(by='Year Added')
fig4 = px.line(added_year, x='Year Added', y='Count', title="Content Added by Year")
st.plotly_chart(fig4, use_container_width=True)

# Show summary stats
st.subheader("Dataset Summary")
st.write(filtered_df.describe(include='all'))
