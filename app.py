import streamlit as st
import pandas as pd
import plotly.express as px
from lifelines import CoxPHFitter
from fpdf import FPDF
import base64
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Harare Asset Engine", layout="wide", page_icon="🇿🇼")

# --- 1. DATA LOADING (MUST BE FIRST) ---
if 'data_loaded' not in st.session_state:
    st.session_state['data_loaded'] = False

if not st.session_state['data_loaded']:
    try:
        st.session_state['terrace_df'] = pd.read_csv("terrace_africa_v2.csv")
        st.session_state['westprop_df'] = pd.read_csv("westprop_v2.csv")
        st.session_state['data_loaded'] = True
    except FileNotFoundError:
        st.error("⚠️ Data missing! Run your Jupyter Notebook first.")
        st.stop()

# --- 2. RESET LOGIC (CALLBACK) ---
def reset_callback():
    if 'terrace_df' in st.session_state:
        all_assets = list(st.session_state['terrace_df']['Asset_Name'].unique())
        st.session_state['widget_t_assets'] = all_assets
        st.session_state['t_assets'] = all_assets
    
    st.session_state['widget_t_expiry'] = (0, 60)
    st.session_state['t_expiry'] = (0, 60)
    st.session_state['widget_t_risk'] = False
    st.session_state['t_risk'] = False
    
    st.session_state['widget_w_sim'] = False
    st.session_state['w_sim'] = False
    st.session_state['widget_w_budget'] = 0
    st.session_state['w_budget'] = 0

# --- 3. HELPER FUNCTIONS ---
def update_state(key, widget_key):
    st.session_state[key] = st.session_state[widget_key]

# --- 4. RECOMMENDATION ENGINE (THE NEW BRAIN) ---
def get_recommendations(mode, df, metrics):
    recs = []
    
    if mode == "Terrace Africa":
        # Extract numerical values safely
        risk_count = metrics['High Risk Tenants']
        rev_risk_str = str(metrics['Revenue at Risk']).replace('$','').replace(',','')
        rev_risk = float(rev_risk_str) if rev_risk_str else 0
        
        # 1. Revenue Risk Logic
        if rev_risk > 150000:
            recs.append("CRITICAL: Revenue exposure exceeds $150k. Immediate legal demand letters recommended for top 5 debtors.")
        elif rev_risk > 50000:
            recs.append("Moderate Revenue Risk. Initiate payment plan negotiations with 'Late Pay' tenants.")
            
        # 2. Tenant Volume Logic
        if risk_count > 25:
            recs.append("Portfolio Health Alert: High volume of at-risk tenants. Review property management collection procedures.")
            
        # 3. Root Cause Logic
        if not df.empty and 'Late_Payments_Last_12M' in df.columns:
            late_payers = len(df[df['Late_Payments_Last_12M'] > 0])
            if late_payers > (len(df) * 0.6):
                recs.append("Dominant Issue: Cash Flow. Tenants are struggling to pay. Review rental levels vs. market turnover.")
            else:
                recs.append("Dominant Issue: Footfall. Tenants are suffering from low traffic. Marketing activations required.")

    else: # WestProp
        # Extract numerical values
        occ_str = str(metrics['Committed Occupancy']).replace('%','')
        committed_occ = float(occ_str) if occ_str else 0
        sim_active = metrics.get('Simulation Active', 'No') == 'Yes'
        
        # 1. Occupancy Logic
        if committed_occ < 30:
            recs.append("Early Stage Risk: Occupancy below 30%. Prioritize Anchor Tenant incentives to unlock line shop interest.")
        elif committed_occ < 60:
            recs.append("Growth Phase: accelerate broker incentives to cross the 60% threshold for bank funding.")
        else:
            recs.append("Stabilization: Strong pre-let status. Focus on 'Tenant Mix' curation and premium rental rates.")
            
        # 2. Simulation Logic
        if sim_active:
            recs.append("SCENARIO: This simulation confirms project viability. Use this report for Bank Funding applications.")
        else:
            recs.append("Pipeline Opportunity: Significant GLA in 'Negotiating' phase. Launch closing campaign to convert pipeline.")

    if not recs:
        recs.append("Operations appear stable based on current filters. Continue routine monitoring.")
        
    return recs

