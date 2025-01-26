from flask import Flask, jsonify, render_template_string, request, Blueprint
import requests

app_map = Blueprint('app_map', __name__)
itineraries = {}

# Single in-memory store for itineraries
# itineraries = {
#     1: {
#         "waypoints": [
#             {
#                 "lon": -73.6151,
#                 "lat": 45.4926,
#                 "title": "Oratory of St Joseph",
#                 "desc": "Canada's largest church",
#                 "stay_minutes": 120,
#                 "arrival_time": "10:00"
#             },
#             {
#                 "lon": -73.5790,
#                 "lat": 45.4972,
#                 "title": "Museum of Fine Arts",
#                 "desc": "Major art museum",
#                 "stay_minutes": 60,
#                 "arrival_time": "14:00"
#             },
#             {
#                 "lon": -73.5794,
#                 "lat": 45.5087,
#                 "title": "McGill University",
#                 "desc": "Historic campus",
#                 "stay_minutes": 30,
#                 "arrival_time": "16:00"
#             }
#         ]
#     },
#     2: {
#         "waypoints": [
#             {
#                 "lon": -73.5565,
#                 "lat": 45.5090,
#                 "title": "Old Port",
#                 "desc": "Historic waterfront district",
#                 "stay_minutes": 90
#             },
#             {
#                 "lon": -73.5696,
#                 "lat": 45.5030,
#                 "title": "Notre-Dame Basilica",
#                 "desc": "Neo-Gothic masterpiece",
#                 "stay_minutes": 30
#             },
#             {
#                 "lon": -73.5855,
#                 "lat": 45.5043,
#                 "title": "Mont Royal Lookout",
#                 "desc": "Iconic city viewpoint",
#                 "stay_minutes": 60
#             }
#         ]
#     }
# }

GOOGLE_MAPS_TOKEN = "AIzaSyCPQ7qn2XeP87kffdvz8EtkHoqrS1IMQaA"

########################################
# Helper function to build step-by-step
# routes for TRANSIT or other modes.
########################################
def build_transit_steps(waypoints, mode):
    total_travel_time = 0
    legs_data = []
    for i in range(len(waypoints) - 1):
        origin = f"{waypoints[i]['lat']},{waypoints[i]['lon']}"
        destination = f"{waypoints[i+1]['lat']},{waypoints[i+1]['lon']}"
        url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": origin,
            "destination": destination,
            "mode": mode.lower(),
            "key": GOOGLE_MAPS_TOKEN
        }
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") == "OK":
            route = data["routes"][0]
            leg = route["legs"][0]
            travel_time = leg["duration"]["value"]
            travel_time_minutes = round(travel_time / 60)
            total_travel_time += travel_time_minutes
            legs_data.append({
                "start_address": leg["start_address"],
                "end_address": leg["end_address"],
                "travel_time_minutes": travel_time_minutes,
                "path": route["overview_polyline"].get("points", "")
            })
        else:
            legs_data.append({
                "error": data.get("status", "UNKNOWN_ERROR"),
                "start": origin,
                "end": destination
            })

        stay_time_minutes = waypoints[i].get("stay_minutes", 0)
        total_travel_time += stay_time_minutes

    return {
        "legs": legs_data,
        "total_travel_time_minutes": total_travel_time
    }

########################################
# Itinerary Routes
########################################

# Create a new day (returns the newly created day's index)
@app_map.route("/itinerary/create", methods=["POST"])
def create_day():
    existing_days = list(itineraries.keys())
    new_day = max(existing_days) + 1 if existing_days else 1
    itineraries[new_day] = {"waypoints": []}
    return jsonify({"message": "Day created", "day": new_day}), 201

# Get the list of days
@app_map.route("/itinerary/days")
def get_days():
    days = list(itineraries.keys())
    days.sort()
    return jsonify({"days": days})

