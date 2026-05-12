import yaml
import streamlit as st
import pathlib

class ConfigLoader:
    @staticmethod
    def load_resource(file_path: str):
        try:
            path = pathlib.Path(file_path)
            with open(path, "r") as f:
                # Check the file extension to decide how to process
                if path.suffix.lower() in ['.yaml', '.yml']:
                    return yaml.safe_load(f)
                
                if path.suffix.lower() == '.css':
                    css_content = f.read()
                    # Injecting directly inside the loader for convenience
                    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
                    return css_content
                
                # Default return for plain text or other files
                return f.read()
                
        except FileNotFoundError:
            st.error(f"File '{file_path}' not found.")
            st.stop()
        except yaml.YAMLError as exc:
            st.error(f"Error parsing YAML: {exc}")
            st.stop()