#!/usr/bin/env bash

# Get the directory where this script lives
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
TARGET_PYTHON="/c/Users/Admin/AppData/Local/Programs/Python/Python313/python"
# Python 3.13.7

echo -e "\n"
echo "Using project directory: $SCRIPT_DIR"
echo "Virtual environment path: $VENV_DIR"
echo "Target Python interpreter: $TARGET_PYTHON"
echo -e "\n"



# Create venv if it doesn't exist
if [ -d "$VENV_DIR" ]; then
    echo "✅ Virtual environment already exists at $VENV_DIR"
else
    echo "⚙️  Creating new virtual environment at $VENV_DIR ..."
    "$TARGET_PYTHON" -m venv "$VENV_DIR"
    echo "✅ New environment created at $VENV_DIR"
fi
echo -e "\n"

# echo "🐍 Before activating Python path: $(which python)"
# echo "🐍 Before activating Python version: $(python --version)"
# echo -e "\n"

# Activate environment
# Git Bash needs 'source', not just execution
if [ -f "$VENV_DIR/Scripts/activate" ]; then
    echo "🔗 Activating virtual environment..."
    source "$VENV_DIR/Scripts/activate"
    echo "✅ Virtual environment activated."
    
else
    echo "❌ Could not find activate script in $VENV_DIR/Scripts/"
    exit 1
fi
echo -e "\n"


echo "🐍 Env Python path: $(which python)"
echo "🐍 Env Python version: $(python --version)"
echo -e "\n"

# pip install --upgrade pip
"$TARGET_PYTHON" -m pip install --upgrade pip
pip install -r "$SCRIPT_DIR/requirements.txt"

echo "✅ Dependencies installed from requirements.txt"
echo -e "\n"
# --- IGNORE ---