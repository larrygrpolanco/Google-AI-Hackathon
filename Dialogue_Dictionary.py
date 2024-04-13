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
            help="Additional options in the extras tab.",
        )

    with tab2:  # Extra settings

        conversation_context = st.text_area(
            "Context",
            placeholder="Ordering food at a restaurant in outer space.",
            help="Give a context to focus the conversation, e.g., ordering at a restaurant, asking for directions.",
        )
        conversation_context = (
            "generic context"
            if not conversation_context
            else conversation_context
        )

        col1, col2 = st.columns(2)
        translation_language = "English"
        translation_language = col1.text_input(
            "Translation Language",
            placeholder="Translation Language",
            label_visibility="collapsed",
        )
        translation_language = (
            "English" if not translation_language else translation_language
        )

        give_translation = col1.toggle(f"{translation_language} Translation")

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

    current_settings = {
        "conversation_context": conversation_context,
        "formality": formality,
        "give_translation": give_translation,
        "translation_language": translation_language,
        "target_language": target_language,
        "learner_level": learner_level,
    }

    if "responses" not in st.session_state:
        st.session_state["responses"] = []

    if "new_clicked" not in st.session_state:
        st.session_state["new_clicked"] = False

    col1, col2, col3, col4 = st.columns(4)

    if col1.button("New Conversation"):
        st.session_state["new_clicked"] = True

    if col4.button("Clear Conversations"):
        st.session_state["responses"] = []
        st.session_state["new_clicked"] = False
        vocab = None

    if st.session_state["new_clicked"] or vocab:
        gemini = GeminiProcessor()
        gemini.set_settings(current_settings)
        with st.spinner("Creating your dialogue..."):
            try:
                response = gemini.generate_convo(vocab)
                st.session_state["responses"].insert(0, response)

                max_responses = 5  # Limit the number of stored responses
                if len(st.session_state["responses"]) > max_responses:
                    st.session_state["responses"] = st.session_state["responses"][
                        :max_responses
                    ]
            except ValueError as e:
                st.error(
                    "Sorry, we're having some trouble finding the perfect conversation, please try again."
                )
                print("Error generating conversation:", str(e))

            st.session_state["new_clicked"] = False

    for response in st.session_state["responses"]:
        st.info(response)
