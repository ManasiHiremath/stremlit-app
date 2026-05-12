import pandas as pd
import numpy as np

class DataAnalyis:
    def __init__(self, dataframe, config):
        self.config = config
        self.df = dataframe
        # Extract mappings
        self.map = self.config.get('datadetails', {})
        self.date_col = self.map.get('forecastdate')
        self.actual_col = self.map.get('actualvalue')
        self.target_col = self.map.get('forecastvalue')
        self.obj_name = self.map.get('objective', 'Value')

    def prepare_data(self):
        """Standardizes dates with strict MM-DD-YYYY check"""
        if self.date_col not in self.df.columns:
            raise ValueError(f"Missing required date column: {self.date_col}")
        
        # 1. Check if the column is already a date (Excel imports often do this)
        # We force a check to ensure it was interpreted correctly
        
        # 2. Strict conversion: force MM-DD-YYYY
        # errors='coerce' will turn wrong formats into NaT (Not a Time)
        temp_dates = pd.to_datetime(self.df[self.date_col], format='%m-%d-%Y', errors='coerce')
        
        # 3. Validation: If more than 10% of rows failed to parse, the format is likely wrong
        fail_count = temp_dates.isna().sum()
        if fail_count > (len(self.df) * 0.1): 
            raise ValueError(
                f"❌ Date Format Error: The column '{self.date_col}' does not match the required 'MM-DD-YYYY' format. "
                "Please check your CSV and ensure dates look like '05-25-2026'."
            )
        
        self.df[self.date_col] = temp_dates
        self.df = self.df.dropna(subset=[self.date_col])
        
        # Add ISO columns
        iso_info = self.df[self.date_col].dt.isocalendar()
        self.df['iso_year'] = iso_info.year
        self.df['iso_week'] = iso_info.week
        return self.df

    def get_ytd_comparison(self, df):
        """Calculates performance for the same period this year vs last year"""
        # 1. Identify current context from data
        max_date = self.df[self.date_col].max()
        curr_year = max_date.isocalendar().year
        curr_week = max_date.isocalendar().week
        
        # 2. Filter Current Year YTD (Up to current week)
        current_ytd = self.df[(self.df['iso_year'] == curr_year) & 
                              (self.df['iso_week'] <= curr_week)]
        
        # 3. Filter Last Year YTD (Same period: Week 1 to curr_week)
        last_year_ytd = self.df[(self.df['iso_year'] == curr_year - 1) & 
                                (self.df['iso_week'] <= curr_week)]
        print(curr_week)
        Num_accuracy= current_ytd[self.actual_col].sum()- current_ytd[self.target_col].sum()
        
        Accuracy_YTD= 100-( ( (Num_accuracy / current_ytd[self.actual_col].sum()) * 100) if current_ytd[self.actual_col].sum() != 0 else 0)
        
        # 4. Aggregate Results
        summary = {
            f"Current_YTD_Actual_{self.obj_name}": current_ytd[self.actual_col].sum(),
            f"Current_YTD_Forecast_{self.obj_name}": current_ytd[self.target_col].sum(),
            f"Current_YTD_Forecast_Accuracy_{self.obj_name}": Accuracy_YTD,
            f"Last_Year_YTD_Forecast_{self.obj_name}": last_year_ytd[self.target_col].sum(),
            f"Current_Week": curr_week,
            f"Current_Year": curr_year,
            f"Last_Year": curr_year - 1
        }
        
        return summary

# # --- Fixed Execution Logic ---
# if __name__ == "__main__":
#     mock_config = {
#         'dataanalysis': {
#             'forecastdate': 'Date',
#             'actualvalue': 'Actual_Value',
#             'forecastvalue': 'Forecast_Value',
#             'objective': 'Revenue'
#         }
#     }
    
#     csv_file = r"C:\Users\MANASI\streamlit\forecast_analysis\weekly_forecast_data.csv"
    
#     try:
#         df_input = pd.read_csv(csv_file)
#         print("✅ CSV Loaded Successfully")
        
#         # Initialize Class
#         analysis = DataAnalyis(df_input, mock_config)
        
#         # Step 1: Prepare
#         enriched_df = analysis.prepare_data()
#         enriched_df.to_csv("enriched_forecast_data.csv", index=False) # Save enriched data for inspection
#         print("✅ Data Prepared Successfully. Enriched data saved to 'enriched_forecast_data.csv'")
        
#         # Step 2: Get Comparison
#         results = analysis.get_ytd_comparison()
        
#         print("\n--- YTD PERIOD COMPARISON ---")
#         print(f"Comparing Week 1 to Week {results['Current_Week']}")
#         print("-" * 30)
#         for key, value in results.items():
#             if isinstance(value, float) or isinstance(value, int):
#                 print(f"{key:.<35} {value:,.2f}")
#             else:
#                 print(f"{key:.<35} {value}")

#     except Exception as e:
#         print(f"❌ Error: {e}")
#         import traceback
#         traceback.print_exc()