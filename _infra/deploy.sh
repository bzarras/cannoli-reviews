#!/bin/bash

# Check Python version
REQUIRED_PYTHON_VERSION="3.11.4"

if ! python -c "import sys; exit(0) if sys.version_info >= (3, 11, 4) else exit(1)"; then
    echo "Required Python version $REQUIRED_PYTHON_VERSION or higher is not installed."
    exit 1
fi

PROJECT_DIR=~/apps
REPO_NAME=cannoli-reviews
VENV_NAME=.venv
VENV_DIR=$PROJECT_DIR/$REPO_NAME/$VENV_NAME
APP_SERVICE_NAME=cannoli-reviews
REPO_URL=https://github.com/bzarras/$REPO_NAME.git
BRANCH=main

# Navigate to the project directory
cd "$PROJECT_DIR"

# Check if the repository directory exists, otherwise clone it
if [ ! -d "$PROJECT_DIR/$REPO_NAME" ]; then
    echo "Repository doesn't exist. Cloning..."
    git clone "$REPO_URL" "$REPO_NAME"
fi

cd "$PROJECT_DIR/$REPO_NAME"

# Check if the virtual environment exists, otherwise create it
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment doesn't exist. Creating..."
    python -m venv "$VENV_NAME"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Pull the latest code from the repository
git pull origin "$BRANCH"

# Install or update dependencies within the virtual environment
pip install -r requirements.txt

# Restart the application (replace this with your actual command)
sudo systemctl restart "$APP_SERVICE_NAME"

# Deactivate the virtual environment
deactivate
