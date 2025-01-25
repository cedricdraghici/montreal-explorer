import React from 'react';
import arrowFrame from '../assets/arrow_frame.svg';
import restaurantFrame from '../assets/restaurant_frame.svg';
import cafesFrame from '../assets/cafes_frame.svg';
import historicalFrame from '../assets/historical_frame.svg';
import artCultureFrame from '../assets/art_culture_frame.svg';
import parksFrame from '../assets/parks_frame.svg';
import viewListFrame from '../assets/view_list_frame.svg';
import rectangleCurved from '../assets/rectangle_curved.svg'; // Import rectangle_curved.svg
import rectangle from '../assets/rectangle.svg'; // Import rectangle.svg

function MapViewPage() {
  return (
    <div className="map-view-container">
      {/* Static Rectangle Backgrounds */}
      <div className="background-container">
        <img src={rectangle} alt="Rectangle" className="rectangle" />
        <img src={rectangleCurved} alt="Curved Rectangle" className="rectangle-curved" />
      </div>

      {/* Arrow Icon */}
      <div className="arrow-container">
        <a href="/home">
          <img src={arrowFrame} alt="Back Arrow" className="arrow-icon" />
        </a>
      </div>

      {/* Category Icons */}
      <div className="categories-container">
        <a href="/restaurants">
          <img src={restaurantFrame} alt="Restaurants" className="category-icon" />
        </a>
        <a href="/cafes">
          <img src={cafesFrame} alt="Cafes" className="category-icon" />
        </a>
        <a href="/historical">
          <img src={historicalFrame} alt="Historical" className="category-icon" />
        </a>
        <a href="/art-culture">
          <img src={artCultureFrame} alt="Art & Culture" className="category-icon" />
        </a>
        <a href="/parks">
          <img src={parksFrame} alt="Parks" className="category-icon" />
        </a>
      </div>

      {/* View List Icon */}
      <div className="view-list-container">
        <a href="/view-list">
          <img src={viewListFrame} alt="View List" className="view-list-icon" />
        </a>
      </div>
    </div>
  );
}

export default MapViewPage;
