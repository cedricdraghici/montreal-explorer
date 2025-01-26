import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import curvedRec from "../assets/curved-rec.svg";
import homeIcon from "../assets/home.svg";
import mapViewIcon from "../assets/mapview.svg";
import "./MapViewPage.css";

function ViewList() {
  const navigate = useNavigate();
  const [days, setDays] = useState([]);
  const [selectedDay, setSelectedDay] = useState(null);
  const [selectedMode, setSelectedMode] = useState("DRIVING");
  const [itinerary, setItinerary] = useState(null);
  const [routeData, setRouteData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDays = async () => {
      try {
        const response = await fetch("http://10.122.141.184:4000/itinerary/days");
        const data = await response.json();
        if (data.days) {
          setDays(data.days);
          if (data.days.length > 0) setSelectedDay(data.days[0]);
        }
      } catch (err) {
        setError("Failed to load days");
      }
    };
    fetchDays();
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      if (!selectedDay) return;
      setLoading(true);
      try {
        const [itRes, routeRes] = await Promise.all([
          fetch(`http://10.122.141.184:4000/itinerary/${selectedDay}`),
          fetch(`http://10.122.141.184:4000/step_route/${selectedDay}?mode=${selectedMode}`)
        ]);
        
        if (!itRes.ok || !routeRes.ok) throw new Error("Data load failed");
        
        const [itData, routeData] = await Promise.all([
          itRes.json(),
          routeRes.json()
        ]);
        
        setItinerary(itData);
        setRouteData(routeData);
        setError("");
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [selectedDay, selectedMode]);

  return (
    <div className="macbook-pro">
      <img className="curved-recfull" src={curvedRec} alt="Curved Background" />

      <div className="home-container">
        <img
          className="home-icon"
          src={homeIcon}
          alt="Home Icon"
          onClick={() => navigate("/")}
          style={{ cursor: "pointer" }}
        />
      </div>

      <div className="viewlist-content">
        <h1>Your Itinerary</h1>

        {/* Day Selector */}
        <div className="day-selector">
          <label>Select Day: </label>
          <select 
            value={selectedDay || ""}
            onChange={(e) => setSelectedDay(Number(e.target.value))}
            disabled={loading}
          >
            {days.map(day => (
              <option key={day} value={day}>Day {day}</option>
            ))}
          </select>
        </div>

        {/* Transport Mode Selector */}
        <div className="transport-modes">
          {["DRIVING", "WALKING", "TRANSIT", "BICYCLING"].map((mode) => (
            <button
              key={mode}
              className={`mode-btn ${selectedMode === mode ? "active" : ""}`}
              onClick={() => setSelectedMode(mode)}
              disabled={loading}
            >
              {mode.toLowerCase()}
            </button>
          ))}
        </div>

        {/* Loading & Error States */}
        {loading && <div className="status-message">Loading itinerary...</div>}
        {error && <div className="error-message">{error}</div>}

        {/* Total Time Display */}
        {routeData?.total_travel_time_minutes && (
          <div className="total-time">
            ⏱ Total Estimated Time: {routeData.total_travel_time_minutes} minutes
          </div>
        )}

        {/* Itinerary List */}
        <div className="itinerary-list">
          {itinerary?.waypoints?.map((wp, index) => (
            <React.Fragment key={index}>
              {/* Waypoint Card */}
              <div className="waypoint-card">
                <div className="waypoint-marker">{index + 1}</div>
                <div className="waypoint-info">
                  <h3>{wp.title}</h3>
                  <p className="description">{wp.desc}</p>
                  <div className="waypoint-meta">
                    {wp.arrival_time && (
                      <span>🕒 Arrive by {wp.arrival_time}</span>
                    )}
                    <span>⏳ Stay for {wp.stay_minutes || 0} minutes</span>
                  </div>
                </div>
              </div>

              {/* Travel Step */}
              {index < itinerary.waypoints.length - 1 && (
                <div className="travel-step">
                  {selectedMode === "TRANSIT" ? (
                    routeData?.legs?.[index] ? (
                      <div className="transit-step">
                        <span>🚆 Public Transport ({routeData.legs[index].travel_time_minutes}min)</span>
                        <p className="transit-route">
                          From {routeData.legs[index].start_address} to{" "}
                          {routeData.legs[index].end_address}
                        </p>
                      </div>
                    ) : (
                      <div className="loading-step">Loading transport info...</div>
                    )
                  ) : (
                    routeData?.api_directions?.routes?.[0]?.legs?.[index] && (
                      <div className="direct-step">
                        <span>
                          {selectedMode === "DRIVING" ? "🚗" : 
                           selectedMode === "WALKING" ? "🚶" : "🚴"} 
                          {routeData.api_directions.routes[0].legs[index].duration.text} 
                          {selectedMode.toLowerCase()}
                        </span>
                      </div>
                    )
                  )}
                </div>
              )}
            </React.Fragment>
          ))}
        </div>
      </div>

      <div className="mapview-container">
        <img
          className="mapview"
          src={mapViewIcon}
          alt="View Map Icon"
          onClick={() => navigate("/mapview")}
          style={{ cursor: "pointer" }}
        />
      </div>
    </div>
  );
}

export default ViewList;