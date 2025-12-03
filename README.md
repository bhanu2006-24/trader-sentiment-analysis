# Trader Sentiment Analysis

## 📌 Project Overview
This project explores and analyzes the relationship between **trader behavior** and **market sentiment** (Fear vs. Greed) in the cryptocurrency market. By combining historical trading data from Hyperliquid with the Bitcoin Fear & Greed Index, we aim to identify patterns, trends, and signals that could influence smarter trading strategies.

## 📂 Project Structure
The project follows a standardized submission format:

```
ds_bhanu/
├── Notebook_0.ipynb          # Exploratory Data Analysis (EDA) and initial processing
├── Notebook_1.ipynb          # Key findings, insights, and visualizations
├── csv_files/                # Raw and processed datasets
│   ├── fear_greed_index.csv
│   ├── historical_data.csv
│   ├── merged.csv
│   ├── sentiment_clean.csv
│   └── trader_clean.csv
├── outputs/                  # Visualizations and graphs
│   ├── %profitable_trade_by_sentiment.png
│   ├── Buy_vs_sell_sentiment.png
│   ├── avg_pnl_by_sentiment.png
│   ├── avg_start_pos_by_sentiment.png
│   ├── buy_sell_ratio_by_sentiment.png
│   ├── total_volume_by_sentiment.png
│   ├── trade_size_vs_closed_pnl_by_sentiment.png
│   └── win_loss_rate_by_sentiment.png
├── links.txt                 # References and data sources
├── Instructions Data Science.pdf # Assignment instructions
└── README.md                 # Project documentation
```

## 📊 Datasets
The analysis is based on two key datasets:

1.  **Bitcoin Market Sentiment Dataset** (`fear_greed_index.csv`)
    *   **Source**: [Google Drive Link](https://drive.google.com/file/d/1PgQC0tO8XN-wqkNyghWc_-mnrYv_nhSf/view?usp=sharing)
    *   **Description**: Contains daily sentiment values classified as "Fear", "Greed", "Extreme Fear", "Extreme Greed", or "Neutral".
    *   **Key Columns**: `Date`, `Value`, `Classification`.

2.  **Historical Trader Data** (`historical_data.csv`)
    *   **Source**: [Google Drive Link](https://drive.google.com/file/d/1IAfLZwu6rJzyWKgBToqwSmmVYU6VbjVs/view?usp=sharing)
    *   **Description**: Detailed trading records from Hyperliquid.
    *   **Key Columns**: `Account`, `Symbol`, `Execution Price`, `Size`, `Side` (Buy/Sell), `Time`, `Closed PnL`, `Leverage`.

## 🛠️ Methodology
The analysis workflow is divided into the following stages:

1.  **Data Loading & Cleaning**:
    *   Loaded raw CSV files using `pandas`.
    *   Converted timestamps to human-readable datetime formats.
    *   Cleaned and filtered relevant columns for analysis.
    *   Saved cleaned versions as `sentiment_clean.csv` and `trader_clean.csv`.

2.  **Data Merging**:
    *   Merged the trader data with sentiment data based on the `Date` column.
    *   Created a unified dataset (`merged.csv`) linking every trade to the market sentiment of that day.

3.  **Exploratory Data Analysis (EDA)**:
    *   Analyzed trading volume, profitability (PnL), and win/loss rates across different sentiment categories.
    *   Investigated if traders are more profitable during "Fear" or "Greed" periods.

4.  **Visualization**:
    *   Generated charts to visualize trends using `matplotlib` and `seaborn`.
    *   Key plots include Average PnL by Sentiment, Buy vs. Sell Ratios, and Total Trade Volume.

## 📈 Key Visualizations
The `outputs/` directory contains the following insights:

*   **`avg_pnl_by_sentiment.png`**: Shows the average profit/loss realized during different sentiment states.
*   **`total_volume_by_sentiment.png`**: Displays the total trading volume (in USD) for each sentiment category.
*   **`win_loss_rate_by_sentiment.png`**: Compares the percentage of profitable trades vs. losing trades across sentiments.
*   **`Buy_vs_sell_sentiment.png`**: Illustrates the ratio of Buy orders to Sell orders during Fear vs. Greed.

## 🚀 Usage & Notebooks
You can run the analysis using the provided Google Colab notebooks:

*   **Notebook 0 (EDA)**: [Open in Colab](https://colab.research.google.com/drive/1fwZSGpqMl1hqfoPYQKiwEIJng-l7Jf5Q#scrollTo=X22qAcYChp5D)
*   **Notebook 1 (Insights)**: [Open in Colab](https://colab.research.google.com/drive/1tGbzZAlgy0sQKBOfTaWTzc6JCMHLoDh5#scrollTo=4f390f66)

### Requirements
To run the code locally, ensure you have the following Python libraries installed:
```bash
pip install pandas matplotlib seaborn numpy
```

## 📝 License
This project is part of a Data Science assignment for the Web3 Trading Team.
