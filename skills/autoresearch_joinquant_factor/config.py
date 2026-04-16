PERIOD_CONFIG = {
    "D": {
        "name": "日频",
        "periods_per_year": 244,
        "trading_cost": 0.002,
        "turnover_limit": 0.3,
        "train_years": 2,
        "test_months": 3,
        "cv_folds": 5,
        "ic_rolling_window": 20,
        "max_factors": 5,
    },
    "W": {
        "name": "周频",
        "periods_per_year": 52,
        "trading_cost": 0.002,
        "turnover_limit": 0.5,
        "train_years": 1,
        "test_months": 3,
        "cv_folds": 3,
        "ic_rolling_window": 12,
        "max_factors": 6,
    },
    "M": {
        "name": "月频",
        "periods_per_year": 12,
        "trading_cost": 0.002,
        "turnover_limit": 1.0,
        "train_years": 1,
        "test_months": 6,
        "cv_folds": 3,
        "ic_rolling_window": 6,
        "max_factors": 8,
    },
}

DEFAULT_PERIOD = "W"
