import streamlit as st
import random
from nltk.corpus import words
import nltk
import os

# Add the preloaded nltk_data folder to the NLTK data path
nltk.data.path.append(os.path.join(os.getcwd(), "nltk_data"))

# Load dictionary of words with 5-7 letters
def load_combined_dictionary():
    custom_words = []
    try:
        with open("myWordList.txt", "r") as file:
            custom_words = [line.strip() for line in file if 5 <= len(line.strip()) <= 7]
    except FileNotFoundError:
        st.warning("Custom word list file 'myWordList.txt' not found. Falling back to NLTK words.")
        custom_words = []
    
    if custom_words:
        return custom_words

    nltk_words = [word for word in words.words() if 5 <= len(word) <= 7]
    return nltk_words

def generate_password(word_list, first_word=None, second_word=None):
    if len(word_list) < 2:
        raise ValueError("Not enough words in the dictionary to generate a password.")

    first_word = first_word.capitalize() if first_word else random.choice([word for word in word_list if 5 <= len(word) <= 7]).capitalize()
    second_word = second_word.capitalize() if second_word else random.choice([word for word in word_list if 5 <= len(word) <= 7]).capitalize()

    number = str(random.randint(0, 9))
    number2 = str(random.randint(0, 9))
    symbol = random.choice(['?', '!', '@', '#', '$', '&'])

    password = f"{first_word}{number}{second_word}{symbol}{number2}"
    return password

# Load and save usage count
def load_usage_count():
    try:
        with open("usage_count.txt", "r") as file:
            count = int(file.read())
    except FileNotFoundError:
        count = 0
    return count

def save_usage_count(count):
    with open("usage_count.txt", "w") as file:
        file.write(str(count))

# Streamlit interface
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        color: #ff6347;
        background: linear-gradient(90deg, rgba(255, 99, 71, 1) 0%, rgba(255, 215, 0, 1) 100%);
        -webkit-background-clip: text;
        color: transparent;
        text-shadow: 0 0 2px rgba(0, 0, 0, 0.4), 0 0 5px rgba(255, 99, 71, 1); /* Reduced shadow size */
        font-family: 'Arial', sans-serif;
        animation: glow 30s ease-in-out infinite; /* Slower animation */
    }
    .counter {
        position: fixed;
        bottom: 10px;
        right: 10px;
        font-size: 12px;
        color: grey;
    }
    .shiny-button {
        width: 80%;  /* Making it match the width of the input fields */
        transition: all 0.5s ease;
        text-align: center;
        padding: 14px;
        font-size: 22px;
        margin: 0 auto;
        background-color: #4CAF50;
        border: none;
        border-radius: 5px;
        display: block;
    }
    .shiny-button:hover {
        background-color: #FFD700;
        box-shadow: 0 0 15px #FFD700; /* Reduced glow effect */
    }
    @keyframes glow {
        0% { text-shadow: 0 0 5px #ff6347, 0 0 10px #ff6347, 0 0 15px #ff6347, 0 0 20px #ff6347; }
        10% { text-shadow: 0 0 3px #ff7f50, 0 0 6px #ff7f50, 0 0 9px #ff7f50, 0 0 12px #ff7f50; }
        20% { text-shadow: 0 0 3px #ff4500, 0 0 6px #ff4500, 0 0 9px #ff4500, 0 0 12px #ff4500; }
        30% { text-shadow: 0 0 3px #32cd32, 0 0 6px #32cd32, 0 0 9px #32cd32, 0 0 12px #32cd32; }
        40% { text-shadow: 0 0 3px #00bfff, 0 0 6px #00bfff, 0 0 9px #00bfff, 0 0 12px #00bfff; }
        50% { text-shadow: 0 0 3px #8a2be2, 0 0 6px #8a2be2, 0 0 9px #8a2be2, 0 0 12px #8a2be2; }
        60% { text-shadow: 0 0 3px #ff1493, 0 0 6px #ff1493, 0 0 9px #ff1493, 0 0 12px #ff1493; }
        70% { text-shadow: 0 0 3px #ff69b4, 0 0 6px #ff69b4, 0 0 9px #ff69b4, 0 0 12px #ff69b4; }
        80% { text-shadow: 0 0 3px #adff2f, 0 0 6px #adff2f, 0 0 9px #adff2f, 0 0 12px #adff2f; }
        90% { text-shadow: 0 0 3px #ff6347, 0 0 6px #ff6347, 0 0 9px #ff6347, 0 0 12px #ff6347; }
        100% { text-shadow: 0 0 3px #FFD700, 0 0 6px #FFD700, 0 0 9px #FFD700, 0 0 12px #FFD700; }
    }
    </style>
    """, unsafe_allow_html=True)

# Centered title with gradient and glowing effect
st.markdown('<h1 class="title">Password Generator</h1>', unsafe_allow_html=True)

# Display usage count in the bottom right
usage_count = load_usage_count()
st.markdown(f'<div class="counter">App Usage Count: {usage_count}</div>', unsafe_allow_html=True)

# Create layout with column to center the button
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # "Generate Password" button centered with custom styling
    generate_password_clicked = st.button("🔓 Generate Password 🔒", key="generate_password", help="Click to generate a password", use_container_width=True)

# Input fields with 12-character limit, resized and centered
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    first_word_input = st.text_input("(Optional:) Enter the first word (up to 12 characters):", max_chars=12, key="first_word_input")
    second_word_input = st.text_input("(Optional:) Enter the second word (up to 12 characters):", max_chars=12, key="second_word_input")

if generate_password_clicked:
    word_list = load_combined_dictionary()

    if word_list:
        password = generate_password(word_list, first_word_input, second_word_input)
        
        # Adjust background color based on theme (dark mode or light mode)
        is_dark_mode = st.get_option("theme.primaryColor") == "#1f1f1f"  # Detecting dark mode (black background)
        background_color = "rgba(255, 255, 255, 0.7)" if is_dark_mode else "rgba(0, 0, 0, 0.1)"  # White background for dark mode, light for light mode
        
        # Display the generated password with background for contrast
        st.markdown(f"<h1 style='text-align: center; font-size: 60px; background-color: {background_color}; padding: 10px; border-radius: 10px;'>{password}</h1>", unsafe_allow_html=True)
        
        save_usage_count(usage_count + 1)
    else:
        st.error("Failed to load dictionary or insufficient words.")