# Add a waypoint to a given day
@app_map.route("/itinerary/<int:day>/add", methods=["POST"])
def add_event(day):
    if day not in itineraries:
        # If day doesn't exist, create it on the fly (optional behavior)
        itineraries[day] = {"waypoints": []}

    body = request.json
    if not body:
        return jsonify({"error": "No data provided"}), 400

    new_wp = {
        "lon": body.get("lon"),
        "lat": body.get("lat"),
        "title": body.get("title", "Untitled"),
        "desc": body.get("desc", ""),
        "stay_minutes": body.get("stay_minutes", 0),
        "arrival_time": body.get("arrival_time")
    }
    itineraries[day]["waypoints"].append(new_wp)
    return jsonify({"message": "Waypoint added", "itinerary": itineraries[day]}), 200

# Remove a waypoint from a given day (by title or index)
@app_map.route("/itinerary/<int:day>/remove", methods=["DELETE"])
def remove_event(day):
    if day not in itineraries:
        return jsonify({"error": "Day not found"}), 404
    body = request.json
    if not body:
        return jsonify({"error": "No data provided"}), 400

    wps = itineraries[day]["waypoints"]
    title = body.get("title")
    idx = body.get("index")

    if title:
        original_len = len(wps)
        itineraries[day]["waypoints"] = [wp for wp in wps if wp["title"] != title]
        if len(itineraries[day]["waypoints"]) < original_len:
            return jsonify({
                "message": f"Waypoint with title '{title}' removed.",
                "itinerary": itineraries[day]
            }), 200
        else:
            return jsonify({"error": f"No waypoint with title '{title}' found."}), 404
    elif idx is not None:
        if 0 <= idx < len(wps):
            removed_wp = itineraries[day]["waypoints"].pop(idx)
            return jsonify({
                "message": "Waypoint removed",
                "removed": removed_wp,
                "itinerary": itineraries[day]
            }), 200
        else:
            return jsonify({"error": "Index out of range"}), 400
    else:
        return jsonify({"error": "No valid removal criteria (title or index) provided"}), 400

# Get all waypoints for a given day
@app_map.route("/itinerary/<int:day>")
def get_itinerary(day):
    if day not in itineraries:
        return jsonify({"error": "Day not found"}), 404
    return jsonify(itineraries[day])

# Build step-by-step route or direct route for a given day
@app_map.route("/step_route/<int:day>")
def step_route(day):
    if day not in itineraries:
        return jsonify({"error": "Day not found"}), 404

    waypoints = itineraries[day]["waypoints"]
    if not waypoints:
        return jsonify({"error": "No waypoints for this day"}), 400

    mode = request.args.get("mode", "driving").upper()

    if mode == "TRANSIT":
        result = build_transit_steps(waypoints, mode)
        return jsonify(result)
    else:
        origin = f"{waypoints[0]['lat']},{waypoints[0]['lon']}"
        destination = f"{waypoints[-1]['lat']},{waypoints[-1]['lon']}"
        if len(waypoints) > 2:
            middle = waypoints[1:-1]
            waypoints_formatted = "|".join([f"via:{wp['lat']},{wp['lon']}" for wp in middle])
        else:
            waypoints_formatted = ""

        url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": origin,
            "destination": destination,
            "waypoints": waypoints_formatted,
            "mode": mode.lower(),
            "key": GOOGLE_MAPS_TOKEN
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("status") == "OK":
            route = data["routes"][0] if data.get("routes") else None
            total_route_time = 0
            if route and route.get("legs"):
                for leg in route["legs"]:
                    total_route_time += leg["duration"]["value"]

            # Sum of stay times (excluding the final stop by convention)
            stay_total = sum(wp.get("stay_minutes", 0) for wp in waypoints[:-1])
            return jsonify({
                "api_directions": data,
                "total_travel_time_minutes": round(total_route_time / 60) + stay_total
            })
        else:
            return jsonify({"error": data.get("status", "UNKNOWN_ERROR")}), 400

