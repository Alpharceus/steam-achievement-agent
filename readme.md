# Steam Achievement Agent

![Logo](pictures/logo.png)

## 🚀 What is This?

**Steam Achievement Agent** is a smart, interactive achievement-tracking web app for Steam gamers.
It connects to your Steam account, fetches all your games and achievements, and lets you:

* **See your achievement progress** for every game you own
* **Quickly browse unlocked or locked achievements**
* **Assign custom priority weights** to each achievement (e.g., “I want this NOW!”)
* **Use a local AI agent** (Llama 3 via Ollama) to automatically rank the best or most important achievements for you—no more endless scrolling or screenshotting
* **Enjoy a beautiful, dark, modern interface with cosmic vibes**

### Why Did I Make This?

I was tired of scrolling through Steam, taking screenshots, and asking LLMs to figure out which achievements to focus on next.
Now, I can track, prioritize, and get AI-powered recommendations—**all in one place**.

---

## 🛠️ Features

* **Instantly see all your games and achievement progress**
* **Filter by unlocked/locked achievements**
* **Personalized weights** for what matters most to *you*
* **AI-powered ranking**: uses a local LLM (Llama 3 via Ollama) for privacy and speed
* **Live achievement progress bar and stats**
* **Modern, cosmic-themed design**
* **Fully open source and customizable**

---

## 💻 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Alpharceus/steam-achievement-agent
cd steam-achievement-agent
```

### 2. (Recommended) Create a virtual environment

This helps keep dependencies clean.

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install [Ollama](https://ollama.com/download) for LLM-powered features

* Download and install Ollama for your system.
* In a terminal, run:

  ```bash
  ollama pull llama3
  ```

  (or use another local model if you wish)

### 5. Install [Streamlit](https://streamlit.io/) if you haven’t already

Already included in `requirements.txt`, but can be installed directly:

```bash
pip install streamlit
```

### 6. Get your Steam API Key and SteamID64

* Go to [https://steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey)
* Log in with your Steam account
* Enter any domain (e.g., `localhost`), and click Register
* Copy your API key

To get your **SteamID64**, go to [https://steamid.io/](https://steamid.io/), paste your profile URL, and copy the 17-digit number shown.

### 7. Set up your config

* Copy `configsample.py` to `config.py`
* Fill in your Steam API key and SteamID64

---

## ⚡ Running the App

**Make sure Ollama is running in the background!**

Start the app from the project root:

```bash
streamlit run ui/streamlit_app.py
```

* Open the link shown in your terminal (usually [http://localhost:8501](http://localhost:8501))
* Choose your game, explore your achievements, set weights, and let the AI recommend what to go for next!

---

## 🙏 Acknowledgements

* **Valve/Steam** for their API and the best gaming platform
* **Ollama** for easy local LLMs
* **Streamlit** for making data web apps fun and fast
* **OpenAI’s ChatGPT-4.1** — for collaborating on this project in a single night, turning an idea into a finished tool


---

## ✨ License

MIT — use, fork, and share as you like!

---

> Made with 💡, ☕, and a lot of cosmic curiosity.
