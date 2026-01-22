import streamlit as st

def load_css():
    """
    Injecte du CSS personnalisé pour améliorer le style de l'application Streamlit.
    """
    st.markdown("""
        <style>
            /* --- Import Google Fonts --- */
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

            /* --- Variables CSS --- */
            :root {
                --primary-color: #007cc2; /* Ed Scan Logo Blue */
                --secondary-color: #f0f8ff; /* Light Blue Background */
                --card-bg: #e6f7ff; /* Very Light Blue for cards */
                --white: #ffffff;
                --text-color: #333333;
                --button-color: #7dc1e0; /* Soft Blue */
                --button-hover: #5aaacd;
                --input-border: #b3e0f2;
            }

            /* --- Global Styles --- */
            .stApp {
                background-color: var(--secondary-color);
                font-family: 'Roboto', sans-serif;
                margin-top: -50px; /* Force move up */
            }

            /* --- Main Container Adjustments --- */
            .main .block-container {
                padding-top: 1rem; /* Reduce top padding */
                padding-bottom: 2rem;
                padding-left: 2rem;
                padding-right: 2rem; 
                max-width: 1200px;
            }

            /* --- Custom Header (Removes white bar) --- */
            .header {
                background-color: var(--primary-color);
                color: white;
                padding: 0.5rem 2rem; /* Reduced padding minimal */
                margin-left: -5rem;
                margin-right: -5rem;
                margin-top: -4rem; 
                margin-bottom: 1rem; /* Reduced bottom margin */
                display: flex;
                flex-direction: column;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .header h1 {
                margin: 0;
                font-size: 1.8rem; /* Slightly reduced to fit better if compact */
                font-weight: 700;
                display: flex;
                align-items: center;
                gap: 5px; /* Tighter gap */
                color: white;
            }
            .header p {
                margin: 0;
                font-size: 0.9rem;
                opacity: 0.95;
            }

            /* --- Tabs Styling --- */
            div[data-testid="stTabs"] {
                background-color: var(--white);
                padding: 1.5rem 1.5rem 0.5rem 1.5rem; /* Reduced bottom padding */
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            }
            
            div[data-baseweb="tab-list"] {
                display: flex;
                width: 100%;
                border-bottom: none;
                margin-bottom: 1rem; /* Reduced margin */
                gap: 10px;
            }
            
            button[data-baseweb="tab"] {
                flex: 1;
                font-weight: 800; 
                font-size: 2rem !important; /* Bumping to 1.5rem to ensure it is visible */
                border-radius: 8px;
                border: 2px solid var(--primary-color);
                background-color: white;
                color: var(--primary-color);
                padding: 0.75rem 1rem;
                transition: all 0.2s ease;
            }
            
             /* Active Tab State */
            button[data-baseweb="tab"][aria-selected="true"] {
                background-color: var(--primary-color) !important;
                color: white !important;
                border: 2px solid var(--primary-color);
            }

            /* --- Custom Separator (HR) --- */
            hr {
                margin: 0.5rem 0 !important; /* Force small margin on markdown '---' */
                border-top: 1px solid #eee !important;
            }

            /* --- Cards & Inputs Styling --- */
            /* Upload zones style */
            div[data-testid="stFileUploader"] section {
                background-color: var(--white);
                border: 2px dashed var(--primary-color);
                border-radius: 8px;
                margin-bottom: 0.5rem; /* Tighten up uploader bottom space */
            }
            
            /* File Uploader Button styling */
             [data-testid="stFileUploader"] button {
                color: var(--primary-color);
                border-color: var(--primary-color);
                background-color: var(--white);
            }
             [data-testid="stFileUploader"] button:hover {
                 background-color: var(--secondary-color);
             }

            /* --- Labels --- */
            .card-label {
                font-size: 1rem;
                font-weight: 600;
                color: #005a8d;
                margin-bottom: 0.2rem; /* Tighter label spacing */
                display: block;
                text-align: left;
            }

            /* --- Buttons --- */
            div.stButton > button {
                width: 100%;
                background-color: #87CEEB;
                color: white;
                font-size: 1.1rem;
                font-weight: 700;
                border: none;
                border-radius: 25px;
                padding: 0.8rem 1rem;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
            }
            div.stButton > button:hover {
                background-color: #70b9d8;
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            }
            
            /* --- Input Fields --- */
            div[data-testid="stNumberInput"] input {
                 border: 1px solid var(--input-border);
                 border-radius: 8px;
                 padding: 0.5rem;
            }
            
            /* Centering Helper (Though we use st.columns for structure) */
            .centered-container {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }

            /* --- Hide Sidebar / Default Elements --- */
            [data-testid="stSidebar"] {
                display: none;
            }
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}

        </style>
    """, unsafe_allow_html=True)

    # Inject Custom Header HTML
    st.markdown("""
        <div class="header">
            <h1>📄 Ed Scan</h1>
            <p>Fusionnez et gérez vos documents PDF facilement</p>
        </div>
    """, unsafe_allow_html=True)

