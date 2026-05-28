import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from datetime import datetime
import time
import io
import json
import requests
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

st.set_page_config(page_title="AI Finance Debt Assistant", page_icon="💼", layout="wide")

st.markdown("""
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

.stApp { background:#f8fbff; font-family:'Inter',sans-serif; }
.block-container { padding:2.2rem 3.2rem; max-width:1550px; }
#MainMenu, footer { visibility:hidden; }

section[data-testid="stSidebar"] {
    background:#ffffff;
    border-right:1px solid #e5e7eb;
    padding: 1.5rem 1rem !important;
}

/* Sidebar input field styling */
div[data-testid="stVerticalBlock"] > div {
    gap: 0.2rem !important;
}

[data-testid="stNumberInput"] {
    background:white;
    border:1px solid #d8dee9;
    border-radius:12px;
    margin-bottom: 8px;
}

[data-testid="stNumberInput"] input {
    border:none!important;
    background:transparent!important;
    font-weight:600;
    color:#0f172a!important;
    padding: 0.5rem 0.75rem !important;
}

[data-testid="stNumberInput"] input::placeholder {
    color: #94a3b8;
    font-weight: 400;
    font-size: 13px;
}

/* Hide default number input label */
[data-testid="stNumberInput"] label {
    display: none !important;
}

.side-icon {
    width:36px;
    height:36px;
    border-radius:10px;
    display:flex;
    align-items:center;
    justify-content:center;
}

.purple { background:#efe7ff; color:#7c3aed; }
.blue { background:#dbeafe; color:#2563eb; }
.green { background:#dcfce7; color:#16a34a; }
.orange { background:#ffedd5; color:#f97316; }
.red { background:#fee2e2; color:#ef4444; }
.pink { background:#fce7f3; color:#ec4899; }

.hero-title {
    margin-top: 18px;
    font-size:44px;
    font-weight:900;
    color:#0f172a;
    letter-spacing:-1px;
}

.hero-subtitle {
    padding-top: 6px;
    color:#64748b;
    font-size:16px;
    margin-bottom:28px;
}

.metric-card {
    background:linear-gradient(135deg,#ffffff 0%,#f8fbff 58%,#eef4ff 100%);
    padding:15px 18px;
    border-radius:18px;
    border:1px solid #e5e7eb;
    box-shadow:0 14px 34px rgba(15,23,42,.07);
    min-height:118px;
    transition: transform 0.2s ease, box-shadow .2s ease;
    position:relative;
    overflow:hidden;
}

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow:0 18px 42px rgba(15,23,42,.10);
}
.metric-card:before {
    content:"";
    position:absolute;
    width:135px;
    height:135px;
    right:-58px;
    top:-58px;
    border-radius:50%;
    background:rgba(37,99,235,.10);
    pointer-events:none;
}
.metric-card.purple-card:before { background:rgba(124,58,237,.13); }
.metric-card.blue-card:before { background:rgba(37,99,235,.13); }
.metric-card.green-card:before { background:rgba(22,163,74,.13); }
.metric-card.orange-card:before { background:rgba(249,115,22,.14); }

.metric-icon {
    width:40px;
    height:40px;
    border-radius:13px;
    margin-bottom:11px;
    display:flex;
    align-items:center;
    justify-content:center;
    position:relative;
    z-index:1;
}

.metric-icon i { font-size:17px; }

.metric-label {
    font-size:11px;
    font-weight:900;
    text-transform:uppercase;
    position:relative;
    z-index:1;
}

.metric-value {
    font-size:24px;
    font-weight:900;
    color:#0f172a;
    margin-top:6px;
    letter-spacing:-.7px;
    position:relative;
    z-index:1;
}

.metric-note {
    color:#64748b;
    margin-top:5px;
    font-size:12px;
    font-weight:700;
    position:relative;
    z-index:1;
}

.metric-badge {
    display:inline-block;
    background:#dcfce7;
    color:#16a34a;
    padding:6px 12px;
    border-radius:10px;
    margin-top:10px;
    font-weight:800;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background:white!important;
    border:1px solid #e5e7eb!important;
    border-radius:28px!important;
    box-shadow:0 18px 45px rgba(15,23,42,.08)!important;
    padding:28px!important;
}

div[data-testid="stVerticalBlockBorderWrapper"] > div {
    padding:0!important;
}

.section-head {
    display:flex;
    align-items:center;
    gap:14px;
    margin-bottom:24px;
}

.section-icon {
    width:50px;
    height:50px;
    border-radius:17px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:21px;
}

.section-title {
    font-size:24px;
    font-weight:900;
    color:#0f172a;
}

.section-sub {
    color:#64748b;
    margin-top:4px;
    font-size:14px;
}

.legend-row {
    display:grid;
    grid-template-columns:1fr 80px 60px;
    gap:14px;
    margin-bottom:16px;
    align-items:center;
    font-size:14px;
}

.legend-left {
    display:flex;
    gap:12px;
    align-items:center;
    font-weight:800;
}

.dot {
    width:13px;
    height:13px;
    border-radius:50%;
}

.advice-green {
    background:linear-gradient(135deg,#ecfdf5,#dcfce7);
    border:1px solid #bbf7d0;
    border-radius:22px;
    padding:24px;
    margin-top:20px;
}

.ratio-box,.debt-input-box {
    background:#f8fafc;
    border:1px solid #e5e7eb;
    border-radius:18px;
    padding:18px;
    margin-top:18px;
}

.success-box {
    background:linear-gradient(135deg,#ecfdf5,#dcfce7);
    border:1px solid #86efac;
    border-radius:22px;
    padding:24px;
    color:#16a34a;
    font-size:20px;
    font-weight:900;
    margin-top:18px;
}

.tip-box {
    background:linear-gradient(135deg,#eef2ff,#f5f3ff);
    border:1px solid #ddd6fe;
    border-radius:18px;
    padding:18px;
    margin-top:20px;
    color:#2563eb;
    font-weight:700;
}

.history-card {
    background: #f8fafc;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 12px;
    border-left: 4px solid;
    transition: all 0.2s ease;
}

.history-card:hover {
    transform: translateX(5px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.history-month {
    font-weight: 800;
    font-size: 16px;
    margin-bottom: 8px;
}

.history-stats {
    display: flex;
    gap: 20px;
    font-size: 13px;
    flex-wrap: wrap;
}

.history-saving {
    color: #16a34a;
}

.history-spending {
    color: #ef4444;
}

.badge-success {
    background: #dcfce7;
    color: #16a34a;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

.badge-warning {
    background: #fed7aa;
    color: #ea580c;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

.badge-danger {
    background: #fee2e2;
    color: #dc2626;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

/* Goal card styling */
.goal-card {
    background: linear-gradient(135deg, #fef3c7, #fde68a);
    border-radius: 16px;
    padding: 16px;
    margin-top: 16px;
    border: 1px solid #fbbf24;
}

.goal-progress {
    background: #e2e8f0;
    border-radius: 10px;
    height: 8px;
    overflow: hidden;
    margin-top: 10px;
}

.goal-progress-bar {
    background: linear-gradient(90deg, #f59e0b, #f97316);
    height: 100%;
    border-radius: 10px;
    transition: width 0.5s ease;
}

/* Budget alert */
.budget-alert {
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 12px;
    padding: 12px;
    margin-top: 12px;
    color: #dc2626;
}

.budget-title-row {
    display:flex;
    align-items:center;
    gap:12px;
    margin: 6px 0 14px 0;
}

.budget-title-icon {
    width:38px;
    height:38px;
    border-radius:12px;
    background:#ffedd5;
    color:#f97316;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:16px;
}

.budget-title-text {
    font-size:18px;
    font-weight:900;
    color:#0f172a;
}

.budget-title-sub {
    font-size:12px;
    color:#64748b;
    margin-top:2px;
}

div.stButton > button {
    border-radius:14px !important;
    font-weight:900 !important;
    border:1px solid #e5e7eb !important;
    padding:0.7rem 1rem !important;
    transition: all 0.2s ease !important;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:0 10px 24px rgba(15,23,42,.10) !important;
}

.history-modern-hero {
    background:linear-gradient(135deg,#0f172a,#1e293b);
    border-radius:26px;
    padding:26px;
    color:white;
    margin-bottom:24px;
    box-shadow:0 22px 55px rgba(15,23,42,.18);
    position:relative;
    overflow:hidden;
}

.history-modern-hero:after {
    content:"";
    position:absolute;
    width:180px;
    height:180px;
    right:-55px;
    top:-55px;
    background:rgba(255,255,255,.10);
    border-radius:50%;
}

.history-hero-title {
    font-size:28px;
    font-weight:900;
    letter-spacing:-.4px;
    position:relative;
    z-index:2;
}

.history-hero-sub {
    color:#cbd5e1;
    margin-top:6px;
    font-size:14px;
    position:relative;
    z-index:2;
}

.history-summary-card {
    background:#ffffff;
    border:1px solid #e5e7eb;
    border-radius:22px;
    padding:22px;
    box-shadow:0 16px 38px rgba(15,23,42,.07);
    min-height:118px;
}

.history-summary-icon {
    width:44px;
    height:44px;
    border-radius:15px;
    display:flex;
    align-items:center;
    justify-content:center;
    margin-bottom:14px;
    font-size:18px;
}

.history-summary-label {
    color:#64748b;
    font-size:13px;
    font-weight:800;
    text-transform:uppercase;
}

.history-summary-value {
    color:#0f172a;
    font-size:24px;
    font-weight:900;
    margin-top:8px;
}

.history-summary-note {
    color:#94a3b8;
    font-size:12px;
    margin-top:5px;
    font-weight:700;
}

.history-chart-card {
    background:#ffffff;
    border:1px solid #e5e7eb;
    border-radius:24px;
    padding:22px;
    margin-top:22px;
    box-shadow:0 14px 34px rgba(15,23,42,.06);
}

.modern-history-card {
    background:#ffffff;
    border:1px solid #e5e7eb;
    border-radius:24px;
    padding:22px;
    margin-bottom:16px;
    box-shadow:0 14px 32px rgba(15,23,42,.07);
    transition:all .2s ease;
}

.modern-history-card:hover {
    transform:translateY(-3px);
    box-shadow:0 22px 45px rgba(15,23,42,.10);
}

.modern-history-top {
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:16px;
    margin-bottom:18px;
}

.modern-history-month-wrap {
    display:flex;
    align-items:center;
    gap:13px;
}

.modern-history-icon {
    width:48px;
    height:48px;
    border-radius:16px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:19px;
}

.modern-history-month {
    color:#0f172a;
    font-weight:900;
    font-size:18px;
}

.modern-history-small {
    color:#64748b;
    font-size:12px;
    margin-top:3px;
    font-weight:700;
}

.modern-history-grid {
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:12px;
}

.modern-history-mini {
    background:#f8fafc;
    border:1px solid #eef2f7;
    border-radius:16px;
    padding:14px;
}

.modern-history-mini-label {
    color:#64748b;
    font-size:12px;
    font-weight:800;
    margin-bottom:7px;
}

.modern-history-mini-value {
    color:#0f172a;
    font-size:17px;
    font-weight:900;
}

.modern-history-breakdown {
    margin-top:14px;
    background:#f8fafc;
    border:1px solid #eef2f7;
    border-radius:16px;
    padding:13px 14px;
    color:#64748b;
    font-size:13px;
    line-height:1.8;
}


/* Modern Savings Goal Tracker */
.goal-modern-wrap {
    background:linear-gradient(135deg,#ffffff,#f8fbff);
    border:1px solid #e5e7eb;
    border-radius:28px;
    padding:24px;
    margin:24px 0 12px 0;
    box-shadow:0 18px 45px rgba(15,23,42,.08);
}

.goal-modern-head {
    display:flex;
    align-items:center;
    gap:14px;
    margin-bottom:18px;
}

.goal-modern-icon {
    width:52px;
    height:52px;
    border-radius:18px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:linear-gradient(135deg,#dbeafe,#eef2ff);
    color:#2563eb;
    font-size:22px;
}

.goal-modern-title {
    font-size:24px;
    font-weight:900;
    color:#0f172a;
}

.goal-modern-sub {
    color:#64748b;
    font-size:13px;
    font-weight:700;
    margin-top:4px;
}

.goal-modern-card {
    background:linear-gradient(135deg,#f8fafc,#ffffff);
    border:1px solid #e5e7eb;
    border-radius:24px;
    padding:22px;
    height:100%;
}

.goal-modern-label {
    color:#64748b;
    font-size:13px;
    font-weight:900;
    text-transform:uppercase;
    display:flex;
    align-items:center;
    gap:8px;
}

.goal-modern-value {
    color:#0f172a;
    font-size:30px;
    font-weight:900;
    margin-top:10px;
    letter-spacing:-.5px;
}

.goal-modern-progress {
    height:13px;
    background:#e2e8f0;
    border-radius:999px;
    overflow:hidden;
    margin-top:16px;
}

.goal-modern-progress-bar {
    height:100%;
    border-radius:999px;
    background:linear-gradient(90deg,#2563eb,#7c3aed,#16a34a);
    box-shadow:0 6px 18px rgba(37,99,235,.25);
}

.goal-modern-foot {
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:10px;
    margin-top:12px;
    color:#64748b;
    font-size:13px;
    font-weight:800;
}

.goal-time-card {
    background:linear-gradient(135deg,#0f172a,#1e293b);
    color:#ffffff;
    border-radius:24px;
    padding:24px;
    min-height:202px;
    box-shadow:0 18px 45px rgba(15,23,42,.18);
    display:flex;
    flex-direction:column;
    justify-content:center;
    text-align:center;
}

.goal-time-icon {
    width:48px;
    height:48px;
    border-radius:16px;
    display:flex;
    align-items:center;
    justify-content:center;
    margin:0 auto 12px auto;
    background:rgba(255,255,255,.12);
    color:#bfdbfe;
    font-size:20px;
}

.goal-time-label {
    color:#cbd5e1;
    font-size:13px;
    font-weight:800;
}

.goal-time-value {
    font-size:38px;
    font-weight:900;
    margin-top:7px;
}

.goal-time-note {
    color:#cbd5e1;
    font-size:12px;
    font-weight:700;
    margin-top:5px;
}

.history-section-card {
    background:#ffffff;
    border:1px solid #e5e7eb;
    border-radius:26px;
    padding:24px;
    margin-top:22px;
    box-shadow:0 16px 38px rgba(15,23,42,.07);
}

.history-breakdown-pill {
    display:inline-flex;
    align-items:center;
    gap:7px;
    background:#ffffff;
    border:1px solid #e5e7eb;
    border-radius:999px;
    padding:8px 11px;
    margin:5px 5px 0 0;
    color:#475569;
    font-size:12px;
    font-weight:800;
}


/* Month selector and modern debt planner */
.month-title-row {
    display:flex;
    align-items:center;
    gap:12px;
    margin: 4px 0 10px 0;
}

.month-title-icon {
    width:38px;
    height:38px;
    border-radius:12px;
    background:#dbeafe;
    color:#2563eb;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:16px;
}

.month-title-text {
    font-size:18px;
    font-weight:900;
    color:#0f172a;
}

.month-title-sub {
    font-size:12px;
    color:#64748b;
    margin-top:2px;
}

[data-testid="stSelectbox"] {
    background:white;
    border:1px solid #d8dee9;
    border-radius:12px;
    margin-bottom: 8px;
}

[data-testid="stSelectbox"] label {
    display:none !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    border:none!important;
    background:transparent!important;
    font-weight:700;
    color:#0f172a!important;
}

.debt-hero-card {
    background:linear-gradient(135deg,#0f172a,#1e293b);
    border-radius:28px;
    padding:26px;
    color:#ffffff;
    margin-bottom:22px;
    box-shadow:0 22px 55px rgba(15,23,42,.18);
    position:relative;
    overflow:hidden;
}

.debt-hero-card:after {
    content:"";
    position:absolute;
    width:180px;
    height:180px;
    right:-60px;
    top:-60px;
    background:rgba(255,255,255,.09);
    border-radius:50%;
}

.debt-hero-title {
    font-size:26px;
    font-weight:900;
    letter-spacing:-.4px;
    position:relative;
    z-index:2;
}

.debt-hero-sub {
    color:#cbd5e1;
    font-size:14px;
    margin-top:6px;
    position:relative;
    z-index:2;
}

.debt-modern-input-card {
    background:linear-gradient(135deg,#ffffff,#f8fafc);
    border:1px solid #e5e7eb;
    border-radius:24px;
    padding:18px;
    min-height:150px;
    box-shadow:0 14px 34px rgba(15,23,42,.06);
}

.debt-modern-input-head {
    display:flex;
    align-items:center;
    gap:12px;
    margin-bottom:12px;
}

.debt-modern-input-icon {
    width:42px;
    height:42px;
    border-radius:14px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:17px;
}

.debt-modern-input-title {
    color:#0f172a;
    font-size:14px;
    font-weight:900;
}

.debt-modern-input-sub {
    color:#64748b;
    font-size:12px;
    font-weight:700;
    margin-top:2px;
}

.debt-result-grid {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:14px;
    margin-top:20px;
}

.debt-result-card {
    background:#ffffff;
    border:1px solid #e5e7eb;
    border-radius:22px;
    padding:20px;
    box-shadow:0 14px 32px rgba(15,23,42,.07);
}

.debt-result-label {
    color:#64748b;
    font-size:11px;
    font-weight:900;
    text-transform:uppercase;
}

.debt-result-value {
    color:#0f172a;
    font-size:27px;
    font-weight:900;
    margin-top:8px;
}

.debt-result-note {
    color:#94a3b8;
    font-size:12px;
    font-weight:700;
    margin-top:4px;
}

.debt-payoff-banner {
    background:linear-gradient(135deg,#ecfdf5,#dcfce7);
    border:1px solid #86efac;
    border-radius:22px;
    padding:18px;
    color:#166534;
    font-weight:900;
    margin-top:18px;
}

@media (max-width: 900px) {
    .debt-result-grid { grid-template-columns:1fr; }
}

@media (max-width: 900px) {
    .modern-history-grid { grid-template-columns:repeat(2,1fr); }
}


/* Animated Finance Insights + Health Level */
.insights-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin:24px 0; }
.insight-card { background:linear-gradient(135deg,#ffffff 0%,#f8fbff 58%,#eef4ff 100%); border:1px solid #e5e7eb; border-radius:22px; padding:20px 22px; box-shadow:0 14px 34px rgba(15,23,42,.07); position:relative; overflow:hidden; animation:floatIn .55s ease both; min-height:118px; }
.insight-card:before { content:""; position:absolute; inset:0; background:radial-gradient(circle at top right, rgba(37,99,235,.12), transparent 35%); pointer-events:none; }
.insight-icon { width:48px; height:48px; border-radius:16px; display:flex; align-items:center; justify-content:center; margin-bottom:14px; font-size:20px; }
.insight-label { color:#64748b; font-size:12px; font-weight:900; text-transform:uppercase; }
.insight-value { color:#0f172a; font-size:26px; font-weight:900; margin-top:7px; letter-spacing:-.5px; }
.insight-note { color:#64748b; font-size:12px; font-weight:700; margin-top:7px; line-height:1.5; }
.health-card { background:linear-gradient(135deg,#0f172a,#1e293b); color:white; border-radius:28px; padding:26px; margin:22px 0; box-shadow:0 20px 50px rgba(15,23,42,.18); position:relative; overflow:hidden; }
.health-card:before { content:""; position:absolute; width:280px; height:280px; background:rgba(124,58,237,.22); border-radius:50%; right:-80px; top:-100px; }
.health-top { display:flex; justify-content:space-between; gap:18px; align-items:center; position:relative; z-index:1; }
.health-title { font-size:24px; font-weight:900; }
.health-sub { color:#cbd5e1; font-size:13px; font-weight:700; margin-top:5px; }
.health-level-badge { background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.18); color:#ffffff; padding:12px 16px; border-radius:18px; font-weight:900; }
.health-progress { height:13px; background:rgba(255,255,255,.14); border-radius:999px; overflow:hidden; margin-top:22px; position:relative; z-index:1; }
.health-progress-bar { height:100%; border-radius:999px; background:linear-gradient(90deg,#ef4444,#f97316,#22c55e,#2563eb); animation:growWidth 1s ease both; }
.health-tips { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:18px; position:relative; z-index:1; }
.health-tip { background:rgba(255,255,255,.10); border:1px solid rgba(255,255,255,.14); border-radius:18px; padding:14px; color:#e2e8f0; font-size:13px; font-weight:700; }
.ai-chat-hero { background:linear-gradient(135deg,#ffffff,#eef2ff); border:1px solid #e5e7eb; border-radius:28px; padding:26px; box-shadow:0 18px 45px rgba(15,23,42,.08); margin-bottom:20px; }
.ai-chat-title { font-size:26px; font-weight:900; color:#0f172a; display:flex; align-items:center; gap:12px; }
.ai-chat-sub { color:#64748b; margin-top:8px; font-weight:700; line-height:1.6; }
.ai-card { background:white; border:1px solid #e5e7eb; border-radius:24px; padding:22px; box-shadow:0 16px 38px rgba(15,23,42,.06); height:100%; }
.ai-card-title { font-weight:900; color:#0f172a; font-size:18px; display:flex; align-items:center; gap:10px; margin-bottom:10px; }
.chat-answer { background:linear-gradient(135deg,#f8fafc,#ffffff); border:1px solid #e5e7eb; border-radius:22px; padding:20px; margin-top:18px; color:#0f172a; line-height:1.75; font-weight:600; }
.report-preview { background:linear-gradient(135deg,#0f172a,#334155); color:white; border-radius:28px; padding:26px; box-shadow:0 18px 45px rgba(15,23,42,.18); }
.report-row { display:flex; justify-content:space-between; border-bottom:1px solid rgba(255,255,255,.12); padding:10px 0; color:#e2e8f0; font-weight:700; }
.receipt-box { background:#f8fafc; border:1px dashed #cbd5e1; border-radius:20px; padding:16px; color:#475569; font-size:13px; font-weight:700; margin-top:10px; }
.quick-summary-card {
    background:linear-gradient(135deg,#ffffff,#f8fbff 55%,#eef4ff);
    border:1px solid #e5e7eb;
    border-radius:26px;
    padding:24px;
    margin:20px 0 24px 0;
    box-shadow:0 16px 38px rgba(15,23,42,.07);
    position:relative;
    overflow:hidden;
}
.quick-summary-card:before { content:""; position:absolute; width:240px; height:240px; right:-100px; top:-110px; background:rgba(124,58,237,.10); border-radius:50%; }
.quick-summary-title { color:#0f172a; font-size:22px; font-weight:900; display:flex; gap:10px; align-items:center; position:relative; z-index:1; }
.quick-summary-sub { color:#64748b; font-size:13px; font-weight:700; margin-top:6px; position:relative; z-index:1; }
.quick-summary-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:18px; position:relative; z-index:1; }
.quick-summary-item { background:rgba(255,255,255,.78); border:1px solid #e5e7eb; border-radius:18px; padding:14px; }
.quick-summary-item-label { color:#64748b; font-size:12px; font-weight:900; text-transform:uppercase; }
.quick-summary-item-value { color:#0f172a; font-size:18px; font-weight:900; margin-top:5px; }
@media (max-width: 1000px) { .quick-summary-grid { grid-template-columns:1fr; } }

@keyframes floatIn { from { opacity:0; transform:translateY(14px); } to { opacity:1; transform:translateY(0); } }
@keyframes growWidth { from { width:0%; } }
@media (max-width: 1000px) { .insights-grid,.health-tips { grid-template-columns:1fr; } }



/* Top right AI assistant card */
.top-ai-shell {
    position: relative;
    max-width: 340px;
    margin-left: auto;
}
.top-ai-launcher {
    background: radial-gradient(circle at 95% 0%, rgba(255,255,255,.18) 0 58px, transparent 60px),
                linear-gradient(135deg, #101827 0%, #1d2a54 48%, #4f46e5 100%);
    border-radius: 22px;
    padding: 18px 18px 76px 18px;
    color: white;
    box-shadow: 0 22px 46px rgba(15,23,42,.20);
    border: 1px solid rgba(255,255,255,.18);
    min-height: 174px;
    position: relative;
    overflow: hidden;
}
.top-ai-launcher:after {
    content:"";
    position:absolute;
    inset:0;
    background:linear-gradient(135deg, rgba(255,255,255,.06), transparent 48%);
    pointer-events:none;
}
.top-ai-kicker {
    display:inline-flex;
    align-items:center;
    gap:7px;
    font-size:12px;
    font-weight:900;
    letter-spacing:.35px;
    text-transform:uppercase;
    color:#dbeafe;
    position:relative;
    z-index:1;
}
.top-ai-title {
    font-size:20px;
    font-weight:900;
    margin-top:10px;
    letter-spacing:-.5px;
    color:#ffffff;
    position:relative;
    z-index:1;
}
.top-ai-sub {
    color:#e5edff;
    font-size:13px;
    line-height:1.48;
    margin-top:9px;
    font-weight:700;
    position:relative;
    z-index:1;
}
.top-ai-actions {
    position: relative;
    z-index: 10;
    margin: -60px 15px 0 15px;
}
.top-ai-static-pill {
    background: rgba(255,255,255,.10);
    border-left: 1px solid rgba(255,255,255,.24);
    padding: 9px 7px;
    font-size: 12px;
    font-weight: 900;
    color: #ffffff;
    min-height: 38px;
    display:flex;
    align-items:center;
    justify-content:center;
    gap:6px;
    border-radius: 0;
}
/* Style only the Ask AI button by its Streamlit key */
.st-key-open_ai_modal_btn button,
.st-key-open_ai_modal_btn button[kind="secondary"] {
    background: linear-gradient(135deg,#7c3aed,#4f46e5) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,.26) !important;
    border-radius: 999px !important;
    padding: 8px 12px !important;
    font-size: 12px !important;
    font-weight: 900 !important;
    box-shadow: 0 10px 22px rgba(79,70,229,.35) !important;
    min-height: 38px !important;
    width: 100% !important;
}
.st-key-open_ai_modal_btn button:hover,
.st-key-open_ai_modal_btn button[kind="secondary"]:hover {
    background: linear-gradient(135deg,#8b5cf6,#6366f1) !important;
    transform: translateY(-1px);
}
.st-key-open_ai_modal_btn button p { color:#ffffff !important; font-weight:900 !important; }
@media (max-width: 1100px) {
    .top-ai-shell { max-width: 100%; margin-top: 18px; }
}
.ai-modal-hero {
    background:linear-gradient(135deg,#0f172a,#1e293b 55%,#4f46e5);
    color:white;
    border-radius:28px;
    padding:24px;
    box-shadow:0 24px 60px rgba(15,23,42,.22);
    position:relative;
    overflow:hidden;
    margin-bottom:18px;
}
.ai-modal-hero:before { content:""; position:absolute; width:230px; height:230px; right:-80px; top:-100px; background:rgba(255,255,255,.12); border-radius:50%; }
.ai-modal-title { font-size:26px; font-weight:900; letter-spacing:-.6px; position:relative; z-index:1; display:flex; gap:12px; align-items:center; }
.ai-modal-sub { color:#dbeafe; margin-top:8px; line-height:1.55; font-weight:700; position:relative; z-index:1; }
.ai-modal-grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:14px; }
.ai-modal-box { background:#ffffff; border:1px solid #e5e7eb; border-radius:22px; padding:18px; box-shadow:0 14px 34px rgba(15,23,42,.07); }
.ai-modal-box-title { font-size:16px; font-weight:900; color:#0f172a; display:flex; gap:9px; align-items:center; margin-bottom:10px; }
@media (max-width: 900px) { .ai-modal-grid { grid-template-columns:1fr; } }


/* Professional top-right AI assistant card */
.top-ai-compact-card {
    background: linear-gradient(135deg,#ffffff 0%,#f8fbff 48%,#eef2ff 100%);
    border: 1px solid #dbeafe;
    border-radius: 24px;
    padding: 22px 22px 20px 22px;
    max-width: 430px;
    width: 100%;
    margin-left: auto;
    box-shadow: 0 22px 50px rgba(15,23,42,.12);
    position: relative;
    overflow: hidden;
}
.top-ai-compact-card:before {
    content:"";
    position:absolute;
    width:150px;
    height:150px;
    right:-50px;
    top:-65px;
    background:rgba(124,58,237,.15);
    border-radius:50%;
}
.top-ai-compact-card:after {
    content:"";
    position:absolute;
    width:95px;
    height:95px;
    left:-38px;
    bottom:-42px;
    background:rgba(37,99,235,.10);
    border-radius:50%;
}
.top-ai-compact-kicker {
    position:relative;
    z-index:1;
    color:#4f46e5;
    font-size:12px;
    font-weight:900;
    letter-spacing:.45px;
    text-transform:uppercase;
    display:flex;
    align-items:center;
    gap:8px;
}
.top-ai-compact-title {
    position:relative;
    z-index:1;
    color:#0f172a;
    font-size:22px;
    font-weight:900;
    margin-top:9px;
    letter-spacing:-.55px;
}
.top-ai-compact-sub {
    position:relative;
    z-index:1;
    color:#64748b;
    font-size:13px;
    font-weight:700;
    line-height:1.55;
    margin-top:6px;
    margin-bottom:0;
}
.ai-button-spacer {
    height:14px;
}
.st-key-open_ai_modal_btn {
    width:100% !important;
    margin-top:14px !important;
    padding-top:2px !important;
}
.st-key-open_ai_modal_btn button,
.st-key-open_ai_modal_btn button[kind="secondary"] {
    width:100% !important;
    background: linear-gradient(135deg,#7c3aed,#4f46e5) !important;
    color:#ffffff !important;
    border:none !important;
    border-radius:16px !important;
    padding:12px 18px !important;
    min-height:48px !important;
    font-size:15px !important;
    font-weight:900 !important;
    box-shadow:0 16px 32px rgba(79,70,229,.30) !important;
}
.st-key-open_ai_modal_btn button:hover,
.st-key-open_ai_modal_btn button[kind="secondary"]:hover {
    background: linear-gradient(135deg,#8b5cf6,#6366f1) !important;
    transform: translateY(-2px);
}
.st-key-open_ai_modal_btn button p { color:#ffffff !important; font-weight:900 !important; }
@media (max-width: 1100px) { .top-ai-compact-card { max-width:100%; margin-top:18px; } }


/* Modern AI popup / dialog design */
div[data-testid="stDialog"] > div {
    border-radius: 32px !important;
    background: #ffffff !important;
    box-shadow: 0 34px 90px rgba(15, 23, 42, .28) !important;
    border: 1px solid rgba(226, 232, 240, .9) !important;
    overflow: hidden !important;
}
div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] p { margin-bottom: 0 !important; }
.ai-modal-hero-modern {
    background: radial-gradient(circle at 92% 5%, rgba(255,255,255,.20) 0 70px, transparent 72px), linear-gradient(135deg,#0f172a 0%,#1e1b4b 48%,#4f46e5 100%);
    color:white; border-radius:30px; padding:26px; box-shadow:0 24px 60px rgba(15,23,42,.25); position:relative; overflow:hidden; margin-bottom:18px;
}
.ai-modal-hero-modern:after { content:""; position:absolute; inset:0; background:linear-gradient(135deg, rgba(255,255,255,.08), transparent 48%); pointer-events:none; }
.ai-modal-badge-modern { display:inline-flex; align-items:center; gap:8px; background:rgba(255,255,255,.13); border:1px solid rgba(255,255,255,.20); color:#e0e7ff; padding:8px 12px; border-radius:999px; font-size:12px; font-weight:900; letter-spacing:.4px; text-transform:uppercase; position:relative; z-index:1; }
.ai-modal-title-modern { font-size:30px; font-weight:900; letter-spacing:-.9px; margin-top:14px; position:relative; z-index:1; }
.ai-modal-sub-modern { color:#dbeafe; margin-top:8px; line-height:1.65; font-weight:700; font-size:14px; max-width:760px; position:relative; z-index:1; }
.ai-modal-stats-modern { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-top:18px; position:relative; z-index:1; }
.ai-modal-stat-modern { background:rgba(255,255,255,.10); border:1px solid rgba(255,255,255,.14); border-radius:18px; padding:12px; }
.ai-modal-stat-label-modern { color:#bfdbfe; font-size:11px; font-weight:900; text-transform:uppercase; }
.ai-modal-stat-value-modern { color:#ffffff; font-size:18px; font-weight:900; margin-top:4px; }
.ai-panel-modern { background:linear-gradient(135deg,#ffffff,#f8fbff); border:1px solid #e5e7eb; border-radius:24px; padding:20px; box-shadow:0 16px 38px rgba(15,23,42,.07); height:100%; }
.ai-panel-title-modern { display:flex; align-items:center; gap:10px; color:#0f172a; font-size:17px; font-weight:900; margin-bottom:8px; }
.ai-panel-sub-modern { color:#64748b; font-size:13px; font-weight:700; line-height:1.5; margin-bottom:14px; }
.ai-suggestion-grid-modern { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin:12px 0 2px 0; }
.ai-suggestion-card-modern { background:#f8fafc; border:1px solid #e5e7eb; border-radius:16px; padding:12px; color:#334155; font-size:12px; font-weight:800; line-height:1.4; }
.ai-suggestion-card-modern i { color:#4f46e5; margin-right:6px; }
.ai-answer-modern { background:linear-gradient(135deg,#f8fafc,#ffffff); border:1px solid #e5e7eb; border-left:5px solid #4f46e5; border-radius:22px; padding:20px; margin-top:18px; color:#0f172a; line-height:1.75; font-weight:600; box-shadow:0 14px 34px rgba(15,23,42,.06); }
.ai-answer-title-modern { font-size:17px; font-weight:900; color:#0f172a; margin-bottom:10px; display:flex; gap:9px; align-items:center; }
.st-key-ask_ollama_modal button, .st-key-clear_ai_modal_fields button { border-radius:16px !important; min-height:48px !important; font-weight:900 !important; }
.st-key-ask_ollama_modal button { background:linear-gradient(135deg,#7c3aed,#4f46e5) !important; color:white !important; border:none !important; box-shadow:0 16px 32px rgba(79,70,229,.28) !important; }
.st-key-ask_ollama_modal button p { color:white !important; font-weight:900 !important; }
.st-key-clear_ai_modal_fields button { background:#f8fafc !important; color:#334155 !important; border:1px solid #e5e7eb !important; }
div[data-baseweb="tab-list"] { gap:8px; }
div[data-baseweb="tab"] { border-radius:14px !important; padding:10px 16px !important; font-weight:900 !important; }
@media (max-width: 900px) { .ai-modal-stats-modern, .ai-suggestion-grid-modern { grid-template-columns:1fr; } }

</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'monthly_history' not in st.session_state:
    st.session_state.monthly_history = []

if 'savings_goal' not in st.session_state:
    st.session_state.savings_goal = 10000

if 'monthly_budget' not in st.session_state:
    st.session_state.monthly_budget = 0

if 'notifications' not in st.session_state:
    st.session_state.notifications = []


def sidebar_input(icon, color, title, key, placeholder):
    """Create sidebar input with icon on the left and placeholder text."""
    col_icon, col_input = st.columns([1, 5])
    with col_icon:
        st.markdown(f'<div class="side-icon {color}" style="width:36px;height:36px;"><i class="fa-solid {icon}"></i></div>', unsafe_allow_html=True)
    with col_input:
        value = st.number_input(
            title,
            min_value=0,
            value=None,
            step=1,
            key=key,
            label_visibility="collapsed",
            placeholder=placeholder
        )
    return value or 0


def metric_card(icon, color, label_color, title, value, note, badge=""):
    badge_html = f'<div class="metric-badge">{badge}</div>' if badge else ""
    st.markdown(f"""
    <div class="metric-card {color}-card">
        <div class="metric-icon {color}"><i class="fa-solid {icon}"></i></div>
        <div class="metric-label" style="color:{label_color};">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)


