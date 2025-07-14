# Project Nexus – Walmart Sparkathon

**Project Nexus** is a futuristic, AI-powered Streamlit app designed for the Walmart Sparkathon. It features advanced user authentication, dynamic UI, predictive shopping, sustainability insights, social commerce, AR/voice integration, and fun AI features like image generation and chatbots.

---

## 🚀 Features
- **User Authentication:** Login, registration, and password security.
- **Dynamic UI:** Responsive, branded interface with Walmart colors and glowing effects.
- **Predictive Shopping:** AI-driven recommendations based on user context, mood, and history.
- **Sustainability Hub:** Eco-score, carbon footprint, and green product suggestions.
- **Social Commerce:** Community trends, friends/family integration, and social shopping.
- **AR/Voice Interface:** Placeholder for AR and voice command features.
- **Fun AI:**
  - AI Product Image Generator (HuggingFace OpenJourney)
  - Shopping Joke Generator (JokeAPI)
  - Sentiment Analysis (TextBlob)
  - AI Chatbot (HuggingFace GPT-2)

---

## 🛠️ Setup Instructions

### 1. **Clone the Repository**
```sh
git clone https://github.com/vijayshreepathak/Project-Nexus.git
cd Project-Nexus
```

### 2. **Install Dependencies**
```sh
pip install -r requirements.txt
```

### 3. **Set Up Environment Variables**
Create a `.env` file in the project root (do **not** commit this file!):
```
HUGGINGFACE_TOKEN=your_huggingface_token_here
```
- Get your token from [HuggingFace Tokens](https://huggingface.co/settings/tokens)

### 4. **Run the App Locally**
```sh
streamlit run app.py
```

---

## ☁️ Deploying on Streamlit Cloud
1. Push your code to GitHub (excluding `.env`).
2. Go to [Streamlit Cloud](https://share.streamlit.io/), connect your repo, and set:
   - **Main file path:** `app.py`
   - **Branch:** `main`
3. In **Advanced settings → Secrets**, add:
   ```toml
   HUGGINGFACE_TOKEN = "your_huggingface_token_here"
   ```
4. Click **Deploy**.

---

## 🔑 Environment Variables
- `HUGGINGFACE_TOKEN`: Your HuggingFace API token for AI features.

---

## 📦 Requirements
- Python 3.9+
- See `requirements.txt` for all dependencies.

---

## 📝 Usage Notes
- **Do NOT commit your `.env` file or any secrets to GitHub.**
- If you change your HuggingFace token, update your `.env` (locally) or Streamlit Cloud secrets.
- Some AI features depend on free-tier HuggingFace models and may be rate-limited.
- For AR/Voice and some social features, placeholders are provided for future expansion.

---

## 🤝 Contributing
Pull requests and suggestions are welcome! Please open an issue to discuss changes.

---

## 📄 License
MIT License. See [LICENSE](LICENSE) for details.

---

## 👩‍💻 Author
- [vijayshreepathak](https://github.com/vijayshreepathak)

---

## 🌟 Acknowledgements
- Walmart Sparkathon
- HuggingFace, Streamlit, and open-source contributors 
