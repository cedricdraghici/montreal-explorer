from flask import Flask, jsonify, render_template_string, request, Blueprint

app_map = Blueprint('app_map',__name__)


import requests

GOOGLE_MAPS_TOKEN = "AIzaSyCPQ7qn2XeP87kffdvz8EtkHoqrS1IMQaA"

# Each waypoint is a dict: {lon, lat, title, desc, stay_minutes, arrival_time (optional)}
# Make sure these days/waypoints actually exist so day=1 or day=2 doesn't 404
itineraries = {
    1: {
        "waypoints": [
            {
                "lon": -73.6151,
                "lat": 45.4926,
                "title": "Oratory of St Joseph",
                "desc": "Canada's largest church",
                "stay_minutes": 120,
                "arrival_time": "10:00"
            },
            {
                "lon": -73.5790,
                "lat": 45.4972,
                "title": "Museum of Fine Arts",
                "desc": "Major art museum",
                "stay_minutes": 60,
                "arrival_time": "14:00"
            },
            {
                "lon": -73.5794,
                "lat": 45.5087,
                "title": "McGill University",
                "desc": "Historic campus",
                "stay_minutes": 30,
                "arrival_time": "16:00"
            }
        ]
    },
    2: {
        "waypoints": [
            {
                "lon": -73.5565,
                "lat": 45.5090,
                "title": "Old Port",
                "desc": "Historic waterfront district",
                "stay_minutes": 90
            },
            {
                "lon": -73.5696,
                "lat": 45.5030,
                "title": "Notre-Dame Basilica",
                "desc": "Neo-Gothic masterpiece",
                "stay_minutes": 30
            },
            {
                "lon": -73.5855,
                "lat": 45.5043,
                "title": "Mont Royal Lookout",
                "desc": "Iconic city viewpoint",
                "stay_minutes": 60
            }
        ]
    }
}

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

        # Add stay time at current waypoint
        stay_time_minutes = waypoints[i].get("stay_minutes", 0)
        total_travel_time += stay_time_minutes

    return {
        "legs": legs_data,
        "total_travel_time_minutes": total_travel_time
    }


@app_map.route("/step_route/<int:day>")
def step_route(day):
    if day not in itineraries:
        return jsonify({"error": "Day not found"}), 404

    waypoints = itineraries[day]["waypoints"]
    mode = request.args.get("mode", "driving").upper()

    # If user selected TRANSIT, do multiple legs
    if mode == "TRANSIT":
        result = build_transit_steps(waypoints, mode)
        return jsonify(result)
    else:
        # For driving/walking/bicycling, gather them into one route
        origin = f"{waypoints[0]['lat']},{waypoints[0]['lon']}"
        destination = f"{waypoints[-1]['lat']},{waypoints[-1]['lon']}"
        if len(waypoints) > 2:
            middle = waypoints[1:-1]
            waypoints_formatted = "|".join(
                [f"via:{wp['lat']},{wp['lon']}" for wp in middle]
            )
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
            stay_total = sum(wp.get("stay_minutes", 0) for wp in waypoints[:-1])
            return jsonify({
                "api_directions": data,
                "total_travel_time_minutes": round(total_route_time / 60) + stay_total
            })
        else:
            return jsonify({
                "error": data.get("status", "UNKNOWN_ERROR")
            }), 400


########################################
# Itinerary add/remove
########################################
@app_map.route("/itinerary/<int:day>/add", methods=["POST"])
def add_event(day):
    if day not in itineraries:
        return jsonify({"error": "Day not found"}), 404
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


@app_map.route("/itinerary/<int:day>")
def get_itinerary(day):
    if day not in itineraries:
        return jsonify({"error": "Day not found"}), 404
    return jsonify(itineraries[day])


