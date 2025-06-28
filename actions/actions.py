import os
import json
from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUtteranceReverted

import google.generativeai as genai

# --- Load business info from JSON file ---
def load_business_info() -> dict:
    file_path = os.path.join(os.path.dirname(__file__), "business_info.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("[ERROR] Could not load business info:", e)
        return {}

# --- Gemini LLM Fallback Action ---
class ActionLlmFallback(Action):
    def name(self) -> Text:
        return "action_llm_fallback"

    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # ✅ Grab current message and last message
        user_message = tracker.latest_message.get("text", "").strip()
        if not user_message:
            dispatcher.utter_message(text="Sorry, I didn’t catch that. Could you rephrase?")
            return [UserUtteranceReverted()]

        user_message_lower = user_message.lower()
        last_user_input = tracker.get_slot("last_user_input") or ""

        print("[DEBUG] User input:", user_message)
        print("[DEBUG] Last input from slot:", last_user_input)

        # ✅ Detect repeated input
        if user_message_lower == last_user_input.lower():
            dispatcher.utter_message(text="You've already asked that. Try something else?")
            return [UserUtteranceReverted()]

        # ✅ Load business context
        business = load_business_info()
        if not business:
            dispatcher.utter_message(text="Sorry, I couldn't access business info.")
            return [
                SlotSet("last_user_input", user_message),
                UserUtteranceReverted()
            ]

        # ✅ Prompt Gemini
        prompt = (
            f"You are Evas, a chatbot assistant for {business.get('business_name')}.\n\n"
            f"{json.dumps(business, indent=2)}\n\n"
            f"Answer this user message in a helpful, warm, short response (max 5 sentences):\n"
            f"{user_message}\n\n"
            f"Do not repeat phrases like 'feel free to ask more'.\nAssistant:"
        )

        try:
            response = self.model.generate_content(prompt)
            reply = response.text.strip()
            if not reply:
                reply = "Sorry, I couldn't generate a response right now."
        except Exception as e:
            print("[ERROR] Gemini API failed:", e)
            reply = "Sorry, something went wrong with my response."

        dispatcher.utter_message(text=reply)
        return [
            SlotSet("last_user_input", user_message),
            UserUtteranceReverted()
        ]
