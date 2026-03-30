# RiceQuant Strategy Skill

Run quantitative trading strategy backtests on RiceQuant platform programmatically.

## Usage

```bash
# Run a backtest with a strategy file
node run-skill.js --strategy path/to/strategy.py --config '{"start_date":"2022-01-01","end_date":"2022-12-31"}'

# List existing strategies
node list-strategies.js

# Fetch backtest report
node fetch-report.js --id <backtestId> [--full]
```

## Configuration

Create `.env` file with:
```
RICEQUANT_USERNAME=your_username
RICEQUANT_PASSWORD=your_password
```

## API Endpoints

RiceQuant uses these endpoints:
- `GET /api/user/v1/workspaces` - Get workspace list
- `GET /api/strategy/v1/workspaces/{id}/strategies` - List strategies
- `POST /api/strategy/v1/workspaces/{id}/strategies` - Create strategy
- `POST /api/backtest/v1/workspaces/{id}/backtests` - Run backtest
- `GET /api/backtest/v1/workspaces/{id}/backtests/{btId}` - Get backtest status
- `GET /api/backtest/v1/workspaces/{id}/backtests/{btId}/risk` - Risk metrics (Sharpe, MaxDrawdown)
- `GET /api/backtest/v1/workspaces/{id}/backtests/{btId}/positions` - Daily positions
- `GET /api/backtest/v1/workspaces/{id}/backtests/{btId}/logs` - Backtest logs

## Backtest Report

The `fetch-report.js` provides:
- Basic info (status, title, dates)
- Risk metrics (Sharpe, Sortino, MaxDrawdown, Alpha, Beta, etc.)
- Position summary (trading days, market value, estimated return)

## Files

```
ricequant_strategy/
├── .env                    # Account credentials
├── browser/
│   ├── capture-session.js  # Browser login automation
│   └── session-manager.js  # Session persistence
├── request/
│   ├── ricequant-client.js # Core HTTP client
│   └── strategy-runner.js  # Strategy workflow
├── run-skill.js            # CLI: Run backtest
├── list-strategies.js      # CLI: List strategies
├── fetch-report.js         # CLI: Get backtest report
└── data/
    └── session.json        # Saved session cookies
```

## Notes

- RiceQuant session requires browser login (uses Playwright)
- Session cookies stored in `data/session.json`
- RQAlpha API differs from JoinQuant:
  - `scheduler.run_monthly()` doesn't support `time` parameter
  - Use `context.portfolio.positions[stock].market_value` for position value
  - Use `/risk` endpoint for statistics (not `/stats`)