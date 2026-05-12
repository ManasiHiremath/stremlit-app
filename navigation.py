import streamlit as st
from streamlit_option_menu import option_menu
from components.configloader import ConfigLoader
from datetime import datetime as dt


class NavigationMenu:
    def __init__(self,config):
        self.config=config
        self.pages = self.config['navigation']['pages']
        self.menu_title = self.config['navigation']['menu_title']
    
    def _render_data_provisioning(self):
        st.sidebar.markdown('<p class="menu-header">📁 Data Provisioning</p>', unsafe_allow_html=True)
        # Forecast File Uploader
        with st.sidebar.expander("Forecast File", expanded=False, key="green_expander_fc"):
            forecast_file = st.file_uploader(
                "Upload Forecast CSV", 
                type=["csv"], 
                key="green_upload_fc"
            )
            if forecast_file:
                st.sidebar.caption(f"Loaded: {forecast_file.name}")
        
        # Simulation File Uploader
        with st.sidebar.expander("Simulation File", expanded=False, key="green_expander_sim"):
            simulation_file = st.file_uploader(
                "Upload Simulation CSV", 
                type=["csv"], 
                key="green_upload_sim"
            )
            if simulation_file:
                st.sidebar.caption(f"Loaded: {simulation_file.name}")
        return forecast_file, simulation_file
    

    def build_sidebar(self):
        labels=[pages['label'] for pages in self.pages]
        icons=[pages['icon'] for pages in self.pages]
        with st.sidebar:         
                selected = option_menu(
                self.menu_title,  # Title of the sidebar
                options=labels,
                icons=icons,
                menu_icon="cast",
                default_index=0,
                styles={
                    "container": {"padding": "0!important", "background-color": "transparent"},
                    "icon": {"color": "#F8F9FA", "font-size": "16px"}, # Slightly smaller icon
                    "menu-title": {"color": "#F8F9FA", "font-size":" 1.5rem" },
                    "nav-link": {
                        "font-size": "14px",
                        "font-family": "var(--main-font)",
                        "color": "#F8F9FA",
                        "text-align": "left",
                        "margin": "5px 0px", # Added slight vertical margin for equal spacing
                        "padding": "10px",   # Makes it feel more like a button
                        "white-space": "nowrap",
                        "border-radius": "8px", # Matches your expander styling
                        "--hover-color": "rgba(255, 255, 255, 0.08)"
                    },
                    "nav-link-selected":{
                        "background-color": "rgba(255, 255, 255, 0.1)", # Use your --primary-purple here
                        "color": "#FFFFFF",
                        "font-family": "var(--main-font)",
                        "font-weight": "bold",
                       "--hover-color": "rgba(255, 255, 255, 0.08)"},
                }
            )

        return selected
    
    def render(self):
        selected_page = self.build_sidebar()
        forecast, simulation = self._render_data_provisioning()
        return forecast, simulation, selected_page
        


