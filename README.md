Password Generator App::

This is a simple password generator built using Streamlit. The app generates secure passwords by combining random words, numbers, and symbols.

Features::

    Generates passwords in the format:
    Word1 + Random Number + Word2 + Symbol + Random Number2
    Example: Apple5Chair@7
    Words are selected from a preloaded dictionary of school-appropriate words with lengths between 4 and 6 characters.
    User-friendly interface powered by Streamlit.

How to Use::

    Open the live app URL password-generator-ja.streamlit.app/
    Click the "Generate Password" button.
    Copy the displayed password for your use.

Requirements::

To run the app locally, ensure the following are installed:

    Python 3.8+
    Required Python packages:

    streamlit

Installation::

Follow these steps to run the app locally:

    Clone the repository:

git clone https://github.com/justjoshinaround/password-generator.git
cd your-repo

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install the dependencies:

pip install -r requirements.txt

Preload the word corpus to avoid runtime errors:

python -c "import nltk; nltk.download('words', download_dir='./nltk_data')"

Run the Streamlit app:

    streamlit run streamlit_app.py

    Open the app in your browser at http://localhost:8501.

Deployment::

This app can be deployed on Streamlit Cloud. Ensure:

    The nltk_data folder is included in the repository for deployment.
    The streamlit_app.py file is the entry point.


Contributions are welcome! Feel free to submit issues or pull requests.