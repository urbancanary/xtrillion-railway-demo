# xtrillion19.py

import streamlit as st
st.set_page_config(
    page_title="XTrillion Demo",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "XTrillion Demo Application"
    }
)
#from chatbot_andy35 import ChatbotAndy, create_google_doc
import uuid
from langchain.schema import AIMessage, HumanMessage
import os
# Google services imports - commented out for Guinness version
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
import numpy as np
import time
from pathlib import Path
import random
import string


from credit_reports import create_country_report_tab
from report_utils import create_fund_report_tab
from user_guide import display_user_guide
from bond_information import create_bond_information_tab, get_bond_options
from qa_engine5 import QAEngine, detect_intent
from welcome_page import display_welcome_page  # Import the new welcome page
from streamlit_deep_dive_radio_wrapped import deep_dive_radio_page, get_sorted_media_files, get_last_modified_date, load_processed_files
import sidebar_demo
from report_utils import fetch_fund_data_with_cache  # Import the new function
import chatbot_demo

# Import RVM Grid corrected layout
try:
    from pages.rvm_grid_corrected import create_rvm_grid_tab
except ImportError:
    # Fallback function if corrected layout is not available
    def create_rvm_grid_tab():
        st.error("RVM Grid module not available. Please check the installation.")


if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
else:
    # Clear old messages if they are not dictionaries
    if len(st.session_state.chat_history) > 0 and not isinstance(st.session_state.chat_history[0], dict):
        st.session_state.chat_history = []

# Clear old session state variables if necessary
for key in ['chat_history']:
    if key in st.session_state:
        del st.session_state[key]


available_reports = {

    "Shin Kong Emerging Wealthy Nations Bond Fund": "🟠 SKEWNBF",
    "Shin Kong Environmental Sustainability Bond Fund": "🟢 SKESBF",
    "Israel": "🇮🇱 Israel",
    "Qatar": "🇶🇦 Qatar",
    "Mexico": "🇲🇽 Mexico",
    "Saudi Arabia": "🇸🇦 Saudi Arabia",
    "Bond Information": "🖥️ Bond Information",
    "RVM Grid": "📊 RVM Grid",
    "ChatbotPage": "💬 ChatbotPage",
    "Ask Jay": "👴 Ask Jay",
    "Report Writer": "📝 Report Writer",
    "Deep Dive Radio": "📻 Deep Dive Radio",
    "Streaming Radio": "📡 Streaming Radio",
    "User Guide": "📖 User Guide",
    "Welcome": "👋 Welcome"
}

def initialize_google_services():
    """
    TODO: Google Docs Integration
    =============================
    This feature allows exporting reports to Google Docs and managing 
    documents in Google Drive. Currently disabled for Guinness version.
    
    To re-enable:
    1. Uncomment the code below
    2. Add credentials.json or set GOOGLE_CREDENTIALS_BASE64 env var
    3. Test with appropriate Google Workspace permissions
    
    Features when enabled:
    - Export reports as Google Docs
    - Save chat conversations to Drive
    - Collaborative document editing
    """
    
    # Placeholder - return None for both services
    st.session_state.docs_service = None
    st.session_state.drive_service = None
    return None, None
    
    # --- ORIGINAL GOOGLE SERVICES CODE (COMMENTED OUT) ---
    # SERVICE_ACCOUNT_FILE = 'credentials.json'
    # SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
    #
    # try:
    #     # Try to load from file first
    #     if os.path.exists(SERVICE_ACCOUNT_FILE):
    #         credentials = service_account.Credentials.from_service_account_file(
    #             SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    #     else:
    #         # Try to load from environment variable
    #         import json
    #         import base64
    #         creds_base64 = os.getenv('GOOGLE_CREDENTIALS_BASE64')
    #         if creds_base64:
    #             creds_json = base64.b64decode(creds_base64).decode('utf-8')
    #             creds_dict = json.loads(creds_json)
    #             credentials = service_account.Credentials.from_service_account_info(
    #                 creds_dict, scopes=SCOPES)
    #         else:
    #             st.warning("Google credentials not found. Some features may be limited.")
    #             return None, None
    #
    #     docs_service = build('docs', 'v1', credentials=credentials)
    #     drive_service = build('drive', 'v3', credentials=credentials)
    #
    #     st.session_state.docs_service = docs_service
    #     st.session_state.drive_service = drive_service
    #
    #     st.success("Google services initialized successfully.")
    #
    #     return docs_service, drive_service  # Return the services
    # except Exception as e:
    #     st.error(f"Failed to initialize Google services: {str(e)}")
    #     return None, None  # Return None for both in case of failure

# Initialize session state attribute if it does not exist
if 'welcome_shown' not in st.session_state:
    st.session_state.welcome_shown = False

# Initialize session state for thumbs clicked
if 'thumbs_up_clicked' not in st.session_state:
    st.session_state.thumbs_up_clicked = set()

if 'thumbs_down_clicked' not in st.session_state:
    st.session_state.thumbs_down_clicked = set()

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a bot. How can I help you?", additional_kwargs={"id": str(uuid.uuid4())})
    ]