# --- PDF ENGINE ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Harare Asset Intelligence | Automated Board Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_report(df, mode, metrics):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title Logic
    is_risk_report = False
    if 'Risk_Flag' in df.columns and not df.empty:
        if df['Risk_Flag'].all(): 
            is_risk_report = True

    title = "CRITICAL RISK WATCHLIST" if is_risk_report and mode == "Terrace Africa" else \
            "ASSET PERFORMANCE REPORT" if mode == "Terrace Africa" else \
            "DEVELOPMENT FEASIBILITY REPORT"

    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=title, ln=True, align='L')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='L')
    pdf.ln(5)
    
    # Metrics Section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Key Performance Indicators", ln=True, align='L')
    pdf.set_font("Arial", size=11)
    
    for key, value in metrics.items():
        clean_value = str(value).encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(200, 8, txt=f"{key}: {clean_value}", ln=True)
    pdf.ln(5)

    # --- NEW: STRATEGIC RECOMMENDATIONS SECTION ---
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 50, 100) # Dark Blue for Professional Look
    pdf.cell(200, 10, txt="Strategic Recommendations / Executive Note", ln=True, align='L')
    pdf.set_font("Arial", 'I', 11) # Italic for advice
    pdf.set_text_color(0, 0, 0) # Back to Black
    
    recs = get_recommendations(mode, df, metrics)
    for rec in recs:
        # Clean text for PDF compatibility
        clean_rec = rec.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 8, txt=f"- {clean_rec}")
    pdf.ln(5)
    
    # Table Logic
    def draw_header(mode_type, is_risk):
        pdf.set_font("Arial", 'B', 10)
        if mode_type == "Terrace Africa":
            if is_risk:
                pdf.set_fill_color(255, 200, 200) # Light Red
            else:
                pdf.set_fill_color(200, 220, 255) # Light Blue
            pdf.cell(60, 10, "Tenant", 1, 0, 'C', 1)
            pdf.cell(40, 10, "Asset", 1, 0, 'C', 1)
            pdf.cell(30, 10, "GLA (m2)", 1, 0, 'C', 1)
            pdf.cell(40, 10, "Status / Risk", 1, 1, 'C', 1)
        else:
            pdf.set_fill_color(220, 255, 220)
            pdf.cell(60, 10, "Tenant", 1, 0, 'C', 1)
            pdf.cell(50, 10, "Status", 1, 0, 'C', 1)
            pdf.cell(40, 10, "Fit-Out Budget ($)", 1, 1, 'C', 1)
    
    if mode == "Terrace Africa":
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Tenant Portfolio Snapshot", ln=True, align='L')
        
        view_df = df.sort_values('GLA_Occupied', ascending=False)
        draw_header("Terrace Africa", is_risk_report)
        pdf.set_font("Arial", size=10)
        
        for index, row in view_df.iterrows():
            if pdf.get_y() > 250:
                pdf.add_page()
                draw_header("Terrace Africa", is_risk_report)
                pdf.set_font("Arial", size=10)

            tenant = str(row['Tenant_Name']).encode('latin-1', 'replace').decode('latin-1')[:25]
            asset = str(row['Asset_Name']).encode('latin-1', 'replace').decode('latin-1')[:25]
            
            if row['Risk_Flag']:
                status = "LATE PAY" if row['Late_Payments_Last_12M'] > 0 else "LOW FOOTFALL"
            else:
                status = "Active / Good"
            
            pdf.cell(60, 10, tenant, 1)
            pdf.cell(40, 10, asset, 1)
            pdf.cell(30, 10, str(row['GLA_Occupied']), 1)
            pdf.cell(40, 10, status, 1, 1)
            
    else: # WestProp Logic
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Leasing Pipeline Snapshot", ln=True, align='L')
        
        view_df = df.sort_values('GLA_Occupied', ascending=False)
        draw_header("WestProp", False)
        pdf.set_font("Arial", size=10)
        
        for index, row in view_df.iterrows():
            if pdf.get_y() > 250:
                pdf.add_page()
                draw_header("WestProp", False)
                pdf.set_font("Arial", size=10)

            tenant = str(row['Tenant_Name']).encode('latin-1', 'replace').decode('latin-1')[:25]
            status = str(row['Pre_Let_Status']).encode('latin-1', 'replace').decode('latin-1')[:20]
            
            pdf.cell(60, 10, tenant, 1)
            pdf.cell(50, 10, status, 1)
            pdf.cell(40, 10, f"${row['Fit_Out_Budget_USD']:,.0f}", 1, 1)

    return pdf.output(dest='S').encode('latin-1')

# --- 5. SIDEBAR CONFIG ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/ec/Flag_of_Zimbabwe.svg", width=50)
st.sidebar.title("Asset Intelligence")

st.sidebar.button("🔄 Reset Dashboard", on_click=reset_callback)

mode = st.sidebar.radio(
    "Select Portfolio Mode:", 
    ["Terrace Africa (Operational)", "WestProp (Development)"],
    key="app_mode" 
)

st.sidebar.markdown("---")
st.sidebar.header("🎛️ Control Panel")

# --- 6. MAIN APPLICATION LOGIC ---

