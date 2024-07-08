import streamlit as st
import os
import json
from .utils import generate_playwright_test

class Step3:
    def render(self, project_name):
        st.write("**3. Create Playwright Test**")
        
        project_dir = os.path.join("projects", project_name)
        project_file = os.path.join(project_dir, "project_data.json")
        app_dir = os.path.join(project_dir, "app")
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)
        
        test_file = os.path.join(app_dir, "test.py")
        
        if os.path.exists(project_file):
            with open(project_file, "r") as f:
                project_data = json.load(f)
        else:
            project_data = {}
        
        changed = False
        if not os.path.exists(test_file):
            with st.spinner("Generating Playwright test..."):
                playwright_test = generate_playwright_test(project_data.get('test_description', ''))
                with open(test_file, "w") as f:
                    f.write(playwright_test)
                changed = True
        else:
            with open(test_file, "r") as f:
                playwright_test = f.read()
        
        st.write("Generated Playwright Test:")
        new_playwright_test = st.text_area("Edit Playwright Test", playwright_test, height=800)
        
        if new_playwright_test != playwright_test:
            with open(test_file, "w") as f:
                f.write(new_playwright_test)
            project_data['playwright_test'] = new_playwright_test
            with open(project_file, "w") as f:
                json.dump(project_data, f)
            changed = True
        
        return changed

    def regenerate(self, project_name):
        project_dir = os.path.join("projects", project_name)
        project_file = os.path.join(project_dir, "project_data.json")
        app_dir = os.path.join(project_dir, "app")
        test_file = os.path.join(app_dir, "test.py")
        
        with open(project_file, "r") as f:
            project_data = json.load(f)
        
        playwright_test = generate_playwright_test(project_data.get('test_description', ''))
        
        with open(test_file, "w") as f:
            f.write(playwright_test)
        
        project_data['playwright_test'] = playwright_test
        with open(project_file, "w") as f:
            json.dump(project_data, f)

    step_names = [
        "Define Application",
        "Define Test Scenario",
        "Create Playwright Test",
        "Build Application",
        "Run Test"
    ]