########################################
# Map Page (Front-end)
########################################
@app_map.route("/map")
def show_map():
    # Determine a default lat/lon based on the first day's first waypoint (if any)
    days = list(itineraries.keys())
    default_lat, default_lon = 45.5017, -73.5673  # Default to Montreal

    if days:
        first_day = min(days)
        wps = itineraries[first_day].get("waypoints", [])
        if wps:
            default_lat, default_lon = wps[0]['lat'], wps[0]['lon']

    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Travel Itinerary</title>
        <link href="https://api.mapbox.com/mapbox-gl-js/v2.13.0/mapbox-gl.css" rel="stylesheet">
        <script src="https://maps.googleapis.com/maps/api/js?key={{ GOOGLE_MAPS_TOKEN }}&libraries=geometry"></script>
        <style>
            body { margin:0; padding:0; }
            #map { width:100%; height:100vh; }
            .mapboxgl-ctrl { margin: 10px !important; }
            .day-button {
                padding: 8px 12px;
                margin: 2px;
                border: none;
                border-radius: 3px;
                cursor: pointer;
                background: #f8f9fa;
                font-size: 14px;
            }
            .day-button:hover { background: #e9ecef; }
            .day-button.active {
                background: #4264fb;
                color: white;
            }
            .add-day-btn {
                background: #28a745 !important;
                color: white !important;
            }
            .transport-controls {
                position: absolute;
                top: 10px;
                right: 10px;
                z-index: 1;
                display: flex;
                gap: 5px;
            }
            .transport-button {
                padding: 8px 12px;
                border-radius: 3px;
                border: 1px solid #ddd;
                background: white;
                cursor: pointer;
                font-size: 14px;
            }
            .transport-button.active {
                background: #007bff;
                color: white;
                border-color: #007bff;
            }
            .info-panel {
                position: absolute;
                bottom: 10px;
                left: 10px;
                background: rgba(255,255,255,0.9);
                padding: 10px;
                border-radius: 5px;
                max-width: 300px;
            }
        </style>
    </head>
    <body>
        <div id="map"></div>
        <div class="info-panel" id="infoPanel">
            <h3>Itinerary Info</h3>
            <p id="details">Select a day and mode to view travel time.</p>
        </div>
        <script>
            const MODE_MAP = {
                'DRIVING': google.maps.TravelMode.DRIVING,
                'WALKING': google.maps.TravelMode.WALKING,
                'BICYCLING': google.maps.TravelMode.BICYCLING,
                'TRANSIT': google.maps.TravelMode.TRANSIT
            };

            class ItineraryMap {
                constructor() {
                    this.map = null;
                    this.directionsService = new google.maps.DirectionsService();
                    this.directionsRenderer = new google.maps.DirectionsRenderer({ suppressMarkers: true });
                    this.markers = [];
                    this.polylines = [];
                    this.currentDay = null;
                    this.transportMode = 'DRIVING';
                    this.dayContainer = null;
                    this.initMap();
                }

                async initMap() {
                    // Initialize Google Map
                    this.map = new google.maps.Map(document.getElementById('map'), {
                        center: new google.maps.LatLng({{ default_lat }}, {{ default_lon }}),
                        zoom: 13,
                        mapTypeControl: false
                    });

                    this.directionsRenderer.setMap(this.map);

                    // Create the UI containers
                    this.createTransportSelector();
                    this.createDayContainer();

                    // Load data
                    await this.refresh();
                }

                createDayContainer() {
                    this.dayContainer = document.createElement('div');
                    this.dayContainer.style.position = 'absolute';
                    this.dayContainer.style.top = '10px';
                    this.dayContainer.style.left = '10px';
                    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(this.dayContainer);
                }

                createTransportSelector() {
                    const transportContainer = document.createElement('div');
                    transportContainer.className = 'transport-controls';
                    transportContainer.innerHTML = `
                        <button class="transport-button active" data-mode="DRIVING">🚗 Drive</button>
                        <button class="transport-button" data-mode="WALKING">🚶 Walk</button>
                        <button class="transport-button" data-mode="BICYCLING">🚴 Cycle</button>
                        <button class="transport-button" data-mode="TRANSIT">🚆 Transit</button>
                    `;
                    transportContainer.addEventListener('click', (e) => {
                        if (e.target.tagName === 'BUTTON') {
                            this.transportMode = e.target.dataset.mode;
                            this.loadDay(this.currentDay);
                            transportContainer.querySelectorAll('.transport-button').forEach(btn => {
                                btn.classList.toggle('active', btn === e.target);
                            });
                        }
                    });
                    this.map.controls[google.maps.ControlPosition.TOP_RIGHT].push(transportContainer);
                }

                async refresh() {
                    // Fetch the list of days
                    const days = await this.fetchDays();
                    // Re-render the day buttons
                    this.renderDayButtons(days);

                    if (days.length === 0) {
                        this.currentDay = null;
                        this.clearMap();
                        document.getElementById('details').innerHTML = 'No days available. Click "+ Add Day" to create one.';
                        return;
                    }
                    // Ensure currentDay is valid
                    if (!this.currentDay || !days.includes(this.currentDay)) {
                        this.currentDay = days[0];
                    }
                    // Load the current day
                    await this.loadDay(this.currentDay);
                }

                async fetchDays() {
                    try {
                        const resp = await fetch('/itinerary/days');
                        const data = await resp.json();
                        if (data.days) {
                            return data.days.sort((a, b) => a - b);
                        }
                    } catch (err) {
                        console.error('Error fetching days:', err);
                    }
                    return [];
                }

                renderDayButtons(days) {
                    // Clear container before re-render
                    this.dayContainer.innerHTML = '';

                    days.forEach(day => {
                        const btn = document.createElement('button');
                        btn.className = 'day-button';
                        if (day === this.currentDay) {
                            btn.classList.add('active');
                        }
                        btn.textContent = `Day ${day}`;
                        btn.dataset.day = day;
                        btn.addEventListener('click', () => {
                            this.handleDayChange(day);
                        });
                        this.dayContainer.appendChild(btn);
                    });

                    // Add a button to create a new day
                    const addDayBtn = document.createElement('button');
                    addDayBtn.className = 'day-button add-day-btn';
                    addDayBtn.textContent = '+ Add Day';
                    addDayBtn.addEventListener('click', () => this.addNewDay());
                    this.dayContainer.appendChild(addDayBtn);
                }

                async addNewDay() {
                    try {
                        const resp = await fetch('/itinerary/create', {
                            method: 'POST'
                        });
                        const data = await resp.json();
                        if (data.day) {
                            this.currentDay = data.day;
                            await this.refresh();
                        }
                    } catch (err) {
                        console.error('Error adding new day:', err);
                    }
                }

                handleDayChange(day) {
                    this.currentDay = day;
                    this.loadDay(day);
                    // Update button styles
                    Array.from(this.dayContainer.querySelectorAll('.day-button')).forEach(btn => {
                        const d = parseInt(btn.dataset.day);
                        btn.classList.toggle('active', d === day);
                    });
                }

                clearMap() {
                    this.markers.forEach(m => m.setMap(null));
                    this.markers = [];
                    this.clearPolylines();
                    this.directionsRenderer.set('directions', null);
                }

                clearPolylines() {
                    this.polylines.forEach(line => line.setMap(null));
                    this.polylines = [];
                }

                async loadDay(day) {
                    const infoPanel = document.getElementById('details');
                    this.clearMap();

                    // Fetch day waypoints
                    let dayData = null;
                    try {
                        const itResp = await fetch(`/itinerary/${day}`);
                        if (!itResp.ok) throw new Error(`Failed to fetch itinerary for Day ${day}`);
                        dayData = await itResp.json();
                    } catch (err) {
                        console.error(err);
                        infoPanel.innerHTML = `<p>Error loading day ${day}</p>`;
                        return;
                    }

                    const dayWaypoints = dayData.waypoints || [];
                    if (!dayWaypoints.length) {
                        infoPanel.innerHTML = `<p>No waypoints for Day ${day}</p>`;
                        return;
                    }

                    // Fetch step route
                    let routeData = null;
                    try {
                        const routeResp = await fetch(`/step_route/${day}?mode=${this.transportMode}`);
                        routeData = await routeResp.json();
                    } catch (err) {
                        console.error('Error fetching route data:', err);
                        infoPanel.innerHTML = `<p>Error fetching route data for Day ${day}</p>`;
                        return;
                    }

                    // Handle transit vs other modes
                    if (this.transportMode === 'TRANSIT') {
                        if (routeData.legs) {
                            // Build polylines from step paths
                            routeData.legs.forEach(leg => {
                                if (leg.path) {
                                    const decodedPath = google.maps.geometry.encoding.decodePath(leg.path);
                                    const polyline = new google.maps.Polyline({
                                        path: decodedPath,
                                        strokeColor: '#4264fb',
                                        strokeOpacity: 0.8,
                                        strokeWeight: 5,
                                        map: this.map
                                    });
                                    this.polylines.push(polyline);
                                }
                            });
                            infoPanel.innerHTML = `
                                <h3>Transit Route</h3>
                                <p>Total Travel Time (including stays): ${routeData.total_travel_time_minutes} minutes</p>
                            `;
                        } else if (routeData.error) {
                            infoPanel.innerHTML = `<p>Error: ${routeData.error}</p>`;
                        }
                    } else {
                        // Driving/Walking/Cycling
                        if (routeData.api_directions?.status === 'OK') {
                            // Render route on the client using DirectionsRenderer
                            this.showClientSideRoute(dayWaypoints);
                            infoPanel.innerHTML = `
                                <h3>Route Info</h3>
                                <p>Total Travel Time (including stays): ${routeData.total_travel_time_minutes} minutes</p>
                            `;
                        } else if (routeData.error) {
                            infoPanel.innerHTML = `<p>Error: ${routeData.error}</p>`;
                        }
                    }

                    // Add markers
                    dayWaypoints.forEach((wp, i) => {
                        const marker = new google.maps.Marker({
                            position: { lat: wp.lat, lng: wp.lon },
                            map: this.map,
                            title: wp.title,
                            label: (i + 1).toString()
                        });
                        const infoWindow = new google.maps.InfoWindow({
                            content: `
                                <h3>${wp.title}</h3>
                                <p>${wp.desc}</p>
                                <p>Stay time: ${wp.stay_minutes} min</p>
                                ${wp.arrival_time ? `<p>Arrival: ${wp.arrival_time}</p>` : ''}`
                        });
                        marker.addListener('click', () => infoWindow.open(this.map, marker));
                        this.markers.push(marker);
                    });

                    // Re-center map on first waypoint
                    this.map.panTo({ lat: dayWaypoints[0].lat, lng: dayWaypoints[0].lon });
                }

                showClientSideRoute(dayWaypoints) {
                    if (dayWaypoints.length < 2) return;

                    const origin = { lat: dayWaypoints[0].lat, lng: dayWaypoints[0].lon };
                    const destination = { lat: dayWaypoints[dayWaypoints.length - 1].lat, lng: dayWaypoints[dayWaypoints.length - 1].lon };
                    const waypts = dayWaypoints.slice(1, -1).map(wp => ({
                        location: { lat: wp.lat, lng: wp.lon },
                        stopover: false
                    }));

                    this.directionsService.route({
                        origin,
                        destination,
                        waypoints: waypts,
                        travelMode: MODE_MAP[this.transportMode]
                    }, (result, status) => {
                        if (status === 'OK') {
                            this.directionsRenderer.setDirections(result);
                        } else {
                            console.error('Directions error:', status);
                        }
                    });
                }
            }

            window.addEventListener('DOMContentLoaded', () => {
                new ItineraryMap();
            });
        </script>
    </body>
    </html>
    ''', default_lat=default_lat, default_lon=default_lon, GOOGLE_MAPS_TOKEN=GOOGLE_MAPS_TOKEN)