def section_header(icon, color, title, subtitle):
    st.markdown(f"""
    <div class="section-head">
        <div class="section-icon {color}"><i class="fa-solid {icon}"></i></div>
        <div>
            <div class="section-title">{title}</div>
            <div class="section-sub">{subtitle}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def save_monthly_data(selected_month, income, rent, bills, food, transport, debt, shopping, total_expenses, remaining, saving_rate):
    """Save selected month's data to history."""
    current_month = selected_month
    
    # Check if current month already exists
    existing_index = None
    for i, record in enumerate(st.session_state.monthly_history):
        if record['month'] == current_month:
            existing_index = i
            break
    
    record = {
        'month': current_month,
        'date': datetime.now(),
        'income': income,
        'expenses': total_expenses,
        'remaining': remaining,
        'saving_rate': saving_rate,
        'rent': rent,
        'food': food,
        'debt': debt,
        'bills': bills,
        'transport': transport,
        'shopping': shopping
    }
    
    if existing_index is not None:
        st.session_state.monthly_history[existing_index] = record
    else:
        st.session_state.monthly_history.insert(0, record)
    
    # Keep only last 12 months
    st.session_state.monthly_history = st.session_state.monthly_history[:12]


def add_notification(message, type="info"):
    """Add a notification message"""
    st.session_state.notifications.append({
        'message': message,
        'type': type,
        'time': datetime.now()
    })
    # Keep only last 5 notifications
    st.session_state.notifications = st.session_state.notifications[-5:]


def export_data_to_csv():
    """Export monthly history to CSV"""
    if st.session_state.monthly_history:
        df = pd.DataFrame(st.session_state.monthly_history)
        csv = df.to_csv(index=False)
        return csv
    return None


def generate_history_pdf_report():
    """Generate a modern PDF report for all saved monthly history records."""
    if not st.session_state.monthly_history:
        return None

    history_df = pd.DataFrame(st.session_state.monthly_history)
    history_df["date"] = pd.to_datetime(history_df["date"], errors="coerce")
    history_df = history_df.sort_values("date")

    total_income = history_df["income"].sum()
    total_expenses_history = history_df["expenses"].sum()
    total_saved_history = history_df["remaining"].sum()
    avg_saving_rate = history_df["saving_rate"].mean()
    best_month = history_df.loc[history_df["saving_rate"].idxmax()]

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=34,
        leftMargin=34,
        topMargin=34,
        bottomMargin=34,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "PDFTitle",
        parent=styles["Title"],
        fontSize=25,
        leading=31,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=8,
        alignment=1,
        fontName="Helvetica-Bold",
    )
    subtitle_style = ParagraphStyle(
        "PDFSubtitle",
        parent=styles["BodyText"],
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=18,
        alignment=1,
    )
    section_style = ParagraphStyle(
        "PDFSection",
        parent=styles["Heading2"],
        fontSize=15,
        leading=20,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=14,
        spaceAfter=8,
        fontName="Helvetica-Bold",
    )
    body_style = ParagraphStyle(
        "PDFBody",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#334155"),
    )

    story = []
    story.append(Paragraph("AI Finance Debt Assistant", title_style))
    story.append(Paragraph("Professional Monthly Finance History PDF Report", subtitle_style))

    summary_data = [
        ["Total Income", "Total Expenses", "Total Saved", "Avg Saving Rate"],
        [
            f"EUR {total_income:,.0f}",
            f"EUR {total_expenses_history:,.0f}",
            f"EUR {total_saved_history:,.0f}",
            f"{avg_saving_rate:.1f}%",
        ],
    ]
    summary_table = Table(summary_data, colWidths=[1.85 * inch, 1.85 * inch, 1.85 * inch, 1.85 * inch])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#eef2ff")),
        ("TEXTCOLOR", (0, 1), (-1, 1), colors.HexColor("#0f172a")),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("PADDING", (0, 0), (-1, -1), 12),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#e5e7eb")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 16))

    story.append(Paragraph("Smart Overview", section_style))
    story.append(Paragraph(
        f"Best saving month: <b>{best_month['month']}</b> with <b>{best_month['saving_rate']:.1f}%</b> saving rate. "
        f"This report includes your saved monthly income, spending, remaining balance, and category breakdowns.",
        body_style,
    ))

    story.append(Paragraph("Monthly Records", section_style))
    table_rows = [["Month", "Income", "Expenses", "Saved", "Saving %", "Status"]]
    for _, record in history_df.iterrows():
        rate = float(record.get("saving_rate", 0))
        status = "Excellent" if rate >= 20 else "Good" if rate >= 10 else "High Spending"
        table_rows.append([
            str(record.get("month", "")),
            f"EUR {record.get('income', 0):,.0f}",
            f"EUR {record.get('expenses', 0):,.0f}",
            f"EUR {record.get('remaining', 0):,.0f}",
            f"{rate:.1f}%",
            status,
        ])

    records_table = Table(table_rows, colWidths=[1.55 * inch, 1.15 * inch, 1.15 * inch, 1.15 * inch, 0.9 * inch, 1.25 * inch])
    records_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563eb")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#0f172a")),
        ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#e2e8f0")),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("FONTSIZE", (0, 0), (-1, -1), 8.7),
    ]))
    story.append(records_table)

    story.append(Paragraph("Category Breakdown", section_style))
    category_totals = {
        "Rent": history_df["rent"].sum(),
        "Bills": history_df["bills"].sum(),
        "Food": history_df["food"].sum(),
        "Transport": history_df["transport"].sum(),
        "Debt": history_df["debt"].sum(),
        "Shopping": history_df["shopping"].sum(),
    }
    category_rows = [["Category", "Total Amount", "Share of Expenses"]]
    for category, amount in category_totals.items():
        share = (amount / total_expenses_history * 100) if total_expenses_history else 0
        category_rows.append([category, f"EUR {amount:,.0f}", f"{share:.1f}%"])

    category_table = Table(category_rows, colWidths=[2.25 * inch, 2.25 * inch, 2.25 * inch])
    category_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7c3aed")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#e2e8f0")),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(category_table)

    story.append(Paragraph("AI Style Suggestions", section_style))
    top_category = max(category_totals, key=category_totals.get)
    suggestions = [
        f"Your highest saved expense category is {top_category}. Review this category first if you want to reduce spending.",
        "Try to keep your saving rate close to or above 20% for stronger financial stability.",
        "If debt pressure grows, prioritize debt reduction before adding new subscriptions or shopping expenses.",
    ]
    for suggestion in suggestions:
        story.append(Paragraph(f"• {suggestion}", body_style))

    story.append(Spacer(1, 18))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%d %B %Y at %H:%M')} by AI Finance Debt Assistant.",
        subtitle_style,
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def get_month_options():
    """Build month dropdown options with current month first and saved months included."""
    now = datetime.now()
    month_options = [datetime(now.year, month, 1).strftime("%B %Y") for month in range(1, 13)]
    current_month = now.strftime("%B %Y")
    if current_month in month_options:
        month_options.remove(current_month)
    month_options.insert(0, current_month)

    saved_months = [record.get("month") for record in st.session_state.monthly_history if record.get("month")]
    for month in saved_months:
        if month not in month_options:
            month_options.append(month)

    return month_options


