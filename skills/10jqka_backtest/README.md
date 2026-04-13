# 10jqka Formula Backtest Skill

This skill allows for automated backtesting of natural language "formulas" on the 10jqka (问财) platform. It mimics the behavior of the web interface to submit backtest tasks and (eventually) poll for results.

## Prerequisites

- Node.js (v18+)
- NPM
- Playwright (installed via `npm install` and `npx playwright install`)

## Quick Start

### 1. Installation

```bash
cd skills/10jqka_backtest
npm install
npx playwright install chromium
```

### 2. Login (Manual or Automated)

You can choose between two login methods:

#### Method A: Automated (Using .env credentials)
```bash
npm run login:auto
```
This will attempt to fill your username and password from `.env` automatically. If a slider appear, it will wait for you to handle it in the browser window.

#### Method B: Manual
```bash
npm run login
```
Use this if the automated method is blocked or fails.

### 3. Verify Session
```bash
npm run test:session
```

### 4. Run a Strategy
```bash
node run-skill.js examples/formula_strategy.json
```
If your session is expired, `run-skill.js` will automatically trigger `npm run login:auto`.


## Strategy Configuration

The strategy configuration is a JSON file. Example:

```json
{
  "formula": [
    "创业板",
    "非ST"
  ],
  "startDate": "2025-01-01",
  "endDate": "2026-04-10",
  "stockHoldCount": 2,
  "takeProfit": 25,
  "stopLoss": 9
}
```

## Architecture

- `browser/`: Scripts for browser-based interaction (login capture).
- `request/`: Low-level HTTP client and configuration normalization.
- `examples/`: Sample strategy files.
- `data/`: Local storage for session cookies and captured API patterns.

## Referencing Other Skills

This skill is designed as a formula-based alternative to:
- `guorn_strategy`: For JoinQuant/Guorn style backtests.
- `thsquant_strategy`: For 10jqka Python-based code strategies.
