import mysql.connector
from mysql.connector import Error
import csv
from datetime import datetime
from googletrans import Translator # since the csv is in French
import time
from typing import Dict, Any

class EventDataImporter:
    def __init__(self):
        try:
            self.translator = Translator()
            self.delay = 1  # Delay between translations to avoid rate limiting
        except Exception as e:
            print(f"Error initializing translator: {e}")

    def translate_text(self, text: str) -> str:
        if not text or text == 'nan':
            return None
        try:
            time.sleep(self.delay)
            return self.translator.translate(text, src='fr', dest='en').text
        except Exception as e:
            print(f"Translation error for text '{text}': {e}")
            return text

    def translate_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        try:
            translated_row = row.copy()
            
            # Fields to translate
            fields_to_translate = {
                'titre': 'title',
                'description': 'description',
                'type_evenement': 'event_type',
                'public_cible': 'target_audience',
                'emplacement': 'location',
                'inscription': 'registration',
                'cout': 'cost',
                'arrondissement': 'borough',
                'titre_adresse': 'address_title',
                'adresse_principale': 'main_address',
                'adresse_secondaire': 'secondary_address'
            }
            
            # Translate each field and store both versions
            for fr_field, en_field in fields_to_translate.items():
                if fr_field in row and row[fr_field] and row[fr_field] != 'nan':
                    translated_row[en_field] = self.translate_text(row[fr_field])
                    translated_row[f"{en_field}_fr"] = row[fr_field]
                else:
                    translated_row[en_field] = None
                    translated_row[f"{en_field}_fr"] = None

            # Copy non-translatable fields
            translated_row['url'] = row['url_fiche']
            translated_row['start_date'] = row['date_debut']
            translated_row['end_date'] = row['date_fin']
            translated_row['postal_code'] = row['code_postal']
            translated_row['latitude'] = row['lat']
            translated_row['longitude'] = row['long']
            translated_row['coord_x'] = row['X']
            translated_row['coord_y'] = row['Y']

            return translated_row
        except Exception as e:
            print(f"Error translating row: {e}")
            return row

    def create_database_connection(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="fuka1010",
                database="montreal_events"
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL Database: {e}")
            return None

    def create_bilingual_tables(self, connection):
        try:
            cursor = connection.cursor()
            
            # Create events table with both French and English columns
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events_bilingual (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    
                    -- Bilingual text fields
                    title VARCHAR(255),
                    title_fr VARCHAR(255),
                    description TEXT,
                    description_fr TEXT,
                    event_type VARCHAR(100),
                    event_type_fr VARCHAR(100),
                    target_audience VARCHAR(100),
                    target_audience_fr VARCHAR(100),
                    location VARCHAR(100),
                    location_fr VARCHAR(100),
                    registration VARCHAR(50),
                    registration_fr VARCHAR(50),
                    cost VARCHAR(50),
                    cost_fr VARCHAR(50),
                    borough VARCHAR(100),
                    borough_fr VARCHAR(100),
                    address_title VARCHAR(255),
                    address_title_fr VARCHAR(255),
                    main_address TEXT,
                    main_address_fr TEXT,
                    secondary_address TEXT,
                    secondary_address_fr TEXT,
                    
                    -- Non-translated fields
                    url TEXT,
                    start_date DATE,
                    end_date DATE,
                    postal_code VARCHAR(10),
                    latitude DECIMAL(10, 8),
                    longitude DECIMAL(11, 8),
                    coord_x DECIMAL(10, 1),
                    coord_y DECIMAL(10, 1),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Bilingual tables created successfully")
            
        except Error as e:
            print(f"Error creating tables: {e}")

    def import_csv_data(self, csv_file_path: str):
        connection = self.create_database_connection()
        if not connection:
            return

        try:
            self.create_bilingual_tables(connection)
            cursor = connection.cursor()
            
            count = 0
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    # Translate the row
                    translated_row = self.translate_row(row)
                    
                    # Prepare insert query
                    insert_query = """
                        INSERT INTO events_bilingual (
                            title, title_fr, description, description_fr,
                            event_type, event_type_fr, target_audience, target_audience_fr,
                            location, location_fr, registration, registration_fr,
                            cost, cost_fr, borough, borough_fr,
                            address_title, address_title_fr, main_address, main_address_fr,
                            secondary_address, secondary_address_fr, url, start_date,
                            end_date, postal_code, latitude, longitude, coord_x, coord_y
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """
                    
                    values = (
                        translated_row['title'], translated_row['title_fr'],
                        translated_row['description'], translated_row['description_fr'],
                        translated_row['event_type'], translated_row['event_type_fr'],
                        translated_row['target_audience'], translated_row['target_audience_fr'],
                        translated_row['location'], translated_row['location_fr'],
                        translated_row['registration'], translated_row['registration_fr'],
                        translated_row['cost'], translated_row['cost_fr'],
                        translated_row['borough'], translated_row['borough_fr'],
                        translated_row['address_title'], translated_row['address_title_fr'],
                        translated_row['main_address'], translated_row['main_address_fr'],
                        translated_row['secondary_address'], translated_row['secondary_address_fr'],
                        translated_row['url'], translated_row['start_date'],
                        translated_row['end_date'], translated_row['postal_code'],
                        translated_row['latitude'], translated_row['longitude'],
                        translated_row['coord_x'], translated_row['coord_y']
                    )
                    
                    cursor.execute(insert_query, values)
                    count += 1
                    
                    if count % 10 == 0:
                        connection.commit()
                        print(f"Imported and translated {count} records...")
            
            connection.commit()
            print(f"Successfully imported and translated {count} events")
            
        except Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error processing CSV file: {e}")
        finally:
            if connection.is_connected():
                connection.close()

def main():
    importer = EventDataImporter()
    csv_file_path = './data_integration/evenements.csv'
    importer.import_csv_data(csv_file_path)

if __name__ == "__main__":
    main()
