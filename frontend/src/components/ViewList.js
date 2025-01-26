import React from "react";
import { useNavigate } from "react-router-dom";
import restaurantsIcon from "../assets/restaurants.svg";
import cafesIcon from "../assets/cafes.svg";
import historicalIcon from "../assets/historical.svg";
import artCultureIcon from "../assets/artculture.svg";
import parksIcon from "../assets/parks.svg";
import curvedRec from "../assets/curved-rec.svg";
import homeIcon from "../assets/home.svg";
import mapViewIcon from "../assets/mapview.svg"; // The one icon we actually need
import "./MapViewPage.css"; // Reuse styles

function ViewList() {
  const navigate = useNavigate();

  const handleHomeClick = () => {
    navigate("/"); // Navigate back to the home page
  };

  const handleMapViewClick = () => {
    navigate("/mapview"); // Navigate to the Map View page
  };

  return (
    <div className="macbook-pro">
      {/* Full background */}
      <img className="curved-recfull" src={curvedRec} alt="Curved Background" />

      {/* Home button */}
      <div className="home-container">
        <img
          className="home-icon"
          src={homeIcon}
          alt="Home Icon"
          onClick={handleHomeClick}
          style={{ cursor: "pointer" }}
        />
      </div>

      {/* Right panel with category icons */}
      <div className="right-panel">
        <img className="restaurants" src={restaurantsIcon} alt="Restaurants Icon" />
        <img className="cafes" src={cafesIcon} alt="Cafes Icon" />
        <img className="historical" src={historicalIcon} alt="Historical Icon" />
        <img className="artculture" src={artCultureIcon} alt="Art & Culture Icon" />
        <img className="parks" src={parksIcon} alt="Parks Icon" />
      </div>

      {/* SINGLE View Map button */}
      <div className="mapview-container">
        <img
          className="mapview"
          src={mapViewIcon}
          alt="View Map Icon"
          onClick={handleMapViewClick}
          style={{ cursor: "pointer" }}
        />
      </div>
    </div>
  );
}

export default ViewList;
