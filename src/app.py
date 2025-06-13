import streamlit as st
import adiftools.adiftools as adiftools
import tempfile
import os
from pathlib import Path
import base64
import pandas as pd
from datetime import datetime

def get_download_link(file_path, file_name):
    """Generate a download link for a file"""
    with open(file_path, "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/png;base64,{b64}" download="{file_name}">Download image</a>'
        return href

def format_date(date_str):
    """Format ADIF date string to readable format"""
    try:
        return datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')
    except:
        return "Unknown"

def get_summary_info(df):
    """Get summary information from ADIF DataFrame"""
    summary = {}
    
    # Basic statistics
    summary['total_records'] = len(df)
    
    # Date information
    if 'QSO_DATE' in df.columns:
        dates = pd.to_datetime(df['QSO_DATE'], format='%Y%m%d')
        summary['first_date'] = format_date(dates.min().strftime('%Y%m%d'))
        summary['last_date'] = format_date(dates.max().strftime('%Y%m%d'))
        summary['date_span'] = (dates.max() - dates.min()).days
    
    # Band information
    if 'BAND' in df.columns:
        summary['bands'] = df['BAND'].unique().tolist()
        summary['band_counts'] = df['BAND'].value_counts().to_dict()
    
    # Mode information
    if 'MODE' in df.columns:
        summary['modes'] = df['MODE'].unique().tolist()
        summary['mode_counts'] = df['MODE'].value_counts().to_dict()
    
    return summary

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
        # Create a status container for the entire process
        with st.status("Processing ADIF file...", expanded=True) as status:
            # Step 1: Save uploaded file
            status.update(label="Saving uploaded file...", state="running")
            with tempfile.NamedTemporaryFile(delete=False, suffix='.adif') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            status.update(label="File saved successfully", state="complete")

            # Step 2: Initialize parser and read file
            status.update(label="Initializing ADIF parser...", state="running")
            parser = adiftools.ADIFParser()
            status.update(label="Reading ADIF file...", state="running")
            df = parser.read_adi(tmp_file_path)
            status.update(label=f"Successfully read {len(df)} QSO records", state="complete")

            # Display summary information
            summary = get_summary_info(df)
            
            # Create columns for summary display
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Basic Information")
                st.metric("Total QSOs", summary['total_records'])
                if 'first_date' in summary:
                    st.metric("First QSO", summary['first_date'])
                if 'last_date' in summary:
                    st.metric("Last QSO", summary['last_date'])
                if 'date_span' in summary:
                    st.metric("Date Span", f"{summary['date_span']} days")
            
            with col2:
                st.subheader("📻 Band & Mode Information")
                if 'bands' in summary:
                    st.write("**Bands Used:**")
                    for band, count in summary['band_counts'].items():
                        st.write(f"- {band}: {count} QSOs")
                
                if 'modes' in summary:
                    st.write("**Modes Used:**")
                    for mode, count in summary['mode_counts'].items():
                        st.write(f"- {mode}: {count} QSOs")

            # Step 3: Create plot
            status.update(label="Preparing to generate graph...", state="running")
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as plot_file:
                plot_path = plot_file.name
            
            status.update(label="Generating monthly activity graph...", state="running")
            parser.plot_monthly(plot_path)
            status.update(label="Graph generated successfully", state="complete")

            # Step 4: Display results
            status.update(label="Displaying results...", state="running")
            st.subheader("📈 Monthly Activity Graph")
            st.image(plot_path)
            download_filename = f"monthly_qso_{Path(uploaded_file.name).stem}.png"
            st.markdown(get_download_link(plot_path, download_filename), unsafe_allow_html=True)
            status.update(label="Process completed successfully!", state="complete")

        # Clean up temporary files
        os.unlink(tmp_file_path)
        os.unlink(plot_path)
        
    except Exception as e:
        st.error(f"Error processing the ADIF file: {str(e)}")
        st.info("Please make sure the uploaded file is a valid ADIF file.") 