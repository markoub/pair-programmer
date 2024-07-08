import streamlit as st
import os
import json
from .utils import save_project_data

class Step1:
    def render(self, project_name):
        st.write("**1. Define Application**")
        
        project_file = os.path.join("projects", project_name, "project_data.json")
        if os.path.exists(project_file):
            with open(project_file, "r") as f:
                project_data = json.load(f)
        else:
            project_data = {}

        app_description = st.text_area(
            "Enter your application description:", 
            value=project_data.get('app_description', ""),
            placeholder="Explain what the application is and what it does.",
            height=200,
        )
        
        changed = False
        if st.button("Next: Generate Test Description"):
            if app_description:
                project_data['app_description'] = app_description
                project_data['current_step'] = 2
                save_project_data(project_name, project_data)
                changed = True
                st.rerun()
            else:
                st.error("Please enter an application description before proceeding.")
        
        return changed

    step_names = [
        "Define Application",
        "Define Test Scenario",
        "Create Playwright Test",
        "Build Application",
        "Run Test"
    ]
