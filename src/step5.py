import streamlit as st
import os
import json
import subprocess
import sys
from .utils import regenerate_application_code

class Step5:
    def render(self, project_name):
        st.write("**5. Run Test**")
        
        project_file = os.path.join("projects", project_name, "project_data.json")
        if os.path.exists(project_file):
            with open(project_file, "r") as f:
                project_data = json.load(f)
        else:
            project_data = {}

        st.write("Playwright Test:")
        test_file_path = os.path.join("projects", project_name, "app", "test.py")
        if os.path.exists(test_file_path):
            with open(test_file_path, "r") as test_file:
                test_code = test_file.read()
            st.code(test_code, language="python")
        else:
            st.error("Test file not found.")
        
        changed = False
        if st.button("Run Test"):
            self.run_test(project_name, project_data, test_code)
            changed = True

        return changed

    def run_test(self, project_name, project_data, test_code):
        project_file = os.path.join("projects", project_name, "project_data.json")
        max_attempts = 5
        for attempt in range(1, max_attempts + 1):
            with st.spinner(f"Running test (Attempt {attempt}/{max_attempts})..."):
                temp_test_file = os.path.join("projects", project_name, "temp_test.py")
                with open(temp_test_file, "w") as f:
                    f.write(test_code.replace("<TARGET_URL>", "file://" + os.path.abspath(os.path.join("projects", project_name, "app", "index.html"))))
                
                result = subprocess.run([sys.executable, "-m", "pytest", "-v", "--tb=short", temp_test_file], 
                                        capture_output=True, text=True)
                
                st.write(f"Test Results (Attempt {attempt}):")
                st.code(result.stdout)
                
                if result.returncode == 0:
                    st.success("Test passed successfully!")
                    break
                else:
                    st.error(f"Test failed (Attempt {attempt}). Regenerating application code...")
                    
                    if attempt < max_attempts:
                        app_file = os.path.join("projects", project_name, "app", "index.html")
                        with open(app_file, "r") as f:
                            current_app_code = f.read()
                        
                        new_app_code = regenerate_application_code(
                            current_app_code,
                            test_code,
                            result.stdout
                        )
                        project_data['app_code'] = new_app_code
                        
                        # Save the new version in a separate file
                        new_version_file = os.path.join("projects", project_name, "app", f"index_v{attempt+1}.html")
                        with open(new_version_file, "w") as f:
                            f.write(new_app_code)
                        
                        # Update the main index.html file
                        with open(app_file, "w") as f:
                            f.write(new_app_code)
                        
                        with open(project_file, "w") as f:
                            json.dump(project_data, f)
                        
                        st.info(f"New version saved as index_v{attempt+1}.html")
                    else:
                        st.error("Maximum attempts reached. Please review the output and adjust your application or test as needed.")

    def regenerate(self, project_name):
        # For Step5, regeneration is not needed as it's the last step
        pass

    step_names = [
        "Define Application",
        "Define Test Scenario",
        "Create Playwright Test",
        "Build Application",
        "Run Test"
    ]