import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title='Zomato Data Analysis', layout='wide', initial_sidebar_state='expanded')

# Load the Zomato data
uploaded_file = st.sidebar.file_uploader("Choose a file", type=['csv'])  # Allow user to upload file
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ---- Data Cleaning Section ----
    df['rate'] = df['rate'].apply(lambda x: float(str(x).split('/')[0]) if '/' in str(x) else None)
    df['approx_cost(for two people)'] = df['approx_cost(for two people)'].replace(',', '', regex=True).astype(float)

    # ---- Sidebar for Filters ----
    st.sidebar.header("Filter Data")
    city_filter = st.sidebar.selectbox("Select Category", options=df['listed_in(type)'].unique())

    # Filter the data based on selection
    df_filtered = df[df['listed_in(type)'] == city_filter]

    # Dashboard Title
    st.title(f"Zomato Restaurant Analytics Dashboard - {city_filter}")

    # ---- KPIs Section ----
    st.markdown('### Key Performance Indicators')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Restaurants", value=len(df_filtered))
    with col2:
        st.metric(label="Average Rating", value=round(df_filtered['rate'].mean(), 2))
    with col3:
        st.metric(label="Avg. Cost for Two", value=f"₹{int(df_filtered['approx_cost(for two people)'].mean())}")
    with col4:
        st.metric(label="Online Orders Available", value=df_filtered['online_order'].value_counts().get('Yes', 0))

    # ---- Ratings Distribution ----
    st.markdown('### Ratings Distribution')
    rating_fig = px.histogram(df_filtered, x='rate', nbins=20, color_discrete_sequence=['#EF553B'])
    rating_fig.update_layout(title_text="Distribution of Restaurant Ratings", xaxis_title="Rating", yaxis_title="Count")
    st.plotly_chart(rating_fig, use_container_width=True)

    # ---- Cost Distribution ----
    st.markdown('### Cost Distribution for Two People')
    cost_fig = px.histogram(df_filtered, x='approx_cost(for two people)', nbins=20, color_discrete_sequence=['#636EFA'])
    cost_fig.update_layout(title_text="Distribution of Approximate Cost for Two", xaxis_title="Cost (₹)", yaxis_title="Count")
    st.plotly_chart(cost_fig, use_container_width=True)

    # ---- Which Type of Restaurant Has More Offline Orders? ----
    st.markdown('### Which Type of Restaurant Has More Offline Orders?')

    # Prepare data for heatmap: Which types of restaurants have more offline orders
    offline_orders = df_filtered[df_filtered['online_order'] == 'No']
    offline_order_counts = offline_orders.groupby('listed_in(type)').size().reset_index(name='Offline Orders')

    # Create heatmap to show which restaurant types have more offline orders
    heatmap_fig = px.imshow(offline_order_counts.pivot_table(values='Offline Orders', index='listed_in(type)'),
                            labels=dict(x="Restaurant Type", y="Offline Orders", color="Offline Orders"),
                            color_continuous_scale=['#EF553B', '#636EFA', '#FFA15A'])

    heatmap_fig.update_layout(title_text="Which Type of Restaurant Has More Offline Orders")
    st.plotly_chart(heatmap_fig, use_container_width=True)

    # ---- Additional Analysis Section ----
    st.markdown('### Online vs Offline Orders Breakdown')

    # Creating a table for online vs offline orders
    online_offline_df = pd.DataFrame({
        'Order Type': ['Online', 'Offline'],
        'Restaurant Count': [df_filtered['online_order'].value_counts().get('Yes', 0), 
                             df_filtered['online_order'].value_counts().get('No', 0)]
    })

    # Table to show the count of online vs offline orders
    st.table(online_offline_df)

    # ---- Bar Graph for Online vs Offline Orders (Optional) ----
    bar_fig = px.bar(online_offline_df, x='Order Type', y='Restaurant Count', color='Order Type',
                     color_discrete_sequence=['#00CC96', '#FFA15A'])
    bar_fig.update_layout(title_text="Comparison: Online vs Offline Orders")
    st.plotly_chart(bar_fig, use_container_width=True)

else:
    st.write("Please upload a CSV file to proceed.")
