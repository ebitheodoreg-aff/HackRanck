import pandas as pd
import os

def load_deletion_requests(filepath="dataset/deletion_requests.csv"):
    """Loads deletion requests CSV file."""
    if not os.path.exists(filepath):
        
        filepath = "deletion_requests.csv"
    df = pd.read_csv(filepath)
    return df