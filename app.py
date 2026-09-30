import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set Page Config
st.set_page_config(
    page_title="A-Flex Sentiment Dashboard",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling to mimic Power BI visual layout
st.markdown("""
    <style>
    .stApp { background-color: #f4f6f9; }
    .card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        margin-bottom: 10px;
    }
    .metric-title { font-size: 13px; color: #555; font-weight: 600; }
    .metric-val { font-size: 22px; font-weight: bold; color: #1e3a8a; }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# SIDEBAR FILTERS (Applies to both pages)
# ----------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/delivery-truck.png", width=60)
    st.title("A-Flex Controls")
    
    st.subheader("Filter Options")
    depot_type = st.selectbox("Depot Type", ["All", "Logistics", "Fresh", "Morrisons", "Co-op"])
    sentiment_filter = st.selectbox("Sentiment", ["All", "Positive", "Neutral", "Negative", "Slightly Negative"])
    intensity_level = st.select_slider("Intensity Level", options=[1, 2, 3, 4, 5], value=(1, 5))
    date_range = st.selectbox("Date Scope", ["Last 3 Years", "Last Year", "Last 6 Months"])
    has_attachment = st.checkbox("Attachment Included Only", value=False)

    st.divider()
    nav_page = st.radio("Select View / Page", ["Page 1: Executive Overview", "Page 2: Paginated Detail Report"])

# Colors matching dashboard palettes
COLOR_PALETTE = ["#007bff", "#002060", "#fd7e14", "#6f42c1", "#e83e8c"]

# ----------------------------------------------------
# PAGE 1: EXECUTIVE OVERVIEW
# ----------------------------------------------------
if nav_page == "Page 1: Executive Overview":
    st.title("🚛 A-Flex Sentiment Dashboard (ver2)")
    
    # Top KPI Metrics Row
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.markdown('<div class="card"><div class="metric-title">Positive Ratio</div><div class="metric-val">0.07</div></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown('<div class="card"><div class="metric-title">Neutral Ratio</div><div class="metric-val">0.35</div></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown('<div class="card"><div class="metric-title">Negative Ratio</div><div class="metric-val">0.58</div></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown('<div class="card"><div class="metric-title"># Block</div><div class="metric-val">44</div></div>', unsafe_allow_html=True)
    with kpi5:
        st.markdown('<div class="card"><div class="metric-title"># Report</div><div class="metric-val">23</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Donut Charts Grid (Row 1)
    col_d1, col_d2, col_d3 = st.columns(3)
    
    with col_d1:
        st.subheader("Issue by Sentiment")
        df_sent = pd.DataFrame({
            "Sentiment": ["Negative", "Neutral", "Slightly Neg.", "Slightly Pos."],
            "Count": [16, 5, 1, 1]
        })
        fig_sent = px.pie(df_sent, names="Sentiment", values="Count", hole=0.5, color_discrete_sequence=COLOR_PALETTE)
        fig_sent.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=220)
        st.plotly_chart(fig_sent, use_container_width=True)

    with col_d2:
        st.subheader("# Report by Depot")
        df_depot = pd.DataFrame({
            "Depot": ["DLU2 (Luton)", "ULO5 (West)", "WD18 (Watford)", "AL7 (Welwyn)", "DHA2"],
            "Count": [13, 5, 3, 1, 1]
        })
        fig_depot = px.pie(df_depot, names="Depot", values="Count", hole=0.5, color_discrete_sequence=COLOR_PALETTE)
        fig_depot.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=220)
        st.plotly_chart(fig_depot, use_container_width=True)

    with col_d3:
        st.subheader("# Report by Depot Type")
        df_dtype = pd.DataFrame({
            "Type": ["Logistics", "Fresh", "Morrisons"],
            "Count": [14, 5, 4]
        })
        fig_dtype = px.pie(df_dtype, names="Type", values="Count", hole=0.5, color_discrete_sequence=COLOR_PALETTE)
        fig_dtype.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=220)
        st.plotly_chart(fig_dtype, use_container_width=True)

    st.markdown("---")

    # Time Series Area Chart & Sentiment Details (Row 2)
    col_a1, col_a2 = st.columns([3, 2])
    
    with col_a1:
        st.subheader("# Block, # Issue, # Report by Month")
        months = ["January", "February", "March", "September", "October", "November", "December"]
        df_time = pd.DataFrame({
            "Month": months,
            "# Block": [1, 10, 7, 7, 9, 10, 1],
            "# Issue": [0, 6, 2, 1, 5, 6, 0],
            "# Report": [0, 10, 3, 3, 5, 10, 0]
        })
        fig_time = go.Figure()
        fig_time.add_trace(go.Scatter(x=df_time["Month"], y=df_time["# Block"], name="# Block", fill='tozeroy', line=dict(color='#007bff')))
        fig_time.add_trace(go.Scatter(x=df_time["Month"], y=df_time["# Issue"], name="# Issue", fill='tozeroy', line=dict(color='#002060')))
        fig_time.add_trace(go.Scatter(x=df_time["Month"], y=df_time["# Report"], name="# Report", fill='tozeroy', line=dict(color='#fd7e14')))
        fig_time.update_layout(margin=dict(t=10, b=10, l=0, r=0), height=280, legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_time, use_container_width=True)

    with col_a2:
        st.subheader("Recent Document Audit Logs")
        df_reports = pd.DataFrame({
            "Document Title": [
                "Gmail - Refrain from lowering my driver rating (delivery block 5-Mar-2024).pdf",
                "Gmail - Refrain from lowering my driver rating (19-Feb-2025).pdf",
                "Gmail - Claim for the extra time of allocated block (26-Oct-2024).pdf",
                "Gmail - Claim for extra time allocated block (1-Mar-2025).pdf"
            ]
        })
        st.dataframe(df_reports, use_container_width=True, hide_index=True)

    # Bar Chart & Word Cloud Row (Row 3)
    col_b1, col_b2 = st.columns([1, 1])
    
    with col_b1:
        st.subheader("Sentiment Details by Category Count")
        df_cat = pd.DataFrame({
            "Category": ["Key Complaints", "Notable Images", "Visual Evidence"],
            "Count": [125, 105, 65]
        })
        fig_cat = px.bar(df_cat, x="Category", y="Count", color_discrete_sequence=["#007bff"])
        fig_cat.update_layout(height=230, margin=dict(t=10, b=0, l=0, r=0))
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_b2:
        st.subheader("Key Sentiment Keywords")
        st.info("📌 **Frequently Extracted Terms:** delivery, block, encountered, road closure, traffic, scheduled, duration, extra time, parcel, stops, customer, app issue, rating, mislabeling.")

# ----------------------------------------------------
# PAGE 2: PAGINATED DETAIL REPORT
# ----------------------------------------------------
else:
    st.title("📄 Detail Sentiment Report (Paginated View)")
    st.caption("Document ID: `20260207_LU_Logistics_delivery_block_LU56JH_20260207_1700_issue_report.docx`")

    # Metadata Header Card
    with st.container():
        st.markdown("""
            <div class="card">
                <h4>📌 Document Metadata</h4>
                <p><b>Date:</b> 07-Feb-2026 &nbsp;|&nbsp; <b>Depot:</b> DLU2 (LU Logistics) &nbsp;|&nbsp; <b>Tone:</b> Factual and Objective</p>
            </div>
        """, unsafe_allow_html=True)

    # Score Metrics Row
    m1, m2, m3 = st.columns(3)
    m1.metric("Positive Score", "0.05")
    m2.metric("Neutral Score", "0.75")
    m3.metric("Negative Score", "0.20")

    st.markdown("---")

    col_r1, col_r2 = st.columns([3, 2])

    with col_r1:
        st.subheader("📝 Overall Sentiment Summary")
        st.write("""
            The document describes several issues encountered during a delivery block, leading to delays and increased time spent. 
            The tone is primarily factual and descriptive of the problems, with a **neutral to slightly negative** overall sentiment.
        """)

        st.subheader("⚠️ Key Complaints")
        st.markdown("""
        * **Extended Schedule:** Delivery block originally scheduled for 5:00 PM - 9:00 PM, but orders were shown for delivery by 10 PM, extending the overall duration.
        * **Parcel Sorting:** Difficulty in finding the target package in the car trunk due to sorting and grouping challenges.
        * **Traffic & Closures:** En-route delays caused by unforeseen road closures and mislabeled route maps in the driver app.
        """)

        st.subheader("📷 Visual Evidence & Summary")
        st.write("""
            The screenshots provide visual confirmation of the delivery schedule, parcel pickup details, itinerary, and map views, 
            supporting the narrative of the issues. Timestamps and itinerary details directly correlate with text descriptions.
        """)

    with col_r2:
        st.subheader("🖼️ Notable Images / Screenshots")
        
        with st.expander("Map View: ROAD CLOSED Sign", expanded=True):
            st.write("Corroborates text regarding blocked roads and route failures.")
            
        with st.expander("Schedule Screenshot (5 PM - 10 PM)"):
            st.write("Confirms original 5 PM - 9 PM schedule extended to 10 PM.")
            
        with st.expander("Pickup Confirmation (42 Parcels)"):
            st.write("Shows 'Picked up at 5:00 PM' notification and itemized count.")

        with st.expander("Itinerary & Route Details"):
            st.write("Illustrates planned delivery route and potential failure points.")

    st.subheader("🏷️ Identified Visual Evidence Categories")
    st.button("App Interfaces")
    st.button("Map Views")
    st.button("Route Screenshots")
