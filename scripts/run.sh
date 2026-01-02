#!/bin/bash
# Wrapper to run java-modernize with correct environment
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Determine correct Python executable
if [ -n "$VIRTUAL_ENV" ]; then
    PYTHON_EXEC="python3"
elif [ -f "$PROJECT_ROOT/venv/bin/python3" ]; then
    PYTHON_EXEC="$PROJECT_ROOT/venv/bin/python3"
else
    echo "Error: Virtual environment not found. Please run 'make setup' first."
    exit 1
fi

export PYTHONPATH="$PROJECT_ROOT/src:$PYTHONPATH"

"$PYTHON_EXEC" -m cli.commands "$@"
