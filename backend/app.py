from flask import Flask, request, Response, jsonify
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
app.config['SQLALCHEMY_BINDS'] = {
    'hotel': 'mysql+pymysql://root:fuka1010@localhost/hotel_db'
}
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
    latitude = db.Column(db.Numeric(10, 8), nullable=False, default=45.5017)
    longitude = db.Column(db.Numeric(11, 8), nullable=False, default=-73.5673)
    coord_x = db.Column(db.Numeric(10, 1))
    coord_y = db.Column(db.Numeric(10, 1))
    created_at = db.Column(db.TIMESTAMP)

    def serialize(self):
        return {
            "name": self.titre,
            "start_date": str(self.date_debut),
            "end_date": str(self.date_fin),
            "type": self.type_evenement,
            "price": self.cout or "Free",
            "latitude": float(self.latitude) if self.latitude else None,
            "longitude": float(self.longitude) if self.longitude else None,
            "registration_required": self.inscription == "Required",
            "arrondissement": self.arrondissement
        }

client = OpenAI(api_key=key, base_url="https://api.deepseek.com")


# Hotel Model
class Hotel(db.Model):
    __bind_key__ = 'hotel'
    __tablename__ = 'Hotels'
    hotel_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    address_street1 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    latitude = db.Column(db.Numeric(9, 6))
    longitude = db.Column(db.Numeric(9, 6))
    hotel_class = db.Column(db.Numeric(3, 1))
    hotel_class_attribution = db.Column(db.String(255))
    main_image_url = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    website = db.Column(db.String(255))
    web_url = db.Column(db.String(255))
    price_level = db.Column(db.String(10))
    price_range = db.Column(db.String(100))
    ranking_denominator = db.Column(db.Integer)
    ranking_position = db.Column(db.Integer)
    ranking_string = db.Column(db.String(255))
    rating = db.Column(db.Numeric(3, 2))
    
    # Relationships
    photos = db.relationship('Photo', backref='hotel', lazy=True)
    review_scores = db.relationship('ReviewScore', backref='hotel', lazy=True)
    metro_stations = db.relationship('MetroStation', backref='hotel', lazy=True)

class MetroLine(db.Model):
    __bind_key__ = 'hotel'
    __tablename__ = 'MetroLines'
    metro_line_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    metro_station_id = db.Column(db.Integer, db.ForeignKey('MetroStations.metro_station_id'))
    line_id = db.Column(db.String(50))
    line_name = db.Column(db.String(255))
    line_symbol = db.Column(db.String(50))
    system_symbol = db.Column(db.String(50))

class MetroStation(db.Model):
    __bind_key__ = 'hotel'
    __tablename__ = 'MetroStations'
    metro_station_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('Hotels.hotel_id'))
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    distance = db.Column(db.String(50))
    latitude = db.Column(db.Numeric(9, 6))
    longitude = db.Column(db.Numeric(9, 6))
    
    metro_lines = db.relationship('MetroLine', backref='metro_station', lazy=True)

class Photo(db.Model):
    __bind_key__ = 'hotel'
    __tablename__ = 'Photos'
    photo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('Hotels.hotel_id'))
    photo_url = db.Column(db.String(255))
    photo_order = db.Column(db.Integer)

class ReviewScore(db.Model):
    __bind_key__ = 'hotel'
    __tablename__ = 'ReviewScores'
    review_score_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('Hotels.hotel_id'))
    category_name = db.Column(db.String(255))
    score = db.Column(db.Numeric(5, 2))
    category_order = db.Column(db.Integer)

# Add these new functions
def get_hotels_with_details(limit=15):
    try:
        return Hotel.query.options(
            db.joinedload(Hotel.photos),
            db.joinedload(Hotel.review_scores),
            db.joinedload(Hotel.metro_stations).joinedload(MetroStation.metro_lines)
        ).limit(limit).all()
    except Exception as e:
        print(f"Hotel query error: {str(e)}")
        return []

def format_hotels_for_gpt(hotels):
    if not hotels:
        return "No hotel data available"
    
    hotel_list = []
    for hotel in hotels:
        entry = f"""**{hotel.name}** (Rating: {hotel.rating}/5)
- Address: {hotel.address_street1}, {hotel.city}
- Price Range: {hotel.price_range or 'Not specified'}
- Class: {hotel.hotel_class}/5
- Metro Access: {', '.join([f"{station.name} ({', '.join(line.line_name for line in station.metro_lines)})" 
                          for station in hotel.metro_stations]) or 'None nearby'}
- Top Amenities: {', '.join([score.category_name for score in hotel.review_scores][:3])}"""
        hotel_list.append(entry)
    
    return "AVAILABLE HOTELS:\n" + "\n\n".join(hotel_list)

def is_hotel_query(user_message, hotels):
    user_msg = user_message.lower()
    hotel_names = [h.name.lower() for h in hotels]
    keywords = {
        'hotel', 'stay', 'lodging', 'accommodation',
        'book a room', 'where to stay', 'place to stay',
        'recommend hotels', 'find hotels', 'hotel near'
    }
    return any(kw in user_msg for kw in keywords) or any(name in user_msg for name in hotel_names)


# trip planning detection function
def is_trip_planning(user_message):
    trip_keywords = {
        'plan my trip', 'itinerary', 'visit montreal', 
        'vacation plan', 'travel plan', 'schedule my visit'
    }
    return any(kw in user_message.lower() for kw in trip_keywords)

