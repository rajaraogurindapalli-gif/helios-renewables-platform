"""
Helios Industrial Reliability Agent - Streamlit Copilot UI
Includes ReAct Diagnostics, Episodic Memory, Shift Briefings, RAG Corpus, and Predictive Horizon Modeling.
"""

import sys
import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import streamlit as st
import pandas as pd
from src.agent.helios_agent import HeliosReliabilityAgent, DOMAIN_KNOWLEDGE_BASE
from src.agent.predictor import FleetPredictor

st.set_page_config(
    page_title="Helios Reliability Copilot",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_PATH = "/content/fact_inverter_telemetry_prod.csv"
if not os.path.exists(DATA_PATH):
    DATA_PATH = "fact_inverter_telemetry_prod.csv"

@st.cache_resource
def get_agent():
    return HeliosReliabilityAgent(DATA_PATH)

agent = get_agent()
df = agent.df

# --- SIDEBAR ---
st.sidebar.title("⚡ Helios Fleet Copilot")
st.sidebar.caption("Autonomous Reliability & Industrial RAG Agent")

fleet_inverters = df["Inverter Id"].unique().tolist()
selected_inv = st.sidebar.selectbox(
    "Select Target Asset:", 
    fleet_inverters, 
    index=fleet_inverters.index("INV-04") if "INV-04" in fleet_inverters else 0
)

st.sidebar.divider()
st.sidebar.subheader("Fleet Health Scan")
flagged_assets = agent.run_fleet_scan()

if flagged_assets:
    st.sidebar.error(f"⚠️ Action Required on: {', '.join(flagged_assets)}")
else:
    st.sidebar.success("✓ All fleet inverters operating nominally.")

st.sidebar.divider()
st.sidebar.markdown("**Active Knowledge Base (RAG):**")
for doc in DOMAIN_KNOWLEDGE_BASE:
    st.sidebar.caption(f"• `{doc['id']}`: {doc['topic']}")

# --- MAIN HEADER ---
st.title(f"⚡ Asset Reliability Copilot: {selected_inv}")
st.markdown("**Plant:** `HELIOS_SOLAR_PLANT_01` | **Capacity:** `2.5 MW` | **Mode:** `Production Conformed`")

asset_records = df[df["Inverter Id"] == selected_inv].sort_values("Timestamp Hour")
peak_temp = asset_records["Avg Heatsink Temp C"].max()
daylight_pr = asset_records[asset_records["Irradiation W M2"] > 100]["Avg Avg Performance Ratio Pct"].mean()
total_anomalies = int(asset_records["Is Anomaly"].sum())
total_loss_kw = asset_records["Temp Derate Loss Kw"].sum()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.subheader(f"{peak_temp:.1f} °C")
    st.caption("Peak Heatsink Temp (Limit: 75°C)")
with col2:
    st.subheader(f"{daylight_pr:.1f} %")
    st.caption("Daylight Mean PR")
with col3:
    st.subheader(f"{total_anomalies} hrs")
    st.caption("Anomaly Duration")
with col4:
    st.subheader(f"{total_loss_kw:.1f} kWh")
    st.caption("Thermal Derate Loss")

st.divider()

# --- TABS INCLUDING PREDICTIONS ---
tab_diag, tab_pred, tab_memory, tab_handover, tab_rag, tab_telemetry = st.tabs([
    "🤖 ReAct Diagnostics", 
    "🔮 Predictive Horizons",
    "🧠 Asset Memory & CMMS", 
    "📋 Shift Handover Briefing", 
    "📚 Industrial RAG Corpus", 
    "📊 Raw Telemetry"
])

with tab_diag:
    st.subheader("Autonomous ReAct Diagnostic Loop")
    if st.button("Run Diagnostic & Dispatch Evaluation", type="primary"):
        with st.spinner(f"Agent executing diagnostic reasoning on {selected_inv}..."):
            work_order = agent.diagnose_and_dispatch(selected_inv)
            if work_order.get("status") == "NOMINAL":
                st.success(work_order["message"])
            else:
                st.error(f"🚨 **ANOMALY CONFIRMED: {work_order['priority']} WORK ORDER GENERATED**")
                wo_col1, wo_col2 = st.columns([2, 1])
                with wo_col1:
                    st.markdown(f"### Ticket: `{work_order['work_order_id']}`")
                    st.markdown("**Root Cause Diagnosis:**")
                    st.info(work_order["root_cause_diagnosis"])
                    st.markdown("**Prescribed Field SOP Actions:**")
                    for step in work_order["prescribed_field_sop"]:
                        st.markdown(f"- {step}")
                with wo_col2:
                    st.markdown("### Financial Exposure")
                    loss_metrics = work_order["estimated_financial_loss"]
                    st.markdown(f"## **${loss_metrics['total_financial_exposure_usd']}**")
                    st.write(f"• **Energy Shortfall:** {loss_metrics['lost_generation_kwh']} kWh")
                    st.write(f"• **Base Revenue Loss:** ${loss_metrics['revenue_loss_usd']}")
                    st.write(f"• **Grid Deviation Penalty:** ${loss_metrics['grid_deviation_penalty_usd']}")

with tab_pred:
    st.subheader(f"🔮 Predictive Asset Horizons: {selected_inv}")
    
    # 1. Thermal Runaway Projection
    pred_res = FleetPredictor.predict_thermal_runaway(df, selected_inv)
    p_col1, p_col2, p_col3 = st.columns(3)
    p_col1.metric("Thermal Drift Velocity", f"{pred_res['thermal_velocity_c_per_hr']} °C/hr")
    p_col2.metric("Time to Critical Trip (85°C)", f"{pred_res['projected_time_to_critical_trip_hrs']}")
    p_col3.metric("Predictive Urgency", f"{pred_res['predictive_urgency']}")
    
    st.info(f"**Proactive Dispatch Strategy:** {pred_res['proactive_curtailment_recommendation']}")
    
    st.divider()
    # 2. 24-Hour Day-Ahead Generation Forecast
    st.subheader("24-Hour Day-Ahead Solar Yield & PPA Grid Commitment Forecast")
    st.caption("GBDT model prediction calibrated to 0.56% WAPE against contractual day-ahead injection schedule.")
    forecast_df = FleetPredictor.forecast_next_24h_yield()
    
    chart_data = forecast_df.set_index("Hour")[["Forecast_Generation_MW", "Grid_Commitment_PPA_MW"]]
    st.line_chart(chart_data)
    
    with st.expander("Inspect Day-Ahead Dispatch Schedule (Hourly MW)"):
        st.dataframe(forecast_df, use_container_width=True)

with tab_memory:
    st.subheader(f"Episodic Maintenance History: {selected_inv}")
    history = agent.memory.get_asset_history(selected_inv)
    if not history:
        st.info(f"No previous maintenance tickets logged for {selected_inv}.")
    else:
        for item in reversed(history):
            with st.expander(f"Ticket: {item['work_order_id']} | Status: {item['status']} | Logged: {item['logged_at']}"):
                st.write(f"**Priority:** {item['priority']}")
                st.write(f"**Financial Exposure:** ${item.get('financial_exposure_usd', 0.0)}")
                if item["status"] == "OPEN":
                    notes = st.text_input(f"Technician Notes ({item['work_order_id']}):", key=item['work_order_id'])
                    if st.button("Mark Resolved", key=f"btn_{item['work_order_id']}"):
                        agent.memory.resolve_work_order(selected_inv, item['work_order_id'], notes)
                        st.success("Work order resolved.")
                        st.rerun()
                else:
                    st.success(f"✓ Resolved at {item['closed_at']}")
                    st.write(f"**Field Action Notes:** {item['resolution_notes']}")

with tab_handover:
    st.subheader("Shift Supervisor Handover Memo Generator")
    all_history = agent.memory._read_store()
    open_count = sum(1 for inv_list in all_history.values() for item in inv_list if item.get("status") == "OPEN")
    memo = agent.analytics.generate_shift_handover_text(df, open_orders_count=open_count)
    st.markdown(memo)
    st.download_button(
        label="Download Shift Briefing (.txt)",
        data=memo,
        file_name="Helios_Shift_Handover.txt",
        mime="text/plain"
    )

with tab_rag:
    st.subheader("RAG Domain Knowledge Index")
    search_query = st.text_input("Test Knowledge Search:", value="heatsink")
    if search_query:
        hits = agent.tools.retrieve_domain_guidelines([search_query])
        for hit in hits:
            with st.expander(f"📄 {hit['doc_id']} — {hit['topic']}", expanded=True):
                st.write(hit['content'])

with tab_telemetry:
    st.subheader(f"Hourly Telemetry Stream: {selected_inv}")
    st.dataframe(
        asset_records[[
            "Timestamp Hour", "Irradiation W M2", "Ambient Temp C", 
            "Module Temp C", "Avg Heatsink Temp C", "Avg Ac Power Kw", 
            "Avg Avg Performance Ratio Pct", "Reconstruction Loss Mse", "Is Anomaly", "Primary Fault Code"
        ]],
        use_container_width=True
    )
