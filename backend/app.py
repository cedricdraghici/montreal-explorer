from flask_cors import CORS
from flask import Flask, request
from openai import OpenAI
import uuid

key = "sk-31b44503ea5243b3be8af9d7cd014122"

app = Flask(__name__)
CORS(app)
client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

# Dictionary to store conversations {session_id: conversation}
sessions = {}

def initialize_session(session_id):
    sessions[session_id] = [{
        "role": "system",
        "content": "You are a helpful travel guide, giving an itinerary of events, attractions and restaurants based on user input"
    }]

@app.route("/gpt", methods=["POST"])
def convo():
    data = request.get_json()
    
    # Get or create session ID
    session_id = data.get("session_id")
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        initialize_session(session_id)
    
    # Get conversation history for this session
    conversation = sessions[session_id]
    
    # Process message
    user_message = data.get("user_message")
    if not user_message:
        return {"error": "Missing user_message"}, 400
    
    conversation.append({"role": "user", "content": user_message})
    
    # Get AI response
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=conversation
    )
    
    # Update conversation history
    assistant_response = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": assistant_response})
    
    return {
        "session_id": session_id,
        "response": assistant_response
    }
