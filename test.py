import streamlit as st

# Set a background gradient so the glassmorphic blur effect is visible
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1f4068, #162447, #1b1b2f);
        background-attachment: fixed;
    }
    
    /* Target Streamlit text input wrapper elements */
    div[data-testid="stTextInput"] input {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    
    /* Focus state for the input box */
    div[data-testid="stTextInput"] input:focus {
        border-color: rgba(255, 255, 255, 0.4) !important;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.1) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Glassmorphism Input Example")

# Standard Streamlit text input styled via the CSS injection above
user_input = st.text_input("Enter your prompt or text:")

if user_input:
    st.success(f"You typed: {user_input}")
