# app/__init__.py
from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app

# app/config.py
class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'fuka1010'
    MYSQL_DB = 'montreal_events'

# app/database/events_db.py
import mysql.connector
from mysql.connector import Error
from app.config import Config

class EventDatabase:
    @staticmethod
    def get_connection():
        try:
            return mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def get_events(self, language='en', limit=10, offset=0):
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            if language == 'en':
                query = """
                    SELECT id, title, description, event_type, 
                           target_audience, location, start_date, end_date
                    FROM events_bilingual
                    LIMIT %s OFFSET %s
                """
            else:
                query = """
                    SELECT id, title_fr as title, description_fr as description,
                           event_type_fr as event_type, target_audience_fr as target_audience,
                           location_fr as location, start_date, end_date
                    FROM events_bilingual
                    LIMIT %s OFFSET %s
                """
            
            cursor.execute(query, (limit, offset))
            events = cursor.fetchall()
            return events
            
        except Error as e:
            print(f"Error fetching events: {e}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def get_event_by_id(self, event_id, language='en'):
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            if language == 'en':
                query = """
                    SELECT *
                    FROM events_bilingual
                    WHERE id = %s
                """
            else:
                query = """
                    SELECT id, title_fr as title, description_fr as description,
                           event_type_fr as event_type, target_audience_fr as target_audience,
                           location_fr as location, start_date, end_date
                    FROM events_bilingual
                    WHERE id = %s
                """
            
            cursor.execute(query, (event_id,))
            event = cursor.fetchone()
            return event
            
        except Error as e:
            print(f"Error fetching event: {e}")
            return None
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

# app/database/users_db.py
# Similar structure for users database operations...

# app/routes.py
from flask import Blueprint, jsonify, request
from app.database.events_db import EventDatabase

main_bp = Blueprint('main', __name__)

@main_bp.route('/api/events', methods=['GET'])
def get_events():
    language = request.args.get('language', 'en')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    offset = (page - 1) * per_page
    
    db = EventDatabase()
    events = db.get_events(language=language, limit=per_page, offset=offset)
    
    return jsonify({
        'events': events,
        'page': page,
        'per_page': per_page
    })

@main_bp.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    language = request.args.get('language', 'en')
    
    db = EventDatabase()
    event = db.get_event_by_id(event_id, language=language)
    
    if event:
        return jsonify(event)
    return jsonify({'error': 'Event not found'}), 404

# run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)