@app_map.route("/map")
def show_map():
    # We'll just default the map center to day=1's first waypoint for an initial view
    # but the user can pick Day 2 after it loads.
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Montreal Itinerary</title>
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
        <div id="map" style="height: 100vh; width: 100%"></div>
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
                    // Basic map objects
                    this.map = null;
                    this.directionsService = new google.maps.DirectionsService();
                    this.directionsRenderer = new google.maps.DirectionsRenderer({ suppressMarkers: true });
                    this.markers = [];
                    this.polylines = [];
                    // Default to day 1
                    this.currentDay = 1;
                    this.transportMode = 'DRIVING';
                    this.initMap();
                }

                initMap() {
                    // Hard-code the initial center to day=1's first waypoint
                    // so we at least see something on load.
                    // If day=1 doesn't exist or is empty, you'll get a server error
                    // or an invalid lat/lng if your data is missing.
                    // Make sure you have day=1 in your itineraries!
                    this.map = new google.maps.Map(document.getElementById('map'), {
                        center: new google.maps.LatLng({{ itineraries[1]["waypoints"][0]["lat"] }}, {{ itineraries[1]["waypoints"][0]["lon"] }}),
                        zoom: 13,
                        mapTypeControl: false
                    });

                    this.createDayButtons();
                    this.createTransportSelector();
                    this.directionsRenderer.setMap(this.map);

                    // Load day 1 itinerary on startup
                    this.loadDay(1);
                }

                createDayButtons() {
                    const dayContainer = document.createElement('div');
                    dayContainer.innerHTML = `
                        <button class="day-button active" data-day="1">Day 1</button>
                        <button class="day-button" data-day="2">Day 2</button>
                    `;
                    dayContainer.style.position = 'absolute';
                    dayContainer.style.top = '10px';
                    dayContainer.style.left = '10px';

                    // Day button event listener
                    dayContainer.addEventListener('click', (e) => {
                        if (e.target.tagName === 'BUTTON') {
                            const day = parseInt(e.target.dataset.day);
                            this.currentDay = day;
                            this.loadDay(day);
                            document.querySelectorAll('.day-button').forEach(btn => {
                                btn.classList.toggle('active', parseInt(btn.dataset.day) === day);
                            });
                        }
                    });

                    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(dayContainer);
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

                clearPolylines() {
                    this.polylines.forEach(line => line.setMap(null));
                    this.polylines = [];
                }

                async loadDay(day) {
                    const infoPanel = document.getElementById('details');
                    // Clear markers & polylines
                    this.markers.forEach(m => m.setMap(null));
                    this.markers = [];
                    this.clearPolylines();
                    this.directionsRenderer.set('directions', null);

                    let dayWaypoints = null;

                    // 1) First, fetch the actual itinerary for the day
                    try {
                        const itResp = await fetch(`/itinerary/${day}`);
                        if (!itResp.ok) {
                            infoPanel.innerHTML = `<p>Error fetching itinerary for Day ${day} (${itResp.statusText})</p>`;
                            return;
                        }
                        const dayData = await itResp.json();
                        if (dayData.error) {
                            infoPanel.innerHTML = `<p>Error: ${dayData.error}</p>`;
                            return;
                        }
                        dayWaypoints = dayData.waypoints || [];
                    } catch (err) {
                        console.error('Error fetching day itinerary:', err);
                        infoPanel.innerHTML = `<p>Could not retrieve itinerary for Day ${day}.</p>`;
                        return;
                    }

                    // If no waypoints, we can't do much
                    if (!dayWaypoints.length) {
                        infoPanel.innerHTML = `<p>No waypoints found for day ${day}.</p>`;
                        return;
                    }

                    // 2) Next, get the directions info from /step_route/<day>
                    let routeData = null;
                    try {
                        const routeResp = await fetch(`/step_route/${day}?mode=${this.transportMode}`);
                        routeData = await routeResp.json();
                    } catch (err) {
                        console.error('Error fetching route for day:', err);
                        infoPanel.innerHTML = `<p>Error fetching route data for Day ${day}.</p>`;
                        return;
                    }

                    // 3) If transit, decode polylines. If non-transit, use DirectionsRenderer
                    if (this.transportMode === 'TRANSIT') {
                        // If success
                        if (routeData.legs) {
                            // Place polylines
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
                        } else {
                            infoPanel.innerHTML = '<p>No transit route data found.</p>';
                        }
                    } else {
                        // Non-transit
                        if (routeData.api_directions && routeData.api_directions.status === 'OK') {
                            infoPanel.innerHTML = `
                                <h3>Route Info</h3>
                                <p>Total Travel Time (including stays): ${routeData.total_travel_time_minutes} minutes</p>
                            `;
                            // Render client-side directions
                            this.showClientSideRoute(dayWaypoints);
                        } else if (routeData.error) {
                            infoPanel.innerHTML = `<p>Error: ${routeData.error}</p>`;
                        } else {
                            infoPanel.innerHTML = '<p>No data returned.</p>';
                        }
                    }

                    // Finally, place markers for each waypoint
                    dayWaypoints.forEach((wp, i) => {
                        const marker = new google.maps.Marker({
                            position: { lat: wp.lat, lng: wp.lon },
                            map: this.map,
                            title: wp.title,
                            label: (i+1).toString()
                        });
                        let arrivalLine = (wp.arrival_time) ? `<p>Arrival: ${wp.arrival_time}</p>` : '';
                        const infoWindow = new google.maps.InfoWindow({
                            content: `<h3>${wp.title}</h3>
                                      <p>${wp.desc}</p>
                                      <p>Stay time: ${wp.stay_minutes} min</p>
                                      ${arrivalLine}`
                        });
                        marker.addListener('click', () => {
                            infoWindow.open(this.map, marker);
                        });
                        this.markers.push(marker);
                    });
                }

                showClientSideRoute(dayWaypoints) {
                    // Use DirectionsRenderer in the browser for a single route
                    const origin = { lat: dayWaypoints[0].lat, lng: dayWaypoints[0].lon };
                    const destination = { lat: dayWaypoints[dayWaypoints.length - 1].lat, lng: dayWaypoints[dayWaypoints.length - 1].lon };
                    const waypts = [];
                    if (dayWaypoints.length > 2) {
                        for (let i = 1; i < dayWaypoints.length - 1; i++) {
                            waypts.push({
                                location: { lat: dayWaypoints[i].lat, lng: dayWaypoints[i].lon },
                                stopover: false
                            });
                        }
                    }
                    this.directionsService.route({
                        origin: origin,
                        destination: destination,
                        waypoints: waypts,
                        travelMode: MODE_MAP[this.transportMode]
                    }, (result, status) => {
                        if (status === 'OK') {
                            this.directionsRenderer.setDirections(result);
                        } else {
                            console.error('Client side directions error:', status);
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
    ''', itineraries=itineraries, GOOGLE_MAPS_TOKEN=GOOGLE_MAPS_TOKEN)



