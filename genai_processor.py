import google.generativeai as genai
import streamlit as st



class GeminiProcessor:
    def __init__(self):
        self.google_api_key = st.secrets["google_api_key"]
        self.settings = {
            "conversation_context": "",
            "formality": "Balanced",
            "preferred_language": "English",
            "translation_on": False,
            "highlight_mistakes_on": False,
            "practice_language": "",
            "learner_level": "",
        }


    def set_settings(self, settings_dict):
        for key, value in settings_dict.items():
            if key in self.settings:
                self.settings[key] = value



    def create_convo_prompt(self, vocab):
        preferred_language = self.settings["preferred_language"]
        translation_on = self.settings["translation_on"]
        highlight_mistakes_on = self.settings["highlight_mistakes_on"]
        practice_language = self.settings["practice_language"]
        learner_level = self.settings["learner_level"]
        conversation_context = self.settings["conversation_context"]
        formality = self.settings["formality"]

        translation_request = (
            f"Proivde a translation into the learner's preferred language ({preferred_language}). Emphasize clarity and accuracy in your translation. Where relevant, include brief annotations or explanations to highlight cultural or contextual nuances. These insights should elucidate expressions, idioms, or cultural references that may not directly translate but are crucial for understanding the dialogue's deeper meanings and implications."
            if translation_on
            else "Provide the dialogue with no translations. Focus on ensuring the dialogue is engaging and educational within the parameters set, allowing the learner to immerse fully in the practice language without direct translation. This approach encourages deeper language intuition and context-based understanding."
        )
        mistakes_request = (
            f"Identify common errors learners might commit when using the vocabulary word '{vocab}'. Illuminate these mistakes by providing a brief explanation of why they are incorrect. Enhance this learning moment by crafting 2-3 model sentences that demonstrate the correct usage of '{vocab}'. These sentences should not only rectify the identified mistakes but also serve as clear examples for learners to emulate, helping them to internalize the correct application of the word in various contexts."
            if highlight_mistakes_on
            else ""
        )

        prompt = f"""
        "Create a dialogue in {practice_language}, tailored specifically to the CEFR level {learner_level}. Your objective is to seamlessly incorporate the target vocabulary word '{vocab}' into a conversation that is relevant to the given theme or context, '{conversation_context}'. Please adhere to the following guidelines to ensure a high-quality learning experience:

        Scenario Introduction: Begin with a concise description of the scenario in the learner's preferred language, '{preferred_language}'. This description should be engaging and clear, setting the stage for the dialogue. Briefly outline the setting, characters involved, and the situation they are in, making sure it aligns with the theme/context '{conversation_context}'.

        Dialogue Construction:

        Compose 3-5 exchanges between characters in {practice_language}, ensuring the dialogue is realistic and relevant to the learners' experiences.
        Integrate the target vocabulary word '{vocab}' naturally into the conversation. Use the word in different forms or contexts if possible to show its versatility.
        Adjust the dialogue to match the specified {practice_language} CEFR level '{learner_level}', considering sentence complexity, vocabulary, and grammatical structures appropriate for that level.
        Formality Register: Ensure the dialogue reflects the requested level of formality ('{formality}'). This could range from informal, using colloquial language and contractions, to formal, employing polite forms, professional terminology, and complete sentences.

        Dialogue Length and Complexity: Aim for a total word count of approximately 100-150 words for the entire dialogue. This ensures enough {practice_language} content for educational value without overwhelming the learner. Sentences should vary in length and complexity according to the CEFR level specified.

        Ensure that your {practice_language} dialogue is not only a learning tool but also a means for reflection and deeper engagement with the language. The goal is to make each dialogue a stepping stone towards fluency, providing learners with practical language skills they can apply in real-world situations.

        {mistakes_request}

        {translation_request}
        """
        return prompt



    def generate_convo(self, prompt):
        model = gemini.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        return response.text

