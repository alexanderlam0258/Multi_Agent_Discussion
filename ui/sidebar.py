import streamlit as st


def render_sidebar() -> int:

    st.sidebar.header("Discussion Settings")

    rounds = st.sidebar.number_input(
        "Discussion rounds",
        min_value=1,
        max_value=10,
        value=3,
        step=1,
    )

    return int(rounds)