def clear_current_data():
    """Clear current input values and keep saved monthly history."""
    input_keys = [
        "income", "rent", "bills", "food", "transport", "debt", "shopping",
        "budget_limit", "total_debt_input", "extra_payment_input", "interest_rate_input"
    ]
    for key in input_keys:
        if key in st.session_state:
            st.session_state[key] = None

    st.session_state.monthly_budget = 0
    add_notification("Current input data cleared", "warning")



def get_financial_health_level(score, saving_rate, debt_rate, remaining):
    if score >= 90 and saving_rate >= 25:
        return "Financial Master", "fa-crown", "You are saving strongly and your money structure looks excellent."
    if score >= 80:
        return "Wealth Builder", "fa-gem", "You are in a strong position. Keep building savings and reduce unnecessary spending."
    if score >= 60:
        return "Smart Saver", "fa-piggy-bank", "Your finances are stable, but there is still room to improve savings."
    if score >= 40:
        return "Stable Beginner", "fa-seedling", "You are managing basics, but debt/spending needs more control."
    return "Risk Zone", "fa-triangle-exclamation", "Focus on essential expenses, debt control, and building emergency savings."


def build_ai_context(income, rent, bills, food, transport, debt, shopping, total_expenses, remaining, saving_rate, debt_rate, score, month):
    return f"""
You are an AI finance assistant. Give practical, simple, safe financial suggestions.
Month: {month}
Income: €{income}
Rent: €{rent}
Bills: €{bills}
Food: €{food}
Transport: €{transport}
Debt payment: €{debt}
Shopping: €{shopping}
Total expenses: €{total_expenses}
Remaining: €{remaining}
Saving rate: {saving_rate}%
Debt rate: {debt_rate}%
Financial score: {score}/100
Do not give risky investment advice. Give clear budgeting suggestions.
"""


