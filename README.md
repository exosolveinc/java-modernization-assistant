# Java Modernization Assistant

An AI-powered tool to automate the modernization of legacy Java applications.

## Features

- **Analysis**: Uses EMT4J to scan for compatibility issues
- **Planning**: Uses Claude AI to generate phased migration plans
- **Transformation**: Uses OpenRewrite to automatically apply code changes
- **Validation**: Verifies compilation and tests

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/java-modernization-assistant.git
cd java-modernization-assistant

# Setup virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
make setup
```

## Usage

### CLI

```bash
# 1. Analyze a project
java-modernize analyze /path/to/legacy-project --from 8 --to 21

# 2. Generate a plan
java-modernize plan /path/to/legacy-project --analysis report.json

# 3. Transform
java-modernize transform /path/to/legacy-project --plan plan.json --phase 1
```

### API

Run the API server:

```bash
make run-api
```

Access Swagger UI at `http://localhost:8000/docs`.
