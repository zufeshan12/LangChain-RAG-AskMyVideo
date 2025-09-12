import streamlit as st
import time
from process_transcript import ProcessTranscript


# Custom CSS for background
def add_title_and_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = "data:image/png;base64," + (data.encode("base64") if hasattr(data, "encode") else __import__("base64").b64encode(data).decode())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .fancy-title {{
            font-size: 3em;
            font-weight: 900;
            text-align: center;
            background: -webkit-linear-gradient(45deg, #667850, #87ab76);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
            margin-bottom: 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
st.markdown('<div class="fancy-title">🎥 Ask My Video </div>', unsafe_allow_html=True)

# Call function with local background image
add_title_and_bg("background.png")

#initialize session state for input query
if "input_query" not in st.session_state:
    st.session_state.input_query = ""

# Custom CSS for text_input label + box
st.markdown(
    """
    <style>
    /* Label styling */
    label[data-baseweb="label"] {
        color: white !important;
        font-size: 1.2em !important;
        font-weight: 600 !important;
    }

    /* Input box styling */
    div[data-baseweb="input"] > div {
        background-color: rgba(255, 255, 255, 0.1) !important; /* semi-transparent */
        border: 1px solid #ccc !important;
        border-radius: 10px !important;
        padding: 8px !important;
    }

    /* Placeholder text styling */
    input::placeholder {
        color: #ddd !important;
        font-size: 1em !important;
    }

    /* Actual text typed */
    input {
        color: grey !important;
        font-size: 1.05em !important;
        font-weight: 200 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# test with example query
url = st.text_input(label="Paste URL link",key="input_url") #"https://www.youtube.com/watch?v=Ny-qhl4N9dY"
query = st.text_input("Type your question",key="input_query",value=st.session_state.input_query)

# Define custom CSS for the button
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #87AE73; #sage-green 
    color: white; 
}
</style>""", unsafe_allow_html=True)

# on-click button
if st.button('Ask AI',width="stretch",type="secondary"):
    if url and query:
            st.markdown(
        """
        <style>
        .answer-box {
            background-color: rgba(0, 0, 0, 0.5); /* dark semi-transparent */
            color: white;
            padding: 15px 20px;
            border-radius: 12px;
            font-size: 1.05em;
            line-height: 1.6;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        }
        </style>
        """,
        unsafe_allow_html=True
            )

        # Display result inside styled box
            result = ProcessTranscript.process_transcript(url=url,query=query)
            st.markdown(f"<div class='answer-box'>{result}</div>", unsafe_allow_html=True)
            
            #st.write("**Answer: **", result)

# Callback function to clear the text area
def clear_text_input():
    st.session_state.input_query = ""
# clear text input on button click
st.button('Clear',on_click=clear_text_input,width="stretch")

# Footer / Citation
st.markdown(
    """
    <hr style="margin-top: 70px; margin-bottom: 10px; border: 1px solid gray;">
    <p style='text-align: center; color: lightgray; font-size: 1.0em;'>
        Crafted with ❤️ by Zufeshan Imran · © 2025
    </p>
    """,
    unsafe_allow_html=True
)
