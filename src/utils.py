import streamlit as st
import os
from openai import OpenAI
import json

# Set up OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_test_description(app_description):
    prompt = f"""
    Given the following application description, generate a detailed test scenario:

    Application Description:
    {app_description}

    Your test scenario should include:
    1. A brief overview of what the test will cover
    2. Specific steps to test key functionalities
    3. Expected outcomes for each step
    4. Do not give anything other than test scenario, do not give explanations, example tests, or anything else.

    Please provide a clear and concise test scenario that can be used to create a Playwright test.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in software testing."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

def generate_playwright_test(test_description):
    prompt = f"""
    Based on the following test scenario, generate a Playwright test script in Python:

    Test Scenario:
    {test_description}

    Please follow these guidelines:
    1. Use the Playwright library for Python
    2. Include necessary imports
    3. Use the 'pytest' framework
    4. Do not cover edge-cases
    5. Handle potential errors or exceptions
    6. Use best practices for Playwright testing
    7. Respond only with python code, nothing else, no explanation. Do not use code blocks or other formatting.
    8. Provide the complete Python script that can be run using pytest. Put the placeholder URL, <TARGET_URL>, in the test code.
    9. Give detailed steps feedback, so it can be used to precisely get feedback at which step it failed if it fails.
    10. Fix exact element selectors, with IDs, classes, and other attributes.
    11. Split test script into multiple tests, wherever suitable, to give feedback on smallest steps.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in Playwright testing."},
            {"role": "user", "content": prompt}
        ]
    )

    # Remove code block fences from the response content
    content = response.choices[0].message.content
    return content.strip().lstrip('```python').rstrip('```')

def generate_application_code(app_description, playwright_test):
    prompt = f"""
    Given the following application description and Playwright test, generate a complete HTML file with embedded JavaScript that implements the described functionality:

    Application Description:
    {app_description}
    Playwright Test:
    {playwright_test}

    Make sure you are following IDs, classes, and other selectors from the Playwright test.

    Please provide a single HTML file that includes all necessary HTML, CSS, and JavaScript to implement the described application. The HTML file should be fully functional and pass the Playwright test scenario.
    Provide only HTML content, no explanations. Do not use code blocks or other formatting.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in web development."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content
    return content.strip().lstrip('```html').rstrip('```')

def regenerate_application_code(current_app_code, playwright_test, test_output):
    prompt = f"""
    Given the following current application code, Playwright test, and test output, generate an improved HTML file with embedded JavaScript that implements the described functionality and passes the test:

    Current Application Code, that is failing and should be fixed:
    {current_app_code}

    Test Output:
    {test_output}

    Please provide a single HTML file that includes all necessary HTML, CSS, and JavaScript to implement the described application. The HTML file should be fully functional and pass the Playwright test scenario.
    Provide only HTML content, no explanations. Do not use code blocks or other formatting. Fix only failing tests, do not change anything else.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in web development."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content
    return content.strip().lstrip('```html').rstrip('```')

def save_project_data(project_name, data):
    project_dir = os.path.join("projects", project_name)
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
    project_file = os.path.join(project_dir, "project_data.json")
    with open(project_file, "w") as f:
        json.dump(data, f)
