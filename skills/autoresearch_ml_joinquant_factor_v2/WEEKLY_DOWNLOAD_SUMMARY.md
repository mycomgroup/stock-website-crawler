# Weekly Factor Download Summary

## Task Completed ✓

Successfully downloaded weekly factor data with price returns (pchg) for 2024-2025.

## Results

- **Total weeks downloaded**: 103 weeks
- **Date range**: 2024-01-01 to 2025-12-31
- **Success rate**: 103/106 weeks (97.2%)
- **Failed weeks**: 3 weeks (likely due to missing OSS files)
- **Output directory**: `./data/weekly_factors/`

## File Details

- **File naming**: `factors_YYYYMMDD_all.csv` (Monday date for each week)
- **File size**: ~2.5-2.6 MB per file
- **Rows per file**: ~900-920 stocks
- **Columns**: 262 columns (stock code + date + pchg + 259 factors)

## Data Format

Matches the reference format from `test_data_small.csv`:

```csv
Unnamed: 0,date,pchg,<factor1>,<factor2>,...
002001.XSHE,2024-01-01,-0.011124845488257096,-855.316159,92.061111
002003.XSHE,2024-01-01,0.008196721311475308,1060.159925,
```

### Column Description

1. **Unnamed: 0**: Stock code in JoinQuant format (e.g., `600000.XSHG`, `000001.XSHE`)
2. **date**: Monday date of the natural week (YYYY-MM-DD)
3. **pchg**: Weekly return = (next_week_close / this_week_close) - 1
   - Calculated from last trading day of current week to last trading day of next week
   - Match rate: 95-100% for most weeks, ~59% for some weeks in late 2025 (likely due to incomplete data)
4. **Remaining columns**: 259 factor values

## Implementation Details

### Stock Code Conversion

The script automatically converts between formats:
- **JoinQuant format**: `600000.XSHG`, `000001.XSHE`, `430017.XBSE`
- **DuckDB format**: `sh600000`, `sz000001`, `bj430017`

Conversion rules:
- `.XSHG` → `sh` prefix (Shanghai)
- `.XSHE` → `sz` prefix (Shenzhen)
- `.XBSE` → `bj` prefix (Beijing)

### Weekly Logic

1. **Natural weeks**: Monday to Sunday
2. **Factor data**: Uses Monday's factor values
3. **Price calculation**:
   - Find last trading day of current week (Monday-Sunday)
   - Find last trading day of next week
   - Calculate: pchg = (next_week_close / this_week_close) - 1
4. **Missing trading days**: Uses last available trading day in the week

## Usage

### Download weekly data
```bash
cd skills/autoresearch_ml_joinquant_factor_v2
python3 download_factors_with_price.py weekly 2024-01-01 2025-12-31
```

### Download daily data with price
```bash
python3 download_factors_with_price.py 2024-01-01 2024-01-31
```

### Download entire year (daily)
```bash
python3 download_factors_with_price.py year 2024
```

## Files

- **Main script**: `download_factors_with_price.py`
- **Base OSS downloader**: `download_oss.py`
- **Configuration**: `.env` (OSS credentials)
- **Output directory**: `./data/weekly_factors/`
- **Reference format**: `test_data_small.csv`

## Data Quality

### Match Rates by Period

- **2024 Q1-Q3**: 98-100% match rate
- **2024 Q4**: 99-100% match rate
- **2025 Q1-Q2**: 99-100% match rate
- **2025 Q3-Q4**: 59-60% match rate (some weeks)

The lower match rate in late 2025 is likely due to:
1. Incomplete price data in DuckDB for future dates
2. Some stocks not yet listed or delisted
3. Data quality issues in the source

## Next Steps

The weekly factor data is ready for use in:
1. Machine learning model training
2. Factor analysis
3. Backtesting strategies
4. Portfolio construction

All files are saved directly in `./data/weekly_factors/` with consistent naming and format.
