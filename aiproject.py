import streamlit as st
from transformers import pipeline
from deep_translator import GoogleTranslator

# Supported languages from deep_translator
translator = GoogleTranslator()  # Create an instance
supported_languages = translator.get_supported_languages(as_dict=True)
language_codes = list(supported_languages.keys())
language_names = list(supported_languages.values())

col1, col2 = st.columns(2, gap="medium")
# Select boxes for input and output languages
with col1:
    input_lang = st.selectbox("Input Language", language_codes)


    # Text input fields
    text_input = st.text_area("Enter text to summarize and translate:", height=450)

with col2:
    output_lang = st.selectbox("Output Language", language_codes)

    if "text_output_value" not in st.session_state:
        st.session_state.text_output_value = ""

    text_output = st.text_area("...", value=st.session_state.text_output_value, height=450)

# Summarization options
summary_length_slider = st.slider(
    "Summary Length", min_value=50, max_value=300, value=150, step=50
)

# Summarization and translation button
if st.button("Summarize and Translate"):

    # Get selected language codes
    input_lang_code = input_lang
    output_lang_code = output_lang

    # Summarize text 1
    summarizer = pipeline("summarization")
    summary = summarizer(text_input, max_length=summary_length_slider, min_length=5)
    summary_text = summary[0]["summary_text"]

    # Translate summarized text 1
    translated_summary = GoogleTranslator(
        source=input_lang_code, target=output_lang_code
    ).translate(summary_text)

    # Display results
    st.success("Summary and translation complete!")
    st.markdown(f"*Translated summary of text ({output_lang}):*")

    new_value = translated_summary  # Access current text area value
    st.session_state.text_output_value = new_value
    st.experimental_rerun()  # Trigger a rerun to display the update