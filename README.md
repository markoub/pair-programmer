# AI-Assisted Test-Driven Development (TDD) Project

This project demonstrates an AI-assisted approach to Test-Driven Development (TDD) using Streamlit, OpenAI's GPT model, and Playwright for testing.

## Features

- Define application requirements
- Generate test scenarios based on requirements
- Create Playwright tests automatically
- Build application code iteratively
- Run tests and regenerate code until tests pass

## Installation

1. Clone the repository:
   ```
   git clone git@github.com:markoub/pair-programmer.git
   cd pair-programmer
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   Create a file named `.streamlit/secrets.toml` and add your API key:
   ```
   OPENAI_API_KEY = "your-api-key-here"
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Follow the steps in the web interface:
   - Define your application
   - Generate test scenarios
   - Create Playwright tests
   - Build your application
   - Run tests and iterate

## Project Structure

- `app.py`: Main Streamlit application
- `src/`: Contains the core logic for each step of the TDD process
- `projects/`: Stores individual project data and generated code
- `utils.py`: Utility functions for API calls and code generation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
