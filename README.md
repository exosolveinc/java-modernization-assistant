# Java Modernization Assistant ☕️➡️🚀

An AI-powered agentic tool designed to automate the modernization of legacy Java applications. It combines static analysis (EMT4J), LLM-based planning (Claude 3.5 Sonnet), and automated code transformation (OpenRewrite) to migrate applications from older Java versions (e.g., Java 8) to modern LTS versions (Java 17/21).

## 🌟 Features

- **🔍 Deep Analysis**: Uses **EMT4J** (Eclipse Migration Toolkit for Java) to scan for version compatibility issues, removed APIs, and deprecated features.
- **🧠 AI Planning**: Leverages **Anthropic Claude** to analyze reports and generate a phased, risk-aware migration plan (JSON).
- **🤖 Automated Transformation**: Orchestrates **OpenRewrite** to automatically apply code changes, dependency upgrades, and formatting fixes.
- **✅ Validation**: (Experimental) compiling and verifying changes after each phase.

## 🛠 Prerequisites

Before you begin, ensure you have the following installed:

- **OS**: macOS or Linux
- **Python**: 3.10+
- **Java**: JDK 17+ (Required to run OpenRewrite and EMT4J)
- **Maven**: 3.6+ (`brew install maven` on macOS)
- **API Key**: An [Anthropic API Key](https://console.anthropic.com/) for the AI planner.

## 🚀 Installation & Setup

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/exosolveinc/java-modernization-assistant.git
    cd java-modernization-assistant
    ```

2.  **Run the Setup Script**
    This will create a virtual environment, install Python dependencies, and download the EMT4J binaries.

    ```bash
    make setup
    # Or manually:
    # python3 -m venv venv && source venv/bin/activate && pip install -e .
    # ./scripts/install_emt4j.sh
    ```

3.  **Configure Environment**
    Create a `.env` file in the root directory:
    ```bash
    cp .env.example .env
    ```
    Edit `.env` and add your API key:
    ```properties
    ANTHROPIC_API_KEY=sk-ant-api03-...
    ```

## 📖 Usage Guide

We provide a wrapper script `scripts/run.sh` to ensure the correct environment and paths are loaded.

### 1. Analyze a Legacy Project

Scan your project for issues preventing migration.

```bash
./scripts/run.sh analyze /path/to/your/project --from-version 8 --to-version 17
```

- **Output**: `analysis_report.json`

### 2. Generate a Migration Plan

Ask the AI to create a step-by-step migration strategy based on the analysis.

```bash
./scripts/run.sh plan /path/to/your/project --analysis analysis_report.json
```

- **Output**: `migration-plan.json`

### 3. Execute Transformation (Phase by Phase)

Apply the changes using OpenRewrite. It is recommended to run a **dry-run** first.

**Dry Run (Preview Changes):**

```bash
./scripts/run.sh transform /path/to/your/project --plan migration-plan.json --phase 1 --dry-run
```

- **Output**: `target/rewrite/rewrite.patch` (View this file to see proposed changes)

**Apply Changes:**

```bash
./scripts/run.sh transform /path/to/your/project --plan migration-plan.json --phase 1
```

### 4. Optimize & Cleanup

After upgrading versions, run the final phase (usually containing cleanup recipes like `RemoveUnusedImports`).

```bash
./scripts/run.sh transform /path/to/your/project --plan migration-plan.json --phase 3
```

## ⚡️ Example Scenario

Migration of the included `GUI-based-Algorithm-Calculator` from Java 8 to 17.

```bash
# 1. Analyze
./scripts/run.sh analyze GUI-based-Algorithm-Calculator --from-version 8 --to-version 17

# 2. Plan (Generates 3 phases: 8->11, 11->17, Cleanup)
./scripts/run.sh plan GUI-based-Algorithm-Calculator --analysis analysis_report.json

# 3. Transform Phase 1 (8 -> 11)
./scripts/run.sh transform GUI-based-Algorithm-Calculator --plan migration-plan.json --phase 1

# 4. Transform Phase 2 (11 -> 17)
./scripts/run.sh transform GUI-based-Algorithm-Calculator --plan migration-plan.json --phase 2

# 5. Cleanup
./scripts/run.sh transform GUI-based-Algorithm-Calculator --plan migration-plan.json --phase 3
```

## 🔧 Troubleshooting

**`mvn: command not found`**

- OpenRewrite requires Maven. Install it: `brew install maven` or `sudo apt install maven`.

**`404 Error` fetching EMT4J**

- Ensure usage of `scripts/install_emt4j.sh` which handles the correct version URL.

**Transformation returns "Recipe not found"**

- OpenRewrite recipe names are case-sensitive. Common ones:
  - `org.openrewrite.java.migrate.Java8toJava11`
  - `org.openrewrite.java.migrate.UpgradeToJava17`
  - `org.openrewrite.java.RemoveUnusedImports`

## 🏗 Architecture

- **`src/analyzer`**: Wraps EMT4J CLI.
- **`src/planner`**: Prompts Claude 3.5 to create JSON plans.
- **`src/transformer`**: Wraps `mvn rewrite:run` commands.
- **`src/cli`**: Click-based CLI interface.

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
