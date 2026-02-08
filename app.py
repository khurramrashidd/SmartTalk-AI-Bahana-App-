from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
# Ensure your .env file has GEMINI_API_KEY=Your_Actual_Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Using a slightly faster/stable model alias if available, or fallback to standard
model = genai.GenerativeModel('gemini-3-flash-preview')

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    sender = data.get("sender", "Someone")
    receiver = data.get("receiver", "Someone")
    situation = data.get("situation", "")
    tone = data.get("tone", "Casual")
    extra = data.get("extra", "")

    # Handle custom inputs
    if sender == "Other":
        sender = data.get("sender_custom", "Person")
    if receiver == "Other":
        receiver = data.get("receiver_custom", "Person")

    # Fun & Informal System Prompt
    system_prompt = f"""
    You are a witty, smart, and helpful communication assistant for a fun web app called 'SmartTalk AI'.
    
    The user is a **{sender}** trying to say something to a **{receiver}**.
    
    **The Scenario:**
    - Situation: {situation}
    - Desired Tone: {tone} (Keep it consistent with this tone)
    - Extra Context: {extra}

    **Instructions:**
    - Write a message that is clear, clean, and fits the requested tone perfectly.
    - Since this is a fun app, if the tone allows (e.g., Casual, Sarcastic, Witty), feel free to be creative.
    - If the tone is 'Professional', keep it safe but not overly robotic.
    - **Do not include headers, subject lines, or explanations.** Just output the message body text itself.
    """

    try:
        response = model.generate_content(system_prompt)
        reply = response.text
    except Exception as e:
        reply = "Oops! My brain froze. Please try again. (Error: " + str(e) + ")"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=5000)