# AskEva Chatbot Backend

This is the backend for AskEva — an AI-powered chatbot designed for automating FAQs in the image consulting domain. It is powered by Rasa and integrates Gemini API as a fallback for handling open-ended or out-of-scope queries.

---

## 🧪 Requirements

- Python 3.8+
- Rasa 3.1
- Poetry (if used)
- Google Gemini API key (for fallback)

---

## 📦 Installation

### 1. Set up Virtual Environment (Windows)

```bash
cd backend
python -m venv rasa_env
rasa_env\Scripts\activate
pip install -r requirements.txt

======Train Rasa Model
rasa train

======Run Rasa Action Server
rasa run actions

======Run Rasa Shell (for testing)
rasa shell

======📁 Project Structure
nlu.yml — intents and training examples
domain.yml — responses, entities, actions
rules.yml — Rasa rules for dialogue
actions.py — custom fallback using Gemini API

======✅ Notes
Avoid using Python versions higher than 3.10 for compatibility.

Use rasa run --enable-api if connecting with the frontend.

⚠️ For the purpose of this academic project, the Gemini API key is temporarily hardcoded inside `actions.py`. This is not recommended for production environments.



