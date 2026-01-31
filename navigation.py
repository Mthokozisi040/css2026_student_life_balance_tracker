import streamlit as st

def sidebar_navigation():
    st.sidebar.title("🎓 Life Balance Tracker")
    
    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Home",
            "📊 Dashboard",
            "📂 History",
            "🧠 Insights"
        ]
    )

    return page