# Modified GPT endpoint
@app.route("/gpt", methods=["POST"])
def convo():
    data = request.get_json()
    user_message = data.get('user_message', '').lower()
    session_id = data.get("session_id") or str(uuid.uuid4())

    try:
        # Validate dates first
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
        
        # Get both datasets
        hotels = get_hotels_with_details()
        events = get_events_by_date(start_date, end_date)
        
        # Format contexts
        hotel_context = format_hotels_for_gpt(hotels)
        event_context = format_events_for_gpt(events)
        
        # Create combined prompt
        system_prompt = f"""COMBINED TRIP PLANNING DATA:
        
        AVAILABLE HOTELS:
        {hotel_context}
        
        SCHEDULED EVENTS ({start_date} to {end_date}):
        {event_context}
        
        Create a detailed daily itinerary with:
        1. Date-specific plans divided into morning/afternoon/evening
        2. Hotel recommendations near each day's events
        3. Metro connections between locations
        4. Price range considerations
        5. Registration requirements for events
        6. Include hotel amenities and metro access details"""
        
        # Session handling
        if session_id not in sessions:
            sessions[session_id] = {
                "conversation": [{"role": "system", "content": system_prompt}],
                "last_activity": datetime.now()
            }
        else:
            sessions[session_id]["conversation"][0]["content"] = system_prompt
            sessions[session_id]["last_activity"] = datetime.now()

        # Add user message
        sessions[session_id]["conversation"].append({"role": "user", "content": user_message})

        # Streaming response
        def generate():
            full_response = []
            stream = client.chat.completions.create(
                model="deepseek-chat",
                messages=sessions[session_id]["conversation"],
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response.append(chunk.choices[0].delta.content)
                    yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"
            
            sessions[session_id]["conversation"].append({"role": "assistant", "content": ''.join(full_response)})
            yield "data: [DONE]\n\n"
        
        return Response(generate(), mimetype="text/event-stream")

    except ValueError as e:
        return jsonify({"error": f"Invalid date format: {str(e)}. Use YYYY-MM-DD format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

sessions = {}

def initialize_session(session_id, date_context=""):
    sessions[session_id] = {
        "conversation": [{
            "role": "system",
            "content": f"""Respond using ONLY these events:
            {date_context}
            
            Requirements:
            1. Create hourly itineraries for requested dates
            2. Include exact event times if available
            3. Note transportation between locations
            4. Flag events needing registration
            5. Never invent fictional events"""
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
            Event.date_debut.between(start_date, end_date)  # Only events STARTING in range
        ).order_by(Event.date_debut).limit(50).all()  # Limit to 50 most relevant
    except Exception as e:
        print(f"Database error: {str(e)}")
        return []

def format_events_for_gpt(events):
    if not events:
        return "No events found for these dates"
    
    event_list = []
    for event in events[:15]:
        # Handle null coordinates
        lat = float(event.latitude) if event.latitude else 45.5017  # Default to Montreal center
        lon = float(event.longitude) if event.longitude else -73.5673
        
        entry = f"""**{event.titre}**
        - Dates: {event.date_debut} to {event.date_fin}
        - Type: {event.type_evenement}
        - Price: {event.cout or 'Free'}
        - Coordinates: ({lat:.6f}, {lon:.6f})
        - Registration: {'Required' if event.inscription else 'Not required'}"""
        
        event_list.append(entry)
    
    return "CURRENT MONTREAL EVENTS:\n" + "\n\n".join(event_list)


# @app.route("/gpt", methods=["POST"])
# def convo():
#     data = request.get_json()
    
#     # Extract dates
#     start_date_str = data.get('start_date')
#     end_date_str = data.get('end_date')
#     date_context = ""
    
#     if start_date_str and end_date_str:
#         try:
#             start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
#             end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
#             events = get_events_by_date(start_date, end_date)
#             date_context = format_events_for_gpt(events)

#             return {
#                 "event_count": len(events),
#                 "date_context_sample": date_context[:500] + "...",
#                 "system_prompt": sessions.get("conversation", [{}])[0].get("content", "")[:500] + "..."
#             }, 200
            
#         except Exception as e:
#             return {"error": f"Invalid date format: {str(e)}"}, 400


    # # Get or create session ID
    # session_id = data.get("session_id")
    # if not session_id or session_id not in sessions:
    #     session_id = str(uuid.uuid4())
    #     initialize_session(session_id)
    
    # conversation = sessions[session_id]["conversation"]
    
    # user_message = data.get("user_message")
    # if not user_message:
    #     return {"error": "Missing user_message"}, 400
    
    # conversation.append({"role": "user", "content": user_message})
    
    # # Create a generator for streaming responses
    # def generate():
    #     full_response = []
    #     stream = client.chat.completions.create(
    #         model="deepseek-chat",
    #         messages=conversation,
    #         stream=True
    #     )
        
    #     for chunk in stream:
    #         delta = chunk.choices[0].delta
    #         if delta.content:
    #             full_response.append(delta.content)
    #             yield f"data: {json.dumps({
    #                 'session_id': session_id,
    #                 'delta': delta.content,
    #                 'chunk_id': chunk.id,
    #                 'finished': False
    #             })}\n\n"
        
    #     conversation.append({"role": "assistant", "content": ''.join(full_response)})
    #     yield f"data: {json.dumps({
    #         'session_id': session_id,
    #         'finished': True
    #     })}\n\n"

    # return Response(generate(), mimetype="text/event-stream")



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

# Temporary test route to check data quality
@app.route("/test-event")
def test_event():
    event = Event.query.filter(
        Event.date_debut == '2025-02-02'
    ).first()
    
    if event:
        return jsonify({
            "exists": True,
            "event": event.serialize(),
            "raw_description": event.description[:100] + "..." if event.description else None
        })
    return jsonify({"exists": False})

if __name__ == "__main__":
    app.run(port=5001)