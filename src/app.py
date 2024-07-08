import streamlit as st
import os
import json
from .step1 import Step1
from .step2 import Step2
from .step3 import Step3
from .step4 import Step4
from .step5 import Step5
from .StepMenu import render_step_menu
from .utils import save_project_data

st.set_page_config(layout="wide")

def load_project_data(project_name):
    project_file = os.path.join("projects", project_name, "project_data.json")
    if os.path.exists(project_file):
        with open(project_file, "r") as f:
            return json.load(f)
    return {}

def main():
    project_name = st.session_state.current_project
    project_data = load_project_data(project_name)

    if 'current_step' not in project_data:
        project_data['current_step'] = 1

    col1, col2 = st.columns([1, 3])

    steps = [Step1(), Step2(), Step3(), Step4(), Step5()]
    step_names = ["Define Application", "Define Test Scenario", "Create Playwright Test", "Build Application", "Run Test"]

    with col1:
        render_step_menu(project_data['current_step'], step_names)

    with col2:
        current_step = steps[project_data['current_step'] - 1]
        changed = current_step.render(project_name)

    col_back, col_next = st.columns(2)
    with col_back:
        if project_data['current_step'] > 1:
            if st.button("← Back", key="back_button"):
                project_data['current_step'] -= 1
                save_project_data(project_name, project_data)
                st.rerun()

    with col_next:
        if project_data['current_step'] < len(steps):
            if st.button("Next →", key="next_button"):
                project_data['current_step'] += 1
                save_project_data(project_name, project_data)
                st.rerun()
        elif project_data['current_step'] == len(steps):
            if st.button("Start Over", key="start_over_button"):
                project_data = {'current_step': 1}
                save_project_data(project_name, project_data)
                st.rerun()