if mode == "Terrace Africa (Operational)":
    df = st.session_state['terrace_df']
    available_assets = df['Asset_Name'].unique()
    
    if 't_assets' not in st.session_state:
        st.session_state['t_assets'] = list(available_assets)
        st.session_state['t_expiry'] = (0, 60)
        st.session_state['t_risk'] = False

    selected_assets = st.sidebar.multiselect(
        "Filter by Asset:", 
        options=available_assets, 
        default=st.session_state['t_assets'],
        key="widget_t_assets",
        on_change=update_state, args=('t_assets', 'widget_t_assets')
    )
    
    max_months = int(df['Lease_Expiry_Months'].max())
    expiry_range = st.sidebar.slider(
        "Filter: Lease Expiry Timeline (Months)",
        min_value=0, 
        max_value=max_months, 
        value=st.session_state['t_expiry'],
        key="widget_t_expiry",
        on_change=update_state, args=('t_expiry', 'widget_t_expiry')
    )
    
    show_risk_only = st.sidebar.checkbox(
        "⚠️ Show 'High Risk' Tenants Only",
        value=st.session_state['t_risk'],
        key="widget_t_risk",
        on_change=update_state, args=('t_risk', 'widget_t_risk')
    )

    filtered_df = df[df['Asset_Name'].isin(selected_assets)]
    filtered_df = filtered_df[
        (filtered_df['Lease_Expiry_Months'] >= expiry_range[0]) & 
        (filtered_df['Lease_Expiry_Months'] <= expiry_range[1])
    ]
    if show_risk_only:
        filtered_df = filtered_df[filtered_df['Risk_Flag'] == True]

    total_gla = filtered_df['GLA_Occupied'].sum()
    monthly_rev = (filtered_df['GLA_Occupied'] * filtered_df['Rent_per_Sqm']).sum()
    risk_subset = filtered_df[filtered_df['Risk_Flag'] == True]
    rev_at_risk = (risk_subset['GLA_Occupied'] * risk_subset['Rent_per_Sqm']).sum()

    st.sidebar.markdown("---")
    st.sidebar.header("📄 Reporting")
    report_metrics = {
        "Assets in View": len(selected_assets),
        "Total GLA Visible": f"{total_gla:,.0f} m2",
        "Monthly Revenue": f"${monthly_rev:,.2f}",
        "Revenue at Risk": f"${rev_at_risk:,.2f}",
        "High Risk Tenants": len(filtered_df) if show_risk_only else len(risk_subset)
    }
    
    if st.sidebar.button("Generate Board Report"):
        pdf_bytes = generate_report(filtered_df, "Terrace Africa", report_metrics)
        st.sidebar.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name="Terrace_Report.pdf",
            mime="application/pdf"
        )

    st.title("🇿🇼 Terrace Africa: Revenue Protection")
    st.markdown(f"**View:** {', '.join(selected_assets) if selected_assets else 'No Assets Selected'}")
    
    if filtered_df.empty:
        st.warning("No tenants match your filters.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Visible GLA", f"{total_gla:,.0f} m²")
        c2.metric("Monthly Revenue", f"${monthly_rev:,.0f}")
        c3.metric("Revenue at Risk", f"${rev_at_risk:,.0f}", delta="Action Required", delta_color="inverse")
        c4.metric("Tenants in View", len(filtered_df))
        
        st.divider()

        st.subheader("📊 Portfolio Composition (Tenant Mix)")
        
        def categorize_tenant(name):
            name = name.lower()
            if any(x in name for x in ['pizza', 'chicken', 'creamy', 'nush', 'smokehouse', 'spur', 'rocomamas', 'ocean', 'mugg', 'kfc']):
                return 'Food & Beverage'
            elif any(x in name for x in ['pick n pay', 'spar', 'woolworths', 'checkers']):
                return 'Grocery / Anchor'
            elif any(x in name for x in ['pharmacy', 'clicks', 'sorbet', 'bank', 'solution']):
                return 'Services / Health'
            elif 'line shop' in name:
                return 'Specialty Retail' 
            else:
                return 'Other Retail'

        viz_df = filtered_df.copy()
        viz_df['Category'] = viz_df['Tenant_Name'].apply(categorize_tenant)
        
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.markdown("**Sector Exposure:**")
            sector_counts = viz_df['Category'].value_counts()
            st.dataframe(sector_counts, use_container_width=True)
            
        with c2:
            fig_sun = px.sunburst(
                viz_df, 
                path=['Category', 'Asset_Name'], 
                values='GLA_Occupied',
                color='Category',
                title="GLA Distribution by Sector",
                color_discrete_map={
                    'Food & Beverage': '#EF553B', 
                    'Grocery / Anchor': '#00CC96', 
                    'Services / Health': '#AB63FA', 
                    'Specialty Retail': '#636EFA',
                    'Other Retail': 'grey'
                }
            )
            st.plotly_chart(fig_sun, use_container_width=True)

        st.subheader("Asset Performance Matrix")
        fig = px.scatter(
            filtered_df, x="Lease_Expiry_Months", y="Rent_per_Sqm", 
            size="GLA_Occupied", color="Asset_Name", hover_name="Tenant_Name",
            title="Interactive Tenant Map: Size = GLA (m²)", size_max=60, height=500
        )
        fig.add_vline(x=12, line_dash="dash", line_color="red", annotation_text="Critial 12-Month Zone")
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📂 View Tenant List"):
            st.dataframe(filtered_df[['Asset_Name', 'Tenant_Name', 'GLA_Occupied', 'Lease_Expiry_Months', 'Risk_Flag']].sort_values('Lease_Expiry_Months'), use_container_width=True)

