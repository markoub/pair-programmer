import streamlit as st
import os
import json
from .utils import generate_application_code

class Step4:
    def render(self, project_name):
        st.write("**4. Build Application**")
        
        project_dir = os.path.join("projects", project_name)
        app_dir = os.path.join(project_dir, "app")
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)
        
        html_file = os.path.join(app_dir, "index.html")
        
        project_file = os.path.join(project_dir, "project_data.json")
        with open(project_file, "r") as f:
            project_data = json.load(f)
        
        changed = False
        if not os.path.exists(html_file):
            with st.spinner("Generating application code..."):
                test_file = os.path.join(app_dir, "test.py")
                with open(test_file, "r") as f:
                    playwright_test = f.read()
                app_code = generate_application_code(project_data.get('app_description', ''), playwright_test)
                with open(html_file, "w") as f:
                    f.write(app_code)
                changed = True
        else:
            with open(html_file, "r") as f:
                app_code = f.read()
        
        st.write("Generated Application Code:")
        new_app_code = st.text_area("Edit Application Code", app_code, height=800)
        
        if new_app_code != app_code:
            with open(html_file, "w") as f:
                f.write(new_app_code)
            changed = True
        
        return changed

    step_names = [
        "Define Application",
        "Define Test Scenario",
        "Create Playwright Test",
        "Build Application",
        "Run Test"
    ]
