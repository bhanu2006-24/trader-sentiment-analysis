import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="Trader Sentiment Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Premium Look ---
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stApp header {
        background-color: #f5f7f9;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    """Loads and processes the sentiment and trader data."""
    try:
        sentiment_df = pd.read_csv("csv_files/fear_greed_index.csv")
        sentiment_df["datetime"] = pd.to_datetime(sentiment_df["timestamp"], unit="s")
        sentiment_clean = sentiment_df[["datetime", "classification", "value"]].copy()
        sentiment_clean["date"] = sentiment_clean["datetime"].dt.date
    except FileNotFoundError:
        st.error("Error: `csv_files/fear_greed_index.csv` not found.")
        return None

    try:
        trader_df = pd.read_csv("csv_files/historical_data.csv")
        trader_df["datetime"] = pd.to_datetime(trader_df["Timestamp"], unit="ms")
        
        cols_to_drop = [
            "Account", "Transaction Hash", "Order ID", "Trade ID",
            "Timestamp", "Timestamp IST" , "Fee", "Coin" ,
            'Direction '
        ]
        trader_clean = trader_df.drop(columns=cols_to_drop, errors="ignore").copy()
        trader_clean["date"] = trader_clean["datetime"].dt.date
    except FileNotFoundError:
        st.error("Error: `csv_files/historical_data.csv` not found.")
        return None

    merged_df = pd.merge(
        trader_clean,
        sentiment_clean[["date", "classification", "value"]],
        on="date",
        how="left"
    )
    
    # Fill missing classifications if any (optional, depending on data quality)
    merged_df["classification"] = merged_df["classification"].fillna("Unknown")
    
    return merged_df

df = load_data()

if df is not None:
    # --- Sidebar ---
    st.sidebar.title("⚙️ Dashboard Settings")
    st.sidebar.markdown("Filter the data to explore specific market conditions.")

    # Date Filter
    min_date = df["date"].min()
    max_date = df["date"].max()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # Sentiment Filter
    all_sentiments = sorted(df["classification"].unique())
    selected_sentiments = st.sidebar.multiselect(
        "Select Market Sentiment",
        all_sentiments,
        default=all_sentiments
    )

    # Trade Side Filter
    all_sides = sorted(df["Side"].unique())
    selected_sides = st.sidebar.multiselect(
        "Select Trade Side",
        all_sides,
        default=all_sides
    )

    # Apply Filters
    if len(date_range) == 2:
        start_date, end_date = date_range
        mask = (
            (df["date"] >= start_date) & 
            (df["date"] <= end_date) &
            (df["classification"].isin(selected_sentiments)) &
            (df["Side"].isin(selected_sides))
        )
        filtered_df = df[mask]
    else:
        filtered_df = df

    # --- Main Content ---
    st.title("📊 Trader Sentiment Analysis")
    st.markdown("### Analyzing the impact of Market Fear & Greed on Trading Performance")
    st.markdown("---")

    # --- Key Metrics ---
    col1, col2, col3, col4 = st.columns(4)
    
    total_pnl = filtered_df["Closed PnL"].sum()
    total_volume = filtered_df["Size USD"].sum()
    win_rate = (filtered_df["Closed PnL"] > 0).mean() * 100
    avg_trade_size = filtered_df["Size USD"].mean()

    col1.metric("Total PnL", f"${total_pnl:,.2f}", delta_color="normal")
    col2.metric("Total Volume", f"${total_volume:,.0f}")
    col3.metric("Win Rate", f"{win_rate:.1f}%")
    col4.metric("Avg Trade Size", f"${avg_trade_size:,.0f}")

    st.markdown("---")

    # --- Tabs for Analysis ---
    tab1, tab2, tab3 = st.tabs(["💰 PnL Analysis", "📉 Volume & Activity", "🧠 Sentiment Insights"])

    with tab1:
        st.subheader("Profit & Loss Analysis")
        
        # Avg PnL by Sentiment
        avg_pnl = filtered_df.groupby("classification")["Closed PnL"].mean().reset_index()
        fig_pnl = px.bar(
            avg_pnl, 
            x="classification", 
            y="Closed PnL", 
            color="classification",
            title="Average Closed PnL by Sentiment",
            color_discrete_sequence=px.colors.qualitative.Bold,
            text_auto='.2f'
        )
        fig_pnl.update_layout(xaxis_title="Sentiment", yaxis_title="Average PnL ($)")
        st.plotly_chart(fig_pnl, use_container_width=True)

        # Percentage of Profitable Trades
        profit_rate = filtered_df.groupby("classification")["Closed PnL"].apply(lambda x: (x > 0).mean() * 100).reset_index(name="Win Rate")
        fig_win = px.bar(
            profit_rate, 
            x="classification", 
            y="Win Rate", 
            color="classification",
            title="Win Rate (%) by Sentiment",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            text_auto='.1f'
        )
        fig_win.update_layout(xaxis_title="Sentiment", yaxis_title="Win Rate (%)")
        st.plotly_chart(fig_win, use_container_width=True)

    with tab2:
        st.subheader("Volume & Trading Activity")
        
        # Total Volume by Sentiment
        vol_by_sentiment = filtered_df.groupby("classification")["Size USD"].sum().reset_index()
        fig_vol = px.bar(
            vol_by_sentiment, 
            x="classification", 
            y="Size USD", 
            color="classification",
            title="Total Trade Volume by Sentiment",
            color_discrete_sequence=px.colors.qualitative.Prism,
            text_auto='.2s'
        )
        fig_vol.update_layout(xaxis_title="Sentiment", yaxis_title="Total Volume ($)")
        st.plotly_chart(fig_vol, use_container_width=True)

        # Average Start Position
        avg_pos = filtered_df.groupby("classification")["Start Position"].mean().reset_index()
        fig_pos = px.bar(
            avg_pos,
            x="classification",
            y="Start Position",
            color="classification",
            title="Average Position Size by Sentiment",
            color_discrete_sequence=px.colors.qualitative.Safe,
            text_auto='.2f'
        )
        fig_pos.update_layout(xaxis_title="Sentiment", yaxis_title="Avg Position Size")
        st.plotly_chart(fig_pos, use_container_width=True)

    with tab3:
        st.subheader("Sentiment & Behavior")
        
        # Buy vs Sell Ratio
        st.markdown("#### Buy vs Sell Distribution per Sentiment")
        
        # We need to create a subplot or just show multiple pie charts. 
        # For a cleaner UI, let's use a selectbox to choose the sentiment to view details for.
        
        target_sentiment = st.selectbox("Select Sentiment to Analyze Detail", all_sentiments)
        
        subset = filtered_df[filtered_df["classification"] == target_sentiment]
        
        if not subset.empty:
            side_counts = subset["Side"].value_counts().reset_index()
            side_counts.columns = ["Side", "Count"]
            
            fig_pie = px.pie(
                side_counts, 
                values="Count", 
                names="Side", 
                title=f"Buy vs Sell Ratio - {target_sentiment}",
                color="Side",
                color_discrete_map={"BUY": "#00CC96", "SELL": "#EF553B"},
                hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info(f"No data available for {target_sentiment} in the selected range.")

    # --- Raw Data Expander ---
    with st.expander("📂 View Raw Data"):
        st.dataframe(filtered_df)

else:
    st.warning("Please ensure the CSV files are present in the `csv_files/` directory.")
