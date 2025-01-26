from flask import Flask, request, Response, Blueprint, jsonify
from flask_cors import CORS
from openai import OpenAI
from map import app_map, itineraries
import uuid
import json

import re

DEEPSEEK_KEY = "sk-31b44503ea5243b3be8af9d7cd014122"

app = Flask(__name__)
CORS(app)
app.register_blueprint(app_map)
app.debug = True
client = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")

sessions = {}

def initialize_session(session_id):
    sessions[session_id] = {
        "conversation": [{
            "role": "system",
            "content": """You are a helpful travel guide. Provide friendly responses, recommended times and durations. Begin with an interactive conversation to pick the right hotel. If the user says "GENERATE", and only then, include 
            a hidden JSON array of itinerary updates using this format (DO NOT ANNOUNCE TO USER PRIOR):
            ```json
            [{
                "day": 1,
                "title": "Location Name",
                "desc": "Description",
                "stay_minutes": 60,
                "arrival_time": "10:00",
                "lat": 45.5017,
                "lon": -73.5673
            }]
            ```"""
        }],
    }

@app.route("/gpt", methods=["POST"])
def convo():
    data = request.get_json()
    session_id = data.get("session_id")
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        initialize_session(session_id)
    
    conversation = sessions[session_id]["conversation"]
    user_message = data.get("user_message")
    if not user_message:
        return {"error": "Missing user_message"}, 400
    
    conversation.append({"role": "user", "content": user_message})
    
    def generate():
        full_visible = []
        json_buffer = []
        json_start_marker = '```json'
        marker_index = 0
        json_started = False
        current_marker_pos = 0
        
        stream = client.chat.completions.create(
            model="deepseek-chat",
            messages=conversation,
            stream=True
        )

        for chunk in stream:
            if not chunk.choices[0].delta.content:
                continue

            delta_content = chunk.choices[0].delta.content
            if json_started:
                json_buffer.append(delta_content)
                continue

            for char in delta_content:
                if char == json_start_marker[current_marker_pos]:
                    current_marker_pos += 1
                    if current_marker_pos == len(json_start_marker):
                        json_started = True
                        visible_content = ''.join(full_visible)
                        if visible_content:
                            yield f"data: {json.dumps({
                                'session_id': session_id,
                                'delta': visible_content,
                                'finished': False
                            })}\n\n"
                        full_visible.clear()
                        current_marker_pos = 0
                        break
                else:
                    if current_marker_pos > 0:
                        full_visible.extend(list(json_start_marker[:current_marker_pos]))
                        current_marker_pos = 0
                    full_visible.append(char)

            if not json_started and full_visible:
                visible_content = ''.join(full_visible)
                yield f"data: {json.dumps({
                    'session_id': session_id,
                    'delta': visible_content,
                    'finished': False
                })}\n\n"
                full_visible.clear()

        if json_started:
            json_str = ''.join(json_buffer)
            json_str = json_str.split('```', 1)[0].strip()
            try:
                updates = json.loads(json_str)
                session_data = sessions[session_id]
                for item in updates:
                    if not all(key in item for key in ['day', 'title', 'lat', 'lon']):
                        continue
                    day = item['day']
                    if day not in itineraries:
                        itineraries[day] = {"waypoints": []}
                    itineraries[day]["waypoints"].append({
                        "lon": item["lon"],
                        "lat": item["lat"],
                        "title": item["title"],
                        "desc": item.get("desc", ""),
                        "stay_minutes": item.get("stay_minutes", 60),
                        "arrival_time": item.get("arrival_time")
                    })
            except json.JSONDecodeError:
                updates = []

            yield f"data: {json.dumps({
                'session_id': session_id,
                'finished': True,
                'itinerary_updates': updates
            })}\n\n"
        else:
            visible_content = ''.join(full_visible)
            conversation.append({"role": "assistant", "content": visible_content})
            yield f"data: {json.dumps({
                'session_id': session_id,
                'finished': True
            })}\n\n"

    return Response(generate(), mimetype="text/event-stream")
