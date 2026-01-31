# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 11:18:01 2026

@author: mbuya
"""

import streamlit as st
from datetime import datetime
import pandas as pd

from logic import calculate_balance_score, mental_state, advice_generator
from storage import save_data, load_user_data
from navigation import sidebar_navigation

st.set_page_config(page_title="Student Life Balance Tracker", layout="centered")

# =========================
# Navigation
# =========================
page = sidebar_navigation()

# =========================
# Session State
# =========================
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

# =========================
# Helper: get latest record
# =========================
def get_latest_user_record(name):
    df = load_user_data(name)
    if df is None or df.empty:
        return None
    return df.iloc[-1]   # last entry

# =========================
# HOME PAGE
# =========================
if page == "🏠 Home":
    st.title("🎓 Student Life Balance Tracker")
    st.caption("Track your daily life balance, wellness, and productivity")

    st.subheader("📥 Daily Input")

    student_name = st.text_input("Student Name", value=st.session_state.student_name)

    study = st.slider("📚 Study Hours", 0, 12, 2)
    sleep = st.slider("😴 Sleep Hours", 0, 12, 6)
    social = st.slider("🧑‍🤝‍🧑 Social Time", 0, 8, 1)
    screen = st.slider("📱 Screen Time", 0, 16, 4)
    stress = st.slider("😖 Stress Level (1–10)", 1, 10, 5)

    if st.button("Analyze My Balance"):
        if student_name.strip() == "":
            st.error("Please enter your name.")
        else:
            score = calculate_balance_score(study, sleep, social, screen, stress)
            state = mental_state(score)

            data = {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Student": student_name,
                "Study Hours": study,
                "Sleep Hours": sleep,
                "Social Hours": social,
                "Screen Hours": screen,
                "Stress Level": stress,
                "Balance Score": score,
                "Mental State": state
            }

            save_data(data)

            # save user
            st.session_state.student_name = student_name

            st.success("✅ Data saved successfully!")
            st.info("Navigate to Dashboard, History or Insights using the sidebar")

# =========================
# DASHBOARD PAGE
# =========================
elif page == "📊 Dashboard":
    st.title("📊 Personal Dashboard")

    name = st.session_state.student_name

    if name == "":
        st.warning("Enter your name on the Home page first.")
    else:
        latest = get_latest_user_record(name)

        if latest is None:
            st.info("No data yet. Add data from Home page.")
        else:
            st.metric("🧠 Balance Score", f"{latest['Balance Score']}/100")
            st.write(f"**Mental Wellness Status:** {latest['Mental State']}")

            st.subheader("💡 Advice")
            tips = advice_generator(
                latest["Study Hours"],
                latest["Sleep Hours"],
                latest["Social Hours"],
                latest["Screen Hours"],
                latest["Stress Level"]
            )
            for tip in tips:
                st.write("- " + tip)

# =========================
# HISTORY PAGE
# =========================
elif page == "📂 History":
    st.title("📂 Personal History")

    name = st.session_state.student_name

    if name == "":
        st.warning("Enter your name on the Home page first.")
    else:
        df_user = load_user_data(name)

        if df_user is None or df_user.empty:
            st.info("No history data yet.")
        else:
            st.subheader("📈 Balance Trend")
            st.line_chart(df_user.set_index("Date")["Balance Score"])

            st.subheader("📋 All Records")
            st.dataframe(df_user)

# =========================
# INSIGHTS PAGE
# =========================
elif page == "🧠 Insights":
    st.title("🧠 Life Insights")

    name = st.session_state.student_name

    if name == "":
        st.warning("Enter your name on the Home page first.")
    else:
        df_user = load_user_data(name)

        if df_user is None or len(df_user) < 2:
            st.info("Not enough data for insights yet.")
        else:
            avg_score = df_user["Balance Score"].mean()
            avg_sleep = df_user["Sleep Hours"].mean()
            avg_stress = df_user["Stress Level"].mean()
            avg_screen = df_user["Screen Hours"].mean()

            st.metric("📊 Avg Balance Score", f"{avg_score:.1f}")
            st.metric("😴 Avg Sleep", f"{avg_sleep:.1f}")
            st.metric("😖 Avg Stress", f"{avg_stress:.1f}")
            st.metric("📱 Avg Screen Time", f"{avg_screen:.1f}")

            st.subheader("🔍 Behavioral Insights")

            if avg_sleep < 6:
                st.write("⚠️ Chronic sleep deprivation pattern detected.")
            if avg_stress > 6:
                st.write("⚠️ High long-term stress pattern detected.")
            if avg_screen > 7:
                st.write("⚠️ Excessive screen dependency detected.")
            if avg_score > 75:
                st.write("✅ Strong life balance pattern detected.")

            st.success("🧠 Insights generated from your data")
