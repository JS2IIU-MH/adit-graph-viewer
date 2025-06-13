import streamlit as st
import adiftools.adiftools as adiftools
import tempfile
import os
from pathlib import Path
import base64

def get_download_link(file_path, file_name):
    """Generate a download link for a file"""
    with open(file_path, "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/png;base64,{b64}" download="{file_name}">Download image</a>'
        return href

st.set_page_config(
    page_title="ADIF Graph Viewer",
    page_icon="📊",
    layout="wide"
)

st.title("ADIF Graph Viewer")
st.markdown("Upload your ADIF file to view monthly activity graphs.")

# File uploader
uploaded_file = st.file_uploader("Choose an ADIF file", type=['adif', 'adi'])

if uploaded_file is not None:
    try:
        # Create a temporary file to save the uploaded content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.adif') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        # Create ADIFParser instance and read the file
        parser = adiftools.ADIFParser()
        
        with st.spinner('Reading ADIF file...'):
            df = parser.read_adi(tmp_file_path)
        
        # Create a temporary file for the plot
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as plot_file:
            plot_path = plot_file.name
        
        # Generate and display the plot
        with st.spinner('Generating monthly activity graph...'):
            parser.plot_monthly(plot_path)
            st.image(plot_path)
            
            # Add download button
            download_filename = f"monthly_qso_{Path(uploaded_file.name).stem}.png"
            st.markdown(get_download_link(plot_path, download_filename), unsafe_allow_html=True)
        
        # Clean up temporary files
        os.unlink(tmp_file_path)
        os.unlink(plot_path)
        
    except Exception as e:
        st.error(f"Error processing the ADIF file: {str(e)}")
        st.info("Please make sure the uploaded file is a valid ADIF file.") 