# Initialize session state for Google services
if 'docs_service' not in st.session_state:
    st.session_state.docs_service = None

if 'drive_service' not in st.session_state:
    st.session_state.drive_service = None

if 'selected_file' not in st.session_state:
    st.session_state.selected_file = None
if 'selected_title' not in st.session_state:
    st.session_state.selected_title = None
if 'file_info' not in st.session_state:
    st.session_state.file_info = {}


# DUPLICATE FUNCTION - REMOVED (see line 80 for the main implementation)
# This was causing issues - keeping commented for reference
# def initialize_google_services():
#     SERVICE_ACCOUNT_FILE = 'credentials.json'
#     SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
#
#     try:
#         credentials = service_account.Credentials.from_service_account_file(
#             SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#
#         docs_service = build('docs', 'v1', credentials=credentials)
#         drive_service = build('drive', 'v3', credentials=credentials)
#
#         st.session_state.docs_service = docs_service
#         st.session_state.drive_service = drive_service
#
#         st.success("Google services initialized successfully.")
#     except Exception as e:
#         st.error(f"Failed to initialize Google services: {str(e)}")
#         # Return None for both services in case of an exception
#         return None, None

# Initialize Google services
if st.session_state.docs_service is None or st.session_state.drive_service is None:
    initialize_google_services()

def initialize_app_state():
    if "state" not in st.session_state:
        st.session_state.state = {
            "selected_reports": list(available_reports.values()),
            "dropdown_reports": list(available_reports.values()),
            "report_checkboxes": {name: True for name in available_reports},
            "current_report": "👋 Welcome",  # Updated to match the dropdown entry
            "time_selection": "Latest",
            "mode": "auto"
        }

    if "bond_selection_sidebar" not in st.session_state:
        st.session_state.bond_selection_sidebar = None

    # Initialize selected_report in session state
    if "selected_report" not in st.session_state:
        st.session_state.selected_report = st.session_state.state["current_report"]

