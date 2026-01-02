#!/bin/bash
set -e

EMT4J_VERSION="0.8.0"
INSTALL_DIR="$HOME/.emt4j"
DOWNLOAD_URL="https://github.com/adoptium/emt4j/releases/download/v${EMT4J_VERSION}/emt4j-${EMT4J_VERSION}.zip"

# Function to check dependencies
check_dependencies() {
    if ! command -v java &> /dev/null; then
        echo "Error: Java is not installed. Please install Java 11 or higher."
        exit 1
    fi
    if ! command -v curl &> /dev/null; then
        echo "Error: curl is not installed."
        exit 1
    fi
    if ! command -v unzip &> /dev/null; then
        echo "Error: unzip is not installed."
        exit 1
    fi
}

install_emt4j() {
    echo "Installing EMT4J version ${EMT4J_VERSION}..."
    
    mkdir -p "$INSTALL_DIR"
    
    echo "Downloading package..."
    curl -L "$DOWNLOAD_URL" -o "${INSTALL_DIR}/emt4j.zip"
    
    echo "Extracting..."
    unzip -o "${INSTALL_DIR}/emt4j.zip" -d "$INSTALL_DIR"
    rm "${INSTALL_DIR}/emt4j.zip"
    
    echo "Setup complete!"
    echo "EMT4J location: ${INSTALL_DIR}/emt4j-${EMT4J_VERSION}"
    echo "Executable script: ${INSTALL_DIR}/emt4j-${EMT4J_VERSION}/bin/analysis.sh"
}

# Main execution
check_dependencies
install_emt4j
