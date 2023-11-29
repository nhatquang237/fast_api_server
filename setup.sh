#!/bin/bash

PYTHON_EXE_PATH=$1
MAIN_SRC_PATH=$2
# Step 1: Create and activate a virtual environment
$PYTHON_EXE_PATH -m venv venv
source venv/Scripts/activate

# Step 2: Install Python packages from requirements.txt
pip install -r requirements.txt

# Step 3: Run the main file
venv/Scripts/python.exe $MAIN_SRC_PATH

exit 0
