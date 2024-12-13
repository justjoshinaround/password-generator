import streamlit as st
import random
from nltk.corpus import words
import nltk

# Download word list if not already present
try:
    nltk.data.find('corpora/words.zip')  # Check if the word list is already downloaded
except LookupError:
    nltk.download('words')  # Download it if not present

# Load dictionary of words with 4-6 letters
def load_dictionary():
    """
    Load a dictionary of words using NLTK's word corpus.
    Filters for words with 4-6 characters.
    """
    return [word for word in words.words() if 4 <= len(word) <= 6]

def generate_password(word_list):
    """
    Generate a password in the format: FirstWord5-6letters+Number+SecondWord4-5letters+Symbol
    """
    if len(word_list) < 2:
        raise ValueError("Not enough words in the dictionary to generate a password.")

    # Select words
    first_word = random.choice([word for word in word_list if 5 <= len(word) <= 6]).capitalize()
    second_word = random.choice([word for word in word_list if 4 <= len(word) <= 5]).capitalize()

    # Generate number and symbol
    number = str(random.randint(0, 9))
    symbol = random.choice(['?', '!', '@', '#', '$', '&'])

    # Combine to form the password
    password = f"{first_word}{number}{second_word}{symbol}"
    return password

# Streamlit interface
st.title("Password Generator")
st.write("Click below to generate a password:")

if st.button("Generate Password"):
    word_list = load_dictionary()

    if word_list:
        password = generate_password(word_list)
        # Display the password in Markdown format
        st.markdown(f"**Generated Password:** `{password}`")
    else:
        st.error("Failed to load dictionary or insufficient words.")
