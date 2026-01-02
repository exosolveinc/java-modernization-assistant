from setuptools import setup, find_packages

setup(
    name="java-modernization-assistant",
    version="0.1.0",
    description="AI-powered Java application modernization toolkit",
    author="DevOps Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi",
        "uvicorn",
        "anthropic",
        "click",
        "pydantic",
        "pydantic-settings",
        "loguru",
        "httpx",
        "gitpython",
        "lxml",
        "xmltodict",
        "pyyaml",
        "pandas",
        "tabulate",
        "python-dotenv",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "java-modernize=cli.commands:cli",
        ],
    },
    python_requires=">=3.10",
)
