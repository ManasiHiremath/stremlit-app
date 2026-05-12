import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st
from components.configloader import ConfigLoader


class DataManager:
    def __init__(self, config):
        # Resolve gets the absolute path to the project root
        self.base_dir = Path(__file__).resolve().parent.parent
        
        self.config = config
        path_config = self.config.get("paths", {})
        
        # Define paths using forward slashes (works on Windows/Linux/Mac)
        self.default_path = self.base_dir / path_config.get("default_path", "data/default_forecast/weekly_forecast_data.csv")
        self.upload_dir = self.base_dir / path_config.get("upload_dir", "data/upload_forecast")
        print(self.default_path)
        
        # Ensure upload directory exists
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def _save_file(self, uploaded_file):
        """Saves the file and returns the new path."""
        target_path = self.upload_dir / uploaded_file.name
        with open(target_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return target_path

    def get_dataframe(self, uploaded_file=None):
        """
        Standard Logic: 
        If uploaded_file is None (default Streamlit state), use self.default_path.
        """
        if uploaded_file is not None:
            file_path = self._save_file(uploaded_file)
            st.sidebar.success(f"✅ Active: {uploaded_file.name}")
        else:
            file_path = self.default_path
            st.sidebar.info("ℹ️ Active: Default Dataset")

        return self.read_csv(file_path)

    def read_csv(self, path):
        try:
            if not path.exists():
                # This helps you debug the exact path being looked for
                st.error(f"File not found: `{path}`")
                return None
            return pd.read_csv(path)
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            return None