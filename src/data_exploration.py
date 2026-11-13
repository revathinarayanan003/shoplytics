import pandas as pd
from pathlib import Path

# Locate the project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Locate the dataset
DATA_PATH = BASE_DIR / "data" / "online_retail.csv"

# Load the dataset
print("Expected file location:", DATA_PATH)
print("Does the file exist?", DATA_PATH.exists())
df = pd.read_csv(DATA_PATH)

# Display first five records
print(df.head())
