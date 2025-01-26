from flask import Flask, request, Response
from flask_cors import CORS
from openai import OpenAI
import uuid
import json
from datetime import datetime, timedelta

key = "sk-31b44503ea5243b3be8af9d7cd014122"

app = Flask(__name__)
CORS(app)
app.debug = True
client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

sessions = {}

def initialize_session(session_id):
    sessions[session_id] = {
        "conversation": [{
            "role": "system",
            "content": "You are a helpful travel guide..."
        }],
        "last_activity": datetime.now()
    }

@app.route("/gpt", methods=["POST"])
def convo():
    data = request.get_json()
    
    # Get or create session ID
    session_id = data.get("session_id")
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        initialize_session(session_id)
    
    conversation = sessions[session_id]["conversation"]
    
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

@app.route("/conversation/done", methods=["POST"])
def end_conversation():
    data = request.get_json()
    session_id = data.get("session_id")
    
    if not session_id:
        return {"error": "Missing session_id"}, 400
    
    if session_id in sessions:
        # Get conversation before deletion
        conversation = sessions[session_id]["conversation"]
        del sessions[session_id]
        return {
            "status": "success",
            "message": "Conversation ended",
            "session_id": session_id,
            "conversation_length": len(conversation)
        }, 200
    else:
        return {"error": "Invalid session_id"}, 404
        
#add automatic cleanup for inactive sessions
def cleanup_sessions():
    now = datetime.now()
    expired = [
        sid for sid, data in sessions.items() 
        if (now - data["last_activity"]) > timedelta(hours=1)
    ]
    for sid in expired:
        del sessions[sid]