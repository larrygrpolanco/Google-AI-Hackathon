import streamlit as st
from genai_processor import GeminiProcessor


st.title("💬 Conversation Dictionary")

st.markdown(
    "Have a word you want to see used in a conversation? Learning new words and phrases in context can help you understand and remember them better."
)


col1, col2 = st.columns(2)
with col1:
    target_language = st.text_input(
        "What language are you learning?",
        placeholder="Chinese, Spanish, etc.",
    )

with col2:
    learner_level = st.selectbox(
        "What is your level?",
        [
            "A1 Beginner",
            "A2 Pre-intermediate",
            "B1 Intermediate",
            "B2 Upper-Intermediate",
            "C1 Advanced",
            "C2 Mastery",
        ],
    )

if target_language:  # if practice_language is not empty

    (
        tab1,
        tab2,
    ) = st.tabs(
        [
            "Dictionary",
            "Extras",
        ]
    )

    with tab1:  # Dictionary
        vocab = st.text_input(
            "Enter the word or words you want to see used in a conversation:",
            placeholder="Vocabulary",
            help="Additional options in the sidebar located at the top left",
        )

    with tab2:  # Extra settings
        conversation_context = st.text_area(
            "Context",
            placeholder="Ordering food at a restaurant in outer space.",
            help="Give a context to focus the conversation, e.g., ordering at a restaurant, asking for directions.",
        )

        col1, col2 = st.columns(2)
        give_translation = col1.toggle("English Translations")
        formality = col2.select_slider(
            "Formality",
            [
                "Informal",
                "Semi-informal",
                "Balanced",
                "Semi-formal",
                "Formal",
            ],
            value="Balanced",
        )

    # Updated to reflect the current settings
    current_settings = {
        "conversation_context": conversation_context,
        "formality": formality,
        "give_translation": give_translation,
        "target_language": target_language,
        "learner_level": learner_level,
    }

    if "responses" not in st.session_state:
        st.session_state["responses"] = []

    if "find_clicked" not in st.session_state:
        st.session_state["find_clicked"] = False

    col1, col2, col3, col4 = st.columns(4)

    if col1.button("Find Conversation"):
        st.session_state["find_clicked"] = True

    if col4.button("Clear Conversations"):
        st.session_state["responses"] = []  # Reset the list of responses
        st.session_state["find_clicked"] = False

    if st.session_state["find_clicked"]:
        gemini = GeminiProcessor()
        gemini.set_settings(current_settings)

        with st.spinner("Creating your dialogue..."):
            response = gemini.generate_convo(vocab)

            st.session_state["responses"].insert(0, response)

            max_responses = 5
            if len(st.session_state["responses"]) > max_responses:
                # Remove the oldest response(s) to maintain only a max number of responses
                st.session_state["responses"] = st.session_state["responses"][
                    :max_responses
                ]

        st.session_state["find_clicked"] = False

    for response in st.session_state["responses"]:
        st.info(response)
