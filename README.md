# Groundwater Level Prediction System

A machine learning-based forecasting system for predicting groundwater levels across Indian states using Prophet time series analysis. This project integrates MongoDB for data management and generates visual forecasts for water level predictions.

## Table of Contents
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [File Descriptions](#file-descriptions)
- [How It Works](#how-it-works)
- [Risk Classification](#risk-classification)
- [Output](#output)

---

## Project Overview

This system predicts groundwater levels for the next 5 years using historical water level data from Indian states. It leverages:
- **Prophet**: Meta's time series forecasting library for trend and seasonality analysis
- **MongoDB**: NoSQL database for storing and managing groundwater data
- **Pandas**: Data manipulation and preprocessing
- **Matplotlib**: Visualization of predictions with confidence intervals

The project consists of two main pipelines:
1. **Data Loading Pipeline** (`load_data.py`) - Ingests CSV data into MongoDB
2. **Forecasting Pipeline** (`forecast.py`) - Trains models and generates predictions

---

## Project Structure

```
GroundWater prediction/
├── forecast.py              # Main forecasting script using Prophet
├── load_data.py             # Data loading and MongoDB integration
├── .env                     # Environment variables (MongoDB credentials)
├── .gitignore               # Git ignore configuration
├── README.md                # This file
├── data/
│   ├── groundwater.csv      # Main groundwater level dataset
│   └── dwlr_india.csv       # Additional DWLR (Dynamic Water Level Recharge) data
├── predictions/             # Output directory for forecast graphs
│   └── [state]_forecast.png # Generated prediction graphs (state-wise)
└── __pycache__/             # Python cache files (auto-generated)
```

---

## Features

✅ **Automated Data Pipeline**
   - Load CSV data into MongoDB with validation and cleaning
   - Batch insertion with progress tracking
   - Error handling and retry mechanisms

✅ **Time Series Forecasting**
   - Prophet-based forecasting with yearly seasonality
   - 5-year prediction horizon
   - 90% confidence intervals

✅ **State-wise Analysis**
   - Process each state independently
   - Minimum 10 data points per state requirement
   - Comprehensive error logging

✅ **Risk Assessment**
   - Classification: EMERGENCY, WARNING, SAFE
   - Customizable thresholds
   - State-wise risk categorization

✅ **Visual Reports**
   - High-resolution forecast graphs (100 DPI)
   - Confidence interval visualization
   - Year-by-year trend analysis
   - Professional formatting with legends and grids

---

## Requirements

### Python Version
- Python 3.8+

### Dependencies
```
pandas>=1.3.0
prophet>=1.1.0
pymongo>=3.12.0
python-dotenv>=0.19.0
matplotlib>=3.4.0
pystan>=2.19.0 (optional, for Prophet)
```

---

## Installation

### 1. Clone or Setup the Project
```bash
cd "d:\VS CODE\GroundWater prediction"
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install pandas prophet pymongo python-dotenv matplotlib
```

### 4. MongoDB Setup
- Create a MongoDB Atlas account (https://www.mongodb.com/cloud/atlas)
- Create a database cluster
- Create a database and collection
- Generate connection credentials

---

## Configuration

### Environment Variables (.env)

Create or update the `.env` file in the project root:

```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=appname
MONGO_DB_NAME=aquawatch
MONGO_COLLECTION_NAME=states
MONGO_STATE_LIMIT=50000
RUN_INITIAL_SYNC=1
INITIAL_SYNC_BACKGROUND=1
```

#### Environment Variable Descriptions:
| Variable | Description | Example |
|----------|-------------|---------|
| `MONGO_URI` | MongoDB connection string with credentials | `mongodb+srv://user:pass@cluster.mongodb.net` |
| `MONGO_DB_NAME` | Database name | `aquawatch` |
| `MONGO_COLLECTION_NAME` | Collection name for raw data | `states` |
| `MONGO_STATE_LIMIT` | Limit for state data processing | `50000` |
| `RUN_INITIAL_SYNC` | Enable initial data sync (1=yes, 0=no) | `1` |
| `INITIAL_SYNC_BACKGROUND` | Run sync in background (1=yes, 0=no) | `1` |

---

## Usage

### Step 1: Load Data into MongoDB

Run the data loading script to ingest CSV files into MongoDB:

```bash
python load_data.py
```

**What it does:**
- Reads `groundwater.csv` from the `data/` folder
- Cleans and validates data (removes missing values)
- Renames columns to standardized format
- Inserts data into MongoDB in batches of 5000 records
- Shows progress with percentage completion
- Includes retry logic for failed batches

**Expected Output:**
```
2025-01-18 10:30:45,123 - INFO - Loaded groundwater.csv with 50000 records
2025-01-18 10:30:46,456 - INFO - After cleaning: 48500 records remaining
2025-01-18 10:30:47,789 - INFO - Progress: 5000/48500 records inserted (10.3%)
...
2025-01-18 10:35:12,345 - INFO - ✓ Successfully inserted all 48500 records into MongoDB
```

### Step 2: Generate Forecasts

Run the forecasting script to train models and generate predictions:

```bash
python forecast.py
```

**What it does:**
- Fetches state-wise data from MongoDB
- Validates minimum data points (10 required)
- Trains Prophet model with yearly seasonality
- Generates 5-year forecasts
- Creates high-resolution graphs with confidence intervals
- Saves predictions to `predictions/` folder
- Logs success/failure for each state

**Expected Output:**
```
2025-01-18 11:00:15,678 - INFO - Found 28 states for prediction
2025-01-18 11:00:16,123 - INFO - Processing state: Rajasthan
2025-01-18 11:00:45,789 - INFO - ✓ Graph saved for Rajasthan: predictions/Rajasthan_forecast.png
...
2025-01-18 11:15:30,456 - INFO - Summary: 27 states processed successfully, 1 failed
2025-01-18 11:15:31,789 - INFO - All graphs saved to: predictions
```

---

## File Descriptions

### `load_data.py`
**Purpose:** Data ingestion and preprocessing

**Key Functions:**
- `load_csv_to_mongodb()` - Main function that handles the entire data loading pipeline

**Process:**
1. Reads `groundwater.csv` from the data directory
2. Renames columns: `State` → `state`, `Date` → `date`, `Water_Level_m_bgl` → `water_level`
3. Removes the `Time` column
4. Converts dates to datetime format
5. Drops records with missing critical values
6. Clears existing MongoDB collection
7. Inserts cleaned data in batches with progress tracking
8. Includes error handling with retry logic

**Batch Configuration:**
- Batch size: 5,000 records
- Delay between batches: 0.5 seconds
- Retry delay on failure: 2 seconds

---

### `forecast.py`
**Purpose:** Time series forecasting and report generation

**Key Functions:**

#### `load_state_data(state)`
Fetches and prepares state-specific data for Prophet
- Parameters: `state` (string) - State name
- Returns: DataFrame with columns `ds` (date) and `y` (water level) or None
- Requires: Minimum 10 data points

#### `classify_risk(level)`
Categorizes water levels based on risk thresholds
- Returns: "EMERGENCY" (< 3.0m), "WARNING" (< 5.0m), "SAFE" (≥ 5.0m)
- Customizable for state-wise thresholds

#### `train_and_predict(df)`
Trains Prophet model and generates forecasts
- Parameters: DataFrame with historical data
- Returns: Tuple of (model, forecast_dataframe)
- Prediction horizon: 5 years with yearly frequency
- Confidence interval: 90%

#### `save_predictions_graph(state, model, forecast)`
Creates and saves forecast visualization
- Generates graphs with:
  - Forecast line (blue)
  - Confidence interval band (light blue fill)
  - Year-based x-axis labels
  - Professional formatting with grid and legend
- Saves to: `predictions/[state]_forecast.png`
- Resolution: 100 DPI

#### `run_prediction_pipeline()`
Main orchestration function
- Fetches all unique states from MongoDB
- Processes each state sequentially
- Tracks success/failure statistics
- Generates summary report

**Model Configuration:**
```python
YEARS_TO_PREDICT = 5        # Forecast horizon
CONFIDENCE_INTERVAL = 0.90  # 90% confidence
MIN_DATA_POINTS = 10        # Minimum records per state
```

---

## How It Works

### Data Flow Diagram

```
CSV Files (data/)
    ↓
load_data.py
    ↓
MongoDB (aquawatch.states)
    ↓
forecast.py
    ├─→ Train Prophet Model
    ├─→ Generate 5-Year Forecast
    └─→ Create Visualization
    ↓
Forecast Graphs (predictions/)
```

### Forecasting Pipeline Details

1. **Data Retrieval**
   - Query MongoDB for each state's historical water levels
   - Sort by date (ascending)
   - Validate minimum 10 data points

2. **Model Training**
   - Initialize Prophet with:
     - Yearly seasonality enabled
     - Weekly/daily seasonality disabled (not relevant for groundwater)
   - Fit model on historical data

3. **Prediction**
   - Create future dates for next 5 years
   - Generate point estimates and confidence intervals
   - Extract last 5 years of predictions

4. **Visualization**
   - Plot forecast with confidence band
   - Format with professional styling
   - Save as PNG image

5. **Error Handling**
   - Skip states with insufficient data
   - Catch and log model training errors
   - Continue processing remaining states
   - Provide summary statistics

---

## Risk Classification

The system classifies groundwater levels into risk categories:

| Category | Threshold | Interpretation |
|----------|-----------|-----------------|
| EMERGENCY | < 3.0 m | Critical water level, immediate action needed |
| WARNING | 3.0 - 5.0 m | Concerning levels, monitoring required |
| SAFE | ≥ 5.0 m | Adequate groundwater availability |

**Note:** These thresholds are configurable in the `classify_risk()` function and can be customized per state based on regional characteristics.

---

## Output

### Generated Files

#### 1. MongoDB Database
- **Database:** `aquawatch`
- **Collection:** `states`
- **Documents:** State-wise water level records
- **Fields:** `state`, `date`, `water_level`

#### 2. Forecast Graphs
**Location:** `predictions/` folder

**Filename Format:** `[state]_forecast.png`

**Example Files:**
- `Rajasthan_forecast.png`
- `Gujarat_forecast.png`
- `Maharashtra_forecast.png`
- etc.

**Graph Contents:**
- Historical data trend (implied)
- 5-year forecast line
- 90% confidence interval (shaded area)
- Year labels (2025-2030)
- Water level axis (meters below ground level)
- Professional formatting with legend

### Log Output
- Real-time progress indicators
- Batch insertion status
- Model training results
- Graph generation confirmations
- Summary statistics

---

## Troubleshooting

### Issue: MongoDB Connection Failed
```
Error: ServerSelectionTimeoutError
```
**Solution:**
- Verify `MONGO_URI` in `.env` file
- Check MongoDB Atlas cluster is active
- Ensure IP whitelist includes your IP address
- Test connection string in MongoDB Compass

### Issue: Insufficient Data for State
```
Warning: Not enough data for [state]
```
**Solution:**
- State has fewer than 10 records
- Check data quality in MongoDB
- May need more historical data collection

### Issue: Prophet Model Training Failed
```
Error: Model training failed
```
**Solution:**
- Ensure data has no NaN values
- Verify date column is in datetime format
- Check water level column contains numeric values

### Issue: Graph Generation Failed
```
Error: Failed to save graph for [state]
```
**Solution:**
- Verify `predictions/` directory exists
- Check disk space availability
- Ensure write permissions on directory

---

## Performance Notes

- **Data Loading:** ~10-15 seconds for 50,000 records with batching
- **Forecasting:** ~5-10 seconds per state (varies by data volume)
- **Graph Generation:** ~2-3 seconds per state
- **Total Pipeline:** 30-45 minutes for 28 states (approximate)

---

## Data Source

- **Primary Dataset:** `groundwater.csv` - Historical groundwater levels by state and date
- **Secondary Dataset:** `dwlr_india.csv` - Dynamic Water Level Recharge data (currently not in pipeline)

**Data Format (groundwater.csv):**
```
State,Date,Time,Water_Level_m_bgl
Rajasthan,2015-01-15,00:00,15.32
Rajasthan,2015-02-15,00:00,15.48
...
```

---

## Future Enhancements

- [ ] State-wise custom risk thresholds
- [ ] API endpoint for real-time predictions
- [ ] Multi-step ahead forecasting (daily, weekly)
- [ ] Anomaly detection in water levels
- [ ] Dashboard with interactive visualizations
- [ ] Email alerts for emergency states
- [ ] Comparison with external data sources (rainfall, etc.)
- [ ] Model performance metrics (RMSE, MAE, MAPE)
- [ ] Automated retraining pipeline with scheduling

---

## Author & License

**Project Name:** GroundWater Level Prediction System  
**Created:** January 2025  
**Purpose:** Environmental Monitoring & Water Resource Management

---

## Support & Contact

For issues, questions, or contributions, please refer to the logging output for detailed error messages and ensure all configuration variables are correctly set.

---

**Last Updated:** January 18, 2026
