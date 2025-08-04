
import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path

def load_processed_files(json_file):
    if json_file.exists():
        with open(json_file, 'r') as f:
            return json.load(f)
    return {}

# Function to get and sort media files by their last modified date
def get_sorted_media_files():
    current_dir = Path(__file__).parent
    media_folder = current_dir / "deep_dive_radio"  # Adjust the folder path if necessary

    # Get all MP4 files in the folder
    media_files = [f for f in media_folder.glob("*.mp4")]

    # Sort the files by last modified date in reverse order (newest first)
    sorted_files = sorted(media_files, key=lambda x: get_last_modified_date(x), reverse=True)

    return sorted_files

def get_last_modified_date(file_path):
    return os.path.getmtime(file_path) if os.path.exists(file_path) else 0

def deep_dive_radio_page():
    """Fixed version that works within the new page structure."""
    
    def load_processed_files_local(json_file):
        if json_file.exists():
            with open(json_file, 'r') as f:
                return json.load(f)
        return {}

    def get_file_info(file, processed_files):
        file_name = file.stem
        if file_name in processed_files:
            return processed_files[file_name]
        return {
            "duration": "Unknown",
            "description": "",
            "source_url": "",
        }

    # Don't override page config - that's handled by the main app
    st.title("📻 Deep Dive Radio")

    # Set up correct paths
    current_dir = Path(__file__).parent
    media_folder = current_dir / "deep_dive_radio"
    json_file = current_dir / "processed_files.json"
    
    processed_files = load_processed_files_local(json_file)

    # Get all MP4 files in the folder
    media_files = [f for f in media_folder.glob("*.mp4")]

    # Sort files by last modified date
    sorted_files = sorted(media_files, key=lambda x: get_last_modified_date(x), reverse=True)

    if not sorted_files:
        st.info("No media files found in the deep_dive_radio directory.")
        return

    # Episodes in sidebar using selectbox to avoid duplicate key issues
    st.sidebar.header("📻 Episodes")
    
    # Initialize session state if needed
    if 'selected_deep_dive_file' not in st.session_state:
        st.session_state.selected_deep_dive_file = None
        st.session_state.selected_deep_dive_title = None
        st.session_state.selected_deep_dive_info = None

    # Create episode options for selectbox
    episode_options = ["Select an episode..."]
    episode_files = {}
    
    for file in sorted_files:
        title = file.stem.replace('_', ' ').title()
        episode_options.append(title)
        episode_files[title] = file
    
    # Use selectbox instead of buttons to avoid key conflicts
    selected_episode = st.sidebar.selectbox(
        "Choose Episode:",
        episode_options,
        index=0,
        key="deep_dive_episode_selector"
    )
    
    # Show episode count and info
    st.sidebar.write(f"📊 **{len(sorted_files)} Episodes Available**")
    
    if selected_episode != "Select an episode...":
        st.sidebar.write(f"🎯 **Selected:** {selected_episode}")
    
    # Handle episode selection
    if selected_episode != "Select an episode..." and selected_episode in episode_files:
        file = episode_files[selected_episode]
        file_info = get_file_info(file, processed_files)
        
        # Update session state only if selection changed
        if (st.session_state.selected_deep_dive_file != file or 
            st.session_state.selected_deep_dive_title != selected_episode):
            st.session_state.selected_deep_dive_file = file
            st.session_state.selected_deep_dive_title = selected_episode
            st.session_state.selected_deep_dive_info = file_info

    # Display content based on selection
    if st.session_state.selected_deep_dive_file:
        file = st.session_state.selected_deep_dive_file
        title = st.session_state.selected_deep_dive_title
        file_info = st.session_state.selected_deep_dive_info
        
        st.subheader(f"▶️ Now Playing: {title}")
        
        # Show description if available
        if file_info.get('description'):
            st.write("**Description:**")
            st.write(file_info['description'])
        
        # Show source if available
        if file_info.get('source_url'):
            st.markdown(f"**Source:** [View Original]({file_info['source_url']})")
        
        # Show duration if available
        if file_info.get('duration') and file_info['duration'] != "Unknown":
            st.write(f"**Duration:** {file_info['duration']}")
        
        # Display the video
        if file.exists():
            st.video(str(file))
        else:
            st.error(f"File not found: {file}")
    else:
        # Welcome message
        st.info("👈 Select an episode from the sidebar to start listening.")
        
        # Show available episodes
        st.subheader("Available Episodes:")
        for i, file in enumerate(sorted_files[:5], 1):  # Show first 5
            title = file.stem.replace('_', ' ').title()
            st.write(f"{i}. **{title}**")
        
        if len(sorted_files) > 5:
            st.write(f"... and {len(sorted_files) - 5} more episodes in the sidebar")

def main():
    """Standalone version for testing."""
    st.set_page_config(page_title="Deep Dive Radio", layout="wide")
    deep_dive_radio_page()

if __name__ == "__main__":
    main()