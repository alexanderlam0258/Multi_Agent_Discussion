import streamlit as st


def display_turn(turn):

    with st.chat_message(
        turn["agent"].lower(),
        avatar=turn["avatar"],
    ):

        st.markdown(
            f"**{turn['agent']}** "
            f"*(Round {turn['round']})*"
        )

        st.markdown(turn["text"])


def display_synthesis(text):

    st.subheader("🏛️ Council Synthesis")

    st.markdown(text)