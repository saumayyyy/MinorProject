import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title='Zomato Data Analysis', layout='wide', initial_sidebar_state='expanded')

# Load the Zomato data
data_path = 'Zomato data .csv'  # Update with the correct path to your dataset
df = pd.read_csv(data_path)

# ---- Data Cleaning Section ----
# Renaming columns for easier access
df.rename(columns={'approx_cost(for two people)': 'cost_for_two'}, inplace=True)

# Convert 'rate' column to float, handling edge cases
df['rate'] = df['rate'].apply(lambda x: float(str(x).split('/')[0]) if '/' in str(x) else None)

# Remove commas from the 'cost_for_two' column and convert it to float
df['cost_for_two'] = df['cost_for_two'].replace(',', '', regex=True).astype(float)

# ---- Sidebar for Filters ----
st.sidebar.header("Filter Data")
# Add an option for "All Categories" in the dropdown
category_filter = st.sidebar.selectbox("Select Category", options=["All Categories"] + list(df['listed_in(type)'].unique()))

# Apply filter based on selection
if category_filter == "All Categories":
    df_filtered = df
else:
    df_filtered = df[df['listed_in(type)'] == category_filter]

# Dashboard Title
st.title(f"Zomato Restaurant Analytics Dashboard - {category_filter}")

# ---- KPIs Section ----
st.markdown('### Key Performance Indicators')
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Restaurants", value=len(df_filtered))
with col2:
    st.metric(label="Average Rating", value=round(df_filtered['rate'].mean(), 2))
with col3:
    st.metric(label="Avg. Cost for Two", value=f"₹{int(df_filtered['cost_for_two'].mean())}")
with col4:
    st.metric(label="Online Orders Available", value=df_filtered['online_order'].value_counts().get('Yes', 0))

# ---- 1. Top-rated Restaurants ----
st.markdown('### Top 10 Highest Rated Restaurants')
top_rated_df = df_filtered.sort_values(by='rate', ascending=False).head(10)
st.dataframe(top_rated_df[['name', 'rate', 'cost_for_two', 'listed_in(type)', 'votes']])

# ---- 2. Restaurant Types with Higher Ratings ----
st.markdown('### Average Ratings by Restaurant Type')
avg_rating_by_type = df.groupby('listed_in(type)')['rate'].mean().reset_index().sort_values(by='rate', ascending=False)
rating_by_type_fig = px.bar(avg_rating_by_type, x='rate', y='listed_in(type)', orientation='h', color='rate', 
                            color_continuous_scale='Viridis', title="Average Rating by Restaurant Type")
rating_by_type_fig.update_layout(xaxis_title="Average Rating", yaxis_title="Restaurant Type")
st.plotly_chart(rating_by_type_fig, use_container_width=True)

# ---- 5. How Ratings Correlate with Cost ----
st.markdown('### Correlation between Rating and Cost for Two')
correlation_fig = px.scatter(df_filtered, x='cost_for_two', y='rate', color='rate', 
                             color_continuous_scale='Bluered', title="Ratings vs Cost for Two People")
correlation_fig.update_layout(xaxis_title="Cost for Two (₹)", yaxis_title="Rating")
st.plotly_chart(correlation_fig, use_container_width=True)

# ---- 8. Most Popular Categories ----
st.markdown('### Most Popular Restaurant Categories')
category_counts = df['listed_in(type)'].value_counts().reset_index()
category_counts.columns = ['Restaurant Type', 'Count']
popular_categories_fig = px.bar(category_counts, x='Restaurant Type', y='Count', 
                                color='Restaurant Type', title="Most Popular Restaurant Categories")
popular_categories_fig.update_layout(xaxis_title="Restaurant Type", yaxis_title="Number of Restaurants")
st.plotly_chart(popular_categories_fig, use_container_width=True)

# ---- 9. Percentage of Restaurants Offering Table Booking ----
st.markdown('### Percentage of Restaurants Offering Table Booking')
table_booking_count = df['book_table'].value_counts()
table_booking_fig = go.Figure(go.Pie(
    labels=table_booking_count.index, 
    values=table_booking_count.values, 
    hole=0.5, marker=dict(colors=['#FF69B4', '#87CEEB'])  # Vibrant colors: Hot pink and Light blue
))
table_booking_fig.update_layout(title_text="Proportion of Restaurants Offering Table Booking")
st.plotly_chart(table_booking_fig, use_container_width=True)

# ---- Ratings Distribution ----
st.markdown('### Ratings Distribution')
rating_fig = px.histogram(df_filtered, x='rate', nbins=20, color_discrete_sequence=['#FF00FF'])  # Magenta
rating_fig.update_layout(title_text="Distribution of Restaurant Ratings", xaxis_title="Rating", yaxis_title="Count")
st.plotly_chart(rating_fig, use_container_width=True)

# ---- Cost Distribution ----
st.markdown('### Cost Distribution for Two People')
cost_fig = px.histogram(df_filtered, x='cost_for_two', nbins=20, color_discrete_sequence=['#ADD8E6'])  # Light blue
cost_fig.update_layout(title_text="Distribution of Approximate Cost for Two", xaxis_title="Cost (₹)", yaxis_title="Count")
st.plotly_chart(cost_fig, use_container_width=True)

# ---- Online vs Offline Orders Analysis ----
st.markdown('### Online vs Offline Orders')
online_vs_offline = pd.DataFrame({
    'Order Type': ['Online', 'Offline'],
    'Average Rating': [df_filtered[df_filtered['online_order'] == 'Yes']['rate'].mean(), 
                       df_filtered[df_filtered['online_order'] == 'No']['rate'].mean()]
})
bar_fig = px.bar(online_vs_offline, x='Order Type', y='Average Rating', color='Order Type',
                 color_discrete_sequence=['#FFFF00', '#00FFFF'])  # Yellow, Cyan
bar_fig.update_layout(title_text="Average Ratings: Online vs Offline Orders")
st.plotly_chart(bar_fig, use_container_width=True)

# ---- Restaurant Preferences ----
st.markdown('### Restaurant Preferences (Online vs Offline)')
preferences_fig = go.Figure(go.Pie(
    labels=['Online Orders', 'Offline Orders'],
    values=[df_filtered['online_order'].value_counts().get('Yes', 0), 
            df_filtered['online_order'].value_counts().get('No', 0)],
    hole=0.5
))
preferences_fig.update_traces(marker=dict(colors=['#FF00FF', '#ADD8E6']))  # Magenta, Light blue
preferences_fig.update_layout(title_text='Proportion of Restaurants Offering Online vs Offline Orders')
st.plotly_chart(preferences_fig, use_container_width=True)
