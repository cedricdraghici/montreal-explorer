import React from "react";
import rectangle from "../assets/rectangle.svg";
import curvedRec from "../assets/curved-rec.svg";
import collapseIcon from "../assets/collapse.svg";
import restaurantsIcon from "../assets/restaurants.svg";
import cafesIcon from "../assets/cafes.svg";
import historicalIcon from "../assets/historical.svg";
import artCultureIcon from "../assets/artculture.svg";
import parksIcon from "../assets/parks.svg";
import viewListIcon from "../assets/viewlist.svg";
import plusIcon from "../assets/plus.svg";
import sendButtonIcon from "../assets/send-button.svg";
import homeIcon from "../assets/home.svg"; // Home Icon import
import "./MapViewPage.css";

function MapViewPage() {
  return (
    <div className="macbook-pro">
      <div className="div">
        {/* Home Icon */}
        <div className="home-container">
          <a href="/">
            <img className="home-icon" src={homeIcon} alt="Home Icon" />
          </a>
        </div>

        <div className="overlap">
          <img className="rectangle" src={rectangle} alt="Background Rectangle" />
          <img className="curved-rec" src={curvedRec} alt="Curved Background" />
          <img className="collapse" src={collapseIcon} alt="Collapse Icon" />
          <img className="restaurants" src={restaurantsIcon} alt="Restaurants Icon" />
          <img className="cafes" src={cafesIcon} alt="Cafes Icon" />
          <img className="historical" src={historicalIcon} alt="Historical Icon" />
          <img className="artculture" src={artCultureIcon} alt="Art & Culture Icon" />
          <img className="parks" src={parksIcon} alt="Parks Icon" />
          <img className="viewlist" src={viewListIcon} alt="View List Icon" />
        </div>
        <div className="overlap-group">
          <div className="askany">Ask anything...</div>
          <img className="plus" src={plusIcon} alt="Plus Icon" />
          <img className="send-button" src={sendButtonIcon} alt="Send Button" />
        </div>
      </div>
    </div>
  );
}

export default MapViewPage;
