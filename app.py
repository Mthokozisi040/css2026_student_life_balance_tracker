# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 11:18:01 2026

@author: mbuya
"""

import streamlit as st
from datetime import datetime

from logic import calculate_balance_score, mental_state, advice_generator
from storage import save_data, load_user_data

st.set_page_config(page_title="Student Life Balance Tracker")

st.title("Student Life Balance Tracker")
st.caption("Track your daily life balance, wellness, and productivity")

# Inputs
st.subheader("Daily Input")

student_name = st.text_input("Student Name")

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

        # Results
        st.subheader("📊 Balance Report")
        st.metric("🧠 Balance Score", f"{score}/100")
        st.write(f"**Mental Wellness Status:** {state}")

        st.subheader("💡 Advice")
        for tip in tips:
            st.write("- " + tip)

        # Save
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
        st.success("✅ Data saved")

        # Trends
        st.subheader("📈 Balance Trend")
        df_user = load_user_data(student_name)

        if df_user is not None and len(df_user) > 1:
            st.line_chart(df_user.set_index("Date")["Balance Score"])
        else:
            st.info("Add more daily entries to see trends.")

        # History
        st.subheader("📂 Your History")
        if df_user is not None:
            st.dataframe(df_user)
