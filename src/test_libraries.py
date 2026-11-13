import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import sklearn
import streamlit as st

print("NumPy:", np.__version__)
print("Pandas:", pd.__version__)
print("Matplotlib:", plt.matplotlib.__version__)
print("Seaborn:", sns.__version__)
print("Plotly:", px.__version__ if hasattr(px, "__version__") else "Imported")
print("Scikit-learn:", sklearn.__version__)
print("Streamlit:", st.__version__)

print("\nAll libraries imported successfully!")