def ask_ollama(prompt, model="llama3.2"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=90
        )
        if response.status_code == 200:
            return response.json().get("response", "No response from Ollama.").strip()
        return f"Ollama error: {response.status_code}. Make sure Ollama is running and the model name is correct."
    except Exception as e:
        return f"Ollama is not connected. Start Ollama first, then try again. Details: {e}"


def read_uploaded_receipt(uploaded_file):
    if uploaded_file is None:
        return ""
    try:
        name = uploaded_file.name.lower()
        if name.endswith('.csv'):
            df_upload = pd.read_csv(uploaded_file)
            return df_upload.head(50).to_string(index=False)
        if name.endswith('.txt'):
            return uploaded_file.read().decode('utf-8', errors='ignore')[:5000]
        return f"Uploaded file: {uploaded_file.name}. Direct text extraction is supported for CSV/TXT in this version."
    except Exception as e:
        return f"Could not read uploaded receipt: {e}"


def generate_monthly_pdf(month, income, total_expenses, remaining, saving_rate, debt_rate, score, health_level, rent, bills, food, transport, debt, shopping):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('ModernTitle', parent=styles['Title'], fontSize=24, leading=30, textColor=colors.HexColor('#0f172a'), spaceAfter=14)
    sub_style = ParagraphStyle('Sub', parent=styles['BodyText'], fontSize=11, leading=16, textColor=colors.HexColor('#475569'))
    story = []
    story.append(Paragraph('AI Finance Monthly Report', title_style))
    story.append(Paragraph(f'Month: <b>{month}</b> | Financial Health: <b>{health_level}</b>', sub_style))
    story.append(Spacer(1, 18))
    summary = [
        ['Metric', 'Value'],
        ['Income', f'€{income:,.0f}'],
        ['Total Expenses', f'€{total_expenses:,.0f}'],
        ['Remaining', f'€{remaining:,.0f}'],
        ['Saving Rate', f'{saving_rate}%'],
        ['Debt Rate', f'{debt_rate}%'],
        ['AI Score', f'{score}/100'],
    ]
    table = Table(summary, colWidths=[2.4*inch, 3.4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8fafc')),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(table)
    story.append(Spacer(1, 18))
    story.append(Paragraph('Expense Breakdown', styles['Heading2']))
    breakdown = [['Category', 'Amount'], ['Rent', f'€{rent:,.0f}'], ['Bills', f'€{bills:,.0f}'], ['Food', f'€{food:,.0f}'], ['Transport', f'€{transport:,.0f}'], ['Debt', f'€{debt:,.0f}'], ['Shopping', f'€{shopping:,.0f}']]
    table2 = Table(breakdown, colWidths=[2.4*inch, 3.4*inch])
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(table2)
    story.append(Spacer(1, 18))
    story.append(Paragraph('AI Suggestions', styles['Heading2']))
    suggestions = []
    if saving_rate < 20:
        suggestions.append('Try to increase your saving rate toward 20% by reducing flexible categories like shopping or eating out.')
    if debt_rate > 30:
        suggestions.append('Debt payment is high compared with income. Focus on debt reduction before adding new expenses.')
    if remaining < 0:
        suggestions.append('Your expenses are higher than income. Create a strict essential-only budget for the next month.')
    if not suggestions:
        suggestions.append('Your finance situation looks healthy. Keep saving consistently and build an emergency fund.')
    for item in suggestions:
        story.append(Paragraph(f'• {item}', sub_style))
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:20px;">
        <div class="side-icon purple" style="width:44px;height:44px;"><i class="fa-solid fa-wallet" style="font-size:22px;"></i></div>
        <div>
            <div style="font-size:20px;font-weight:900;">Finance Input</div>
            <div style="color:#64748b;font-size:12px;">Enter your monthly finance data</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div class="month-title-row">
        <div class="month-title-icon"><i class="fa-solid fa-calendar-days"></i></div>
        <div>
            <div class="month-title-text">Month</div>
            <div class="month-title-sub">Choose the month for this record</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    month_options = get_month_options()
    selected_month = st.selectbox(
        "Month",
        options=month_options,
        index=0,
        key="selected_month",
        label_visibility="collapsed"
    )
    
    income = sidebar_input("fa-money-bill-wave", "green", "Monthly Income", "income", "Monthly Income")
    rent = sidebar_input("fa-house", "purple", "Rent", "rent", "Rent")
    bills = sidebar_input("fa-file-invoice", "blue", "Bills", "bills", "Bills")
    food = sidebar_input("fa-utensils", "green", "Food", "food", "Food")
    transport = sidebar_input("fa-car", "orange", "Transport", "transport", "Transport")
    debt = sidebar_input("fa-credit-card", "red", "Debt Payment", "debt", "Debt Payment")
    shopping = sidebar_input("fa-bag-shopping", "pink", "Shopping", "shopping", "Shopping")
    
    st.markdown("---")
    
    # Monthly Budget Setting
    st.markdown("""
    <div class="budget-title-row">
        <div class="budget-title-icon"><i class="fa-solid fa-bullseye"></i></div>
        <div>
            <div class="budget-title-text">Monthly Budget Limit</div>
            <div class="budget-title-sub">Set your monthly spending target</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    monthly_budget_limit = st.number_input("Set monthly budget limit (€)", min_value=0, value=st.session_state.monthly_budget, step=100, key="budget_limit")
    st.session_state.monthly_budget = monthly_budget_limit

    if st.button("Clear Data", icon=":material/delete_sweep:", use_container_width=True, on_click=clear_current_data):
        with st.spinner("Clearing data..."):
            time.sleep(0.4)
        st.success("Current input data cleared.")
        st.rerun()
    
    st.markdown("---")
    
    # Save button for monthly history
    if st.button("Save This Month's Data", icon=":material/save:", use_container_width=True):
        if income > 0:
            with st.spinner("Saving monthly data..."):
                time.sleep(0.5)
                total_expenses_calc = rent + bills + food + transport + debt + shopping
                remaining_calc = income - total_expenses_calc
                saving_rate_calc = round((remaining_calc / income) * 100, 1) if income else 0
                save_monthly_data(selected_month, income, rent, bills, food, transport, debt, shopping, total_expenses_calc, remaining_calc, saving_rate_calc)
                add_notification(f"Data saved for {selected_month}!", "success")
            st.rerun()
        else:
            st.warning("Please enter your income before saving.")
            
    
    # Export PDF report button
    pdf_report = generate_history_pdf_report()
    if pdf_report:
        st.download_button(
            label="Download History PDF Report",
            icon=":material/picture_as_pdf:",
            data=pdf_report,
            file_name=f"finance_history_report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    st.markdown("""
    <div class="tip-box">
        <i class="fa-solid fa-lightbulb"></i> <strong>Pro Tips</strong><br>
        • Set a monthly budget to track overspending<br>
        • Save data monthly to see your progress<br>
        • Download a professional PDF report
    </div>
    """, unsafe_allow_html=True)


total_expenses = rent + bills + food + transport + debt + shopping
remaining = income - total_expenses
saving_rate = round((remaining / income) * 100, 1) if income else 0
debt_rate = round((debt / income) * 100, 1) if income else 0

score = 0 if income == 0 else 100

if income:
    if remaining < 0:
        score -= 40
    if saving_rate < 10:
        score -= 20
    if debt_rate > 30:
        score -= 25

score = max(0, min(100, score))
health_level, health_icon, health_message = get_financial_health_level(score, saving_rate, debt_rate, remaining)


if hasattr(st, "dialog"):
    @st.dialog("Ollama Finance AI", width="large")
    def open_ai_chatbot_dialog():
        st.markdown(f"""
        <div class="ai-modal-hero-modern">
            <div class="ai-modal-badge-modern"><i class="fa-solid fa-wand-magic-sparkles"></i> AI Finance Assistant</div>
            <div class="ai-modal-title-modern">Ask AI about your money</div>
            <div class="ai-modal-sub-modern">Get smart budget advice, debt suggestions, savings guidance, or upload a receipt / CSV / TXT file for quick financial analysis.</div>
            <div class="ai-modal-stats-modern">
                <div class="ai-modal-stat-modern"><div class="ai-modal-stat-label-modern">Income</div><div class="ai-modal-stat-value-modern">€{income:,.0f}</div></div>
                <div class="ai-modal-stat-modern"><div class="ai-modal-stat-label-modern">Expenses</div><div class="ai-modal-stat-value-modern">€{total_expenses:,.0f}</div></div>
                <div class="ai-modal-stat-modern"><div class="ai-modal-stat-label-modern">Remaining</div><div class="ai-modal-stat-value-modern">€{remaining:,.0f}</div></div>
                <div class="ai-modal-stat-modern"><div class="ai-modal-stat-label-modern">AI Score</div><div class="ai-modal-stat-value-modern">{score}/100</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab_chat, tab_upload, tab_snapshot = st.tabs(["Ask AI", "Receipt / Data", "Finance Snapshot"])
        receipt_text_top = ""

        with tab_chat:
            st.markdown("""
            <div class="ai-panel-modern">
                <div class="ai-panel-title-modern"><i class="fa-solid fa-comments"></i> Smart finance question</div>
                <div class="ai-panel-sub-modern">Ask anything about your budget, debt, expenses, saving plan, or monthly progress.</div>
            </div>
            """, unsafe_allow_html=True)
            st.text_input("Ollama model", value="llama3.2", placeholder="Example: llama3.2, llama3, mistral", key="ollama_model_modal")
            st.text_area("Your question", placeholder="Example: How can I save more money this month?", height=150, key="ai_user_question_modal")
            st.markdown("""
            <div class="ai-suggestion-grid-modern">
                <div class="ai-suggestion-card-modern"><i class="fa-solid fa-piggy-bank"></i> How can I save more this month?</div>
                <div class="ai-suggestion-card-modern"><i class="fa-solid fa-credit-card"></i> Is my debt payment too high?</div>
                <div class="ai-suggestion-card-modern"><i class="fa-solid fa-chart-line"></i> What should I improve first?</div>
            </div>
            """, unsafe_allow_html=True)

        with tab_upload:
            st.markdown("""
            <div class="ai-panel-modern">
                <div class="ai-panel-title-modern"><i class="fa-solid fa-receipt"></i> Upload receipt or bank data</div>
                <div class="ai-panel-sub-modern">Upload a CSV or TXT file. Ollama will analyze spending patterns and suggest improvements.</div>
            </div>
            """, unsafe_allow_html=True)
            uploaded_receipt_top = st.file_uploader("Upload receipt / bank CSV / TXT", type=["csv", "txt"], key="receipt_upload_modal")
            receipt_text_top = read_uploaded_receipt(uploaded_receipt_top)
            if receipt_text_top:
                st.success("Receipt/data loaded successfully.")
                with st.expander("Preview uploaded data"):
                    st.text(receipt_text_top[:2000])

        with tab_snapshot:
            st.markdown(f"""
            <div class="ai-panel-modern">
                <div class="ai-panel-title-modern"><i class="fa-solid fa-chart-simple"></i> Current financial snapshot</div>
                <div class="ai-panel-sub-modern">This is the context Ollama will use for your advice.</div>
                <div class="ai-suggestion-grid-modern">
                    <div class="ai-suggestion-card-modern"><i class="fa-solid fa-calendar"></i> Month: {selected_month}</div>
                    <div class="ai-suggestion-card-modern"><i class="fa-solid fa-scale-balanced"></i> Saving rate: {saving_rate}%</div>
                    <div class="ai-suggestion-card-modern"><i class="fa-solid fa-heart-pulse"></i> Health: {health_level}</div>
                    <div class="ai-suggestion-card-modern"><i class="fa-solid fa-house"></i> Rent: €{rent:,.0f}</div>
                    <div class="ai-suggestion-card-modern"><i class="fa-solid fa-utensils"></i> Food: €{food:,.0f}</div>
                    <div class="ai-suggestion-card-modern"><i class="fa-solid fa-bag-shopping"></i> Shopping: €{shopping:,.0f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        btn_left, btn_right = st.columns([2, 1])
        with btn_left:
            ask_clicked = st.button("Generate Professional AI Advice", icon=":material/auto_awesome:", use_container_width=True, key="ask_ollama_modal")
        with btn_right:
            clear_clicked = st.button("Clear Chat", icon=":material/refresh:", use_container_width=True, key="clear_ai_modal_fields")

        if clear_clicked:
            st.info("Please select the question text and delete it, then ask again.")

        user_question_top = st.session_state.get("ai_user_question_modal", "")
        ollama_model_top = st.session_state.get("ollama_model_modal", "llama3.2")
        uploaded_state_file = st.session_state.get("receipt_upload_modal")
        if uploaded_state_file and not receipt_text_top:
            receipt_text_top = read_uploaded_receipt(uploaded_state_file)

        if ask_clicked:
            if not user_question_top and not receipt_text_top:
                st.warning("Please write a question or upload a receipt/CSV/TXT first.")
            else:
                context_top = build_ai_context(income, rent, bills, food, transport, debt, shopping, total_expenses, remaining, saving_rate, debt_rate, score, selected_month)
                full_prompt_top = f"""{context_top}
User question: {user_question_top}
Uploaded receipt/bank data:
{receipt_text_top}

Analyze the user's situation. Give:
1. Short summary
2. Problems detected
3. Practical suggestions
4. Simple action plan
Use clear English and bullet points.
"""
                with st.spinner("Ollama is thinking and preparing your financial advice..."):
                    answer_top = ask_ollama(full_prompt_top, ollama_model_top)
                answer_html = answer_top.replace(chr(10), "<br>")
                st.markdown("<div class='ai-answer-modern'><div class='ai-answer-title-modern'><i class='fa-solid fa-sparkles'></i> AI Financial Advice</div>" + answer_html + "</div>", unsafe_allow_html=True)
else:
    def open_ai_chatbot_dialog():
        st.info("Your Streamlit version does not support pop-up dialogs. Please update Streamlit: pip install --upgrade streamlit")

# Budget Alert
if st.session_state.monthly_budget > 0 and total_expenses > st.session_state.monthly_budget:
    st.markdown(f"""
    <div class="budget-alert">
        <i class="fa-solid fa-circle-exclamation"></i> <strong>Budget Alert!</strong><br>
        Your expenses (€{total_expenses:,.0f}) exceed your monthly budget limit (€{st.session_state.monthly_budget:,.0f}) by <strong>€{total_expenses - st.session_state.monthly_budget:,.0f}</strong>!
    </div>
    """, unsafe_allow_html=True)

hero_left, hero_right = st.columns([2.65, 1.15], vertical_alignment="top")

with hero_left:
    st.markdown('<div class="hero-title">AI Finance Debt Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Track your finances, get AI insights, and monitor your monthly progress.</div>', unsafe_allow_html=True)

with hero_right:
    st.markdown("""
    <div class="top-ai-compact-card">
        <div class="top-ai-compact-kicker">
            <i class="fa-solid fa-wand-magic-sparkles"></i> AI Assistant
        </div>
        <div class="top-ai-compact-title">Ollama Finance AI</div>
        <div class="top-ai-compact-sub">Smart chat, receipt review, and personal money advice.</div>
        <div class="ai-button-spacer"></div>
    """, unsafe_allow_html=True)

    if st.button("Ask AI", icon=":material/smart_toy:", use_container_width=True, key="open_ai_modal_btn"):
        open_ai_chatbot_dialog()

    st.markdown("</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("fa-wallet", "purple", "#7c3aed", "Income", f"€{income:,.0f}", "Monthly income")

with col2:
    metric_card("fa-receipt", "blue", "#2563eb", "Expenses", f"€{total_expenses:,.0f}", "Total expenses")

with col3:
    metric_card("fa-piggy-bank", "green", "#16a34a", "Remaining", f"€{remaining:,.0f}", f"Saving rate: {saving_rate}%")

with col4:
    badge_text = "Excellent" if score >= 80 else "Good" if score >= 60 else "Fair" if score >= 40 else "Poor"
    metric_card("fa-brain", "orange", "#f97316", "AI Score", f"{score}/100", "", badge_text)

st.markdown(f"""
<div class="health-card">
    <div class="health-top">
        <div>
            <div class="health-title"><i class="fa-solid {health_icon}"></i> Financial Health Level</div>
            <div class="health-sub">{health_message}</div>
        </div>
        <div class="health-level-badge">{health_level} · {score}/100</div>
    </div>
    <div class="health-progress"><div class="health-progress-bar" style="width:{score}%;"></div></div>
    <div class="health-tips">
        <div class="health-tip"><i class="fa-solid fa-piggy-bank"></i> Save first, spend after.</div>
        <div class="health-tip"><i class="fa-solid fa-bullseye"></i> Keep a clear monthly limit.</div>
        <div class="health-tip"><i class="fa-solid fa-bolt"></i> Reduce high-risk spending.</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="quick-summary-card">
    <div class="quick-summary-title"><i class="fa-solid fa-clipboard-list"></i> Smart Monthly Summary</div>
    <div class="quick-summary-sub">Clean overview of this month based on your income, spending, saving rate, and debt pressure.</div>
    <div class="quick-summary-grid">
        <div class="quick-summary-item">
            <div class="quick-summary-item-label">Main Status</div>
            <div class="quick-summary-item-value">{health_level}</div>
        </div>
        <div class="quick-summary-item">
            <div class="quick-summary-item-label">Best Focus</div>
            <div class="quick-summary-item-value">{('Keep saving' if saving_rate >= 20 else 'Increase savings')}</div>
        </div>
        <div class="quick-summary-item">
            <div class="quick-summary-item-label">Risk Area</div>
            <div class="quick-summary-item-value">{('Debt pressure' if debt_rate > 30 else 'Controlled')}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# Savings Goal Tracker
if income > 0 and remaining > 0:
    st.markdown("""
    <div class="goal-modern-wrap">
        <div class="goal-modern-head">
            <div class="goal-modern-icon"><i class="fa-solid fa-bullseye"></i></div>
            <div>
                <div class="goal-modern-title">Savings Goal Tracker</div>
                <div class="goal-modern-sub">Track your annual savings goal with a cleaner modern progress design.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    savings_goal = st.number_input(
        "Set your savings goal (€)",
        min_value=0,
        value=st.session_state.savings_goal,
        step=1000,
        key="savings_goal_input"
    )
    st.session_state.savings_goal = savings_goal

    if savings_goal > 0:
        progress = min(100, int((remaining * 12) / savings_goal * 100))
        months_to_goal = round(savings_goal / remaining, 1) if remaining > 0 else 0
        annual_savings = remaining * 12
        col_goal1, col_goal2 = st.columns([2, 1])

        with col_goal1:
            st.markdown(f"""
            <div class="goal-modern-card">
                <div class="goal-modern-label"><i class="fa-solid fa-chart-line" style="color:#2563eb;"></i> Annual Savings Progress</div>
                <div class="goal-modern-value">€{annual_savings:,.0f} / €{savings_goal:,.0f}</div>
                <div class="goal-modern-progress">
                    <div class="goal-modern-progress-bar" style="width:{progress}%;"></div>
                </div>
                <div class="goal-modern-foot">
                    <span>{progress}% toward your goal</span>
                    <span><i class="fa-solid fa-piggy-bank"></i> Monthly saved: €{remaining:,.0f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_goal2:
            st.markdown(f"""
            <div class="goal-time-card">
                <div class="goal-time-icon"><i class="fa-solid fa-hourglass-half"></i></div>
                <div class="goal-time-label">Estimated time to reach goal</div>
                <div class="goal-time-value">{months_to_goal}</div>
                <div class="goal-time-note">months at current savings rate</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


selected = option_menu(
    menu_title=None,
    options=["Dashboard", "AI Solver", "Debt Planner", "Monthly History"],
    icons=["pie-chart-fill", "robot", "graph-up-arrow", "calendar-check"],
    orientation="horizontal",
    default_index=0,
    styles={
        "container": {
            "padding": "10px",
            "margin-top": "28px",
            "margin-bottom": "22px",
            "background-color": "#ffffff",
            "border": "1px solid #e5e7eb",
            "border-radius": "22px",
            "box-shadow": "0 16px 40px rgba(15, 23, 42, 0.07)",
        },
        "icon": {
            "font-size": "20px",
            "margin-right": "8px",
        },
        "nav-link": {
            "font-size": "16px",
            "font-weight": "900",
            "color": "#334155",
            "padding": "15px 34px",
            "border-radius": "17px",
            "margin": "0 8px",
        },
        "nav-link-selected": {
            "background": "linear-gradient(135deg, #1e293b, #0f172a)",
            "color": "#ffffff",
            "box-shadow": "none",
        },
    }
)

df = pd.DataFrame({
    "Category": ["Rent", "Food", "Debt Payment", "Bills", "Shopping", "Transport"],
    "Amount": [rent, food, debt, bills, shopping, transport],
    "Color": ["#7c3aed", "#3b82f6", "#22c55e", "#f97316", "#ef4444", "#fbbf24"]
})
df = df[df["Amount"] > 0]


if selected == "Dashboard":
    with st.container(border=True):
        section_header("fa-chart-pie", "blue", "Expense Overview", "Breakdown of your monthly expenses")

        if df.empty:
            st.info("Please fill the input fields from the sidebar to see your expense chart.")
        else:
            left, right = st.columns([1.15, 1])

            with left:
                fig = go.Figure(data=[go.Pie(
                    labels=df["Category"],
                    values=df["Amount"],
                    hole=0.56,
                    marker=dict(colors=df["Color"], line=dict(color="white", width=3)),
                    textinfo="percent",
                    textfont=dict(color="white", size=14),
                    sort=False
                )])

                fig.add_annotation(
                    text=f"<b>€{total_expenses:,.0f}</b><br><span style='font-size:13px;color:#64748b'>Total Expenses</span>",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=24, color="#0f172a")
                )

                fig.update_layout(
                    height=390,
                    showlegend=False,
                    margin=dict(t=0, b=0, l=0, r=0),
                    paper_bgcolor="white",
                    plot_bgcolor="white"
                )

                st.plotly_chart(fig, use_container_width=True)

            with right:
                st.write("")
                for _, row in df.iterrows():
                    percent = round((row["Amount"] / total_expenses) * 100, 1)
                    st.markdown(f"""
                    <div class="legend-row">
                        <div class="legend-left">
                            <span class="dot" style="background:{row['Color']};"></span>
                            <span>{row['Category']}</span>
                        </div>
                        <div>€{row['Amount']:,.0f}</div>
                        <div>{percent}%</div>
                    </div>
                    """, unsafe_allow_html=True)


elif selected == "AI Solver":
    with st.container(border=True):
        section_header("fa-robot", "purple", "AI Financial Solver", "Smart recommendation based on your money situation")

        if income == 0:
            st.info("Please enter your monthly income first.")
        else:
            if score >= 80:
                title = "Excellent Financial Health!"
                msg = "Your financial health looks strong. Keep saving monthly and build your emergency fund. Consider investing for long-term growth."
                icon = "fa-circle-check"
            elif score >= 50:
                title = "Moderate Risk Level"
                msg = "Your financial health is medium. Reduce unnecessary expenses and improve your saving rate to build a stronger financial cushion."
                icon = "fa-triangle-exclamation"
            else:
                title = "Critical Risk Alert"
                msg = "Your financial health is risky. Focus on rent, bills, food and debt first. Consider creating a strict budget and exploring additional income sources."
                icon = "fa-circle-exclamation"

            st.markdown(f"""
            <div class="advice-green">
                <div style="display:flex;gap:14px;align-items:flex-start;">
                    <div class="side-icon green"><i class="fa-solid {icon}"></i></div>
                    <div>
                        <div style="font-size:18px;font-weight:900;color:#0f172a;">{title}</div>
                        <div style="color:#0f172a;line-height:1.7;margin-top:8px;">{msg}</div>
                    </div>
                </div>
            </div>

            <div class="ratio-box">
                <div style="display:flex;justify-content:space-between;margin-bottom:12px;">
                    <b><i class="fa-solid fa-piggy-bank" style="color:#16a34a;"></i> Saving Rate</b>
                    <b style="color:#16a34a;">{saving_rate}%</b>
                </div>
                <div style="display:flex;justify-content:space-between;">
                    <b><i class="fa-solid fa-credit-card" style="color:#ef4444;"></i> Debt Rate</b>
                    <b>{debt_rate}%</b>
                </div>
            </div>
            """, unsafe_allow_html=True)


elif selected == "Debt Planner":
    with st.container(border=True):
        section_header("fa-chart-line", "green", "Debt Payoff Planner", "Calculate how fast you can finish your debt")

        st.markdown("""
        <div class="debt-hero-card">
            <div class="debt-hero-title"><i class="fa-solid fa-route"></i> Smart Debt Payoff Plan</div>
            <div class="debt-hero-sub">Add your total debt, extra payment, and interest rate to see a clean payoff overview.</div>
        </div>
        """, unsafe_allow_html=True)

        debt_col1, debt_col2, debt_col3 = st.columns(3)

        with debt_col1:
            st.markdown("""
            <div class="debt-modern-input-card">
                <div class="debt-modern-input-head">
                    <div class="debt-modern-input-icon red"><i class="fa-solid fa-credit-card"></i></div>
                    <div>
                        <div class="debt-modern-input-title">Total Debt</div>
                        <div class="debt-modern-input-sub">Full amount you still owe</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            total_debt = st.number_input("Total Debt (€)", min_value=0, value=None, step=100, key="total_debt_input", placeholder="Total Debt") or 0
            st.markdown("</div>", unsafe_allow_html=True)

        with debt_col2:
            st.markdown("""
            <div class="debt-modern-input-card">
                <div class="debt-modern-input-head">
                    <div class="debt-modern-input-icon green"><i class="fa-solid fa-circle-plus"></i></div>
                    <div>
                        <div class="debt-modern-input-title">Extra Payment</div>
                        <div class="debt-modern-input-sub">Extra amount per month</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            extra_payment = st.number_input("Extra Monthly Payment (€)", min_value=0, value=None, step=50, key="extra_payment_input", placeholder="Extra Payment") or 0
            st.markdown("</div>", unsafe_allow_html=True)

        with debt_col3:
            st.markdown("""
            <div class="debt-modern-input-card">
                <div class="debt-modern-input-head">
                    <div class="debt-modern-input-icon orange"><i class="fa-solid fa-percent"></i></div>
                    <div>
                        <div class="debt-modern-input-title">Interest Rate</div>
                        <div class="debt-modern-input-sub">Yearly interest percentage</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            interest_rate = st.number_input("Interest Rate (%)", min_value=0, value=None, step=1, key="interest_rate_input", placeholder="Interest Rate") or 0
            st.markdown("</div>", unsafe_allow_html=True)

        monthly_payment = debt + extra_payment

        if total_debt > 0 and monthly_payment > 0:
            monthly_rate = (interest_rate / 100) / 12 if interest_rate > 0 else 0
            balance = float(total_debt)
            months_count = 0
            total_interest = 0.0

            while balance > 0 and months_count < 600:
                interest_amount = balance * monthly_rate
                total_interest += interest_amount
                balance = balance + interest_amount - monthly_payment
                months_count += 1

            months = months_count if months_count < 600 else 600
            years = months // 12
            remaining_months = months % 12
            total_paid = total_debt + total_interest

            st.markdown(f"""
            <div class="debt-result-grid">
                <div class="debt-result-card">
                    <div class="debt-result-label"><i class="fa-solid fa-calendar-check" style="color:#2563eb;"></i> Payoff Timeline</div>
                    <div class="debt-result-value">{months} months</div>
                    <div class="debt-result-note">{years} years {remaining_months} months</div>
                </div>
                <div class="debt-result-card">
                    <div class="debt-result-label"><i class="fa-solid fa-money-bill-wave" style="color:#16a34a;"></i> Monthly Payment</div>
                    <div class="debt-result-value">€{monthly_payment:,.0f}</div>
                    <div class="debt-result-note">Debt payment + extra payment</div>
                </div>
                <div class="debt-result-card">
                    <div class="debt-result-label"><i class="fa-solid fa-percent" style="color:#f97316;"></i> Total Interest</div>
                    <div class="debt-result-value">€{total_interest:,.0f}</div>
                    <div class="debt-result-note">Estimated interest until payoff</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if extra_payment > 0 and debt > 0:
                base_monthly_rate = monthly_rate
                base_balance = float(total_debt)
                base_months = 0
                while base_balance > 0 and base_months < 600:
                    base_balance = base_balance + (base_balance * base_monthly_rate) - debt
                    base_months += 1
                months_saved = max(0, base_months - months)
                if months_saved > 0:
                    st.markdown(f"""
                    <div class="debt-payoff-banner">
                        <i class="fa-solid fa-bolt"></i> By adding €{extra_payment:,.0f} extra each month, you can save about {months_saved} months.
                    </div>
                    """, unsafe_allow_html=True)
        elif total_debt > 0 and monthly_payment == 0:
            st.warning("Please enter your current debt payment in the sidebar or add an extra payment.")
        else:
            st.info("Enter debt information to calculate payoff time.")

elif selected == "Monthly History":
    with st.container(border=True):
        section_header("fa-calendar-check", "blue", "Monthly Financial History", "Track your savings and spending patterns over time")
        
        if not st.session_state.monthly_history:
            st.info("No data saved yet. Fill in your monthly finances in the sidebar and click 'Save This Month's Data' to start tracking your history.")
        else:
            history_df = pd.DataFrame(st.session_state.monthly_history)
            history_df['date'] = pd.to_datetime(history_df['date'])
            history_df = history_df.sort_values('date')

            avg_saving = history_df['saving_rate'].mean()
            best_month = history_df.loc[history_df['saving_rate'].idxmax()]
            avg_remaining = history_df['remaining'].mean()
            total_saved = history_df['remaining'].sum()
            latest_saving = history_df['saving_rate'].iloc[-1]
            first_saving = history_df['saving_rate'].iloc[0]
            trend_text = "Improving" if latest_saving > first_saving else "Needs review"
            trend_icon = "fa-arrow-trend-up" if latest_saving > first_saving else "fa-arrow-trend-down"
            trend_color = "green" if latest_saving > first_saving else "orange"

            st.markdown(f"""
            <div class="history-modern-hero">
                <div class="history-hero-title"><i class="fa-solid fa-chart-line"></i> Your Monthly Finance Progress</div>
                <div class="history-hero-sub">A clean overview of your saved monthly income, expenses, savings, and budget behavior.</div>
            </div>
            """, unsafe_allow_html=True)
            
            col_trend1, col_trend2, col_trend3, col_trend4 = st.columns(4)
            
            with col_trend1:
                st.markdown(f"""
                <div class="history-summary-card">
                    <div class="history-summary-icon green"><i class="fa-solid fa-piggy-bank"></i></div>
                    <div class="history-summary-label">Avg Savings Rate</div>
                    <div class="history-summary-value">{avg_saving:.1f}%</div>
                    <div class="history-summary-note"><i class="fa-solid {trend_icon}"></i> {trend_text}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_trend2:
                st.markdown(f"""
                <div class="history-summary-card">
                    <div class="history-summary-icon orange"><i class="fa-solid fa-trophy"></i></div>
                    <div class="history-summary-label">Best Month</div>
                    <div class="history-summary-value" style="font-size:20px;">{best_month['month']}</div>
                    <div class="history-summary-note">Saving: {best_month['saving_rate']:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_trend3:
                st.markdown(f"""
                <div class="history-summary-card">
                    <div class="history-summary-icon blue"><i class="fa-solid fa-wallet"></i></div>
                    <div class="history-summary-label">Avg Remaining</div>
                    <div class="history-summary-value">€{avg_remaining:,.0f}</div>
                    <div class="history-summary-note">per month</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_trend4:
                st.markdown(f"""
                <div class="history-summary-card">
                    <div class="history-summary-icon purple"><i class="fa-solid fa-sack-dollar"></i></div>
                    <div class="history-summary-label">Total Saved</div>
                    <div class="history-summary-value">€{total_saved:,.0f}</div>
                    <div class="history-summary-note">over all months</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div style="height:26px;"></div>', unsafe_allow_html=True)
            section_header("fa-chart-column", "blue", "Income vs Expenses", "Compare your monthly income and spending side by side")
            
            fig_compare = go.Figure()
            fig_compare.add_trace(go.Bar(
                x=history_df['month'],
                y=history_df['income'],
                name='Income',
                marker_color='#3b82f6',
                marker_line_width=0
            ))
            fig_compare.add_trace(go.Bar(
                x=history_df['month'],
                y=history_df['expenses'],
                name='Expenses',
                marker_color='#ef4444',
                marker_line_width=0
            ))
            fig_compare.update_layout(
                height=390,
                xaxis_title="Month",
                yaxis_title="Amount (€)",
                barmode='group',
                template="plotly_white",
                margin=dict(t=20, b=20, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_compare, use_container_width=True)
            
            section_header("fa-list-check", "purple", "Monthly Breakdown", "Detailed records for each saved month")
            
            for record in st.session_state.monthly_history:
                if record['saving_rate'] >= 20:
                    status = "Excellent Saving Month"
                    badge_class = "badge-success"
                    status_icon = 'fa-piggy-bank'
                    status_color = 'green'
                    accent_color = '#16a34a'
                elif record['saving_rate'] >= 10:
                    status = "Good Month"
                    badge_class = "badge-warning"
                    status_icon = 'fa-chart-line'
                    status_color = 'orange'
                    accent_color = '#ea580c'
                else:
                    status = "High Spending Month"
                    badge_class = "badge-danger"
                    status_icon = 'fa-triangle-exclamation'
                    status_color = 'red'
                    accent_color = '#dc2626'
                
                st.html(f"""
                <div class="modern-history-card" style="border-top:4px solid {accent_color};">
                    <div class="modern-history-top">
                        <div class="modern-history-month-wrap">
                            <div class="modern-history-icon {status_color}"><i class="fa-solid {status_icon}"></i></div>
                            <div>
                                <div class="modern-history-month">{record['month']}</div>
                                <div class="modern-history-small">Saved record overview</div>
                            </div>
                        </div>
                        <span class="{badge_class}">{status}</span>
                    </div>

                    <div class="modern-history-grid">
                        <div class="modern-history-mini">
                            <div class="modern-history-mini-label"><i class="fa-solid fa-wallet" style="color:#2563eb;"></i> Income</div>
                            <div class="modern-history-mini-value">€{record['income']:,.0f}</div>
                        </div>
                        <div class="modern-history-mini">
                            <div class="modern-history-mini-label"><i class="fa-solid fa-receipt" style="color:#ef4444;"></i> Expenses</div>
                            <div class="modern-history-mini-value">€{record['expenses']:,.0f}</div>
                        </div>
                        <div class="modern-history-mini">
                            <div class="modern-history-mini-label"><i class="fa-solid fa-piggy-bank" style="color:#16a34a;"></i> Saved</div>
                            <div class="modern-history-mini-value">€{record['remaining']:,.0f}</div>
                        </div>
                        <div class="modern-history-mini">
                            <div class="modern-history-mini-label"><i class="fa-solid fa-chart-simple" style="color:#7c3aed;"></i> Saving Rate</div>
                            <div class="modern-history-mini-value">{record['saving_rate']}%</div>
                        </div>
                    </div>

                    <div class="modern-history-breakdown">
                        <strong><i class="fa-solid fa-layer-group"></i> Breakdown</strong><br>
                        <span class="history-breakdown-pill"><i class="fa-solid fa-house" style="color:#7c3aed;"></i> Rent €{record['rent']}</span>
                        <span class="history-breakdown-pill"><i class="fa-solid fa-utensils" style="color:#16a34a;"></i> Food €{record['food']}</span>
                        <span class="history-breakdown-pill"><i class="fa-solid fa-credit-card" style="color:#ef4444;"></i> Debt €{record['debt']}</span>
                        <span class="history-breakdown-pill"><i class="fa-solid fa-file-invoice" style="color:#2563eb;"></i> Bills €{record['bills']}</span>
                        <span class="history-breakdown-pill"><i class="fa-solid fa-bag-shopping" style="color:#ec4899;"></i> Shopping €{record['shopping']}</span>
                        <span class="history-breakdown-pill"><i class="fa-solid fa-car" style="color:#f97316;"></i> Transport €{record.get('transport', 0)}</span>
                    </div>
                </div>
                """)
            
            st.markdown("---")
            if st.button("Clear All History", icon=":material/delete:", use_container_width=True):
                with st.spinner("Clearing history..."):
                    time.sleep(0.4)
                    st.session_state.monthly_history = []
                    add_notification("History cleared", "warning")
                st.rerun()
