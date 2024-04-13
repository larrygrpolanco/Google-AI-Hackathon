import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["google_api_key"])
model = genai.GenerativeModel("gemini-pro")


class GeminiProcessor:
    def __init__(self):
        self.settings = {
            "conversation_context": "",
            "formality": "Balanced",
            "give_translation": False,
            "translation_language": "",
            "target_language": "",
            "learner_level": "",
        }

    def set_settings(self, settings_dict):
        for key, value in settings_dict.items():
            if key in self.settings:
                self.settings[key] = value

    def create_prompt(self, vocab):
        target_language = self.settings["target_language"]
        learner_level = self.settings["learner_level"]
        give_translation = self.settings["give_translation"]
        translation_language = self.settings["translation_language"]
        conversation_context = self.settings["conversation_context"]
        formality = self.settings["formality"]

        translation_request = (
            f"Provide a {translation_language} translation of the dialogue for the student."
            if give_translation
            else "Provide the dialogue with no translations."
        )

        prompt = f"""
        You are a language teacher creating a dialogue exercise for your students. Use the following scenario to create a dialogue in {target_language} that incorporates the vocabulary word '{vocab}'.
        
        {translation_request}

        Begin with a concise description of the scenario in {translation_language}.

        Write a dialogue in {target_language} about '{conversation_context}'. The conversation should be engaging and natural, with each character contributing significantly. Incorporate the vocabulary word '{vocab}' contextually to enhance understanding.

        Craft a {target_language} dialogue about '{conversation_context}' at CEFR level '{learner_level}'. Adjust sentence complexity, vocabulary, and grammar to suit this level. Use a '{formality}' tone. Keep the dialogue within 100-150 words, incorporating the word '{vocab}' effectively.

        Bold the target vocabulary word '{vocab}' each time it appears in the dialogue.

        Always include a line break between each character's dialogue to clearly distinguish their responses.
        """
        return prompt

    def generate_convo(self, vocab):
        prompt = self.create_prompt(vocab)
        response = model.generate_content(prompt)

        return response.text
