from flask import Flask, request, Response
from flask_cors import CORS
from openai import OpenAI
import uuid
import json
key = "sk-31b44503ea5243b3be8af9d7cd014122"

app = Flask(__name__)
CORS(app)
app.debug = True
client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

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
    
    conversation = sessions[session_id]
    
    user_message = data.get("user_message")
    if not user_message:
        return {"error": "Missing user_message"}, 400
    
    conversation.append({"role": "user", "content": user_message})
    
    # Create a generator for streaming responses
    def generate():
        full_response = []
        stream = client.chat.completions.create(
            model="deepseek-chat",
            messages=conversation,
            stream=True
        )
        
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                full_response.append(delta.content)
                yield f"data: {json.dumps({
                    'session_id': session_id,
                    'delta': delta.content,
                    'chunk_id': chunk.id,
                    'finished': False
                })}\n\n"
        
        conversation.append({"role": "assistant", "content": ''.join(full_response)})
        yield f"data: {json.dumps({
            'session_id': session_id,
            'finished': True
        })}\n\n"

    return Response(generate(), mimetype="text/event-stream")
