# 🧠 Methodology & Logic

This document outlines the data science techniques and logic used to power the Harare Asset Intelligence Engine.

## 1. Data Generation (Synthetic Market Data)
The project uses a Python script (`data_generation.ipynb`) to generate realistic, market-calibrated datasets for two distinct portfolios.
* **Calibration:** Tenant sizes (GLA) are calibrated to real-world expectations (e.g., Supermarkets ~2,500m², Line Shops ~100m²).
* **Randomization:** We use `numpy.random` with set seeds to ensure reproducibility while creating realistic variance in rent rolls, lease expiries, and payment behaviors.

## 2. Risk Detection Logic (Terrace Africa)
The "Revenue at Risk" metric is not a simple sum. It is calculated based on a **Risk Flag** derived from two key variables:
1.  **Late Payments:** Tenants with >1 late payment in the last 12 months.
2.  **Footfall Trend:** Tenants marked with 'Declining' footfall patterns.

The engine filters for these specific conditions and sums the `(GLA * Rent_per_Sqm)` for flagged tenants to quantify the exact monthly revenue exposure.

## 3. Development Simulation (WestProp)
The simulator addresses the "Pre-Let" challenge in property development.
* **State:** Tenants begin in a 'Negotiating' state with a specific probability of closure.
* **Simulation:** When the "Close All Deals" toggle is activated, the Pandas DataFrame is manipulated in-memory. The status of all 'Negotiating' tenants is programmatically changed to 'Committed (Simulated)'.
* **Visualization:** This updates the Occupancy Rate metrics and Bar Charts in real-time to visualize the impact of closing the pipeline.

## 4. Automated Reporting (PDF Engine)
We utilize the `fpdf` library to generate binary PDF files on the fly.
* **Dynamic filtering:** The report engine respects the current state of the dashboard (filters, sliders, simulations).
* **Layout:** It constructs a professional document structure with Headers, Date Stamps, KPI Summaries, and Data Tables that handle page breaks automatically.