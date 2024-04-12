import streamlit as st


st.title("💬 Conversation Dictionary")

st.markdown(
    "Have a word you want to see used in a conversation? Learning new words and phrases in context can help you understand and remember them better."
)


tab1, tab2, = st.tabs(["Settings", "Extras",])


with tab2: # Extra settings
    formality = st.select_slider(
        "Formality",
        [
            "Informal",
            "Balanced",
            "Formal",
        ],
        value="Balanced",
    )
    st.divider()
    preferred_language = st.text_input(
        "Preferred Language",
        value="English",
        help="Set language for the explanations and translations.",
    )
    translation_on = st.toggle(
        f"{preferred_language} explanations",
        help=f"Check this to request {preferred_language} translations and cultural explinations.",
    )
    highlight_mistakes_on = st.toggle(
        "Show common mistakes",
        help="Check this to show common mistakes learners might make.",
    )


with tab1:
    col1, col2, col3 = st.columns(3)

    with col1:
        practice_language = st.text_input(
            "Target Language",
            placeholder="e.g., Chinese, Spanish.",
            help="Enter the language you're learning.",
        )

    with col2:
        learner_level = st.selectbox(
            "CEFR Level (Proficiency)",
            [
                "A1 Beginner",
                "A2 Pre-intermediate",
                "B1 Intermediate",
                "B2 Upper-Intermediate",
                "C1 Advanced",
                "C2 Mastery",
            ],
        )

    with col3:
        st.markdown("#")
        # Button to clear responses
        if st.button("Clear All Responses"):
            st.session_state["responses"] = []  # Reset the list of responses


    col1, col2 = st.columns(2)
    with col1:
        # UI for input outside of the settings, so users can submit words anytime.
        with st.form("myform"):
            vocab_text = st.text_input(
                "Enter the word or words you want to see used in a conversation:",
                placeholder="Vocabulary",
                help="Additional options in the sidebar located at the top left",
            )
            submitted = st.form_submit_button("Submit")

    with col2:
        conversation_context = st.text_area(
                    "Context",
                    placeholder="Ordering food at a restaurant in outer space.",
                    help="Specify a context to focus the conversation, e.g., ordering at a restaurant, asking for directions.",
                )

if "responses" not in st.session_state:
    st.session_state["responses"] = []

# Ensure consistent use of keys and proper initialization
if "llm_processor" not in st.session_state:
    st.session_state["llm_processor"] = LanguageModelProcessor(
        st.secrets["GOOGLE_API_KEY"], st.secrets["OPENAI_API_KEY"]
    )

# Updated to reflect the current settings
current_settings = {
    "conversation_context": conversation_context,
    "formality": formality,
    "preferred_language": preferred_language,
    "translation_on": translation_on,
    "highlight_mistakes_on": highlight_mistakes_on,
    "practice_language": practice_language,
    "learner_level": learner_level,
    "llm_choice": llm_choice,
    "custom_api_key": None,  # or the appropriate value
}

# Apply the settings to your processor
st.session_state["llm_processor"].set_settings(current_settings)

# Generating conversation using the corrected instance
if submitted:
    if not vocab_text.strip():
        st.warning("Enter a vocabulary word.")

    if not practice_language.strip():
        st.warning("Set your target langauge in the sidebar located at the top left.")

    with st.spinner("Creating your dialogue..."):
        if "user_template" in st.session_state:  # Check for user prompt
            user_template = st.session_state["user_template"]
            prompt = process_user_template(user_template, current_settings)
        else:
            prompt = st.session_state["llm_processor"].create_convo_prompt(vocab_text)

        # Run LLM model
        if llm_choice == "Google Gemini-Pro":
            gemini_processor = GeminiProcessor(
                st.secrets["GOOGLE_API_KEY"], st.secrets["OPENAI_API_KEY"]
            )
            response = gemini_processor.generate_convo(prompt)
        elif llm_choice == "OpenAI ChatGPT 4":
            chatgpt_processor = ChatGPTProcessor(
                st.secrets["GOOGLE_API_KEY"], st.secrets["OPENAI_API_KEY"]
            )
            response = chatgpt_processor.generate_convo(prompt)

        # Append new response to the start of the list so it appears at the top
        st.session_state["responses"].insert(0, response)

        # Limit the number of responses to a specific max value
        max_responses = 5
        if len(st.session_state["responses"]) > max_responses:
            # Remove the oldest response(s) to maintain only a max number of responses
            st.session_state["responses"] = st.session_state["responses"][
                :max_responses
            ]


for response in st.session_state["responses"]:
    st.info(response)
