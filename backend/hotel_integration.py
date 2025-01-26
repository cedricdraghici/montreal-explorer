import mysql.connector
from mysql.connector import Error
import csv
import os
from pathlib import Path
import sys
import traceback


class HotelDBManager:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'fuka1010',
            'database': 'hotel_db'
        }
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            print("Successfully connected to database")
            return True
        except Error as e:
            print(f"Connection error: {e}")
            return False

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Connection closed")

    def insert_hotel_from_csv_row(self, row):
        """Insert data from CSV row into normalized tables"""
        try:
            cursor = self.conn.cursor()

            def safe_float(value):
                try:
                    return float(value) if value.strip() else None
                except:
                    return None

            def safe_int(value):
                try:
                    return int(value) if value.strip() else None
                except:
                    return None

            # Insert main hotel data
            hotel_data = (
                row.get('name', ''),
                row.get('description', ''),
                row.get('addressObj/street1', ''),
                row.get('addressObj/city', ''),
                row.get('addressObj/country', ''),
                row.get('addressObj/postalcode', ''),
                safe_float(row.get('latitude', '')),
                safe_float(row.get('longitude', '')),
                safe_float(row.get('hotelClass', '')),
                row.get('hotelClassAttribution', ''),
                row.get('image', ''),
                row.get('phone', ''),
                row.get('website', ''),
                row.get('webUrl', ''),
                row.get('priceLevel', ''),
                row.get('priceRange', ''),
                safe_int(row.get('rankingDenominator', '')),
                safe_int(row.get('rankingPosition', '')),
                row.get('rankingString', ''),
                safe_float(row.get('rating', ''))
            )

            insert_hotel = """
            INSERT INTO Hotels (
                name, description, address_street1, city, country, postal_code,
                latitude, longitude, hotel_class, hotel_class_attribution,
                main_image_url, phone, website, web_url, price_level, price_range,
                ranking_denominator, ranking_position, ranking_string, rating
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_hotel, hotel_data)
            hotel_id = cursor.lastrowid

            # Insert review scores
            for i in range(6):  # Assuming max 6 review categories
                category_key = f'categoryReviewScores/{i}/categoryName'
                score_key = f'categoryReviewScores/{i}/score'
                
                if row.get(category_key) and row.get(score_key):

                    try:
                        review_score = safe_float(row[score_key])
                        if review_score is not None:
                            review_data = (
                                hotel_id,
                                row[category_key],
                                float(row[score_key]),
                                i  # Preserve original order
                            )
                            cursor.execute("""
                                INSERT INTO ReviewScores 
                                (hotel_id, category_name, score, category_order)
                                VALUES (%s, %s, %s, %s)
                            """, review_data)

                    except Exception as e:
                        print(f"Skipping invalid review score in row: {e}")

            # Insert photos
            for i in range(16):  # Assuming photos/0 to photos/15
                photo_key = f'photos/{i}'
                if photo_key in row and row[photo_key].strip():
                    try:
                        cursor.execute("""
                            INSERT INTO Photos 
                            (hotel_id, photo_url, photo_order)
                            VALUES (%s, %s, %s)
                        """, (hotel_id, row[photo_key], i))
                    except Exception as e:
                        print(f"Skipping invalid photo URL in position {i}: {e}")


            # Insert metro stations
            if row.get('nearestMetroStations/0/name', '').strip():
                try:
                    metro_data = (
                        hotel_id,
                        row['nearestMetroStations/0/name'],
                        row.get('nearestMetroStations/0/address', ''),
                        row.get('nearestMetroStations/0/distance', ''),
                        safe_float(row.get('nearestMetroStations/0/latitude', '')),
                        safe_float(row.get('nearestMetroStations/0/longitude', ''))
                    )
                    cursor.execute("""
                        INSERT INTO MetroStations 
                        (hotel_id, name, address, distance, latitude, longitude)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, metro_data)
                    metro_id = cursor.lastrowid


                # Insert metro lines
                    if row.get('nearestMetroStations/0/lines/0/lineName', '').strip():
                        line_data = (
                            metro_id,
                            row.get('nearestMetroStations/0/lines/0/id', ''),
                            row['nearestMetroStations/0/lines/0/lineName'],
                            row.get('nearestMetroStations/0/lines/0/lineSymbol', ''),
                            row.get('nearestMetroStations/0/lines/0/systemSymbol', '')
                        )
                        cursor.execute("""
                            INSERT INTO MetroLines 
                            (metro_station_id, line_id, line_name, line_symbol, system_symbol)
                            VALUES (%s, %s, %s, %s, %s)
                        """, line_data)

                except Exception as e:
                    print(f"Skipping invalid metro station data: {e}")


            self.conn.commit()
            print(f"Successfully inserted hotel {hotel_id} with related data")
            return True

        except Error as e:
                self.conn.rollback()
                print(f"Database error: {e}")
                return False
        except Exception as e:
            self.conn.rollback()
            print(f"Processing error: {e}")
            return False

        finally:
            if cursor:
                cursor.close()

    def get_hotel_details(self, hotel_id):
        """Retrieve complete hotel information with related data"""
        try:
            cursor = self.conn.cursor(dictionary=True)

            # Get hotel base info
            cursor.execute("SELECT * FROM Hotels WHERE hotel_id = %s", (hotel_id,))
            hotel = cursor.fetchone()
            if not hotel:
                return None

            # Get related data
            cursor.execute("SELECT * FROM ReviewScores WHERE hotel_id = %s", (hotel_id,))
            hotel['review_scores'] = cursor.fetchall()

            cursor.execute("SELECT * FROM Photos WHERE hotel_id = %s", (hotel_id,))
            hotel['photos'] = cursor.fetchall()

            cursor.execute("""
                SELECT ms.*, ml.line_name 
                FROM MetroStations ms
                LEFT JOIN MetroLines ml ON ms.metro_station_id = ml.metro_station_id
                WHERE ms.hotel_id = %s
            """, (hotel_id,))
            hotel['metro_stations'] = cursor.fetchall()

            return hotel

        except Error as e:
            print(f"Query error: {e}")
            return None
        finally:
            if cursor:
                cursor.close()


def import_hotel_data():
    db = HotelDBManager()
    if not db.connect():
        return
    
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    csv_path = script_dir / "hotel.csv"
    
    if not csv_path.exists():
        print(f"Error: hotel.csv not found in {script_dir}")
        return

    try:
        with open(csv_path, 'r', encoding='latin-1') as file:
            reader = csv.DictReader(file)
            for row_num, row in enumerate(reader, 1):
                print(f"Processing row {row_num}...")
                db.insert_hotel_from_csv_row(row)
                print(f"Completed row {row_num}")
                
        print("\nCSV import completed successfully")
        
    except Exception as e:
        print(f"Error processing CSV: {e}")
    finally:
        db.disconnect()

# Example usage for data retrieval
def get_hotel_info(hotel_id):
    db = HotelDBManager()
    if not db.connect():
        return
    
    hotel = db.get_hotel_details(hotel_id)
    if hotel:
        print(f"Hotel Name: {hotel['name']}")
        print(f"Rating: {hotel['rating']}")
        print(f"Review Categories:")
        for score in hotel['review_scores']:
            print(f"- {score['category_name']}: {score['score']}")
    
    db.disconnect()

# Execute these to test
if __name__ == "__main__":
    import_hotel_data()  
    get_hotel_info(1)  # Get info for hotel with ID 1