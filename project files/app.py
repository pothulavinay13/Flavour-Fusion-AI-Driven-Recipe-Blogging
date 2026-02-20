import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- INITIALIZE ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="Flavour Fusion AI", layout="wide")

# --- CUSTOM CSS FOR BLACK & WHITE CHAT ---
st.markdown("""
    <style>
    .stChatFloatingInputContainer { background-color: #FFFFFF; border-top: 1px solid #E0E0E0; }
    .stChatMessage { border-radius: 5px; border: 1px solid #F0F2F6; margin-bottom: 10px; }
    /* Force chat input to the bottom of the main area */
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (Memory for Iteration) ---
if "messages" not in st.session_state:
    st.session_state.messages = [] # Stores chat history

# --- SIDEBAR (Initial Parameters) ---
with st.sidebar:
    st.markdown(" FOODIE AI RECIPE CREATOR")
    st.divider()
    topic = st.text_input("RECIPE TOPIC", placeholder="e.g. Italian Pasta")
    ingredients = st.text_area("INVENTORY", placeholder="Garlic, Tomato, Basil...")
    word_count = st.select_slider("WORD COUNT", options=[300, 500, 800], value=500)
    
    if st.button("START NEW RECIPE"):
        st.session_state.messages = [] # Clear history to start fresh
        initial_prompt = f"Create a {word_count} word recipe blog for {topic} using {ingredients}."
        st.session_state.messages.append({"role": "user", "content": initial_prompt})
        
        # Immediate AI Response for the initial request
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(initial_prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- MAIN CHAT AREA ---
st.header("📋 RECIPE CONVERSATION")

# 1. Display Chat History
for message in st.session_state.messages:
    # Use "user" for your prompts and "assistant" for AI
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. Chat Input (Pinned to the bottom for Iteration)
if prompt := st.chat_input("Suggest a change... (e.g. 'Add a vegan substitute' or 'Make it shorter')"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate iterative response
    with st.chat_message("assistant"):
        with st.spinner("◼️ REFINING RECIPE..."):
            model = genai.GenerativeModel('gemini-2.5-flash')
            # Pass full context for iteration
            full_history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            response = model.generate_content(full_history)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})