else:
    df = st.session_state['westprop_df']
    
    if 'w_sim' not in st.session_state:
        st.session_state['w_sim'] = False
        st.session_state['w_budget'] = 0

    st.sidebar.subheader("🚀 Simulation Tools")
    
    simulate_success = st.sidebar.checkbox(
        "✅ Simulate: Close All Pipeline Deals",
        value=st.session_state['w_sim'],
        key="widget_w_sim",
        on_change=update_state, args=('w_sim', 'widget_w_sim')
    )
    
    min_budget = st.sidebar.number_input(
        "Minimum Fit-Out Budget ($)", 
        0, 10000000, 
        value=st.session_state['w_budget'], 
        step=50000,
        key="widget_w_budget",
        on_change=update_state, args=('w_budget', 'widget_w_budget')
    )

    filtered_df = df[df['Fit_Out_Budget_USD'] >= min_budget]
    
    if simulate_success:
        filtered_df = filtered_df.copy()
        filtered_df.loc[filtered_df['Pre_Let_Status'] == 'Negotiating', 'Pre_Let_Status'] = 'Committed (Simulated)'
        st.success("🔮 Simulation Active: Projecting 100% conversion of pipeline deals.")

    total_gla = 90000
    committed_mask = filtered_df['Pre_Let_Status'].str.contains('Committed')
    committed_gla = filtered_df[committed_mask]['GLA_Occupied'].sum()
    occupied_gla = filtered_df['GLA_Occupied'].sum()
    vacant_gla = total_gla - occupied_gla

    st.sidebar.markdown("---")
    st.sidebar.header("📄 Reporting")
    report_metrics = {
        "Simulation Active": "Yes" if simulate_success else "No",
        "Master Plan GLA": "90,000 m2",
        "Committed Occupancy": f"{(committed_gla/total_gla)*100:.1f}%",
        "Pipeline/Negotiating": f"{(occupied_gla - committed_gla):,.0f} m2"
    }
    
    if st.sidebar.button("Generate Feasibility Report"):
        pdf_bytes = generate_report(filtered_df, "WestProp Holdings", report_metrics)
        st.sidebar.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name="WestProp_Report.pdf",
            mime="application/pdf"
        )

    st.title("🏗️ Mall of Zimbabwe: Feasibility Engine")
    c1, c2, c3 = st.columns(3)
    c1.metric("Master Plan GLA", "90,000 m²")
    c2.metric("Committed Occupancy", f"{committed_gla:,.0f} m²", f"{(committed_gla/total_gla)*100:.1f}%")
    c3.metric("Remaining Vacancy", f"{vacant_gla:,.0f} m²")
    
    st.divider()
    st.subheader("Leasing Velocity Tracker")
    status_counts = filtered_df.groupby('Pre_Let_Status')['GLA_Occupied'].sum().reset_index()
    status_counts = pd.concat([status_counts, pd.DataFrame({'Pre_Let_Status': ['Vacant Space'], 'GLA_Occupied': [vacant_gla]})])
    
    fig_bar = px.bar(
        status_counts, y="Pre_Let_Status", x="GLA_Occupied", orientation='h', color="Pre_Let_Status",
        title="90,000m² Fill-Rate Analysis",
        color_discrete_map={"Committed": "#000080", "Committed (Simulated)": "#4169E1", "Negotiating": "orange", "Vacant Space": "lightgrey"}
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.subheader("⚓ Anchor Tenant Status")
    anchors = filtered_df[filtered_df['GLA_Occupied'] > 2000].sort_values('GLA_Occupied', ascending=False)
    st.dataframe(anchors[['Tenant_Name', 'GLA_Occupied', 'Pre_Let_Status', 'Fit_Out_Budget_USD', 'Deposit_Paid']], use_container_width=True)