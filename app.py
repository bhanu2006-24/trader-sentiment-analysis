import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set page configuration
st.set_page_config(page_title="Trader Sentiment Analysis Dashboard", layout="wide")

# Title and Introduction
st.title("Trader Sentiment Analysis Dashboard")
st.markdown("""
This dashboard visualizes the relationship between market sentiment (Fear & Greed Index) and trading activity.
It replicates the analysis performed in `Notebook_1.ipynb`.
""")

# --- Data Loading and Processing ---

@st.cache_data
def load_data():
    """Loads and processes the sentiment and trader data."""
    
    # Load Sentiment Data
    try:
        sentiment_df = pd.read_csv("csv_files/fear_greed_index.csv")
        sentiment_df["datetime"] = pd.to_datetime(sentiment_df["timestamp"], unit="s")
        sentiment_clean = sentiment_df[["datetime", "classification"]].copy()
        sentiment_clean["date"] = sentiment_clean["datetime"].dt.date
    except FileNotFoundError:
        st.error("Error: `csv_files/fear_greed_index.csv` not found.")
        return None

    # Load Trader Data
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

    # Merge Data
    merged_df = pd.merge(
        trader_clean,
        sentiment_clean[["date", "classification"]],
        on="date",
        how="left"
    )
    
    return merged_df

# Load the data
merged_df = load_data()

if merged_df is not None:
    # --- Sidebar Filters ---
    st.sidebar.header("Filters")
    
    # Date Range Filter
    min_date = merged_df["date"].min()
    max_date = merged_df["date"].max()
    
    start_date, end_date = st.sidebar.date_input(
        "Select Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter data based on date range
    filtered_df = merged_df[
        (merged_df["date"] >= start_date) & 
        (merged_df["date"] <= end_date)
    ]
    
    # --- Visualizations ---
    
    st.header("Exploratory Data Analysis")

    # 1. Average Closed PnL by Sentiment
    st.subheader("1. Average Closed PnL by Sentiment")
    st.markdown("This chart shows the average Profit and Loss (PnL) for trades, grouped by market sentiment.")
    
    avg_pnl = filtered_df.groupby("classification")["Closed PnL"].mean().reset_index()
    
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=avg_pnl, x="classification", y="Closed PnL", hue="classification", palette="coolwarm", legend=False, ax=ax1)
    ax1.set_title("Average Closed PnL by Sentiment")
    ax1.set_xlabel("Sentiment")
    ax1.set_ylabel("Average PnL")
    st.pyplot(fig1)

    # 2. Total Trade Volume by Sentiment
    st.subheader("2. Total Trade Volume by Sentiment")
    st.markdown("This chart displays the total amount of money (in USD) traded during each market sentiment.")
    
    total_volume = filtered_df.groupby("classification")["Size USD"].sum().reset_index()
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=total_volume, x="classification", y="Size USD", hue="classification", palette="viridis", legend=False, ax=ax2)
    ax2.set_title("Total Trade Volume (USD) by Sentiment")
    ax2.set_xlabel("Sentiment")
    ax2.set_ylabel("Total USD Traded")
    st.pyplot(fig2)

    # 3. Buy vs. Sell Ratio by Sentiment
    st.subheader("3. Buy vs. Sell Ratio by Sentiment")
    st.markdown("These charts show the proportion of 'BUY' vs 'SELL' trades for each market sentiment.")
    
    sentiments = filtered_df["classification"].dropna().unique()
    
    if len(sentiments) > 0:
        # Calculate number of rows needed for subplots (2 columns)
        n_sentiments = len(sentiments)
        n_cols = 2
        n_rows = (n_sentiments + 1) // n_cols
        
        fig3, axes = plt.subplots(n_rows, n_cols, figsize=(12, 6 * n_rows))
        axes = axes.flatten()
        
        for i, sentiment in enumerate(sentiments):
            subset = filtered_df[filtered_df["classification"] == sentiment]
            side_counts = subset["Side"].value_counts()
            
            if not side_counts.empty:
                axes[i].pie(
                    side_counts,
                    labels=side_counts.index,
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=["#66b3ff", "#ff9999"]
                )
                axes[i].set_title(f"Buy vs Sell - {sentiment}")
            else:
                axes[i].text(0.5, 0.5, "No Data", ha='center')
                axes[i].set_title(f"Buy vs Sell - {sentiment}")

        # Hide unused subplots
        for j in range(i + 1, len(axes)):
            axes[j].axis('off')
            
        st.pyplot(fig3)
    else:
        st.info("No sentiment data available for the selected range.")

    # 4. Percentage of Profitable Trades by Sentiment
    st.subheader("4. Percentage of Profitable Trades by Sentiment")
    st.markdown("This chart illustrates the percentage of trades that resulted in a profit, broken down by sentiment.")
    
    profit_rate = filtered_df.groupby("classification")["Closed PnL"].apply(lambda x: (x > 0).mean() * 100).reset_index(name="Profit Rate (%)")
    
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=profit_rate, x="classification", y="Profit Rate (%)", hue="classification", palette="Set2", legend=False, ax=ax4)
    ax4.set_title("Percentage of Profitable Trades by Sentiment")
    ax4.set_ylabel("Profit Rate (%)")
    ax4.set_xlabel("Sentiment")
    st.pyplot(fig4)

    # 5. Average Start Position by Sentiment
    st.subheader("5. Average Start Position by Sentiment")
    st.markdown("This bar chart displays the average 'Start Position' for trades, categorized by market sentiment.")
    
    # Check if 'Start Position' column exists (it wasn't explicitly dropped but let's be safe)
    if "Start Position" in filtered_df.columns:
        avg_position = filtered_df.groupby("classification")["Start Position"].mean().reset_index()
        
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        sns.barplot(data=avg_position, x="classification", y="Start Position", hue="classification", palette="magma", legend=False, ax=ax5)
        ax5.set_title("Average Start Position by Sentiment")
        ax5.set_xlabel("Sentiment")
        ax5.set_ylabel("Average Start Position")
        st.pyplot(fig5)
    else:
        st.warning("Column 'Start Position' not found in the dataset.")

else:
    st.warning("Please ensure the CSV files are present in the `csv_files/` directory.")
