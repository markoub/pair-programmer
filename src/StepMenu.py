import streamlit as st

def render_step_menu(current_step, step_names):
    st.subheader("TDD Steps")
    for i, step_name in enumerate(step_names, 1):
        if i == current_step:
            st.markdown(f"**{i}. {step_name}** 👈")
        else:
            st.markdown(f"{i}. {step_name}")


