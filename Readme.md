🚀 Social Media Agent — AI Content & Caption Generator (Streamlit App)

A fast, lightweight AI-powered tool that generates content ideas, captions, and hashtags for multiple social media platforms.
Built with Streamlit + OpenAI (with full offline fallback mode so it works even without API access).

Perfect for hackathons, prototypes, portfolio projects, and demo submissions.

✨ Features
🧠 AI-powered Caption & Content Generation

Generate:
✔ Content ideas
✔ Captions (Instagram, LinkedIn, X/Twitter, Facebook, TikTok)
✔ Hashtags (5 per post)

⚙️ Smart Options

Choose Platform, Tone, Post Count, Model

Supports OpenAI models (gpt-3.5-turbo, gpt-4o-mini, etc.)

Offline mode (no API key required)

💾 Export Options

Download generated results as:

CSV

JSON

Copy-to-clipboard button for fast posting

🎨 Improved UI

Clean layout with cards

Sidebar settings

Preset topic buttons

Responsive and user-friendly

📸 Demo Screenshots (Optional)

Add screenshots of your running Streamlit app here.

Example:

[Upload screenshot.png]

🏗️ Project Structure
│── app.py               # Main Streamlit application
│── requirements.txt     # Python dependencies
│── README.md            # Project documentation
│── .gitignore           # Ignored files
│── LICENSE (optional)   # Project license

🚀 Getting Started (Local Setup)
1️⃣ Clone the repository
git clone https://github.com/<your-username>/social-media-agent-demo.git
cd social-media-agent-demo

2️⃣ Create Virtual Environment (optional)
python -m venv .venv


Activate:

Windows

.venv\Scripts\activate


Mac/Linux

source .venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add OpenAI API Key (Optional)

Live mode needs an API key.

Mac/Linux:

export OPENAI_API_KEY="sk-..."


Windows (PowerShell):

setx OPENAI_API_KEY "sk-..."


If you don’t have an API key → just select the offline model in the sidebar.

5️⃣ Run the Streamlit App
streamlit run app.py

🌐 Deployment (Streamlit Cloud)

Push your repo to GitHub

Go to: https://share.streamlit.io

Click New App → select repo & branch

Add secret under App Settings → Secrets

OPENAI_API_KEY = "sk-..."


Deploy!

💡 Tech Stack

Streamlit – UI framework

OpenAI API – AI generation

Python – backend logic

Pandas – CSV export

📦 Requirements

Your requirements.txt should include:

streamlit>=1.22
openai>=0.27.0
pandas>=1.5