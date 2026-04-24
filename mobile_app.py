import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables for local testing
load_dotenv()

# --- Page Configuration ---
st.set_page_config(page_title="Mobile Selector AI", page_icon="📱", layout="wide")

# Custom CSS for chat layout
st.markdown("""
    <style>
        .block-container { padding-bottom: 100px; }
        div[data-testid="stChatInput"] { position: fixed; bottom: 20px; z-index: 99; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for the current conversation only
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MOBILE SELECTOR SYSTEM INSTRUCTIONS ---
system_instruction = """
You are a Mobile Expert Advisor. You must follow this EXACT 5-step flow:

1. START: Enlist popular mobile companies (Samsung, Apple, Xiaomi, Vivo, Oppo, Infinix, etc.) and ask: "Which mobile company do you prefer?"
2. BUDGET: Once a company is chosen, ask: "What is your budget range (e.g., in PKR or USD)?"
3. RAM: Then ask: "How much RAM do you need (e.g., 4GB, 8GB, 12GB)?"
4. STORAGE: Then ask: "How much Internal Memory/Storage do you need (e.g., 64GB, 128GB, 256GB)?"
5. SUGGEST: Finally, provide a list of 3-5 specific mobile models that match ALL the user's criteria. Include brief key specs for each.

STRICT RULES:
- Do not jump ahead. Wait for the user to answer each question.
- Be professional and helpful.
- If a specific model isn't available for that budget/RAM, suggest the closest alternative.
"""

# --- Sidebar ---
with st.sidebar:
    st.title("📱 Mobile Advisor")
    st.write("Find your next smartphone.")
    st.write("---")
    if st.button("🗑️ Clear Search History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Main UI ---
st.title("📱 Smart Mobile Selector")
st.markdown("#### *Find the perfect smartphone based on your needs*")

# Display current chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
prompt = st.chat_input("Type your preference here...")

# Groq API Setup (Checks .env or Streamlit Secrets)
api_key = os.getenv("groq_api") or st.secrets.get("groq_api")

if prompt:
    if not api_key:
        st.error("API Key missing! Please add 'groq_api' to your secrets.")
    else:
        # Add user message to state and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": system_instruction}] + st.session_state.messages,
                model="llama-3.1-8b-instant"
            )
            reply = response.choices[0].message.content
            
            # Display assistant response and add to state
            with st.chat_message("assistant"):
                st.markdown(reply)
                
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
        except Exception as e:
            st.error(f"Error connecting to AI: {e}")