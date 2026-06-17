import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Portfolio Website",
    layout="wide"
)

st.title("Portfolio Website")

if "portfolio_html" in st.session_state:
    components.html(
        st.session_state["portfolio_html"],
        height=1200,
        scrolling=True
    )
else:
    st.warning(
        "Please generate a portfolio from the Home page first."
    )
