import streamlit as st
import random
from nltk.corpus import words
import nltk
import os

# Add the preloaded nltk_data folder to the NLTK data path
nltk.data.path.append(os.path.join(os.getcwd(), "nltk_data"))

# Load dictionary of words with 5-7 letters
def load_combined_dictionary():
    """
    Load a combined dictionary of words using NLTK's word corpus and a custom text file.
    Filters for words with 5-7 characters.
    Prioritizes local dictionary; falls back on NLTK if needed.
    """
    custom_words = []

    # Try loading custom words from a text file first
    try:
        with open("myWordList.txt", "r") as file:
            custom_words = [line.strip() for line in file if 5 <= len(line.strip()) <= 7]
    except FileNotFoundError:
        st.warning("Custom word list file 'myWordList.txt' not found. Falling back to NLTK words.")
        custom_words = []

    # If custom words are available, use them; otherwise, fall back to NLTK
    if custom_words:
        return custom_words

    # If no custom dictionary, load words from NLTK
    nltk_words = [word for word in words.words() if 5 <= len(word) <= 7]
    return nltk_words

def generate_password(word_list, first_word=None, second_word=None):
    """
    Generate a password in the format: FirstWord5-7letters+Number+SecondWord5-7letters+Symbol+Number2
    """
    if len(word_list) < 2:
        raise ValueError("Not enough words in the dictionary to generate a password.")

    # Auto-generate words if not provided by the user
    first_word = first_word.capitalize() if first_word else random.choice([word for word in word_list if 5 <= len(word) <= 7]).capitalize()
    second_word = second_word.capitalize() if second_word else random.choice([word for word in word_list if 5 <= len(word) <= 7]).capitalize()

    # Generate numbers and symbol
    number = str(random.randint(0, 9))
    number2 = str(random.randint(0, 9))
    symbol = random.choice(['?', '!', '@', '#', '$', '&'])

    # Combine to form the password
    password = f"{first_word}{number}{second_word}{symbol}{number2}"
    return password

# Streamlit interface
st.title("Password Generator")

# Move "Generate Password" button above the inputs and make it larger
generate_password_clicked = st.button("🔒 Generate Password", use_container_width=True)

# Input fields with 12-character limit
first_word_input = st.text_input("Enter the first word (Optional, up to 12 characters):", max_chars=12)
second_word_input = st.text_input("Enter the second word (Optional, up to 12 characters):", max_chars=12)

if generate_password_clicked:
    word_list = load_combined_dictionary()

    if word_list:
        password = generate_password(word_list, first_word_input, second_word_input)
        st.markdown(f"<h1 style='text-align: center; font-size: 60px; color: black;'>{password}</h1>", unsafe_allow_html=True)
    else:
        st.error("Failed to load dictionary or insufficient words.")