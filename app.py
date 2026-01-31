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

st.set_page_config(page_title="Student Life Balance Tracker", layout="centered")

# =========================
# Sidebar Navigation
# =========================
st.sidebar.title("🎓 Life Balance Tracker")
page = st.sidebar.radio("Navigation", [
    "🏠 Home",
    "📊 Dashboard",
    "📂 History",
    "🧠 Insights"
])

# Shared session state
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "latest_data" not in st.session_state:
    st.session_state.latest_data = None

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
            tips = advice_generator(study, sleep, social, screen, stress)

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

            # Save in session
            st.session_state.student_name = student_name
            st.session_state.latest_data = data

            st.success("✅ Data saved successfully!")
            st.info("Go to the Dashboard to view your results 📊")

# =========================
# DASHBOARD PAGE
# =========================
elif page == "📊 Dashboard":
    st.title("📊 Personal Dashboard")

    if st.session_state.latest_data is None:
        st.warning("No data yet. Please enter data on the Home page.")
    else:
        data = st.session_state.latest_data

        st.metric("🧠 Balance Score", f"{data['Balance Score']}/100")
        st.write(f"**Mental Wellness Status:** {data['Mental State']}")

        st.subheader("💡 Advice")
        tips = advice_generator(
            data["Study Hours"],
            data["Sleep Hours"],
            data["Social Hours"],
            data["Screen Hours"],
            data["Stress Level"]
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

            st.metric("📊 Average Balance Score", f"{avg_score:.1f}")
            st.metric("😴 Avg Sleep Hours", f"{avg_sleep:.1f}")
            st.metric("😖 Avg Stress Level", f"{avg_stress:.1f}")
            st.metric("📱 Avg Screen Time", f"{avg_screen:.1f}")

            st.subheader("🔍 Behavioral Insights")

            if avg_sleep < 6:
                st.write("⚠️ Chronic sleep deprivation detected.")
            if avg_stress > 6:
                st.write("⚠️ High long-term stress pattern detected.")
            if avg_screen > 7:
                st.write("⚠️ Excessive screen dependency detected.")
            if avg_score > 75:
                st.write("✅ Strong life balance pattern detected.")

            st.success("🧠 Insights generated from your behavioral data")

