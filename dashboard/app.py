from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="SILENT SHIFT | SOC",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@400;500;600;700&display=swap');
    :root {
        --display-font: 'DM Serif Display', Georgia, 'Times New Roman', serif;
        --ui-font: Inter, Manrope, 'Segoe UI', Arial, sans-serif;
    }
    .stApp { background: #ffffff; color: #202938; font-family: var(--ui-font); }
    [data-testid="stHeader"] { display: none; }
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stMainBlockContainer"] {
        box-sizing: border-box; width: calc(100% - 250px); max-width: none;
        margin-left: 250px; padding: 24px 2.6rem 3rem;
    }
    [data-testid="stMainBlockContainer"] .element-container:has(style),
    [data-testid="stMainBlockContainer"] .element-container:has(.custom-sidebar) {
        display: contents;
    }
    [data-testid="stMainBlockContainer"] .element-container:has(.hero-brand) {
        margin-top: -32px;
    }
    .custom-sidebar {
        position: fixed; inset: 0 auto 0 0; z-index: 1000; width: 250px;
        box-sizing: border-box; display: flex; flex-direction: column;
        padding: 30px 24px 24px; background: #ffffff;
        border-right: 1px solid #e6eaf0; font-family: var(--ui-font);
    }
    .custom-sidebar p { margin: 0; }
    .custom-brand { flex: 0 0 auto; }
    .custom-logo { width: 48px; height: 48px; margin: 0 0 13px; overflow: visible; }
    .custom-logo .brand-mark { width: 48px; height: 48px; overflow: visible; color: #3975d0; border-color: #3975d0; line-height: 1; }
    .custom-brand-name { color: #172033; font-family: var(--display-font); font-size: 1.2rem; letter-spacing: .08em; line-height: 1.1; }
    .custom-brand-subtitle { color: #68758a; font-size: .73rem; margin-top: 6px; }
    .custom-nav-section { flex: 0 0 auto; margin-top: 38px; }
    .custom-nav-label, .custom-system-label {
        color: #8a96a8; font-size: .66rem; font-weight: 800;
        letter-spacing: .11em; margin: 0 0 12px;
    }
    .custom-nav { display: flex; flex-direction: column; gap: 4px; }
    .custom-nav a {
        display: flex; align-items: center; gap: 11px; min-height: 40px;
        box-sizing: border-box; padding: 10px 11px; border-radius: 9px;
        color: #536075; font-size: .82rem; font-weight: 600;
        text-decoration: none; transition: background .15s ease, color .15s ease;
    }
    .custom-nav a:hover, .custom-nav a.active { background: #edf4ff; color: #245fc2; }
    .custom-nav-icon { width: 17px; height: 17px; flex: 0 0 17px; display: inline-flex; }
    .custom-nav-icon svg { width: 100%; height: 100%; stroke: currentColor; fill: none; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
    .custom-spacer { flex: 1 1 auto; min-height: 32px; }
    .custom-system { flex: 0 0 auto; border-top: 1px solid #e6eaf0; padding-top: 15px; }
    .custom-stat { color: #7a8799; font-size: .68rem; padding: 0 0 9px; }
    .custom-stat strong { color: #202938; display: block; font-size: .9rem; font-weight: 600; margin-top: 4px; }
    .custom-sidebar-footer { flex: 0 0 auto; border-top: 1px solid #e6eaf0; margin-top: 3px; padding-top: 12px; color: #7a8799; font-family: var(--display-font); font-size: .76rem; line-height: 1.4; }
    @media (max-width: 850px) {
        .custom-sidebar { width: 220px; padding: 20px 18px 12px; }
        .custom-logo, .custom-logo .brand-mark { width: 42px; height: 42px; }
        .custom-logo { margin-bottom: 9px; }
        .custom-nav-section { margin-top: 24px; }
        .custom-nav a { min-height: 34px; padding: 7px 10px; }
        .custom-system { padding-top: 10px; }
        .custom-stat { padding-bottom: 5px; }
        .custom-sidebar-footer { padding-top: 8px; }
        [data-testid="stMainBlockContainer"] {
            width: calc(100% - 220px); margin-left: 220px;
            padding-left: 1.3rem; padding-right: 1.3rem;
        }
    }
    h1, h2, h3 { color: #172033 !important; font-family: var(--display-font); font-weight: 400 !important; letter-spacing: .015em; }
    h1 { font-size: 2.25rem !important; margin-bottom: 0.1rem !important; }
    h2 { font-size: 1.5rem !important; margin-top: 0.4rem !important; }
    h3 { font-size: 1.2rem !important; }
    p, label, button, input, textarea, [data-testid="stDataFrame"], [data-testid="stMetric"] {
        font-family: var(--ui-font);
    }
    .subtitle { color: #69758b; margin-bottom: 1rem; }
    .eyebrow { color: #71809a; font-size: .72rem; font-weight: 800; letter-spacing: .08em; word-break: keep-all; overflow-wrap: normal; }
    .card { background: #fff; border: 1px solid #e2e7f0; border-radius: 10px; padding: 16px 18px; box-shadow: 0 2px 10px rgba(22, 35, 61, .035); }
    .card-title { color: #344159; font-size: .86rem; font-weight: 800; margin-bottom: 10px; }
    .kpi { height: 152px; min-height: 152px; box-sizing: border-box; }
    .kpi-icon { width: 18px; height: 18px; display: inline-flex; align-items: center; justify-content: center; color: #3975d0; margin-bottom: 8px; }
    .kpi-icon svg, .section-icon svg { width: 100%; height: 100%; stroke: currentColor; fill: none; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
    .kpi-icon.high-icon { color: #c74646; }
    .kpi-icon.medium-icon { color: #bd7a16; }
    .kpi-icon.low-icon { color: #2d8a68; }
    .kpi-value { color: #172033; font-size: 1.8rem; font-weight: 800; margin-top: 4px; white-space: nowrap; }
    .kpi-note { color: #8390a5; font-size: .75rem; margin-top: 5px; }
    .badge { display: inline-block; border-radius: 999px; padding: 3px 9px; font-size: .68rem; font-weight: 800; letter-spacing: .04em; }
    .high { color: #b42318; background: #fff0ee; }
    .medium { color: #a15c00; background: #fff6df; }
    .low { color: #16704a; background: #eaf8f1; }
    .status { color: #4e5d75; background: #eef2f7; }
    .brand-mark { width: 34px; height: 34px; border: 1px solid #2ed3c6; border-radius: 10px 10px 13px 13px; display: grid; place-items: center; color: #58e1d6; font-size: 1.05rem; font-weight: 900; position: relative; }
    .brand-mark:after { display: none; }
    .sidebar-brand { font-family: var(--display-font); font-size: 1.15rem; font-weight: 400; letter-spacing: .08em; color: #172033 !important; }
    .sidebar-subtitle { color: #68758a !important; font-size: .72rem; margin-top: -4px; }
    .sidebar-tagline { color: #77849a !important; font-size: .68rem; line-height: 1.35; margin: 13px 0 16px; }
    .sidebar-stat { border-top: 1px solid #e6eaf0; padding: 12px 0 4px; margin-top: 12px; }
    .sidebar-stat strong { display: block; color: #172033; font-size: 1.05rem; }
    .sidebar-stat span { color: #768399; font-size: .72rem; }
    .disclaimer { color: #7b879b; font-size: .75rem; border-top: 1px solid #e2e7f0; padding-top: 12px; margin-top: 24px; }
    .hero-brand { display: flex; gap: 13px; align-items: center; margin-bottom: 2px; }
    .hero-brand .brand-mark { width: 42px; height: 42px; background: #ffffff; }
    .hero-name { font-family: var(--display-font); font-size: 2.05rem; line-height: 1; font-weight: 400; letter-spacing: .055em; color: #142238; }
    .hero-subtitle { color: #5d6c83; font-size: .82rem; margin-top: 5px; }
    .hero-tagline { color: #71809a; font-family: var(--display-font); font-size: .96rem; letter-spacing: .035em; margin: 8px 0 12px; }
    .hero-supporting { color: #66748a; font-size: .78rem; line-height: 1.55; margin-bottom: 12px; }
    .section-heading { display: flex; align-items: center; gap: 7px; color: #344159; font-size: .92rem; font-weight: 800; letter-spacing: .02em; margin: 4px 0 10px; }
    .section-icon { width: 16px; height: 16px; color: #3975d0; display: inline-flex; }
    [data-testid="stDataFrame"] { border: 1px solid #e2e7f0; border-radius: 10px; }
    div[data-testid="stMetric"] { background: white; border: 1px solid #e2e7f0; border-radius: 10px; padding: 12px 15px; }
    </style>
    """,
    unsafe_allow_html=True,
)


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    summary = pd.read_csv(DATA_DIR / "final_engine_results.csv")
    events = pd.read_csv(DATA_DIR / "user_activity.csv", parse_dates=["timestamp"])
    return summary, events


summary, events = load_data()
summary["final_risk_score"] = pd.to_numeric(summary["final_risk_score"])
summary["anomaly_count"] = pd.to_numeric(summary["anomaly_count"])
summary["high_sequence_count"] = pd.to_numeric(summary["high_sequence_count"])
summary["shift_ratio"] = pd.to_numeric(summary["shift_ratio"])

if "investigation_status" not in st.session_state:
    st.session_state.investigation_status = {}
if "selected_user" not in st.session_state:
    st.session_state.selected_user = summary.sort_values("final_risk_score", ascending=False).iloc[0]["user_id"]
if "page" not in st.session_state:
    st.session_state.page = "Overview"
valid_pages = {"Overview", "Alerts", "Investigations", "Users", "Analytics"}
requested_page = st.query_params.get("page")
if requested_page in valid_pages:
    st.session_state.page = requested_page


def risk_badge(level: str) -> str:
    return f'<span class="badge {level.lower()}">{level}</span>'


def icon(name: str) -> str:
    paths = {
        "layout": '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>',
        "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
        "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
        "activity": '<polyline points="3 12 7 12 10 4 14 20 17 12 21 12"/>',
        "alert": '<path d="m10.3 3.3-8 14A2 2 0 0 0 4 20h16a2 2 0 0 0 1.7-2.7l-8-14a2 2 0 0 0-3.4 0Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
        "warning": '<path d="m10.3 3.3-8 14A2 2 0 0 0 4 20h16a2 2 0 0 0 1.7-2.7l-8-14a2 2 0 0 0-3.4 0Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
        "check": '<path d="M12 22a10 10 0 1 0-10-10"/><polyline points="22 4 12 14.01 9 11.01"/>',
        "pie": '<path d="M21 12a9 9 0 1 1-9-9v9Z"/><path d="M12 3a9 9 0 0 1 9 9h-9Z"/>',
        "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>',
        "ranking": '<path d="M4 19V5"/><path d="M4 5h10l-2 3 2 3H4"/><path d="M20 19V9"/><path d="m17 12 3-3 3 3"/>',
        "trend": '<polyline points="3 17 9 11 13 15 21 7"/><polyline points="15 7 21 7 21 13"/>',
        "timeline": '<circle cx="6" cy="6" r="2"/><circle cx="6" cy="18" r="2"/><path d="M6 8v8"/><path d="M10 6h10"/><path d="M10 18h10"/>',
        "chart": '<line x1="4" y1="19" x2="4" y2="5"/><line x1="4" y1="19" x2="20" y2="19"/><rect x="8" y="11" width="3" height="5"/><rect x="14" y="7" width="3" height="9"/>',
    }
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{paths[name]}</svg>'


def section_heading(label: str, icon_name: str) -> str:
    return f'<div class="section-heading"><span class="section-icon">{icon(icon_name)}</span>{label}</div>'


def page_header(title: str, subtitle: str) -> None:
    st.markdown(f"# {title}", unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{subtitle}</div>', unsafe_allow_html=True)


def display_table(frame: pd.DataFrame, height: int = 360) -> None:
    st.dataframe(frame, width="stretch", hide_index=True, height=height)


def user_status(user_id: str) -> str:
    return st.session_state.investigation_status.get(user_id, "New")


def navigate_to_investigation(user_id: str) -> None:
    st.session_state.selected_user = user_id
    st.session_state.page = "Investigations"
    st.rerun()


def overview() -> None:
    st.markdown(
        '<div class="hero-brand"><div class="brand-mark">S</div><div>'
        '<div class="hero-name">SILENT SHIFT</div>'
        '<div class="hero-subtitle">Behavioral Intelligence</div></div></div>'
        '<div class="hero-tagline">A Silent Shift Into The Future</div>'
        '<div class="hero-supporting">Every Threat Leaves a Behavioral Trace.<br>'
        'See the shift before it becomes an incident.</div>',
        unsafe_allow_html=True,
    )

    st.write("")
    total = summary["user_id"].nunique()
    total_events = len(events)
    counts = summary["final_risk_level"].value_counts()
    kpis = [
        ("ACCOUNTS MONITORED", total, "Behavioral coverage"),
        ("EVENTS ANALYZED", total_events, "30-day detection window"),
        ("HIGH RISK", int(counts.get("HIGH", 0)), "Requires analyst review"),
        ("MEDIUM RISK", int(counts.get("MEDIUM", 0)), "Monitor for change"),
        ("LOW RISK", int(counts.get("LOW", 0)), "Within expected range"),
    ]
    cols = st.columns(5)
    kpi_icons = ["users", "activity", "alert", "warning", "check"]
    kpi_classes = ["", "", "high-icon", "medium-icon", "low-icon"]
    for col, (label, value, note), icon_name, icon_class in zip(cols, kpis, kpi_icons, kpi_classes):
        with col:
            st.markdown(
                f'<div class="card kpi"><div class="kpi-icon {icon_class}">{icon(icon_name)}</div>'
                f'<div class="eyebrow">{label}</div>'
                f'<div class="kpi-value">{value:,}</div><div class="kpi-note">{note}</div></div>',
                unsafe_allow_html=True,
            )
    st.write("")
    left, right = st.columns([1.35, 1])
    with left:
        st.markdown(f'<div class="card">{section_heading("Priority Alerts", "alert")}', unsafe_allow_html=True)
        alerts = summary[summary["final_risk_level"].isin(["HIGH", "MEDIUM"])].sort_values(
            "final_risk_score", ascending=False
        ).head(5)
        for _, row in alerts.iterrows():
            c1, c2, c3 = st.columns([1, 1.2, .7])
            c1.markdown(risk_badge(row["final_risk_level"]), unsafe_allow_html=True)
            c2.write(f"**{row['user_id']}** · {int(row['anomaly_count'])} anomalies")
            c3.write(f"**{row['final_risk_score']:.0f}** / 100")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown(f'<div class="card">{section_heading("Risk Distribution", "pie")}', unsafe_allow_html=True)
        dist = counts.reindex(["HIGH", "MEDIUM", "LOW"]).fillna(0).astype(int)
        fig = px.pie(values=dist.values, names=dist.index, hole=.68, color=dist.index,
                     color_discrete_map={"HIGH": "#d95d5d", "MEDIUM": "#e5a43a", "LOW": "#48a87b"})
        fig.update_layout(height=220, margin=dict(l=0, r=0, t=0, b=0), showlegend=True,
                          legend=dict(orientation="h", y=-.08))
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    st.write("")
    left, right = st.columns([1.35, 1])
    with left:
        st.markdown(f'<div class="card">{section_heading("Behavioral Activity", "activity")}', unsafe_allow_html=True)
        daily = events.assign(day=events["timestamp"].dt.date).groupby("day", as_index=False).agg(
            events=("user_id", "size"), files=("files_accessed", "mean")
        )
        fig = px.area(daily, x="day", y="events", color_discrete_sequence=["#4769d8"])
        fig.update_layout(height=220, margin=dict(l=0, r=0, t=10, b=0), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown(f'<div class="card">{section_heading("Risk Factors", "shield")}', unsafe_allow_html=True)
        user_location_counts = events.groupby("user_id")["location"].nunique()
        location_change = (user_location_counts > 1).mean() * 100
        login_events = events[events["action"].eq("login")].copy()
        login_shift = (
            login_events.groupby("user_id")["timestamp"].apply(
                lambda values: values.dt.hour.max() - values.dt.hour.min()
            ).mean() if not login_events.empty else 0
        )
        factors = pd.DataFrame({
            "factor": ["File activity", "Location change", "Login time shift",
                       "Anomaly count", "Behavioral trend", "High-risk sequences"],
            "value": [summary["late_behavior"].mean(), location_change / 10, login_shift,
                      summary["anomaly_count"].mean(), (summary["trend_score"] > 0).mean() * 10,
                      summary["high_sequence_count"].mean()],
        }).sort_values("value")
        fig = px.bar(factors, x="value", y="factor", orientation="h", color_discrete_sequence=["#6c82d9"])
        fig.update_layout(height=220, margin=dict(l=0, r=0, t=10, b=0), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    st.write("")
    st.markdown(section_heading("User Risk Ranking", "ranking"), unsafe_allow_html=True)
    ranking = summary.sort_values("final_risk_score", ascending=False).head(8).copy()
    ranking["Risk Level"] = ranking["final_risk_level"].map(risk_badge)
    display_table(ranking[["user_id", "Risk Level", "final_risk_score", "anomaly_count", "shift_ratio", "high_sequence_count"]]
                  .rename(columns={"user_id": "User ID", "final_risk_score": "Risk Score", "anomaly_count": "Anomalies",
                                   "shift_ratio": "Shift Ratio", "high_sequence_count": "Sequences"}), 300)
    st.markdown('<div class="disclaimer">See the shift before it becomes an incident.</div>',
                unsafe_allow_html=True)


def alerts() -> None:
    page_header("Alerts", "Behavioral signals requiring investigation.")
    c1, c2, c3, c4, c5 = st.columns([1, 1.1, 1.2, 1, 1.1])
    with c1:
        risk = st.selectbox("Risk level", ["All", "HIGH", "MEDIUM", "LOW"])
    with c2:
        min_score = st.slider("Minimum risk score", 0, 100, 0)
    with c3:
        search = st.text_input("Search user", placeholder="e.g. U0060")
    with c4:
        status = st.selectbox("Investigation status", ["All", "New", "Under Investigation", "Monitoring", "Resolved"])
    with c5:
        context = st.selectbox("Context", ["All", "Known change", "No known change"])
    filtered = summary.copy()
    if risk != "All":
        filtered = filtered[filtered["final_risk_level"] == risk]
    filtered = filtered[filtered["final_risk_score"] >= min_score]
    if search:
        filtered = filtered[filtered["user_id"].str.contains(search.strip().upper(), na=False)]
    if status != "All":
        filtered = filtered[filtered["user_id"].map(user_status) == status]
    if context != "All":
        known = filtered["context_status"].eq("LEGITIMATE_CHANGE")
        filtered = filtered[known if context == "Known change" else ~known]
    filtered = filtered.sort_values("final_risk_score", ascending=False)
    st.caption(f"{len(filtered):,} matching accounts")
    view = filtered.copy()
    view["Severity"] = view["final_risk_level"].map(risk_badge)
    view["Status"] = view["user_id"].map(user_status).map(lambda value: f'<span class="badge status">{value}</span>')
    view["Latest Activity"] = view["user_id"].map(
        events.groupby("user_id")["timestamp"].max().dt.strftime("%d %b %H:%M")
    )
    view["Context"] = view["context_status"].map(lambda x: "Known change" if x == "LEGITIMATE_CHANGE" else "No known change")
    display_table(view[["Severity", "user_id", "final_risk_score", "anomaly_count", "shift_ratio",
                        "high_sequence_count", "Latest Activity", "Context", "Status"]].rename(columns={
                            "user_id": "User ID", "final_risk_score": "Risk Score", "anomaly_count": "Anomalies",
                            "shift_ratio": "Shift Ratio", "high_sequence_count": "Sequences"}))
    if not filtered.empty:
        selected = st.selectbox("Open account investigation", filtered["user_id"].tolist())
        if st.button("Open investigation", type="primary"):
            navigate_to_investigation(selected)


def investigations() -> None:
    page_header("Investigations", "Review evidence for a selected account without inferring intent.")
    users = summary.sort_values("final_risk_score", ascending=False)["user_id"].tolist()
    default_index = users.index(st.session_state.selected_user) if st.session_state.selected_user in users else 0
    selected = st.selectbox("Select user", users, index=default_index)
    st.session_state.selected_user = selected
    user = summary[summary["user_id"] == selected].iloc[0]
    st.markdown(f"### {selected} &nbsp; {risk_badge(user['final_risk_level'])}", unsafe_allow_html=True)
    st.caption(f"Risk score {user['final_risk_score']:.0f} / 100 · Investigation status: {user_status(selected)}")
    cols = st.columns(4)
    for col, label, value in zip(cols, ["ANOMALOUS EVENTS", "BASELINE SHIFT", "BEHAVIOR TREND", "SUSPICIOUS SEQUENCES"],
                                 [int(user["anomaly_count"]), f"{user['shift_ratio']:.1f}×",
                                  "Increasing" if user["trend_slope"] > 0 else "Stable", int(user["high_sequence_count"])]):
        col.markdown(f'<div class="card kpi"><div class="eyebrow">{label}</div><div class="kpi-value">{value}</div></div>',
                     unsafe_allow_html=True)
    st.write("")
    st.markdown("### Why this account was flagged")
    reasons = [
        f"{int(user['anomaly_count'])} anomalous event(s) detected",
        f"File activity reached {user['shift_ratio']:.1f}× baseline",
        "Behavioral deviation increased over time" if user["trend_slope"] > 0 else "No increasing trend detected",
        f"{int(user['high_sequence_count'])} suspicious sequence(s) detected",
        "Known context recorded" if user["context_status"] == "LEGITIMATE_CHANGE" else "No known legitimate context recorded",
    ]
    st.markdown("\n".join(f"- {reason}" for reason in reasons))
    chart_col, factor_col = st.columns([1.55, 1])
    user_events = events[events["user_id"] == selected].sort_values("timestamp").copy()
    user_events["day"] = (user_events["timestamp"].dt.normalize() - events["timestamp"].dt.normalize().min()).dt.days + 1
    daily = user_events.groupby("day", as_index=False)["files_accessed"].mean()
    with chart_col:
        st.markdown(section_heading("Behavioral Shift", "trend"), unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily["day"], y=daily["files_accessed"], mode="lines+markers",
                                 name="Daily activity", line=dict(color="#4769d8", width=3)))
        fig.add_hline(y=user["baseline_average"], line_dash="dash", line_color="#8b97ab", name="Baseline")
        fig.add_vrect(x0=.5, x1=15.5, fillcolor="#dbe6ff", opacity=.35, line_width=0,
                      annotation_text="BASELINE", annotation_position="top left")
        fig.add_vrect(x0=15.5, x1=30.5, fillcolor="#fff0d2", opacity=.3, line_width=0,
                      annotation_text="DETECTION", annotation_position="top right")
        fig.update_layout(height=330, margin=dict(l=0, r=0, t=15, b=0), xaxis_title="Day",
                          yaxis_title="Average files accessed", legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    with factor_col:
        st.markdown(section_heading("Risk Factors", "shield"), unsafe_allow_html=True)
        factor_df = pd.DataFrame({"Factor": ["ML anomalies", "Behavioral shift", "Trend", "Sequences"],
                                  "Score": [user["ml_score"], user["shift_score"], user["trend_score"], user["sequence_score"]]})
        fig = px.bar(factor_df.sort_values("Score"), x="Score", y="Factor", orientation="h",
                     color_discrete_sequence=["#6c82d9"])
        fig.update_layout(height=330, margin=dict(l=0, r=0, t=15, b=0), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.markdown("### Investigation status")
    st.session_state.investigation_status[selected] = st.selectbox(
        "Update status", ["New", "Under Investigation", "Monitoring", "Resolved"],
        index=["New", "Under Investigation", "Monitoring", "Resolved"].index(user_status(selected)),
        label_visibility="collapsed",
    )
    st.markdown(section_heading("Event Timeline", "timeline"), unsafe_allow_html=True)
    timeline = user_events[["timestamp", "action", "location", "files_accessed", "behaviour"]].rename(
        columns={"timestamp": "Timestamp", "action": "Action", "location": "Location",
                 "files_accessed": "Files", "behaviour": "Risk Signal"})
    display_table(timeline.tail(100), 360)


def users() -> None:
    page_header("Users", "Search and triage account-level behavioral summaries.")
    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1.1])
    with c1:
        search = st.text_input("Search user", placeholder="Search by user ID")
    with c2:
        risk = st.multiselect("Risk level", ["HIGH", "MEDIUM", "LOW"], default=["HIGH", "MEDIUM", "LOW"])
    with c3:
        score = st.slider("Risk score", 0, 100, (0, 100))
    with c4:
        context = st.selectbox("Context", ["All", "Known change", "No known change"])
    filtered = summary[summary["final_risk_level"].isin(risk) & summary["final_risk_score"].between(*score)].copy()
    if search:
        filtered = filtered[filtered["user_id"].str.contains(search.strip().upper(), na=False)]
    if context != "All":
        known = filtered["context_status"].eq("LEGITIMATE_CHANGE")
        filtered = filtered[known if context == "Known change" else ~known]
    filtered = filtered.sort_values("final_risk_score", ascending=False)
    st.caption(f"{len(filtered):,} of {len(summary):,} accounts")
    view = filtered.assign(
        Trend=filtered["trend_slope"].map(lambda value: "Increasing" if value > 0 else "Stable"),
        Context=filtered["context_status"].map(lambda value: "Known change" if value == "LEGITIMATE_CHANGE" else "No known change"),
        Status=filtered["user_id"].map(user_status),
    )
    display_table(view[["user_id", "final_risk_level", "final_risk_score", "anomaly_count", "shift_ratio",
                        "Trend", "high_sequence_count", "Context", "Status"]].rename(columns={
                            "user_id": "User ID", "final_risk_level": "Risk Level", "final_risk_score": "Risk Score",
                            "anomaly_count": "Anomalies", "shift_ratio": "Shift Ratio",
                            "high_sequence_count": "Sequences"}), 500)
    if not filtered.empty:
        selected = st.selectbox("Select account", filtered["user_id"].tolist())
        if st.button("Open selected investigation", type="primary"):
            navigate_to_investigation(selected)


def analytics() -> None:
    page_header("Analytics", "Higher-level signals across the Silent Shift detection window.")
    counts = summary["final_risk_level"].value_counts().reindex(["HIGH", "MEDIUM", "LOW"]).fillna(0)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total anomalous events", f"{summary['anomaly_count'].sum():,.0f}")
    c2.metric("Average anomalies / user", f"{summary['anomaly_count'].mean():.1f}")
    c3.metric("High-risk sequences", f"{summary['high_sequence_count'].sum():,.0f}")
    left, right = st.columns(2)
    with left:
        st.markdown(section_heading("Risk Distribution", "pie"), unsafe_allow_html=True)
        fig = px.bar(x=counts.index, y=counts.values, color=counts.index,
                     color_discrete_map={"HIGH": "#d95d5d", "MEDIUM": "#e5a43a", "LOW": "#48a87b"})
        fig.update_layout(height=300, showlegend=False, xaxis_title=None, yaxis_title="Users")
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    with right:
        st.markdown(section_heading("Behavioral Activity", "activity"), unsafe_allow_html=True)
        daily = events.assign(day=events["timestamp"].dt.date).groupby("day", as_index=False).agg(
            events=("user_id", "size"), files=("files_accessed", "mean"))
        fig = px.line(daily, x="day", y=["events", "files"], markers=True,
                      color_discrete_sequence=["#4769d8", "#e5a43a"])
        fig.update_layout(height=300, margin=dict(t=10), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    left, right = st.columns(2)
    with left:
        st.markdown(section_heading("Silent Shift Statistics", "trend"), unsafe_allow_html=True)
        shift = summary["shift_status"].value_counts()
        fig = px.bar(x=shift.values, y=shift.index, orientation="h", color_discrete_sequence=["#6c82d9"])
        fig.update_layout(height=250, xaxis_title="Users", yaxis_title=None)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    with right:
        st.markdown(section_heading("Location Distribution", "chart"), unsafe_allow_html=True)
        loc = events["location"].value_counts().head(8).sort_values()
        fig = px.bar(x=loc.values, y=loc.index, orientation="h", color_discrete_sequence=["#8a9de0"])
        fig.update_layout(height=250, xaxis_title="Events", yaxis_title=None)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.markdown(section_heading("Action Distribution", "chart"), unsafe_allow_html=True)
    actions = events["action"].value_counts().sort_values()
    fig = px.bar(x=actions.index, y=actions.values, color_discrete_sequence=["#4769d8"])
    fig.update_layout(height=250, xaxis_title=None, yaxis_title="Events")
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


nav_items = [
    ("layout", "Overview"),
    ("alert", "Alerts"),
    ("search", "Investigations"),
    ("users", "Users"),
    ("chart", "Analytics"),
]
nav_markup = []
for nav_icon, page_name in nav_items:
    active = " active" if st.session_state.page == page_name else ""
    nav_markup.append(
        f'<a class="{active.strip()}" href="?page={page_name}" target="_self">'
        f'<span class="custom-nav-icon">{icon(nav_icon)}</span>{page_name}</a>'
    )
sidebar_markup = (
    '<aside class="custom-sidebar">'
    '<div class="custom-brand">'
    '<div class="custom-logo"><div class="brand-mark">S</div></div>'
    '<div class="custom-brand-name">SILENT SHIFT</div>'
    '<div class="custom-brand-subtitle">Behavioral Intelligence</div>'
    '</div>'
    '<div class="custom-nav-section"><div class="custom-nav-label">NAVIGATION</div>'
    f'<nav class="custom-nav">{"".join(nav_markup)}</nav>'
    '</div>'
    '<div class="custom-spacer"></div>'
    '<div class="custom-system"><div class="custom-system-label">SYSTEM</div>'
    f'<div class="custom-stat">EVENTS<strong>{len(events):,} Events</strong></div>'
    f'<div class="custom-stat">ACCOUNTS<strong>{summary["user_id"].nunique():,} Accounts</strong></div></div>'
    '<div class="custom-sidebar-footer">SILENT SHIFT<br>A Silent Shift Into The Future</div>'
    '</aside>'
)
st.markdown(sidebar_markup, unsafe_allow_html=True)

if st.session_state.page == "Overview":
    overview()
elif st.session_state.page == "Alerts":
    alerts()
elif st.session_state.page == "Investigations":
    investigations()
elif st.session_state.page == "Users":
    users()
else:
    analytics()
