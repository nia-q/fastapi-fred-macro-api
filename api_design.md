
## 📊 FRED Macro API – Endpoint Summary & Purpose

This API simplifies and transforms economic data from the Federal Reserve’s FRED API into actionable insights for use in investment analysis, trading dashboards, and economic modeling.

---

### 🔹 `GET /macro/indicator/{series_id}` (added)

**What it does**:
Fetches the latest value for a single macroeconomic indicator (e.g., CPI, Unemployment, GDP).

**Why it matters**:
Investors and strategists constantly track key indicators to assess market conditions. This endpoint provides quick, programmatic access for dashboards and reports.

---

### 🔹 `GET /macro/trend/{series_id}?months=12` (added)

**What it does**:
Calculates percent change and trend direction for an indicator over a specified period (e.g., past 12 months).

**Why it matters**:
The direction of movement (up/down) is often more meaningful than a raw number. Traders and economists use this to assess momentum, inflation acceleration, or job market stability.

---

### 🔹 `GET /macro/compare?series=CPIAUCSL,UNRATE`

**What it does**:
Returns side-by-side values and trends for multiple macro indicators.

**Why it matters**:
Comparing indicators is essential in macro research (e.g., inflation vs. unemployment). This endpoint enables multi-variable analysis used in trading decisions or strategy validation.

---

### 🔹 `GET /macro/summary`

**What it does**:
Returns a curated summary of the most important U.S. economic indicators including CPI, GDP, Unemployment Rate, and Federal Funds Rate.

**Why it matters**:
This one-call dashboard view is ideal for financial firms, traders, or researchers who need a real-time snapshot of macroeconomic health without hitting multiple endpoints.

---

### 🔹 `GET /macro/regime`

**What it does**:
Classifies the current macroeconomic “regime” (e.g., expansion, tightening, stagnation) based on thresholds of key indicators.

**Why it matters**:
Quantitative firms often adapt their models based on regime. This endpoint simplifies regime detection and can be used as input to dynamic trading strategies or risk management systems.

---

### 🔹 `POST /macro/event-impact`

**What it does**:
Analyzes how key indicators shifted before and after a specified event date (e.g., COVID crash, 2008 crisis).

**Why it matters**:
Understanding macro shifts around major events is critical for backtesting, research, and strategy development. This feature is not natively available in FRED and adds unique historical context.

---

Let me know if you want this formatted into a downloadable `.md` file or added to your actual project `README.md`.
