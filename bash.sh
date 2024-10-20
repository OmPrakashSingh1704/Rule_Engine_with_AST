#!/bin/bash

# Step 1: Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
  echo "Error: requirements.txt not found!"
  exit 1
fi

# Step 2: Install the required Python packages
echo "Installing Python packages from requirements.txt..."
pip install -r requirements.txt

# Check if the installation was successful
if [ $? -ne 0 ]; then
  echo "Error: Failed to install the required packages."
  exit 1
fi

# Step 3: Run the app.py file
echo "Running app.py..."
streamlit run app.py

# Check if app.py ran successfully
if [ $? -ne 0 ]; then
  echo "Error: Failed to run app.py."
  exit 1
fi

echo "app.py finished running successfully."
