import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import math

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Illegal Mining Detection by Using Satellite Data",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #0d2137 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 { margin: 0; font-size: 1.8rem; }
    .main-header p { margin: 0.3rem 0 0 0; opacity: 0.85; font-size: 0.95rem; }
    .kpi-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1.2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        border-left: 4px solid #0ea5e9;
    }
    .kpi-card h3 { margin: 0; font-size: 2rem; color: #38bdf8; }
    .kpi-card p { margin: 0.3rem 0 0 0; font-size: 0.8rem; opacity: 0.7; text-transform: uppercase; }
    .risk-critical { border-left-color: #ef4444; }
    .risk-critical h3 { color: #ef4444; }
    .risk-high { border-left-color: #f97316; }
    .risk-high h3 { color: #f97316; }
    .risk-medium { border-left-color: #eab308; }
    .risk-medium h3 { color: #eab308; }
    .risk-low { border-left-color: #22c55e; }
    .risk-low h3 { color: #22c55e; }
    .alert-box {
        background: #1a1a2e;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        color: white;
    }
    .demo-badge {
        background: #f59e0b;
        color: black;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: bold;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #0ea5e9;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# GLOBAL MINING SITES DATA
# ─────────────────────────────────────────────────────────────
MINING_SITES = [
    {"id": "MG-2026-00421", "name": "Keonjhar Iron Ore Sector", "lat": 21.8423, "lon": 85.5812,
     "country": "India", "mineral": "Iron Ore", "risk_score": 91, "risk": "CRITICAL",
     "disturbed_ha": 14.2, "lease_status": "Outside Registered Lease", "distance_m": 180,
     "ndvi_change": -0.47, "bsi_change": 0.63, "sar_delta": 5.7, "confidence": 96,
     "detection_date": "2026-08-18", "status": "Pending Verification"},
    {"id": "MG-2026-00388", "name": "Pilbara Iron Complex (Mt. Whaleback)", "lat": -23.3631, "lon": 119.6714,
     "country": "Australia", "mineral": "Iron Ore", "risk_score": 78, "risk": "HIGH",
     "disturbed_ha": 22.5, "lease_status": "Active Lease - Boundary Breach", "distance_m": 420,
     "ndvi_change": -0.31, "bsi_change": 0.45, "sar_delta": 4.2, "confidence": 88,
     "detection_date": "2026-08-20", "status": "Under Review"},
    {"id": "MG-2026-00395", "name": "Carajás Mining Complex (N4W/N5)", "lat": -6.0592, "lon": -50.1834,
     "country": "Brazil", "mineral": "Iron Ore", "risk_score": 85, "risk": "HIGH",
     "disturbed_ha": 18.7, "lease_status": "Buffer Zone Encroachment", "distance_m": 310,
     "ndvi_change": -0.39, "bsi_change": 0.52, "sar_delta": 5.1, "confidence": 92,
     "detection_date": "2026-08-22", "status": "Pending Verification"},
    {"id": "MG-2026-00402", "name": "Minera Escondida (Atacama)", "lat": -24.2691, "lon": -69.0722,
     "country": "Chile", "mineral": "Copper", "risk_score": 67, "risk": "MEDIUM",
     "disturbed_ha": 9.4, "lease_status": "Within Lease Boundary", "distance_m": 0,
     "ndvi_change": -0.15, "bsi_change": 0.28, "sar_delta": 3.1, "confidence": 74,
     "detection_date": "2026-08-21", "status": "Verified - Compliant"},
    {"id": "MG-2026-00415", "name": "Bushveld Igneous Complex", "lat": -25.0, "lon": 29.5,
     "country": "South Africa", "mineral": "Platinum Group", "risk_score": 72, "risk": "HIGH",
     "disturbed_ha": 11.3, "lease_status": "Expired Lease Area", "distance_m": 650,
     "ndvi_change": -0.28, "bsi_change": 0.41, "sar_delta": 3.8, "confidence": 81,
     "detection_date": "2026-08-19", "status": "Pending Verification"},
    {"id": "MG-2026-00430", "name": "Kalimantan Coal Belt", "lat": -1.5, "lon": 116.0,
     "country": "Indonesia", "mineral": "Coal", "risk_score": 88, "risk": "CRITICAL",
     "disturbed_ha": 31.2, "lease_status": "Protected Forest Zone", "distance_m": 0,
     "ndvi_change": -0.55, "bsi_change": 0.71, "sar_delta": 6.2, "confidence": 94,
     "detection_date": "2026-08-17", "status": "Pending Verification"},
    {"id": "MG-2026-00445", "name": "Sudbury Basin Nickel Mine", "lat": 46.49, "lon": -81.0,
     "country": "Canada", "mineral": "Nickel", "risk_score": 35, "risk": "LOW",
     "disturbed_ha": 4.1, "lease_status": "Active Lease - Compliant", "distance_m": 0,
     "ndvi_change": -0.08, "bsi_change": 0.12, "sar_delta": 1.5, "confidence": 62,
     "detection_date": "2026-08-15", "status": "Verified - Compliant"},
    {"id": "MG-2026-00460", "name": "Nevada Gold Corridor", "lat": 40.8, "lon": -117.5,
     "country": "USA", "mineral": "Gold", "risk_score": 54, "risk": "MEDIUM",
     "disturbed_ha": 7.8, "lease_status": "Federal Land - Unauthorized", "distance_m": 1200,
     "ndvi_change": -0.19, "bsi_change": 0.33, "sar_delta": 2.8, "confidence": 71,
     "detection_date": "2026-08-16", "status": "Under Review"},
]

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛰️ Navigation")
    page = st.radio(
        "Go to",
        ["📊 Dashboard", "🗺️ Risk Map", "🚨 Alerts", "📡 Satellite Analysis",
         "⛏️ Mining Leases", "🤖 AI Models", "📋 Field Verification",
         "📈 Reports", "🔧 Settings"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown(f'<span class="demo-badge">DEMO DATA</span> <small>Sample demonstration data</small>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Illegal Mining Detection by Using Satellite Data")
    st.caption("AI-Powered Surveillance System v2.0")

# ─────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────
def risk_color(risk):
    return {"CRITICAL": "#ef4444", "HIGH": "#f97316", "MEDIUM": "#eab308", "LOW": "#22c55e"}.get(risk, "#64748b")

def risk_icon(risk):
    return {"CRITICAL": "⛔", "HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(risk, "⚪")

# ─────────────────────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────────────────────
if page == "📊 Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>🛰️ Illegal Mining Detection by Using Satellite Data</h1>
        <p>AI-Powered Satellite Mining Surveillance, Change Detection & Early-Warning System</p>
    </div>
    """, unsafe_allow_html=True)

    # KPI Cards
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("🌍 Monitored Areas", "128")
    c2.metric("🚨 Active Alerts", "24")
    c3.metric("⚠️ High Risk", "8")
    c4.metric("📐 Disturbed Area", "184.6 ha")
    c5.metric("✅ Verified", "11")
    c6.metric("⏳ Pending", "13")

    st.markdown("---")

    # Charts Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Risk Distribution")
        risk_df = pd.DataFrame({
            "Risk Level": ["Critical", "High", "Medium", "Low"],
            "Count": [3, 8, 6, 7]
        })
        fig = px.pie(risk_df, values="Count", names="Risk Level",
                     color="Risk Level",
                     color_discrete_map={"Critical": "#ef4444", "High": "#f97316",
                                         "Medium": "#eab308", "Low": "#22c55e"},
                     hole=0.5)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="white", height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Alerts Over Time")
        dates = pd.date_range(end=datetime.now(), periods=30, freq="D")
        alerts_ts = pd.DataFrame({
            "Date": dates,
            "Alerts": np.random.poisson(lam=4, size=30)
        })
        fig = px.area(alerts_ts, x="Date", y="Alerts",
                      color_discrete_sequence=["#38bdf8"])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="white", height=350)
        st.plotly_chart(fig, use_container_width=True)

    # Charts Row 2
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Land Disturbance Trend (ha)")
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"]
        disturbance = [45.2, 52.1, 61.8, 78.3, 95.4, 120.7, 155.2, 184.6]
        fig = px.line(x=months, y=disturbance, markers=True,
                      color_discrete_sequence=["#f97316"])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="white", height=350, xaxis_title="Month", yaxis_title="Hectares")
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("Mining Activity by Country")
        country_df = pd.DataFrame({
            "Country": [s["country"] for s in MINING_SITES],
            "Risk Score": [s["risk_score"] for s in MINING_SITES]
        })
        fig = px.bar(country_df, x="Country", y="Risk Score",
                     color="Risk Score",
                     color_continuous_scale=["#22c55e", "#eab308", "#f97316", "#ef4444"])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="white", height=350)
        st.plotly_chart(fig, use_container_width=True)

    # Verification Status
    st.subheader("Verification Status")
    vc1, vc2, vc3, vc4 = st.columns(4)
    statuses = [s["status"] for s in MINING_SITES]
    vc1.metric("Pending", statuses.count("Pending Verification"))
    vc2.metric("Under Review", statuses.count("Under Review"))
    vc3.metric("Verified Compliant", statuses.count("Verified - Compliant"))
    vc4.metric("Confirmed Illegal", "0")


# ─────────────────────────────────────────────────────────────
# PAGE: RISK MAP
# ─────────────────────────────────────────────────────────────
elif page == "🗺️ Risk Map":
    st.markdown("""
    <div class="main-header">
        <h1>🗺️ Global Risk Map</h1>
        <p>Interactive GIS surveillance map with mining disturbance zones worldwide</p>
    </div>
    """, unsafe_allow_html=True)

    # Filters
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        risk_filter = st.multiselect("Risk Level", ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
                                     default=["CRITICAL", "HIGH", "MEDIUM", "LOW"])
    with fc2:
        country_filter = st.multiselect("Country", list(set(s["country"] for s in MINING_SITES)),
                                        default=list(set(s["country"] for s in MINING_SITES)))
    with fc3:
        mineral_filter = st.multiselect("Mineral", list(set(s["mineral"] for s in MINING_SITES)),
                                        default=list(set(s["mineral"] for s in MINING_SITES)))

    filtered = [s for s in MINING_SITES
                if s["risk"] in risk_filter and s["country"] in country_filter and s["mineral"] in mineral_filter]

    # Map
    m = folium.Map(location=[15, 30], zoom_start=2, tiles="CartoDB dark_matter")

    for site in filtered:
        color = risk_color(site["risk"])
        popup_html = f"""
        <div style="width:280px;font-family:sans-serif;">
            <h4 style="margin:0;color:{color};">Alert {site['id']}</h4>
            <hr style="margin:4px 0;">
            <b>📍 {site['name']}</b><br>
            <b>🌍 {site['country']}</b><br><br>
            <table style="width:100%;font-size:12px;">
                <tr><td>Risk Score</td><td><b style="color:{color};">{site['risk_score']}/100</b></td></tr>
                <tr><td>Priority</td><td><b style="color:{color};">{site['risk']}</b></td></tr>
                <tr><td>Disturbed Area</td><td>{site['disturbed_ha']} ha</td></tr>
                <tr><td>Lease Status</td><td>{site['lease_status']}</td></tr>
                <tr><td>Distance</td><td>{site['distance_m']} m</td></tr>
                <tr><td>NDVI Change</td><td>{site['ndvi_change']}</td></tr>
                <tr><td>BSI Change</td><td>+{site['bsi_change']}</td></tr>
                <tr><td>SAR Δ</td><td>{site['sar_delta']} dB</td></tr>
                <tr><td>Confidence</td><td>{site['confidence']}%</td></tr>
                <tr><td>Detected</td><td>{site['detection_date']}</td></tr>
                <tr><td>Status</td><td>{site['status']}</td></tr>
            </table>
        </div>
        """
        # Add 500m buffer circle
        folium.Circle(
            location=[site["lat"], site["lon"]],
            radius=5000,  # visual scale for world map
            color=color, fill=True, fill_color=color, fill_opacity=0.15,
            weight=1
        ).add_to(m)

        folium.CircleMarker(
            location=[site["lat"], site["lon"]],
            radius=max(8, site["risk_score"] / 8),
            color=color, fill=True, fill_color=color, fill_opacity=0.8,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{site['name']} — Risk: {site['risk_score']}/100"
        ).add_to(m)

    st_folium(m, width=None, height=600, use_container_width=True)

    # Summary table
    st.subheader("Detected Sites Summary")
    df = pd.DataFrame(filtered)[["id", "name", "country", "mineral", "risk_score", "risk",
                                   "disturbed_ha", "lease_status", "confidence", "status"]]
    df.columns = ["Alert ID", "Location", "Country", "Mineral", "Risk Score", "Risk",
                  "Disturbed (ha)", "Lease Status", "Confidence %", "Status"]
    st.dataframe(df, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────
# PAGE: ALERTS
# ─────────────────────────────────────────────────────────────
elif page == "🚨 Alerts":
    st.markdown("""
    <div class="main-header">
        <h1>🚨 Alert Management</h1>
        <p>AI-generated mining disturbance alerts with explainable risk dossiers</p>
    </div>
    """, unsafe_allow_html=True)

    sorted_sites = sorted(MINING_SITES, key=lambda x: x["risk_score"], reverse=True)

    for site in sorted_sites:
        color = risk_color(site["risk"])
        with st.expander(f"{risk_icon(site['risk'])} {site['id']} — {site['name']} ({site['country']}) — Risk: {site['risk_score']}/100"):
            ac1, ac2, ac3 = st.columns(3)
            ac1.metric("Risk Score", f"{site['risk_score']}/100")
            ac2.metric("Disturbed Area", f"{site['disturbed_ha']} ha")
            ac3.metric("Confidence", f"{site['confidence']}%")

            st.markdown("#### Spectral Evidence")
            ec1, ec2, ec3, ec4 = st.columns(4)
            ec1.metric("NDVI Change", f"{site['ndvi_change']}", delta=f"{site['ndvi_change']}")
            ec2.metric("BSI Change", f"+{site['bsi_change']}", delta=f"+{site['bsi_change']}", delta_color="inverse")
            ec3.metric("SAR Δ (dB)", f"{site['sar_delta']}")
            ec4.metric("Distance from Lease", f"{site['distance_m']} m")

            st.markdown(f"**Lease Status:** {site['lease_status']}")
            st.markdown(f"**Detection Date:** {site['detection_date']}")
            st.markdown(f"**Verification Status:** {site['status']}")

            st.markdown("#### Risk Factor Breakdown")
            factors = {
                "Vegetation Loss (NDVI)": min(abs(site['ndvi_change']) * 100, 20),
                "Bare Soil Gain (BSI)": min(site['bsi_change'] * 25, 20),
                "SAR Roughness Δ": min(site['sar_delta'] * 3, 15),
                "Lease Boundary Violation": 20 if "Outside" in site['lease_status'] or "Expired" in site['lease_status'] else 5,
                "Disturbed Area Scale": min(site['disturbed_ha'] * 1.2, 15),
                "Historical Pattern": np.random.uniform(3, 10),
                "Proximity to Protected Zone": np.random.uniform(2, 8),
            }
            fig = px.bar(x=list(factors.values()), y=list(factors.keys()), orientation="h",
                         color=list(factors.values()),
                         color_continuous_scale=["#22c55e", "#eab308", "#ef4444"])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font_color="white", height=300, showlegend=False,
                              xaxis_title="Score Contribution", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# PAGE: SATELLITE ANALYSIS
# ─────────────────────────────────────────────────────────────
elif page == "📡 Satellite Analysis":
    st.markdown("""
    <div class="main-header">
        <h1>📡 Satellite Data Analysis</h1>
        <p>Multi-sensor temporal analysis — Sentinel-2 Optical + Sentinel-1 SAR</p>
    </div>
    """, unsafe_allow_html=True)

    selected = st.selectbox("Select Site", [s["name"] for s in MINING_SITES])
    site = next(s for s in MINING_SITES if s["name"] == selected)

    st.markdown("### Temporal Spectral Index Timeline")

    years = [2022, 2023, 2024, 2025, 2026]
    base_ndvi = 0.68
    ndvi_vals = [base_ndvi + site["ndvi_change"] * (i / 4) for i in range(5)]
    bsi_vals = [-0.22 + site["bsi_change"] * (i / 4) for i in range(5)]
    ndwi_vals = [-0.12 - 0.05 * i for i in range(5)]

    timeline_df = pd.DataFrame({
        "Year": years * 3,
        "Value": ndvi_vals + bsi_vals + ndwi_vals,
        "Index": ["NDVI"] * 5 + ["BSI"] * 5 + ["NDWI"] * 5
    })

    fig = px.line(timeline_df, x="Year", y="Value", color="Index", markers=True,
                  color_discrete_map={"NDVI": "#22c55e", "BSI": "#f97316", "NDWI": "#3b82f6"})
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="white", height=400)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### SAR Radar Backscatter Timeline")
    sar_vv = [-14.8 + site["sar_delta"] * (i / 4) for i in range(5)]
    sar_vh = [-21.4 + (site["sar_delta"] * 0.8) * (i / 4) for i in range(5)]
    sar_df = pd.DataFrame({
        "Year": years * 2,
        "Backscatter (dB)": sar_vv + sar_vh,
        "Polarization": ["VV"] * 5 + ["VH"] * 5
    })
    fig = px.line(sar_df, x="Year", y="Backscatter (dB)", color="Polarization", markers=True,
                  color_discrete_map={"VV": "#a855f7", "VH": "#06b6d4"})
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="white", height=350)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Band Values (Latest Observation)")
    bands = {"B02": 0.14, "B03": 0.18, "B04": 0.26, "B08": 0.15, "B11": 0.38, "B12": 0.32}
    fig = px.bar(x=list(bands.keys()), y=list(bands.values()),
                 color_discrete_sequence=["#38bdf8"])
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="white", height=300, xaxis_title="Sentinel-2 Band", yaxis_title="Reflectance")
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# PAGE: MINING LEASES
# ─────────────────────────────────────────────────────────────
elif page == "⛏️ Mining Leases":
    st.markdown("""
    <div class="main-header">
        <h1>⛏️ Mining Lease Explorer</h1>
        <p>Global mining lease boundaries and compliance monitoring</p>
    </div>
    """, unsafe_allow_html=True)

    df = pd.DataFrame(MINING_SITES)[["id", "name", "country", "mineral", "lease_status",
                                      "distance_m", "disturbed_ha", "risk_score", "status"]]
    df.columns = ["Alert ID", "Site", "Country", "Mineral", "Lease Status",
                  "Distance (m)", "Disturbed (ha)", "Risk", "Verification"]

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("### Lease Compliance Overview")
    lease_cats = df["Lease Status"].value_counts()
    fig = px.pie(values=lease_cats.values, names=lease_cats.index, hole=0.4,
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="white", height=400)
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# PAGE: AI MODELS
# ─────────────────────────────────────────────────────────────
elif page == "🤖 AI Models":
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI/ML Model Architecture</h1>
        <p>Deep learning models powering mining disturbance detection</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Model Pipeline")
    st.markdown("""
    ```
    Sentinel-2 L2A (Optical BOA)  ──┐
                                     ├──► Temporal Feature     ──► Siamese CNN      ──► Change Map
    Sentinel-1 GRD (SAR Radar)   ──┘     Extraction               Change Detection
                                                                        │
                                                                        ▼
                                                                   U-Net Segmentation ──► Mining Pit /
                                                                        │                  Overburden /
                                                                        ▼                  Vegetation Loss
                                                                   Risk Engine (0-100)
                                                                        │
                                                                        ▼
                                                                   Explainable Alert Dossier
    ```
    """)

    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.markdown("#### 🔄 Siamese Change Detection")
        st.markdown("""
        - **Architecture:** Siamese CNN with shared weights
        - **Input:** Bi-temporal 6-band composites (B2,B3,B4,B8,B11,B12)
        - **Output:** Pixel-level change probability map
        - **Training:** Contrastive loss on mining change pairs
        """)

    with mc2:
        st.markdown("#### 🎯 U-Net Segmentation")
        st.markdown("""
        - **Architecture:** U-Net with ResNet-34 encoder
        - **Classes:** Mining pit, overburden dump, vegetation clearance, haul road, water body
        - **Input:** 12-band Sentinel-2 + 2-band SAR
        - **Loss:** Dice + Focal loss combination
        """)

    with mc3:
        st.markdown("#### 📊 Risk Scoring Engine")
        st.markdown("""
        - **Method:** Weighted 7-factor normalized scoring
        - **Factors:** NDVI drop, BSI gain, SAR Δ, area scale, lease violation, proximity, history
        - **Output:** Explainable score 0-100
        - **Thresholds:** LOW <40, MEDIUM 40-65, HIGH 65-85, CRITICAL >85
        """)

    st.markdown("### Spectral Index Formulas")
    st.latex(r"NDVI = \frac{B08 - B04}{B08 + B04}")
    st.latex(r"NDWI = \frac{B03 - B08}{B03 + B08}")
    st.latex(r"NDBI = \frac{B11 - B08}{B11 + B08}")
    st.latex(r"BSI = \frac{(B11 + B04) - (B08 + B02)}{(B11 + B04) + (B08 + B02)}")


# ─────────────────────────────────────────────────────────────
# PAGE: FIELD VERIFICATION
# ─────────────────────────────────────────────────────────────
elif page == "📋 Field Verification":
    st.markdown("""
    <div class="main-header">
        <h1>📋 Field Verification Portal</h1>
        <p>Human-in-the-loop ground truth validation for AI-generated alerts</p>
    </div>
    """, unsafe_allow_html=True)

    pending = [s for s in MINING_SITES if s["status"] == "Pending Verification"]

    if pending:
        selected_alert = st.selectbox("Select Alert for Verification",
                                       [f"{s['id']} — {s['name']}" for s in pending])
        alert = next(s for s in pending if s["id"] in selected_alert)

        st.markdown(f"### Alert: {alert['id']}")
        vc1, vc2, vc3 = st.columns(3)
        vc1.metric("Risk Score", f"{alert['risk_score']}/100")
        vc2.metric("Location", alert['name'])
        vc3.metric("Disturbed Area", f"{alert['disturbed_ha']} ha")

        with st.form("verification_form"):
            st.markdown("#### Field Inspector Report")
            inspector = st.text_input("Inspector Name")
            verdict = st.selectbox("Verification Verdict",
                                   ["Confirmed - Illegal Mining", "Confirmed - Legal Activity",
                                    "Inconclusive - Requires Further Investigation", "False Positive"])
            ground_area = st.number_input("Ground-Measured Area (ha)", min_value=0.0, value=float(alert['disturbed_ha']))
            notes = st.text_area("Field Observations")
            gps_coords = st.text_input("DGPS Coordinates", value=f"{alert['lat']}, {alert['lon']}")
            photos = st.file_uploader("Upload Field Photos", type=["jpg", "png"], accept_multiple_files=True)

            submitted = st.form_submit_button("Submit Verification Report", type="primary")
            if submitted:
                st.success(f"✅ Verification report for {alert['id']} submitted successfully!")
                st.balloons()


# ─────────────────────────────────────────────────────────────
# PAGE: REPORTS
# ─────────────────────────────────────────────────────────────
elif page == "📈 Reports":
    st.markdown("""
    <div class="main-header">
        <h1>📈 Analysis Reports</h1>
        <p>Comprehensive mining surveillance intelligence reports</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Global Mining Surveillance Summary")

    rc1, rc2, rc3, rc4 = st.columns(4)
    rc1.metric("Total Sites Monitored", len(MINING_SITES))
    rc2.metric("Countries Covered", len(set(s["country"] for s in MINING_SITES)))
    rc3.metric("Total Disturbed Area", f"{sum(s['disturbed_ha'] for s in MINING_SITES):.1f} ha")
    rc4.metric("Avg Risk Score", f"{np.mean([s['risk_score'] for s in MINING_SITES]):.0f}/100")

    st.markdown("### Risk Score Distribution")
    risk_scores = [s["risk_score"] for s in MINING_SITES]
    fig = px.histogram(x=risk_scores, nbins=10, color_discrete_sequence=["#38bdf8"],
                       labels={"x": "Risk Score", "y": "Count"})
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="white", height=350)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Mineral-wise Risk Analysis")
    mineral_df = pd.DataFrame(MINING_SITES)
    fig = px.box(mineral_df, x="mineral", y="risk_score",
                 color="mineral", points="all")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="white", height=400, xaxis_title="Mineral", yaxis_title="Risk Score")
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# PAGE: SETTINGS
# ─────────────────────────────────────────────────────────────
elif page == "🔧 Settings":
    st.markdown("""
    <div class="main-header">
        <h1>🔧 System Settings</h1>
        <p>Configuration for satellite data sources and AI pipeline</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Data Source Configuration")
    st.markdown("#### Copernicus Data Space Ecosystem (CDSE)")
    cdse_id = st.text_input("COPERNICUS_CLIENT_ID", type="password", placeholder="Enter your CDSE client ID")
    cdse_secret = st.text_input("COPERNICUS_CLIENT_SECRET", type="password", placeholder="Enter your CDSE client secret")

    st.markdown("#### Sentinel Hub")
    sh_id = st.text_input("SENTINEL_HUB_CLIENT_ID", type="password", placeholder="Enter Sentinel Hub client ID")
    sh_secret = st.text_input("SENTINEL_HUB_CLIENT_SECRET", type="password", placeholder="Enter Sentinel Hub client secret")

    st.markdown("### Processing Settings")
    pc1, pc2 = st.columns(2)
    with pc1:
        max_cloud = st.slider("Max Cloud Coverage (%)", 0, 100, 30)
        temporal_window = st.number_input("Temporal Window (days)", 30, 365, 90)
    with pc2:
        risk_threshold = st.slider("Alert Risk Threshold", 0, 100, 65)
        buffer_m = st.number_input("Surveillance Buffer (m)", 100, 2000, 500)

    st.markdown("### System Architecture")
    st.markdown("""
    ```
    ┌──────────────────────────────────────────────────────────────┐
    │                    FRONTEND (React/Streamlit)                │
    │   Dashboard │ Risk Map │ Alerts │ Satellite │ Verification  │
    ├──────────────────────────────────────────────────────────────┤
    │                    BACKEND (FastAPI/Python)                  │
    │   REST API │ Auth │ Satellite Services │ AI Pipeline        │
    ├──────────────────────────────────────────────────────────────┤
    │                    AI/ML ENGINE                              │
    │   Siamese CNN │ U-Net │ Risk Scoring │ Change Detection     │
    ├──────────────────────────────────────────────────────────────┤
    │                    DATA SOURCES                              │
    │   Copernicus CDSE │ Sentinel-1 SAR │ Sentinel-2 Optical     │
    └──────────────────────────────────────────────────────────────┘
    ```
    """)

    if st.button("Save Settings", type="primary"):
        st.success("✅ Settings saved successfully!")
