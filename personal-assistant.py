from dotenv import load_dotenv
import streamlit as st
import os
import textwrap
import google.generativeai as genai


# Function to format text as markdown with blockquote style
def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)


# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to generate response using Gemini API
def get_gemini_response(question):
    try:
        model = genai.GenerativeModel('gemini-pro')  # Ensure this is the correct model name
        response = model.generate_content(question)

        if response and hasattr(response, 'text'):
            return response.text
        else:
            if hasattr(response, 'candidate') and hasattr(response.candidate, 'safety_ratings'):
                print("Response blocked due to safety ratings:", response.candidate.safety_ratings)
            return "The response was blocked due to safety concerns."
    except ValueError as e:
        print(f"An error occurred: {e}")
        return "An error occurred while generating the response."


# Function to allow response text to be downloadable
def download_response(response_text):
    # Convert the response to a text file
    response_bytes = response_text.encode()
    st.download_button(
        label="Download Response",
        data=response_bytes,
        file_name="response.txt",
        mime="text/plain"
    )


# Set up the Streamlit page configuration
st.set_page_config(page_title="Rahul's Personal Assistant")

# Add custom CSS for styling (using a different color scheme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@200..700&display=swap');
    body {
        background-color: #2E3B4E;
        font-family: 'Oswald';
    }
    .main {
        color: #FFFFFF;
        background-color: #2E3B4E;
        border-radius: 10px;
        padding: 20px;
    }
    .stTextInput > div > div > input {
        border: 2px solid #4CAF50;
        border-radius: 5px;
        padding: 15px;
        font-size: 24px;
        color: #FFFFFF; /* White color for input text */
        background-color: #1E2A36; /* Dark background for input */
        width: 100%;
        font-family: 'Oswald';
    }
    .stButton > button {
        background-color: #F1C40F;
        color: black;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        font-family: 'Roboto', sans-serif;
    }
    .stButton > button:hover {
        background-color: #D4AC0D;
        color: white;
    }
    .stHeader {
        color: #F1C40F !important;
        font-weight: bold !important;
        font-style: italic;
        font-size: 36px !important;
        font-family: 'Roboto', sans-serif !important;
    }
    .input-label {
        color: #F1C40F;
        font-weight: bold;
        font-style: italic;
        font-size: 30px;
        font-family: 'Roboto', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Display the header with a new name
st.markdown('<h1 class="stHeader">Hey! I am Rahul\'s Personal Assistant. Ask me anything! I would love to help you🐋</h1>',
            unsafe_allow_html=True)

# Input label and text box with updated styling
st.markdown('<p class="input-label">Input:</p>', unsafe_allow_html=True)
input_text = st.text_input("", key="input")

# Ask button with updated styling
submit = st.button("Ask the question")

# Process the input and display the response
if submit:
    response = get_gemini_response(input_text)
    st.subheader("The Response is")
    st.write(to_markdown(response))  # Using the to_markdown function for formatting
    download_response(response)  # Add the download button for the response
