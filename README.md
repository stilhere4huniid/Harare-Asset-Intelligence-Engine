# 🇿🇼 Harare Asset Intelligence Engine

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)
![License](https://img.shields.io/badge/License-MIT-green)

**A professional-grade Real Estate Intelligence Dashboard designed for the Zimbabwean market.**

This tool serves two distinct profiles:
1.  **Terrace Africa (Operational Defense):** Protecting revenue by identifying at-risk tenants using Survival Analysis.
2.  **WestProp Holdings (Development Offense):** Simulating leasing velocity and pre-let occupancy for the Mall of Zimbabwe.

---

## 🚀 Key Features
* **Automated Board Reporting:** Generates instant, PDF-ready "Board Packs" for executive meetings.
* **Revenue Risk Detection:** Uses statistical modeling to flag tenants with "Late Pay" or "Low Footfall" risks.
* **Leasing Simulation Engine:** A "What-If" simulator that projects occupancy rates if pipeline deals close.
* **State Management:** Robust session handling ensures data persists when switching between profiles.
* **Tenant Mix Analysis:** Visualizes sector exposure (Retail vs. Food vs. Services) using Sunburst charts.

---

## 📸 Visual Walkthrough

### Scenario A: Revenue Protection (Terrace Africa)
*Identifying \$273k in monthly revenue at risk across the portfolio.*

| **Live Dashboard Risk Detection** | **Automated PDF Risk Report** |
|:---:|:---:|
| ![Risk Dashboard](assets/2025-12-27%2012%2023%2024.png) | ![Risk Report](assets/2025-12-27%2012%2025%2020.png) |

### Scenario B: Asset Deep Dive (Highland Park)
*Drilling down into specific assets to view tenant mix and lease expiries.*

| **Asset Level View** | **Asset Performance Report** |
|:---:|:---:|
| ![Asset Dashboard](assets/2025-12-27%2012%2026%2054.png) | ![Asset Report](assets/2025-12-27%2012%2028%2035.png) |

### Scenario C: Development Feasibility (WestProp)
*Simulating a 100% conversion rate on the leasing pipeline to secure bank funding.*

| **Leasing Simulator (Pre-Simulation)** | **Feasibility Report (Simulated)** |
|:---:|:---:|
| ![Sim Dashboard](assets/2025-12-27%2012%2032%2004.png) | ![Sim Report](assets/2025-12-27%2012%2033%2050.png) |

### Scenario D: High-Value Tenant Filtering
*Filtering the pipeline for "Blue Chip" Anchor tenants with fit-out budgets > \$3M.*

| **Anchor Tenant Tracker** | **Executive Budget Report** |
|:---:|:---:|
| ![Budget Dashboard](assets/2025-12-27%2012%2030%2053.png) | ![Budget Report](assets/2025-12-27%2012%2031%2024.png) |

---

## 🛠️ Tech Stack
* **Core Logic:** Python 3.9+
* **Frontend:** Streamlit
* **Data Visualization:** Plotly Express
* **Reporting Engine:** FPDF (PDF Generation)
* **Data Manipulation:** Pandas & NumPy
* **Statistical Modeling:** Lifelines (Cox Proportional Hazards)

---

Harare-Asset-Intelligence-Engine/
│
├── assets/                     # Folder for all your screenshots
│   ├── dashboard_terrace_risk.png
│   ├── report_terrace_risk.pdf.png
│   ├── dashboard_highland_park.png
│   ├── report_highland_park.png
│   ├── dashboard_westprop_anchors.png
│   ├── report_westprop_anchors.png
│   ├── dashboard_westprop_sim.png
│   ├── report_westprop_sim.png
│   └── ... (other images)
│
├── venv/                       # Virtual Environment (Do not commit to GitHub)
├── .gitignore                  # Git Ignore file
├── app.py                      # Main Application Script
├── terrace_africa_v2.csv       # Generated Data
├── westprop_v2.csv             # Generated Data
├── data_generation.ipynb       # Renamed from 'Untitled.ipynb' for clarity
├── requirements.txt            # Dependencies
├── README.md                   # Main Landing Page
├── METHODOLOGY.md              # The Math & Logic
├── DOCUMENTATION.md            # User Manual
└── LICENSE                     # MIT License

---

## 💻 Installation & Usage

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/stilhere4huniid/Harare-Asset-Intelligence-Engine.git](https://github.com/stilhere4huniid/Harare-Asset-Intelligence-Engine.git)
    cd Harare-Asset-Intelligence-Engine
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Data Generator (Optional)**
    If you want fresh random data, run the Jupyter Notebook:
    * Open `data_generation.ipynb` and run all cells to update the CSV files.

4.  **Launch the Dashboard**
    ```bash
    streamlit run app.py
    ```

---

## ⚠️ Disclaimer
This is an independent Data Science portfolio project created strictly for educational and demonstration purposes.

I am not affiliated with **WestProp Holdings** or **Terrace Africa**. All financial figures, rental assumptions, tenant names (outside of known anchors), and construction estimates are **hypothetical simulations** used to demonstrate financial modeling capabilities. This tool does not constitute professional investment advice, and the creator assumes no liability for decisions made based on its outputs.

---

## 📬 Contact
**Adonis Chiruka**
*Data Science & Financial Modeling*

* 📧 **Email:** stillhere4hunnid@gmail.com
* 🔗 **LinkedIn:** [Adonis Chiruka](https://www.linkedin.com/in/adonis-chiruka-70b265323)
* 🐙 **GitHub:** [stilhere4huniid](https://github.com/stilhere4huniid)

---
*MIT License © 2025 Adonis Chiruka*