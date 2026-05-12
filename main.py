import streamlit as st
from streamlit_tile import streamlit_tile
# 1. Import your page modules
from components.configloader import ConfigLoader    
from components.navigation import NavigationMenu
from components.FileHandler import DataManager 
from components.pages import overviewpage,forecastanalysis


def main():
    # 1. Load your config data
    config = ConfigLoader.load_resource("config.yaml")
    page_title=config.get("app_config", {}).get("app_title", "Default Planning Tool")
    #3.ge Configuration
    st.set_page_config(page_title=page_title,layout="wide",page_icon="🧊")  
  
    # 2. Load and automatically apply your CSS
    ConfigLoader.load_resource("assets/styles.css")

    ## 4. Build Navigation
    nav = NavigationMenu(config)
    forecast_file, simulation_file, selected_page = nav.render()
    
    # # 3. Optional: Add a button to clear the upload and return to default
    # if st.sidebar.button("Clear Upload & Reset to Default"):
    #     st.rerun()
   
    # 1. Initialize your page instances first
    # Make sure these classes are imported correctly at the top of your file
    overview_inst = overviewpage.OverviewPage(config=config)
    forecast_inst = forecastanalysis.ForecastAnalysisPage(config=config)

    # 2. Create the mapping dictionary using the instances
    page_registry = {
        "Overview": overview_inst,
        "Demand Forecast": forecast_inst,
    }

    # 3. Render the selected page
    if selected_page in page_registry:
        # Retrieve the class instance from the dictionary using the key
        page = page_registry[selected_page]
        # Now you can call the .show() method on the instance
        page.show(forecast_file, simulation_file)



if __name__ == "__main__":
    main()