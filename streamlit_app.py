import streamlit as st
import random
from nltk.corpus import words
import nltk
import os
import json

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

# Load and save leaderboard
def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_leaderboard(leaderboard):
    with open("leaderboard.json", "w") as file:
        json.dump(leaderboard, file)

def update_leaderboard(password, leaderboard):
    if password not in leaderboard:
        leaderboard.append(password)
        if len(leaderboard) > 50:
            leaderboard.pop(0)
    return leaderboard

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
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.4);
        font-family: 'Arial', sans-serif;
        animation: glow 25s ease-in-out infinite;
    }
    @keyframes glow { 
        0% { text-shadow: 0 0 5px #ff6347, 0 0 10px #ff6347, 0 0 15px #ff6347, 0 0 20px #ff6347; } 
        10% { text-shadow: 0 0 5px #ff7f50, 0 0 10px #ff7f50, 0 0 15px #ff7f50, 0 0 20px #ff7f50; } 
        20% { text-shadow: 0 0 5px #ff4500, 0 0 10px #ff4500, 0 0 15px #ff4500, 0 0 20px #ff4500; } 
        30% { text-shadow: 0 0 5px #32cd32, 0 0 10px #32cd32, 0 0 15px #32cd32, 0 0 20px #32cd32; } 
        40% { text-shadow: 0 0 5px #00bfff, 0 0 10px #00bfff, 0 0 15px #00bfff, 0 0 20px #00bfff; } 
        50% { text-shadow: 0 0 5px #8a2be2, 0 0 10px #8a2be2, 0 0 15px #8a2be2, 0 0 20px #8a2be2; } 
        60% { text-shadow: 0 0 5px #ff1493, 0 0 10px #ff1493, 0 0 15px #ff1493, 0 0 20px #ff1493; } 
        70% { text-shadow: 0 0 5px #ff69b4, 0 0 10px #ff69b4, 0 0 15px #ff69b4, 0 0 20px #ff69b4; } 
        80% { text-shadow: 0 0 5px #adff2f, 0 0 10px #adff2f, 0 0 15px #adff2f, 0 0 20px #adff2f; } 
        90% { text-shadow: 0 0 5px #ff6347, 0 0 10px #ff6347, 0 0 15px #ff6347, 0 0 20px #ff6347; } 
        100% { text-shadow: 0 0 5px #FFD700, 0 0 10px #FFD700, 0 0 15px #FFD700, 0 0 20px #FFD700; } 
    } 
    </style> 
    """, unsafe_allow_html=True) 

# Centered title
st.markdown('<h1 class="title">Password Generator</h1>', unsafe_allow_html=True)

# Display usage count
usage_count = load_usage_count()
st.markdown(f'<div style="position: fixed; bottom: 10px; right: 10px; font-size: 12px; color: grey;">App Usage Count: {usage_count}</div>', unsafe_allow_html=True)

# Generate password button
col1, col2, col3 = st.columns([1.5, 2, 1])
with col2:
    generate_password_clicked = st.button("🔓 Generate Password 🔒")

# Input fields for custom words
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    first_word_input = st.text_input("First word (optional):", max_chars=12)
    second_word_input = st.text_input("Second word (optional):", max_chars=12)

# Generate and display password
if generate_password_clicked:
    word_list = load_combined_dictionary()

    if word_list:
        password = generate_password(word_list, first_word_input, second_word_input)
        st.session_state.generated_password = password  # Save password in session state

        # Display the generated password
        st.markdown(f"<h2 style='text-align: center; font-size: 35px;'>{password}</h2>", unsafe_allow_html=True)
        save_usage_count(usage_count + 1)
    else:
        st.error("Failed to load dictionary or insufficient words.")

# Ensure the password persists across reruns
password = st.session_state.get("generated_password", None)

# Checkbox to add password to leaderboard
if password:
    if st.checkbox("Add this password to the leaderboard"):
        leaderboard = load_leaderboard()
        leaderboard = update_leaderboard(password, leaderboard)
        save_leaderboard(leaderboard)
        st.success("Password added to the pin board!")

# Display the leaderboard with adjusted text size
st.markdown("""<h3 style='text-align: center; font-size: 20px;'>Password Showcase</h3>""", unsafe_allow_html=True)
leaderboard = load_leaderboard()
if leaderboard:
    for i, pw in enumerate(reversed(leaderboard), start=1):
        st.markdown(f"{i}. {pw}")
else:
    st.markdown("<p style='text-align: center;'>No passwords in the pin board yet.</p>", unsafe_allow_html=True)