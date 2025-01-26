from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_
from flask_cors import CORS
from openai import OpenAI
import uuid
import json
from datetime import datetime, timedelta


key = "sk-31b44503ea5243b3be8af9d7cd014122"

app = Flask(__name__)
CORS(app)
app.debug = True

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:fuka1010@localhost/montreal_events'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Event Model
class Event(db.Model):
    __tablename__ = 'events'  
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255))
    url_fiche = db.Column(db.Text)
    description = db.Column(db.Text)
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    type_evenement = db.Column(db.String(100))
    public_cible = db.Column(db.String(100))
    emplacement = db.Column(db.String(100))
    inscription = db.Column(db.String(50))
    cout = db.Column(db.String(50))
    arrondissement = db.Column(db.String(100))
    titre_adresse = db.Column(db.String(255))
    adresse_principale = db.Column(db.Text)
    adresse_secondaire = db.Column(db.Text)
    code_postal = db.Column(db.String(10))
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))
    coord_x = db.Column(db.Numeric(10, 1))
    coord_y = db.Column(db.Numeric(10, 1))
    created_at = db.Column(db.TIMESTAMP)

client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

sessions = {}

def initialize_session(session_id, date_context=""):
    sessions[session_id] = {
        "conversation": [{
            "role": "system",
            "content": f"""You are a Montreal travel expert. Use this event data:
                {date_context}
                Provide detailed itineraries including:
                - Event locations with full addresses
                - Dates and times
                - Costs and registration requirements
                - Target audiences
                - Links to official pages
                Mention transportation options and nearby amenities when possible."""
        }],
        "last_activity": datetime.now()
    }

#add automatic cleanup for inactive sessions
def cleanup_sessions():
    now = datetime.now()
    expired = [
        sid for sid, data in sessions.items() 
        if (now - data["last_activity"]) > timedelta(hours=1)
    ]
    for sid in expired:
        del sessions[sid]

def get_events_by_date(start_date, end_date):
    try:
        return Event.query.filter(
            (Event.date_debut <= end_date) & 
            (Event.date_fin >= start_date)
        ).order_by(Event.date_debut).all()
    except Exception as e:
        print(f"Database error: {str(e)}")
        return []


def format_events_for_gpt(events):
    if not events:
        return "No scheduled events found for these dates"
    
    event_descriptions = []
    for event in events:
        desc = f"""Event: {event.titre}
        - Type: {event.type_evenement}
        - Dates: {event.date_debut} to {event.date_fin}
        - Location: {event.emplacement} ({event.adresse_principale})
        - Audience: {event.public_cible}
        - Cost: {event.cout or 'Free'}
        - Registration: {event.inscription or 'Not required'}
        - Details: {event.description[:200]}... [Full details: {event.url_fiche}]"""
        
        event_descriptions.append(desc)
    
    return "Current Montreal events:\n" + "\n\n".join(event_descriptions)


@app.route("/gpt", methods=["POST"])
def convo():
    data = request.get_json()
    
    # Extract dates
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    date_context = ""
    
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            events = get_events_by_date(start_date, end_date)
            date_context = format_events_for_gpt(events)
        except Exception as e:
            return {"error": f"Invalid date format: {str(e)}"}, 400



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


@app.route("/test-db")
def test_db():
    try:
        event_count = Event.query.count()
        sample_event = Event.query.first()
        return {
            "status": "connected",
            "total_events": event_count,
            "sample_event": {
                "title": sample_event.titre,
                "dates": f"{sample_event.date_debut} to {sample_event.date_fin}"
            } if sample_event else None
        }
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/")
def home():
    return "Server is running!", 200

if __name__ == "__main__":
    app.run(port=5001)