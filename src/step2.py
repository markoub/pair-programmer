import streamlit as st
import os
import json
from .utils import generate_test_description, save_project_data

class Step2:
    def render(self, project_name):
        st.write("**2. Define Test Scenario**")
        
        project_file = os.path.join("projects", project_name, "project_data.json")
        if os.path.exists(project_file):
            with open(project_file, "r") as f:
                project_data = json.load(f)
        else:
            project_data = {}

        if 'test_description' not in project_data:
            with st.spinner("Generating test scenario..."):
                project_data['test_description'] = generate_test_description(project_data['app_description'])
                save_project_data(project_name, project_data)

        st.write("Test Description:")
        new_test_description = st.text_area("Edit Test Description", project_data['test_description'], height=800)

        if new_test_description != project_data['test_description']:
            project_data['test_description'] = new_test_description
            changed = True
        
        changed = False
        
        return changed

    step_names = [
        "Define Application",
        "Define Test Scenario",
        "Create Playwright Test",
        "Build Application",
        "Run Test"
    ]