import streamlit as st
import openai
import time
import markdown2
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="BRIGHT Sports AI Support",
    page_icon="⚽",
    layout="wide"
)

# Configure OpenAI
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    ASSISTANT_ID = st.secrets.get("ASSISTANT_ID", "asst_wJLIS47W6EnaQFjrHRwPXpOC")
except Exception as e:
    st.error("Please configure OPENAI_API_KEY in your Streamlit secrets.")
    st.stop()

# BRIGHT-themed CSS matching the website aesthetic
st.markdown("""
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global styling - black background like BRIGHT website */
    .stApp {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Main content styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: #000000;
    }
    
    /* Chat container styling */
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
        background-color: #000000;
    }
    
    /* Header styling with white text */
    .bright-header {
        text-align: center;
        margin-bottom: 30px;
        padding: 20px;
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .bright-subheader {
        text-align: center;
        color: #ffffff;
        font-size: 1.1rem;
        margin-bottom: 30px;
        opacity: 0.9;
    }
    
    /* Message bubbles */
    .message-container {
        margin: 15px 0;
        width: 100%;
        clear: both;
    }
    
    .user-container {
        text-align: right;
    }
    
    .bot-container {
        text-align: left;
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #fdbc2c, #fda503);
        color: #000000;
        padding: 15px 20px;
        border-radius: 20px 20px 6px 20px;
        max-width: 70%;
        min-width: 80px;
        word-wrap: break-word;
        box-shadow: 0 4px 16px rgba(253, 188, 44, 0.3);
        font-size: 15px;
        line-height: 1.5;
        display: inline-block;
        text-align: left;
        white-space: pre-wrap;
        vertical-align: top;
        margin: 0;
        font-weight: 500;
        border: 1px solid rgba(253, 188, 44, 0.5);
    }
    
    /* Remove extra spacing from user bubble content */
    .user-bubble * {
        margin: 0;
        padding: 0;
        color: #000000;
    }
    
    .user-bubble *:last-child {
        margin-bottom: 0;
    }
    
    .bot-bubble {
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
        color: #ffffff;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 6px;
        max-width: 70%;
        min-width: 80px;
        word-wrap: break-word;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
        font-size: 15px;
        line-height: 1.5;
        border: 1px solid rgba(253, 165, 3, 0.2);
        display: inline-block;
        text-align: left;
        white-space: pre-wrap;
        vertical-align: top;
        position: relative;
    }
    
    /* BRIGHT gradient border effect for bot messages */
    .bot-bubble::before {
        content: '';
        position: absolute;
        inset: -1px;
        padding: 1px;
        background: linear-gradient(90deg, #fda503 -10%, #f737d8 20%, #0e60ff 80%, #07c2f7);
        border-radius: inherit;
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask-composite: exclude;
        -webkit-mask-composite: xor;
        z-index: -1;
    }
    
    /* Markdown styling within bot bubbles */
    .bot-bubble h1, .bot-bubble h2, .bot-bubble h3 {
        margin-top: 12px;
        margin-bottom: 8px;
        background: linear-gradient(90deg, #fda503, #f737d8);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
    }
    
    .bot-bubble p {
        margin: 8px 0;
        color: #ffffff;
    }
    
    .bot-bubble ul, .bot-bubble ol {
        margin: 12px 0;
        padding-left: 20px;
        color: #ffffff;
    }
    
    .bot-bubble li {
        margin: 4px 0;
        color: #ffffff;
    }
    
    .bot-bubble code {
        background: linear-gradient(135deg, #fdbc2c, #fda503);
        color: #000000;
        padding: 3px 6px;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        font-weight: 500;
    }
    
    .bot-bubble pre {
        background-color: #0a0a0a;
        border: 1px solid rgba(253, 165, 3, 0.3);
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #fdbc2c;
        overflow-x: auto;
        margin: 12px 0;
        color: #ffffff;
    }
    
    .bot-bubble pre code {
        background: none;
        color: #ffffff;
        padding: 0;
    }
    
    /* Remove extra spacing from bot bubble content */
    .bot-bubble * {
        margin-bottom: 0;
    }
    
    .bot-bubble *:last-child {
        margin-bottom: 0;
    }
    
    /* Timestamp styling */
    .timestamp {
        font-size: 11px;
        color: #888;
        margin: 4px 8px;
        opacity: 0.8;
    }
    
    /* Input styling with BRIGHT theme */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid rgba(253, 165, 3, 0.3);
        padding: 15px 25px;
        font-size: 15px;
        background-color: #1a1a1a;
        color: #ffffff;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border: 2px solid #fdbc2c;
        box-shadow: 0 0 0 0.2rem rgba(253, 188, 44, 0.25);
        background-color: #2d2d2d;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #888;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        text-align: center;
    }
    
    .stSpinner > div > div {
        border-color: #fdbc2c #transparent #transparent #transparent;
    }
    
    /* Demo notice styling with BRIGHT theme */
    .demo-notice {
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
        border: 1px solid rgba(253, 165, 3, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin: 30px 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        position: relative;
    }
    
    .demo-notice::before {
        content: '';
        position: absolute;
        inset: -1px;
        padding: 1px;
        background: linear-gradient(90deg, #fda503 -10%, #f737d8 20%, #0e60ff 80%, #07c2f7);
        border-radius: inherit;
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask-composite: exclude;
        -webkit-mask-composite: xor;
        z-index: -1;
    }
    
    .demo-notice strong {
        background: linear-gradient(90deg, #fdbc2c, #fda503);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .demo-notice {
        color: #ffffff;
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        justify-content: flex-start;
        margin: 15px 0;
    }
    
    .typing-bubble {
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
        border: 1px solid rgba(253, 165, 3, 0.2);
        border-radius: 20px 20px 20px 6px;
        padding: 12px 18px;
        color: #fdbc2c;
        font-style: italic;
        animation: brightPulse 2s ease-in-out infinite;
    }
    
    @keyframes brightPulse {
        0% { 
            opacity: 0.6;
            box-shadow: 0 0 10px rgba(253, 188, 44, 0.1);
        }
        50% { 
            opacity: 1;
            box-shadow: 0 0 20px rgba(253, 188, 44, 0.3);
        }
        100% { 
            opacity: 0.6;
            box-shadow: 0 0 10px rgba(253, 188, 44, 0.1);
        }
    }
    
    /* Scrollable chat area */
    .chat-messages {
        max-height: 65vh;
        overflow-y: auto;
        padding-right: 10px;
        margin-bottom: 25px;
        scroll-behavior: smooth;
    }
    
    /* Custom scrollbar with BRIGHT theme */
    .chat-messages::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: #1a1a1a;
        border-radius: 10px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #fdbc2c, #fda503);
        border-radius: 10px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #fda503, #f737d8);
    }
    
    /* Footer styling */
    .bright-footer {
        text-align: center;
        margin-top: 30px;
        color: #888;
        font-size: 12px;
    }
    
    .bright-footer strong {
        background: linear-gradient(90deg, #fdbc2c, #fda503);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
    }
    
    /* Title styling override */
    .stApp h1 {
        display: none;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .user-bubble, .bot-bubble {
            max-width: 85%;
            font-size: 14px;
        }
        
        .bright-header {
            font-size: 2rem;
        }
        
        .chat-container {
            padding: 15px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "thread_id" not in st.session_state:
    try:
        thread = openai.beta.threads.create()
        st.session_state.thread_id = thread.id
        st.session_state.messages = []
        st.session_state.is_processing = False
    except Exception as e:
        st.error(f"Failed to create OpenAI thread: {str(e)}")
        st.stop()

# Function to get assistant response
def get_assistant_response(user_message):
    try:
        # Add user message to thread
        openai.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=user_message
        )
        
        # Create and run the assistant
        run = openai.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=ASSISTANT_ID
        )
        
        # Wait for completion with timeout
        timeout = 60  # 60 seconds timeout
        start_time = time.time()
        
        while True:
            if time.time() - start_time > timeout:
                raise Exception("Request timed out")
                
            status = openai.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
            
            if status.status == "completed":
                break
            elif status.status == "failed":
                raise Exception("Assistant run failed")
            elif status.status == "expired":
                raise Exception("Assistant run expired")
                
            time.sleep(1)
        
        # Get the latest message
        messages = openai.beta.threads.messages.list(
            thread_id=st.session_state.thread_id,
            limit=1
        )
        
        if messages.data:
            return messages.data[0].content[0].text.value
        else:
            raise Exception("No response received")
            
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Function to send message
def send_message():
    user_input = st.session_state.user_input.strip()
    if not user_input or st.session_state.is_processing:
        return
    
    # Add user message to chat
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user", 
        "content": user_input,
        "timestamp": timestamp
    })
    
    # Set processing state
    st.session_state.is_processing = True
    st.session_state.user_input = ""
    
    # Get assistant response
    assistant_response = get_assistant_response(user_input)
    
    # Add assistant response to chat
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "assistant", 
        "content": assistant_response,
        "timestamp": timestamp
    })
    
    # Reset processing state
    st.session_state.is_processing = False

# Custom header with BRIGHT branding
st.markdown("""
    <div class="bright-header">
        BRIGHT SPORTS AI
    </div>
    <div class="bright-subheader">
        Your AI-powered sports equipment assistant • Available 24/7
    </div>
""", unsafe_allow_html=True)

# Chat messages container
with st.container():
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    # Display welcome message if no chat history
    if not st.session_state.messages:
        st.markdown(f"""
            <div class="message-container bot-container">
                <div>
                    <div class="bot-bubble">
                        🌟 <strong>Welcome to BRIGHT Sports AI Support!</strong><br><br>
                        I'm here to help you with:<br>
                        • Product information about our holographic sports equipment<br>
                        • Order status and shipping details<br>
                        • Technical specifications and features<br>
                        • Returns and warranty support<br><br>
                        How can I light up your game today?
                    </div>
                    <div class="timestamp">{datetime.now().strftime("%H:%M")}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Display chat history
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f"""
                <div class="message-container user-container">
                    <div>
                        <div class="user-bubble">{msg['content']}</div>
                        <div class="timestamp" style="text-align: right;">{msg.get('timestamp', '')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Convert markdown to HTML for assistant messages
            try:
                html_content = markdown2.markdown(
                    msg['content'], 
                    extras=['fenced-code-blocks', 'tables', 'code-friendly']
                )
            except:
                html_content = msg['content']
            
            st.markdown(f"""
                <div class="message-container bot-container">
                    <div>
                        <div class="bot-bubble">{html_content}</div>
                        <div class="timestamp">{msg.get('timestamp', '')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Show typing indicator when processing
    if st.session_state.is_processing:
        st.markdown("""
            <div class="typing-indicator">
                <div class="typing-bubble">
                    🔥 BRIGHT AI is thinking...
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Input section
st.markdown("---")

# Single column for input
st.text_input(
    label="Message",
    placeholder="Ask about BRIGHT products, orders, or support..." + (" (Processing...)" if st.session_state.is_processing else ""),
    key="user_input",
    on_change=send_message,
    label_visibility="collapsed",
    disabled=st.session_state.is_processing
)

# Demo notice with BRIGHT branding
st.markdown("""
<div class="demo-notice">
    <strong>⚡ Demo Notice:</strong> This is a demonstration of BRIGHT Sports AI customer support capabilities. 
    The production version will include full product catalog integration and real-time order tracking. 
    For custom features or integration support, contact us at <strong>hello@altorix.co.uk</strong>
</div>
""", unsafe_allow_html=True)

# Footer with BRIGHT branding
st.markdown("""
<div class="bright-footer">
    Powered by <strong>ALTORIX</strong> • Built for athletes who light up the night
</div>
""", unsafe_allow_html=True)

# Auto-scroll to bottom (JavaScript injection)
if st.session_state.messages or st.session_state.is_processing:
    st.markdown("""
        <script>
        setTimeout(function() {
            var chatMessages = document.querySelector('.chat-messages');
            if (chatMessages) {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        }, 100);
        </script>
    """, unsafe_allow_html=True)
