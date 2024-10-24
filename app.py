import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set a custom theme using Streamlit's built-in theme options
st.set_page_config(page_title='Zomato Data Analysis', layout='wide')

# Load the Zomato data
data_path = 'Zomato data .csv'
df = pd.read_csv(data_path)

# Clean the rate column
def handleRate(value):
    value = str(value).split('/')
    return float(value[0])

df['rate'] = df['rate'].apply(handleRate)

# Clean the 'approx_cost(for two people)' column (removing commas and converting to numeric)
df['approx_cost(for two people)'] = df['approx_cost(for two people)'].replace(',', '', regex=True).astype(float)

# Add custom CSS styling to change fonts, margins, and headings
st.markdown("""
    <style>
    body {
        font-family: "Arial", sans-serif;
        background-color: #f4f4f9;
    }
    .header {
        color: #2c3e50;
        font-size: 36px;
        text-align: center;
        margin-bottom: 40px;
    }
    .subheader {
        color: #34495e;
        font-size: 28px;
        margin-bottom: 20px;
    }
    .metric-container {
        margin: 20px 0;
        text-align: center;
        display: flex;
        justify-content: space-around;
    }
    .metric {
        padding: 10px;
        background-color: #e8eaf6;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# App title
st.markdown('<div class="header">Zomato Restaurant Data Analysis</div>', unsafe_allow_html=True)

# Dataset Section
st.markdown('<div class="subheader">Dataset Overview</div>', unsafe_allow_html=True)
st.dataframe(df)

# Adding Ratings functionality
st.markdown('<div class="subheader">Restaurant Ratings Distribution</div>', unsafe_allow_html=True)

# Allow users to filter by rating
min_rating, max_rating = st.slider(
    'Select Rating Range',
    min_value=float(df['rate'].min()),
    max_value=float(df['rate'].max()),
    value=(df['rate'].min(), df['rate'].max())
)

# Filter data based on the selected rating range
filtered_data_by_rating = df[(df['rate'] >= min_rating) & (df['rate'] <= max_rating)]
st.write(f"Displaying data for restaurants with ratings between {min_rating} and {max_rating}")
st.dataframe(filtered_data_by_rating)

# Visualization: Ratings Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['rate'], kde=False, bins=20, color='blue')
plt.xlabel('Rating')
plt.ylabel('Number of Restaurants')
plt.title('Distribution of Restaurant Ratings')
st.pyplot(plt)

# Adding Cost functionality
st.markdown('<div class="subheader">Preferred Restaurants by Approximate Cost</div>', unsafe_allow_html=True)

# Allow users to filter by approximate cost with step as float
min_cost = float(df['approx_cost(for two people)'].min())
max_cost = float(df['approx_cost(for two people)'].max())

# Use a tuple of floats for the 'value' argument
cost_range = st.slider(
    'Select Approximate Cost for Two People',
    min_value=min_cost,
    max_value=max_cost,
    value=(min_cost, max_cost),
    step=0.01
)

# Filter data based on the selected cost range
filtered_data_by_cost = df[(df['approx_cost(for two people)'] >= cost_range[0]) & (df['approx_cost(for two people)'] <= cost_range[1])]
st.write(f"Displaying data for restaurants with approximate cost between {cost_range[0]} and {cost_range[1]}")
st.dataframe(filtered_data_by_cost)

# Visualization: Approximate Cost Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['approx_cost(for two people)'], kde=False, bins=20, color='green')
plt.xlabel('Approximate Cost for Two People')
plt.ylabel('Number of Restaurants')
plt.title('Distribution of Approximate Costs')
st.pyplot(plt)

# Metrics: Online vs Offline Orders Rating Comparison
st.markdown('<div class="subheader">Do Online Orders Receive Higher Ratings?</div>', unsafe_allow_html=True)

# Group data by online order availability
online_order_avg = df[df['online_order'] == 'Yes']['rate'].mean()
offline_order_avg = df[df['online_order'] == 'No']['rate'].mean()

# Display metrics
st.markdown('<div class="metric-container">', unsafe_allow_html=True)
st.markdown(f'<div class="metric"><strong>Average Rating (Online Orders):</strong><br>{online_order_avg:.2f}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric"><strong>Average Rating (Offline Orders):</strong><br>{offline_order_avg:.2f}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Create a bar plot to compare the ratings
ratings_data = pd.DataFrame({
    'Order Type': ['Online', 'Offline'],
    'Average Rating': [online_order_avg, offline_order_avg]
})

plt.figure(figsize=(6, 4))
sns.barplot(x='Order Type', y='Average Rating', data=ratings_data, palette='viridis')
plt.title('Average Ratings: Online vs Offline Orders')
st.pyplot(plt)

# Adding Functionality to Show Restaurant Preferences (Online vs Offline Orders)
st.markdown('<div class="subheader">Restaurant Preferences: Online vs Offline Orders</div>', unsafe_allow_html=True)

# Count the number of restaurants that prefer online orders vs offline orders
online_order_counts = df['online_order'].value_counts()

# Display the counts
st.markdown('<div class="metric-container">', unsafe_allow_html=True)
st.markdown(f'<div class="metric"><strong>Online Orders:</strong><br>{online_order_counts["Yes"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric"><strong>Offline Orders:</strong><br>{online_order_counts["No"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Create a bar plot to visualize the preferences
plt.figure(figsize=(6, 4))
sns.barplot(x=online_order_counts.index, y=online_order_counts.values, palette='coolwarm')
plt.xlabel('Order Type')
plt.ylabel('Number of Restaurants')
plt.title('Number of Restaurants Offering Online vs Offline Orders')
st.pyplot(plt)
