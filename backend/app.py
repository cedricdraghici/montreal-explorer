from flask import Flask, request
from openai import OpenAI

key = "sk-31b44503ea5243b3be8af9d7cd014122"

app = Flask(__name__)
client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

conversation = [{"role": "system", "content": "You are a helpful travel guide, giving an itinerary of events, attractions and restaurants based on user input"}]

@app.route("/gpt", methods=["POST"])
def convo():
    data = request.get_json()
    user_message = data.get("user_message")

    if not user_message:
        return "Missing user_message parameter", 400

    conversation.append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=conversation
    )
    conversation.append({"role": "assistant", "content": response.choices[0].message.content})
    return response.choices[0].message.content
