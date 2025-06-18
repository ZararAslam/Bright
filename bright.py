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
    
    /* Hide Streamlit default elements - Safe approach */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    
    /* Hide Streamlit mobile navigation - targeted approach */
    .stActionButton {display: none !important;}
    div[data-testid="stActionButtonIcon"] {display: none !important;}
    .stDeployButton {display: none !important;}
    div[data-testid="stDeployButton"] {display: none !important;}
    div[data-testid="stBottomBlockContainer"] {display: none !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    
    /* Mobile specific - safe selectors only */
    @media (max-width: 768px) {
        .stActionButton {display: none !important;}
        div[data-testid="stActionButtonIcon"] {display: none !important;}
        .stDeployButton {display: none !important;}
        div[data-testid="stDeployButton"] {display: none !important;}
        
        /* Try to hide the navigation bar at bottom */
        .css-1d391kg {display: none !important;}
        .css-1rs6os {display: none !important;}
        .css-17eq0hr {display: none !important;}
    }
    
    /* Global styling - black background like BRIGHT website */
    .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Main content styling */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        background-color: #000000 !important;
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
        text-align: center !important;
        margin-bottom: 30px !important;
        padding: 20px !important;
        color: #ffffff !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
    }
    
    .bright-subheader {
        text-align: center !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        margin-bottom: 30px !important;
        opacity: 0.9 !important;
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
        background: linear-gradient(135deg, #fdbc2c, #fda503) !important;
        color: #000000 !important;
        padding: 15px 20px !important;
        border-radius: 20px 20px 6px 20px !important;
        max-width: 70% !important;
        min-width: 80px !important;
        word-wrap: break-word !important;
        box-shadow: 0 4px 16px rgba(253, 188, 44, 0.3) !important;
        font-size: 15px !important;
        line-height: 1.5 !important;
        display: inline-block !important;
        text-align: left !important;
        white-space: pre-wrap !important;
        vertical-align: top !important;
        margin: 0 !important;
        font-weight: 500 !important;
        border: 1px solid rgba(253, 188, 44, 0.5) !important;
    }
    
    /* Remove extra spacing from user bubble content */
    .user-bubble * {
        margin: 0 !important;
        padding: 0 !important;
        color: #000000 !important;
    }
    
    .user-bubble *:last-child {
        margin-bottom: 0 !important;
    }
    
    .bot-bubble {
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d) !important;
        color: #ffffff !important;
        padding: 15px 20px !important;
        border-radius: 20px 20px 20px 6px !important;
        max-width: 70% !important;
        min-width: 80px !important;
        word-wrap: break-word !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
        font-size: 15px !important;
        line-height: 1.5 !important;
        border: 1px solid rgba(253, 165, 3, 0.2) !important;
        display: inline-block !important;
        text-align: left !important;
        white-space: pre-wrap !important;
        vertical-align: top !important;
        position: relative !important;
        font-weight: 500 !important;
    }
    
    /* Markdown styling within bot bubbles */
    .bot-bubble h1, .bot-bubble h2, .bot-bubble h3 {
        margin-top: 12px !important;
        margin-bottom: 8px !important;
        background: linear-gradient(90deg, #fda503, #f737d8) !important;
        background-clip: text !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-weight: 600 !important;
    }
    
    .bot-bubble p {
        margin: 8px 0 !important;
        color: #ffffff !important;
    }
    
    .bot-bubble ul, .bot-bubble ol {
        margin: 12px 0 !important;
        padding-left: 20px !important;
        color: #ffffff !important;
    }
    
    .bot-bubble li {
        margin: 4px 0 !important;
        color: #ffffff !important;
    }
    
    .bot-bubble code {
        background: linear-gradient(135deg, #fdbc2c, #fda503) !important;
        color: #000000 !important;
        padding: 3px 6px !important;
        border-radius: 6px !important;
        font-family: 'Courier New', monospace !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }
    
    .bot-bubble pre {
        background-color: #0a0a0a !important;
        border: 1px solid rgba(253, 165, 3, 0.3) !important;
        padding: 12px !important;
        border-radius: 8px !important;
        border-left: 4px solid #fdbc2c !important;
        overflow-x: auto !important;
        margin: 12px 0 !important;
        color: #ffffff !important;
    }
    
    .bot-bubble pre code {
        background: none !important;
        color: #ffffff !important;
        padding: 0 !important;
    }
    
    /* Remove extra spacing from bot bubble content */
    .bot-bubble * {
        margin-bottom: 0 !important;
        color: #ffffff !important;
    }
    
    .bot-bubble *:last-child {
        margin-bottom: 0 !important;
    }
    
    /* Timestamp styling */
    .timestamp {
        font-size: 11px !important;
        color: #888 !important;
        margin: 4px 8px !important;
        opacity: 0.8 !important;
    }
    
    /* Input styling with BRIGHT luminous border */
    .stTextInput > div > div {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        border: 2px solid transparent !important;
        background: linear-gradient(#1a1a1a, #1a1a1a) padding-box, 
                    linear-gradient(90deg, #fda503 -10%, #f737d8 20%, #0e60ff 80%, #07c2f7) border-box !important;
        padding: 15px 25px !important;
        font-size: 15px !important;
        color: #ffffff !important;
        transition: all 0.3s ease !important;
        outline: none !important;
        box-shadow: none !important;
    }
    
    .stTextInput > div > div > input:focus {
        background: linear-gradient(#2d2d2d, #2d2d2d) padding-box, 
                    linear-gradient(90deg, #fda503 -10%, #f737d8 20%, #0e60ff 80%, #07c2f7) border-box !important;
        box-shadow: 0 0 20px rgba(253, 165, 3, 0.4) !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #888 !important;
    }
    
    .stTextInput > div > div > input:disabled {
        background: linear-gradient(#0a0a0a, #0a0a0a) padding-box, 
                    linear-gradient(90deg, rgba(253, 165, 3, 0.3) -10%, rgba(247, 55, 216, 0.3) 20%, rgba(14, 96, 255, 0.3) 80%, rgba(7, 194, 247, 0.3)) border-box !important;
        opacity: 0.6 !important;
        cursor: not-allowed !important;
        color: #888 !important;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        text-align: center !important;
    }
    
    .stSpinner > div > div {
        border-color: #fdbc2c transparent transparent transparent !important;
    }
    
    /* Demo notice styling with BRIGHT theme */
    .demo-notice {
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d) !important;
        border: 1px solid rgba(253, 165, 3, 0.3) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        margin: 30px 0 !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
        position: relative !important;
    }
    
    .demo-notice::before {
        content: '' !important;
        position: absolute !important;
        inset: -1px !important;
        padding: 1px !important;
        background: linear-gradient(90deg, #fda503 -10%, #f737d8 20%, #0e60ff 80%, #07c2f7) !important;
        border-radius: inherit !important;
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0) !important;
        mask-composite: exclude !important;
        -webkit-mask-composite: xor !important;
        z-index: -1 !important;
    }
    
    .demo-notice strong {
        background: linear-gradient(90deg, #fdbc2c, #fda503) !important;
        background-clip: text !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    
    .demo-notice {
        color: #ffffff !important;
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex !important;
        justify-content: flex-start !important;
        margin: 15px 0 !important;
    }
    
    .typing-bubble {
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d) !important;
        border: 1px solid rgba(253, 165, 3, 0.2) !important;
        border-radius: 20px 20px 20px 6px !important;
        padding: 12px 18px !important;
        color: #fdbc2c !important;
        font-style: italic !important;
        animation: brightPulse 2s ease-in-out infinite !important;
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
        max-height: 65vh !important;
        overflow-y: auto !important;
        padding-right: 10px !important;
        margin-bottom: 25px !important;
        scroll-behavior: smooth !important;
    }
    
    /* Custom scrollbar with BRIGHT theme */
    .chat-messages::-webkit-scrollbar {
        width: 8px !important;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: #1a1a1a !important;
        border-radius: 10px !important;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #fdbc2c, #fda503) !important;
        border-radius: 10px !important;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #fda503, #f737d8) !important;
    }
    
    /* Footer styling */
    .bright-footer {
        text-align: center !important;
        margin-top: 30px !important;
        color: #888 !important;
        font-size: 12px !important;
    }
    
    .bright-footer strong {
        background: linear-gradient(90deg, #fdbc2c, #fda503) !important;
        background-clip: text !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-weight: 600 !important;
    }
    
    /* Title styling override */
    .stApp h1 {
        display: none !important;
    }
    
    /* Mobile-friendly adjustments */
    @media (max-width: 768px) {
        .user-bubble, .bot-bubble {
            max-width: 85% !important;
            font-size: 14px !important;
        }
        
        .bright-header {
            font-size: 2rem !important;
        }
        
        .chat-container {
            padding: 15px !important;
        }
        
        /* Mobile chat messages container */
        .chat-messages {
            max-height: 60vh !important;
            margin-bottom: 20px !important;
            padding-bottom: 20px !important;
        }
        
        /* Mobile input styling - fixed positioning above keyboard */
        .stTextInput {
            position: fixed !important;
            bottom: 0 !important;
            left: 0 !important;
            right: 0 !important;
            z-index: 1000 !important;
            background-color: #000000 !important;
            padding: 15px !important;
            border-top: 1px solid rgba(253, 165, 3, 0.2) !important;
        }
        
        .stTextInput > div > div > input {
            font-size: 16px !important; /* Prevents zoom on iOS */
            padding: 12px 20px !important;
            width: 100% !important;
        }
        
        /* Add bottom padding to main content to prevent overlap */
        .main .block-container {
            padding-bottom: 100px !important;
        }
    }
    
    /* Desktop specific styles */
    @media (min-width: 769px) {
        .stTextInput {
            position: relative !important;
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

# Function to send message (WhatsApp-style)
def send_message():
    user_input = st.session_state.user_input.strip()
    if not user_input or st.session_state.is_processing:
        return
    
    # Add user message to chat immediately
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user", 
        "content": user_input,
        "timestamp": timestamp
    })
    
    # Set processing state and clear input immediately
    st.session_state.is_processing = True
    # Clear the input by setting it to empty string
    st.session_state.user_input = ""

# Custom header with BRIGHT branding
st.markdown("""
    <div class="bright-header">
        BRIGHT SPORTS AI
    </div>
    <div class="bright-subheader">
        Your AI-powered <span style="background: linear-gradient(90deg, #fda503 -10%, #f737d8 20%, #0e60ff 80%, #07c2f7); background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 600;">BRIGHT</span> assistant • Available <span style="background: linear-gradient(90deg, #fda503 -10%, #f737d8 20%, #0e60ff 80%, #07c2f7); background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 600;">24/7</span>
    </div>
""", unsafe_allow_html=True)

# Chat messages container
with st.container():
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
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
                    🔥 BRIGHT is typing...
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Process assistant response if needed
if st.session_state.is_processing and len(st.session_state.messages) > 0:
    # Get the last user message
    last_user_message = None
    for msg in reversed(st.session_state.messages):
        if msg["role"] == "user":
            last_user_message = msg["content"]
            break
    
    if last_user_message:
        # Get assistant response
        assistant_response = get_assistant_response(last_user_message)
        
        # Add assistant response to chat
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "assistant", 
            "content": assistant_response,
            "timestamp": timestamp
        })
        
        # Reset processing state
        st.session_state.is_processing = False
        st.rerun()

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

# Auto-scroll to bottom for new messages
if st.session_state.messages or st.session_state.is_processing:
    st.markdown("""
        <script>
        function smartScroll() {
            // Only scroll the chat messages container, not the whole page
            var chatMessages = document.querySelector('.chat-messages');
            if (chatMessages) {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
            
            // On mobile, keep messages visible above the fixed input
            if (window.innerWidth <= 768) {
                // Don't scroll the page on mobile, just the chat container
                var lastMessage = document.querySelector('.message-container:last-child');
                if (lastMessage && chatMessages) {
                    // Scroll within the chat container to show the latest message
                    var containerBottom = chatMessages.offsetTop + chatMessages.offsetHeight;
                    var messageBottom = lastMessage.offsetTop + lastMessage.offsetHeight;
                    
                    if (messageBottom > containerBottom) {
                        chatMessages.scrollTop = chatMessages.scrollHeight;
                    }
                }
            } else {
                // On desktop, gently scroll to show the latest message
                setTimeout(function() {
                    var lastMessage = document.querySelector('.message-container:last-child');
                    if (lastMessage) {
                        lastMessage.scrollIntoView({ 
                            behavior: 'smooth', 
                            block: 'nearest'
                        });
                    }
                }, 100);
            }
        }
        
        // Execute scroll function
        smartScroll();
        
        // Execute again after content loads
        setTimeout(smartScroll, 300);
        </script>
    """, unsafe_allow_html=True)
