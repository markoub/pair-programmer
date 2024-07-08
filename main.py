import streamlit as st
import os
from src.app import main

def get_projects():
    projects_dir = "projects"
    if not os.path.exists(projects_dir):
        os.makedirs(projects_dir)
    return [d for d in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, d))]

def create_new_project(project_name):
    project_dir = os.path.join("projects", project_name)
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)

if __name__ == "__main__":
    st.title("AI-Powered Test-Driven Development")

    projects = get_projects()
    project_action = st.sidebar.radio("Project Action", ["Select Existing", "Create New"])

    if project_action == "Select Existing":
        if projects:
            selected_project = st.sidebar.selectbox("Select a project", projects)
            st.session_state.current_project = selected_project
        else:
            st.sidebar.warning("No existing projects. Please create a new one.")
    else:
        new_project_name = st.sidebar.text_input("Enter new project name")
        if st.sidebar.button("Create Project"):
            if new_project_name:
                create_new_project(new_project_name)
                st.session_state.current_project = new_project_name
                st.sidebar.success(f"Project '{new_project_name}' created successfully!")
            else:
                st.sidebar.error("Please enter a project name.")

    if 'current_project' in st.session_state:
        st.write(f"Current Project: {st.session_state.current_project}")
        main()
    else:
        st.write("Please select or create a project to continue.")