st.markdown("""
    <style>
    .stApp {
        background-color: #1f1f1f;
        color: #ffffff;
    }
    .thumb-container {
        display: flex;
        gap: 10px;
        margin-top: 5px;
    }
    .thumb-image {
        cursor: pointer;
        transition: transform 0.2s;
    }
    .thumb-image:hover {
        transform: scale(1.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Define the color palette used by the reports
color_palette = [
    "#FFA500",  # Bright Orange
    "#007FFF",  # Azure Blue
    "#DC143C",  # Cherry Red
    "#39FF14",  # Electric Lime Green
    "#00FFFF",  # Cyan
    "#DA70D6"   # Vivid Purple
]

def scroll_to_top():
    scroll_script = """
    <script>
        window.scrollTo(0, 0);
    </script>
    """
    st.markdown(scroll_script, unsafe_allow_html=True)

def get_last_modified_date(file_path):
    return os.path.getmtime(file_path) if os.path.exists(file_path) else 0

def get_file_info(file, processed_files):
    file_name = file.stem
    if file_name in processed_files:
        return processed_files[file_name]
    return {
        "duration": "Unknown",
        "description": "",
        "source_url": "",
    }

def render_deep_dive_radio(sorted_files):
    st.title("Deep Dive Radio")

    # Set up correct paths
    current_dir = Path(__file__).parent
    json_file = current_dir / "processed_files.json"  # Ensure the file exists at this location

    # Load processed files metadata
    processed_files = load_processed_files(json_file)

    # Create placeholders for main content
    title_placeholder = st.empty()
    description_placeholder = st.empty()
    source_placeholder = st.empty()
    video_placeholder = st.empty()

    # Episodes in sidebar (if needed)
    # st.sidebar.header("Episodes")
    # for file in sorted_files:
    #     # Episode handling code...

    # Display selected episode
    if 'selected_file' in st.session_state and st.session_state.selected_file:
        file = st.session_state.selected_file
        file_info = get_file_info(file, processed_files)
        title = file.stem.replace('_', ' ').title()
        title_placeholder.write(f"Now playing: {title}")
        description_placeholder.write(file_info.get('description', ''))
        if file_info.get('source_url'):
            source_placeholder.markdown(f"[Source]({file_info['source_url']})")
        else:
            source_placeholder.empty()
        if file.exists():
            video_placeholder.video(str(file))
        else:
            video_placeholder.error(f"File not found: {file}")
    else:
        title_placeholder.write("Welcome to Deep Dive Radio")
        description_placeholder.write("Select an episode from the sidebar to start listening.")

def render_chatbot_page():
    st.title("Xtrillion Chatbot")
    st.write("Welcome to the Xtrillion Chatbot! Ask me anything about our reports and data.")
    
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatbotAndy(
            response_mode=st.session_state.state.get("mode", "auto"),
            docs_service=st.session_state.get("docs_service"),
            drive_service=st.session_state.get("drive_service")
        )
    
    # Call the main function from chatbot_demo
    chatbot_demo.main()

def render_main_content():
    current_report = st.session_state.get("selected_report", "👋 Welcome")

    if current_report == "👋 Welcome":
        display_welcome_page()
    elif current_report == "🖥️ Bond Information":
        create_bond_information_tab()
    elif current_report == "📖 User Guide":
        display_user_guide()
    elif current_report == "🟠 SKEWNBF":
        create_fund_report_tab(
            "Shin Kong Emerging Wealthy Nations Bond Fund",
            color_palette,
            st.session_state.state["time_selection"]
        )
    elif current_report == "🟢 SKESBF":
        create_fund_report_tab(
            "Shin Kong Environmental Sustainability Bond Fund",
            color_palette,
            st.session_state.state["time_selection"]
        )
    elif current_report == "🇮🇱 Israel":
        create_country_report_tab("Israel", color_palette)
    elif current_report == "🇶🇦 Qatar":
        create_country_report_tab("Qatar", color_palette)
    elif current_report == "🇲🇽 Mexico":
        create_country_report_tab("Mexico", color_palette)
    elif current_report == "🇸🇦 Saudi Arabia":
        create_country_report_tab("Saudi Arabia", color_palette)
    elif current_report == "📻 Deep Dive Radio":
        sorted_files = get_sorted_media_files()
        render_deep_dive_radio(sorted_files)
    elif current_report == "💬 ChatbotPage":
        render_chatbot_page()
    elif current_report == "📊 RVM Grid":
        # Use the corrected layout with sidebar status
        create_rvm_grid_tab()
    else:
        st.warning(f"Selected report '{current_report}' is not available.")

def generate_unique_key():
    timestamp = int(time.time() * 1000)
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"user_input_{timestamp}_{random_string}"

def handle_user_input(chatbot):
    unique_key = generate_unique_key()
    user_input = st.chat_input("Type your message here...", key=unique_key)

    if user_input:
        user_message_id = str(uuid.uuid4())
        user_message = {
            "type": "human",
            "content": user_input,
            "id": user_message_id,
        }
        st.session_state.chat_history.append(user_message)

        with st.chat_message("human", avatar="human_icon.png"):
            st.markdown(user_input)

        with st.chat_message("ai", avatar="chatbot_icon.png"):
            response_placeholder = st.empty()
            full_response = chatbot.generate_response(user_input, response_placeholder)

        ai_message_id = str(uuid.uuid4())
        ai_message = {
            "type": "ai",
            "content": full_response,
            "id": ai_message_id,
        }
        st.session_state.chat_history.append(ai_message)

        # Render thumbs immediately after generating the response
        chatbot.render_thumb_icons(ai_message_id, len(st.session_state.chat_history) - 1)


def load_engine():
    sentences_file = './openai_large_embeddings/openai_large_combined_sentences.txt'
    embeddings_file = './openai_large_embeddings/openai_large_combined_embeddings.npy'
    return QAEngine(sentences_file, embeddings_file)

def render_welcome_page():
    st.markdown("<h1 style='text-align: center;'>👋 Welcome to Xtrillion3 Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Your gateway to comprehensive credit reports, bond information, and AI-powered assistance.</p>", unsafe_allow_html=True)
    
    # You can add an image or any other welcome content here
    st.image("xtrillion_splash.png", use_column_width=True)
    
    # "Continue" button centered
    if st.button("Continue"):
        st.session_state.welcome_shown = True
        st.rerun()

def process_query(question, mode="auto", sentence_length="auto"):
    if mode == "none":
        # Use OpenAI directly without custom embeddings
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}],
            max_tokens=150
        )
        return {"answer": response.choices[0].message.content, "mode": "none"}
    
    engine = load_engine()
    
    if mode == "auto":
        mode = detect_intent(question)
    
    num_sentences = 7  # Default to 7 sentences as per your preference
    if sentence_length != "auto":
        try:
            num_sentences = int(sentence_length)
        except ValueError:
            st.warning("Invalid sentence length. Using default of 7 sentences.")
    
    answer = engine.get_answer(question, num_sentences, response_mode=mode)
    return {"answer": answer, "mode": mode}

def render_chatbot_page():
    chatbot_demo.main()

def render_report_writer():
    st.write("Report Writer page is under construction.")

def render_streaming_radio():
    st.write("Streaming Radio page is under construction.")

def render_ask_jay():
    st.write("Ask Jay page is under construction.")

def main():
 

    if "state" not in st.session_state:
        st.session_state.state = {
            "selected_reports": list(available_reports.values()),
            "dropdown_reports": list(available_reports.values()),
            "report_checkboxes": {name: True for name in available_reports},
            "current_report": "🇲🇽 Mexico",  # Set the default to Mexico
            "time_selection": "Latest",
            "mode": "auto"
        }

    if "selected_report" not in st.session_state:
        st.session_state.selected_report = st.session_state.state["current_report"]

    sorted_files = get_sorted_media_files()
    
    # Render the sidebar
    sidebar_demo.render_sidebar(available_reports, sorted_files)

    # Main content area
    main_content_placeholder = st.empty()
    with main_content_placeholder.container():
        if st.session_state.selected_report == "🇲🇽 Mexico":
            create_country_report_tab("Mexico", color_palette)
        else:
            render_main_content()

if __name__ == "__main__":
    main()
