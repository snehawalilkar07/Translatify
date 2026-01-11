import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import tempfile
import base64

# ---------- PAGE CONFIG ----------
st.set_page_config("Translatify 🌐", layout="centered")

# ---------- STYLING ----------
st.markdown("""
<style>
/* Hide Streamlit menu and footer */
#MainMenu, footer {
    visibility: hidden;
}

/* Body and headings */
body {
    background: #0f1117;
    color: #fff;
    font-family: 'Segoe UI', sans-serif;
}

h1 {
    text-align: center;
    font-size: 42px;
    margin-bottom: 5px;
}

h2 {
    text-align: center;
    font-size: 22px;
    color: #bbb;
    margin-top: -5px;
}

/* Textarea styling */
textarea {
    border-radius: 12px !important;
    font-size: 16px;
    padding: 12px;
    background: #1c1e29;
    color: #fff;
}

/* Button styling */
.stButton > button {
    border-radius: 12px;
    width: 100%;
    height: 50px;
    font-size: 16px;
    margin-top: 10px;
    background: #4b6cb7;
    color: white;
    transition: 0.3s;
}

.stButton > button:hover {
    background: #3a55a2;
    cursor: pointer;
}

/* Selectbox and text input spacing */
.stSelectbox, .stTextInput {
    margin-bottom: 10px;
}

/* Translation card styling */
.card {
    background-color: #1c1e29;
    border-radius: 16px;
    padding: 20px;
    margin-top: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.6);
    transition: transform 0.2s;
}

.card:hover {
    transform: translateY(-5px);
}

.card h3 {
    margin-bottom: 10px;
    color: #4b6cb7;
}

.translation-text {
    font-size: 26px;
    font-weight: bold;
    margin-bottom: 5px;
    color: #fff;
}

.transliteration {
    font-size: 18px;
    font-style: italic;
    color: #ccc;
    margin-bottom: 10px;
}

.audio-container {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 10px;
    background-color: #2a2c3d;
    padding: 8px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("🌐 Translatify")
st.markdown("<h2>Translate text instantly and listen to translations!</h2>", unsafe_allow_html=True)

# ---------- DATA ----------
languages = {
    "English": "en", "Hindi": "hi", "Marathi": "mr", "Tamil": "ta",
    "Telugu": "te", "Bengali": "bn", "Gujarati": "gu",
    "Kannada": "kn", "Malayalam": "ml", "Punjabi": "pa",
    "Urdu": "ur", "Sanskrit": "sa", "Nepali": "ne",
    "French": "fr", "Spanish": "es", "German": "de",
    "Italian": "it", "Japanese": "ja", "Korean": "ko",
    "Arabic": "ar", "Russian": "ru"
}

scripts = {
    "hi": sanscript.DEVANAGARI, "mr": sanscript.DEVANAGARI, "sa": sanscript.DEVANAGARI,
    "ne": sanscript.DEVANAGARI, "ta": sanscript.TAMIL, "te": sanscript.TELUGU,
    "bn": sanscript.BENGALI, "gu": sanscript.GUJARATI, "kn": sanscript.KANNADA,
    "ml": sanscript.MALAYALAM, "pa": sanscript.GURMUKHI
}

# ---------- USER INPUT ----------
# from_lang = st.selectbox("🌏 From Language", languages.keys(), index=0)
# to_lang = st.selectbox("🌐 To Language", languages.keys(), index=1)
# text_input = st.text_area("📝 Enter text to translate", height=150)

col1, col2 = st.columns(2)
with col1:
    from_lang = st.selectbox("🌏 From Language", languages.keys(), index=0)
with col2:
    to_lang = st.selectbox("🌐 To Language", languages.keys(), index=2)

text_input = st.text_area("📝 Enter text to translate", height=100)


# ---------- TRANSLATION ----------
if st.button("🔁 Translate"):
    if text_input.strip() == "":
        st.warning("Please enter some text to translate!")
    else:
        try:
            # Translate text
            translated = GoogleTranslator(
                source=languages[from_lang],
                target=languages[to_lang]
            ).translate(text_input)

            # Transliteration for Indic languages
            if languages[to_lang] in scripts:
                roman = transliterate(translated, scripts[languages[to_lang]], sanscript.ITRANS).lower()
            else:
                roman = translated

            # Generate TTS
            tts = gTTS(translated, lang=languages[to_lang])
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                tts.save(f.name)
                audio_file = f.name

            # Display translation card
            # st.markdown(f"""
            # <div class="card">
            #     <h3>🗣️ Translation</h3>
            #     <p class="translation-text">{translated}</p>
            #     <p class="transliteration">{roman}</p>
            #     <div class="audio-container">
            #         <audio controls style="width:100%; border-radius:12px;">
            #             <source src="data:audio/mp3;base64,{base64.b64encode(open(audio_file,'rb').read()).decode()}" type="audio/mp3">
            #             Your browser does not support the audio element.
            #         </audio>
            #     </div>
            # </div>
            # """, unsafe_allow_html=True)

            # Display translation card with improved UI

            st.markdown(f"""
            <style>
            #MainMenu, footer {{visibility:hidden;}}
            body {{background:#0f1117; color:#fff; font-family: 'Segoe UI', sans-serif;}}

            .card {{
                background-color: #1c1e29;  /* dark blue-ish card */
                border-radius: 16px;
                padding: 20px;
                margin-top: 15px;
                margin-bottom: 20px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.6);
                transition: transform 0.2s;
            }}
            .card:hover {{transform: translateY(-5px);}}

            .card h3 {{
                margin-bottom: 10px;
                color: #4b6cb7;  /* main blue accent */
                font-family: 'Segoe UI', sans-serif;
            }}

            .translation-text {{
                font-size: 26px;
                font-weight: bold;
                margin-bottom: 5px;
                color: #ffffff;
            }}

            .transliteration {{
                font-size: 18px;
                font-style: italic;
                color: #a0c4ff;  /* lighter blue for contrast */
                margin-bottom: 10px;
            }}

            .audio-container {{
                background-color: #2a2c3d;  /* slightly lighter dark bg */
                padding: 8px;
                border-radius: 12px;
                display: flex;
                align-items: center;
            }}
            audio {{
                width: 100%;
                border-radius: 12px;
            }}
            </style>

            <div class="card">
                <h3>🗣️ Translation</h3>
                <p class="translation-text">{translated}</p>
                <p class="transliteration">{roman}</p>
                <div class="audio-container">
                    <audio controls>
                        <source src="data:audio/mp3;base64,{base64.b64encode(open(audio_file,'rb').read()).decode()}" type="audio/mp3">
                        Your browser does not support the audio element.
                    </audio>
                </div>
            </div>
            """, unsafe_allow_html=True)



        except Exception as e:
            st.error(f"⚠️ Translation failed: {e}")
